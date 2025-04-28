from pithon.syntax import PiLiteral, PiSyntaxTree


def empty_env() -> dict[str, PiLiteral]:
    return {}


def evaluate(node: PiSyntaxTree, env: dict[str, PiLiteral]) -> PiLiteral:
    pass