from pithon.syntax import PiAssignment, PiBinaryOperation, PiLiteral, PiSyntaxTree, PiVariable


def empty_env() -> dict[str, PiLiteral]:
    return {}


def evaluate(node: PiSyntaxTree, env: dict[str, PiLiteral]) -> PiLiteral:
    if isinstance(node, PiLiteral):
        return node

    elif isinstance(node, PiVariable):
        if node.name not in env:
            raise NameError(f"Variable '{node.name}' is not defined.")
        return env[node.name]

    elif isinstance(node, PiBinaryOperation):
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)

        if node.operator == '+':
            return PiLiteral(left.value + right.value)
        elif node.operator == '-':
            return PiLiteral(left.value - right.value)
        elif node.operator == '*':
            return PiLiteral(left.value * right.value)
        elif node.operator == '/':
            return PiLiteral(left.value / right.value)
        else:
            raise ValueError(f"Unsupported operator: {node.operator}")

    elif isinstance(node, PiAssignment):
        value = evaluate(node.value, env)
        env[node.name] = value
        return value

    else:
        raise TypeError(f"Unsupported node type: {type(node)}")
