from typing import Any, Type, TypeVar
from pithon.evaluator.envframe import EnvFrame
from pithon.syntax import (
    PiAssignment, PiBinaryOperation, PiNumber, PiBool, PiStatement, PiProgram, PiVariable,
    PiIfThenElse, PiNot, PiAnd, PiOr, PiWhile, PiNone, PiList, PiTuple, PiString,
    PiFunctionDef, PiFunctionCall, PiFor, PiBreak, PiContinue, PiIn, PiReturn
)
from pithon.evaluator.envvalue import EnvValue, FunctionClosure

def primitive_add(args):
    a, b = args
    return PiNumber(a.value + b.value)
def primitive_sub(args):
    a, b = args
    return PiNumber(a.value - b.value)
def primitive_mul(args):
    a, b = args
    return PiNumber(a.value * b.value)
def primitive_div(args):
    a, b = args
    return PiNumber(a.value / b.value)
def primitive_mod(args):
    a, b = args
    return PiNumber(a.value % b.value)
def primitive_eq(args):
    a, b = args
    return PiBool(a == b)
def primitive_neq(args):
    a, b = args
    return PiBool(a != b)
def primitive_lt(args):
    a, b = args
    return PiBool(a.value < b.value)
def primitive_lte(args):
    a, b = args
    return PiBool(a.value <= b.value)
def primitive_gt(args):
    a, b = args
    return PiBool(a.value > b.value)
def primitive_gte(args):
    a, b = args
    return PiBool(a.value >= b.value)
def primitive_print(args):
    v, = args
    if isinstance(v, list):
        print([x.value if hasattr(x, 'value') else x for x in v])
    elif isinstance(v, tuple):
        print(tuple(x.value if hasattr(x, 'value') else x for x in v))
    elif hasattr(v, 'value'):
        print(v.value)
    else:
        print(v)
    return PiNone(value=None)

def initial_env() -> EnvFrame:
    env = EnvFrame()
    env.vars.update({
        '+': primitive_add,
        '-': primitive_sub,
        '*': primitive_mul,
        '/': primitive_div,
        '%': primitive_mod,
        '==': primitive_eq,
        '!=': primitive_neq,
        '<': primitive_lt,
        '<=': primitive_lte,
        '>': primitive_gt,
        '>=': primitive_gte,
        'print': primitive_print,
    })
    return env

def lookup(env: EnvFrame, name: str) -> EnvValue:
    return env.lookup(name)

def insert(env: EnvFrame, name: str, value: EnvValue) -> None:
    env.insert(name, value)

def evaluate(node: PiProgram, env: EnvFrame) -> EnvValue:
    if isinstance(node, list):
        last_value = PiNone(value=None)
        for stmt in node:
            last_value = evaluate_stmt(stmt, env)
        return last_value
    elif isinstance(node, PiStatement):
        return evaluate_stmt(node, env)
    else:
        raise TypeError(f"Type de nœud non supporté : {type(node)}")

