from pithon.syntax import (
    PiAssignment, PiBinaryOperation, PiNumber, PiBool, PiValue, PiProgram, PiVariable,
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
    # PiProgram = list[PiStatement]
    if isinstance(node, list):  # PiProgram
        last_value = None
        for stmt in node:
            last_value = evaluate(stmt, env)
        return last_value

    if isinstance(node, PiNumber):
        return node

    elif isinstance(node, PiBool):
        return node

    elif isinstance(node, PiNone):
        return node

    elif isinstance(node, PiVariable):
        return lookup(env, node.name)

    elif isinstance(node, PiBinaryOperation):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
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
        elif node.operator == '==':
            return PiBool(left.value == right.value)
        elif node.operator == '!=':
            return PiBool(left.value != right.value)
        elif node.operator == '<':
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
        value = evaluate(node.value, env)
        insert(env, node.name, value)
        return value

    elif isinstance(node, PiIfThenElse):
        cond = evaluate(node.condition, env)
        if not isinstance(cond, PiBool):
            raise TypeError("La condition d'un if doit être un booléen.")
        branch = node.then_branch if cond.value else node.else_branch
        last_value = PiNone(value=None)
        for stmt in branch:
            last_value = evaluate(stmt, env)
        return last_value

    elif isinstance(node, PiNot):
        operand = evaluate(node.operand, env)
        if not isinstance(operand, PiBool):
            raise TypeError("L'opérande de 'not' doit être un booléen.")
        return PiBool(not operand.value)

    elif isinstance(node, PiAnd):
        left = evaluate(node.left, env)
        if not isinstance(left, PiBool):
            raise TypeError("L'opérande gauche de 'and' doit être un booléen.")
        if not left.value:
            return PiBool(False)
        right = evaluate(node.right, env)
        if not isinstance(right, PiBool):
            raise TypeError("L'opérande droite de 'and' doit être un booléen.")
        return PiBool(right.value)

    elif isinstance(node, PiOr):
        left = evaluate(node.left, env)
        if not isinstance(left, PiBool):
            raise TypeError("L'opérande gauche de 'or' doit être un booléen.")
        if left.value:
            return PiBool(True)
        right = evaluate(node.right, env)
        if not isinstance(right, PiBool):
            raise TypeError("L'opérande droite de 'or' doit être un booléen.")
        return PiBool(right.value)

    elif isinstance(node, PiWhile):
        last_value = PiNone(value=None)
        while True:
            cond = evaluate(node.condition, env)
            if not isinstance(cond, PiBool):
                raise TypeError("La condition d'une boucle while doit être un booléen.")
            if not cond.value:
                break
            for stmt in node.body:
                last_value = evaluate(stmt, env)
        return last_value

    elif isinstance(node, PiPrint):
        value = evaluate(node.value, env)
        print(value.value)
        return PiNone(value=None)

    else:
        raise TypeError(f"Type de nœud non supporté : {type(node)}")
