from object import object
from my_ast import ast


def eval(node: ast.Node | None) -> object.Object | None:
    if isinstance(node, ast.Program):
        return eval_statements(node.statements)
    # expressions
    elif isinstance(node, ast.ExpressionStatement):
        return eval(node.expression)
    elif isinstance(node, ast.IntegerLiteral):
        return object.Integer(node.value)
    return None


def eval_statements(stmts: list[ast.Statement]) -> object.Object | None:
    result: object.Object | None = None
    for stmt in stmts:
        result = eval(stmt)
    return result