def evaluate_stmt(node: PiStatement, env: EnvFrame) -> EnvValue:

    if isinstance(node, PiNumber):
        return node

    elif isinstance(node, PiBool):
        return node

    elif isinstance(node, PiNone):
        return node

    elif isinstance(node, PiString):
        return node

    elif isinstance(node, PiList):
        elements = [evaluate_stmt(e, env) for e in node.elements]
        return elements  # EnvValue: list of EnvValue

    elif isinstance(node, PiTuple):
        elements = tuple(evaluate_stmt(e, env) for e in node.elements)
        return elements  # EnvValue: tuple of EnvValue

    elif isinstance(node, PiVariable):
        return lookup(env, node.name)

    elif isinstance(node, PiBinaryOperation):
        # Treat as function call to primitive or user-defined function
        fct_call = PiFunctionCall(
            function=PiVariable(name=node.operator),
            args=[node.left, node.right]
        )
        return evaluate_stmt(fct_call, env)

    elif isinstance(node, PiAssignment):
        value = evaluate_stmt(node.value, env)
        insert(env, node.name, value)
        return value

    elif isinstance(node, PiIfThenElse):
        cond = evaluate_stmt(node.condition, env)
        cond = check_type(cond, PiBool)
        branch = node.then_branch if cond.value else node.else_branch
        last_value = evaluate(branch, env)
        return last_value

    elif isinstance(node, PiNot):
        operand = evaluate_stmt(node.operand, env)
        operand = check_type(operand, PiBool)
        return PiBool(not operand.value)

    elif isinstance(node, PiAnd):
        left = evaluate_stmt(node.left, env)
        left = check_type(left, PiBool)
        if not left.value:
            return PiBool(False)
        right = evaluate_stmt(node.right, env)
        right = check_type(right, PiBool)
        return PiBool(right.value)

    elif isinstance(node, PiOr):
        left = evaluate_stmt(node.left, env)
        left = check_type(left, PiBool)
        if left.value:
            return PiBool(True)
        right = evaluate_stmt(node.right, env)
        right = check_type(right, PiBool)
        return PiBool(right.value)

    elif isinstance(node, PiWhile):
        last_value = PiNone(value=None)
        while True:
            cond = evaluate_stmt(node.condition, env)
            cond = check_type(cond, PiBool)
            if not cond.value:
                break
            last_value = evaluate(node.body, env)
        return last_value

    elif isinstance(node, PiFunctionDef):
        closure = FunctionClosure(node, env)
        insert(env, node.name, closure)
        return PiNone(value=None)

    elif isinstance(node, PiReturn):
        value = evaluate_stmt(node.value, env)
        raise ReturnException(value)

    elif isinstance(node, PiFunctionCall):
        func_val = evaluate_stmt(node.function, env)
        args = [evaluate_stmt(arg, env) for arg in node.args]
        # Primitive function
        if callable(func_val):
            return func_val(args)
        # User-defined function
        if not isinstance(func_val, FunctionClosure):
            raise TypeError("Tentative d'appel d'un objet non-fonction.")
        funcdef = func_val.funcdef
        closure_env = func_val.closure_env
        call_env = EnvFrame(parent=closure_env)
        for i, arg_name in enumerate(funcdef.arg_names):
            if i < len(args):
                call_env.insert(arg_name, args[i])
            else:
                raise TypeError("Argument manquant pour la fonction.")
        if funcdef.vararg:
            call_env.insert(funcdef.vararg, args[len(funcdef.arg_names):])
        elif len(args) > len(funcdef.arg_names):
            raise TypeError("Trop d'arguments pour la fonction.")
        result = PiNone(value=None)
        try:
            for stmt in funcdef.body:
                result = evaluate_stmt(stmt, call_env)
        except ReturnException as ret:
            return ret.value
        return result

    elif isinstance(node, PiFor):
        iterable_val = evaluate_stmt(node.iterable, env)
        if not isinstance(iterable_val, (list, tuple)):
            raise TypeError("La boucle for attend une liste ou un tuple.")
        last_value = PiNone(value=None)
        for item in iterable_val:
            loop_env = EnvFrame(parent=env)
            loop_env.insert(node.var, item)
            last_value = evaluate(node.body, loop_env)
        return last_value

    elif isinstance(node, PiBreak):
        raise NotImplementedError("break n'est pas encore géré.")

    elif isinstance(node, PiContinue):
        raise NotImplementedError("continue n'est pas encore géré.")

    elif isinstance(node, PiIn):
        container = evaluate_stmt(node.container, env)
        element = evaluate_stmt(node.element, env)
        if isinstance(container, (list, tuple)):
            return PiBool(element in container)
        elif isinstance(container, PiString):
            return PiBool(element.value in container.value)
        else:
            raise TypeError("'in' n'est supporté que pour les listes et chaînes.")
    elif hasattr(node, 'collection') and hasattr(node, 'index'):  # PiSubscript
            collection = evaluate_stmt(node.collection, env)
            index = evaluate_stmt(node.index, env)
            if isinstance(collection, list):
                idx = check_type(index, PiNumber)
                return collection[int(idx.value)]
            elif isinstance(collection, tuple):
                idx = check_type(index, PiNumber)
                return collection[int(idx.value)]
            elif isinstance(collection, PiString):
                idx = check_type(index, PiNumber)
                return PiString(collection.value[int(idx.value)])
            else:
                raise TypeError("L'indexation n'est supportée que pour les listes, tuples et chaînes.")

    else:
        raise TypeError(f"Type de nœud non supporté : {type(node)}")


T = TypeVar('T')
def check_type(obj: Any, mytype: Type[T]) -> T:
    if not isinstance(obj, mytype):
        raise TypeError(f"Type attendu : {mytype.__name__}, obtenu : {type(obj).__name__}")
    return obj

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
