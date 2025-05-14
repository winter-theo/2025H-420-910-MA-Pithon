import ast

from pithon.syntax import (
    PiAssignment, PiBinaryOperation, PiNumber, PiBool, PiVariable, PiIfThenElse,
    PiNot, PiAnd, PiOr, PiWhile, PiPrint, PiExpression, PiNone
)

class SimpleParser(ast.NodeVisitor):
    """
    Un parseur simple pour le langage Pithon.
    Il utilise le module ast de Python pour analyser le code source et
    retourner un arbre syntaxique abstrait (AST) simplifié propre à Pithon.
    """
    def parse(self, source_code: str):
        tree = ast.parse(source_code)
        return [self.visit(stmt) for stmt in tree.body]

    def visit_Expr(self, node: ast.Expr) -> PiExpression:
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

    def visit_Constant(self, node: ast.Constant) -> PiExpression:
        if node.value is None:
            return PiNone(value=None)
        if isinstance(node.value, bool):
            return PiBool(value=node.value)
        elif isinstance(node.value, int) or isinstance(node.value, float):
            return PiNumber(value=node.value)
        else:
            raise ValueError("Seuls les littéraux numériques, booléens ou None sont autorisés.")

    def visit_If(self, node: ast.If) -> PiIfThenElse:
        condition = self.visit(node.test)
        then_branch = [self.visit(stmt) for stmt in node.body]
        else_branch = [self.visit(stmt) for stmt in node.orelse] if node.orelse else []
        return PiIfThenElse(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visit_IfExp(self, node: ast.IfExp) -> PiIfThenElse:
        # Pour les expressions ternaires (x if cond else y)
        condition = self.visit(node.test)
        then_branch = [self.visit(node.body)]
        else_branch = [self.visit(node.orelse)]
        return PiIfThenElse(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> PiExpression:
        if isinstance(node.op, ast.Not):
            operand = self.visit(node.operand)
            return PiNot(operand=operand)
        else:
            raise ValueError("Seul l'opérateur 'not' unaire est supporté.")

    def visit_BoolOp(self, node: ast.BoolOp) -> PiExpression:
        if isinstance(node.op, ast.And):
            left = self.visit(node.values[0])
            right = self.visit(node.values[1])
            return PiAnd(left=left, right=right)
        elif isinstance(node.op, ast.Or):
            left = self.visit(node.values[0])
            right = self.visit(node.values[1])
            return PiOr(left=left, right=right)
        else:
            raise ValueError("Seuls les opérateurs 'and' et 'or' sont supportés.")

    def visit_While(self, node: ast.While) -> PiWhile:
        condition = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        return PiWhile(condition=condition, body=body)

    def visit_Call(self, node: ast.Call) -> PiExpression:
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            if len(node.args) != 1:
                raise ValueError("print prend exactement un argument.")
            value = self.visit(node.args[0])
            return PiPrint(value=value)
        else:
            raise ValueError("Seule la fonction print est supportée.")

    def visit_Compare(self, node: ast.Compare) -> PiBinaryOperation:
        if len(node.ops) != 1 or len(node.comparators) != 1:
            raise ValueError("Seules les comparaisons simples sont supportées.")
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        operator = self.operator_symbol(node.ops[0])
        return PiBinaryOperation(left=left, operator=operator, right=right)

    def operator_symbol(self, op) -> str:
        if isinstance(op, ast.Add):
            return '+'
        elif isinstance(op, ast.Sub):
            return '-'
        elif isinstance(op, ast.Mult):
            return '*'
        elif isinstance(op, ast.Div):
            return '/'
        elif isinstance(op, ast.Mod):
            return '%'
        elif isinstance(op, ast.Eq):
            return '=='
        elif isinstance(op, ast.NotEq):
            return '!='
        elif isinstance(op, ast.Lt):
            return '<'
        elif isinstance(op, ast.LtE):
            return '<='
        elif isinstance(op, ast.Gt):
            return '>'
        elif isinstance(op, ast.GtE):
            return '>='
        else:
            raise ValueError(f"Opérateur non pris en charge {op}.")

    def generic_visit(self, node):
        raise ValueError(f"Type de nœud AST non supporté : {type(node).__name__}")

