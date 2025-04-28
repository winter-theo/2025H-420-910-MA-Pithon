import ast

from pithon.syntax import PiAssignment, PiBinaryOperation, Expression, PiLiteral, PiSyntaxTree, PiVariable



class SimpleParser(ast.NodeVisitor):
    """
    Un parseur simple pour le langage Pithon.
    Il utilise le module ast de Python pour analyser le code source et
    retourner un arbre syntaxique abstrait (AST) simplifié propre à Pithon.
    """
    def parse(self, source_code: str) -> PiSyntaxTree:
        tree = ast.parse(source_code)
        if len(tree.body) != 1:
            raise ValueError("Une seule instruction à la fois est autorisée.")
        stmt = tree.body[0]
        return self.visit(stmt)

    def visit_Expr(self, node: ast.Expr) -> Expression:
        return self.visit(node.value)

    def visit_Assign(self, node: ast.Assign) -> PiAssignment:
        if len(node.targets) != 1:
            raise ValueError("Seule l'affectation simple est prise en charge.")
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            raise ValueError("Les affectations ne peuvent être faites qu'à des variables.")
        name = target.id
        value = self.visit(node.value)
        return PiAssignment(name=name, value=value)

    def visit_BinOp(self, node: ast.BinOp) -> PiBinaryOperation:
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = self.operator_symbol(node.op)
        return PiBinaryOperation(left=left, operator=operator, right=right)

    def visit_Name(self, node: ast.Name) -> PiVariable:
        return PiVariable(name=node.id)

    def visit_Constant(self, node: ast.Constant) -> PiLiteral:
        if not isinstance(node.value, int):
            raise ValueError("Seuls les littéraux entiers sont autorisés.")
        return PiLiteral(value=node.value)

    def operator_symbol(self, op) -> str:
        if isinstance(op, ast.Add):
            return '+'
        elif isinstance(op, ast.Sub):
            return '-'
        elif isinstance(op, ast.Mult):
            return '*'
        elif isinstance(op, ast.Div):
            return '/'
        else:
            raise ValueError(f"Opérateur non pris en charge {op}.")

