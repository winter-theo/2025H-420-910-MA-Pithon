from typing import Any, Type, TypeVar
from pithon.syntax import (
    PiAssignment, PiBinaryOperation, PiNumber, PiBool, PiStatement, PiValue, PiProgram, PiVariable,
    PiIfThenElse, PiNot, PiAnd, PiOr, PiWhile, PiPrint, PiNone
)

def empty_env() -> list[tuple[str, PiValue]]:
    return []

def lookup(env: list[tuple[str, PiValue]], name: str) -> PiValue:
    for var, value in reversed(env):
        if var == name:
            return value
    raise NameError(f"Variable '{name}' non définie.")

def insert(env: list[tuple[str, PiValue]], name: str, value: PiValue) -> None:
    env.append((name, value))

def evaluate(node: PiProgram, env: list[tuple[str, PiValue]]) -> PiValue:
    if isinstance(node, list):
        last_value = PiNone(value=None)
        for stmt in node:
            last_value = evaluate_stmt(stmt, env)
        return last_value

def evaluate_stmt(node: PiStatement, env: list[tuple[str, PiValue]]) -> PiValue:

    if isinstance(node, PiNumber):
        return node

    elif isinstance(node, PiBool):
        return node

    elif isinstance(node, PiNone):
        return node

    elif isinstance(node, PiVariable):
        return lookup(env, node.name)

    elif isinstance(node, PiBinaryOperation):
        left = evaluate_stmt(node.left, env)
        right = evaluate_stmt(node.right, env)
        if node.operator in ('+', '-', '*', '/', '%'):
            left = check_type(left, PiNumber)
            right = check_type(right, PiNumber)
            if node.operator == '+':
                return PiNumber(left.value + right.value)
            elif node.operator == '-':
                return PiNumber(left.value - right.value)
            elif node.operator == '*':
                return PiNumber(left.value * right.value)
            elif node.operator == '/':
                return PiNumber(left.value / right.value)
            elif node.operator == '%':
                return PiNumber(left.value % right.value)
        elif node.operator in ('==', '!='):
            # Comparaison autorisée pour tous types de PiValue
            return PiBool(left.value == right.value) if node.operator == '==' else PiBool(left.value != right.value)
        elif node.operator in ('<', '<=', '>', '>='):
            left = check_type(left, PiNumber)
            right = check_type(right, PiNumber)
            if node.operator == '<':
                return PiBool(left.value < right.value)
            elif node.operator == '<=':
                return PiBool(left.value <= right.value)
            elif node.operator == '>':
                return PiBool(left.value > right.value)
            elif node.operator == '>=':
                return PiBool(left.value >= right.value)
        else:
            raise ValueError(f"Opérateur non supporté : {node.operator}")

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

    elif isinstance(node, PiPrint):
        value = evaluate_stmt(node.value, env)
        print(value.value)
        return PiNone(value=None)

    else:
        raise TypeError(f"Type de nœud non supporté : {type(node)}")


T = TypeVar('T')
def check_type(obj: Any, mytype: Type[T]) -> T:
    if not isinstance(obj, mytype):
        raise TypeError(f"Type attendu : {mytype.__name__}, obtenu : {type(obj).__name__}")
    return obj
