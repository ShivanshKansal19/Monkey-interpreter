from object import object
from my_ast import ast

NULL = object.Null()
TRUE = object.Boolean(True)
FALSE = object.Boolean(False)


def eval(node: ast.Node | None) -> object.Object:
    if isinstance(node, ast.Program):
        return eval_statements(node.statements)
    # Statements
    elif isinstance(node, ast.ExpressionStatement):
        return eval(node.expression)
    # Expressions
    elif isinstance(node, ast.IntegerLiteral):
        return object.Integer(node.value)
    elif isinstance(node, ast.Boolean):
        return native_bool_to_boolean_object(node.value)
    elif isinstance(node, ast.PrefixExpression):
        right = eval(node.right)
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, ast.InfixExpression):
        left = eval(node.left)
        right = eval(node.right)
        return eval_infix_expression(node.operator, left, right)
    return NULL


def eval_statements(stmts: list[ast.Statement]) -> object.Object:
    result = NULL
    for stmt in stmts:
        result = eval(stmt)
    return result


def eval_prefix_expression(operator: str, right: object.Object) -> object.Object:
    match operator:
        case '!':
            return eval_bang_operator_expression(right)
        case '-':
            return eval_minus_prefix_operator_expression(right)
        case _:
            return NULL


def eval_bang_operator_expression(right: object.Object) -> object.Object:
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE


def eval_minus_prefix_operator_expression(right: object.Object) -> object.Object:
    if not isinstance(right, object.Integer):
        return NULL
    value = right.value
    return object.Integer(-value)


def eval_infix_expression(operator: str, left: object.Object, right: object.Object) -> object.Object:
    if isinstance(left, object.Integer) and isinstance(right, object.Integer):
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)
    else:
        return NULL


def eval_integer_infix_expression(operator: str, left: object.Integer, right: object.Integer) -> object.Object:
    left_val, right_val = left.value, right.value
    match operator:
        case '+':
            return object.Integer(left_val+right_val)
        case '-':
            return object.Integer(left_val-right_val)
        case '*':
            return object.Integer(left_val*right_val)
        case '/':
            return object.Integer(left_val//right_val)
        case '<':
            return native_bool_to_boolean_object(left_val < right_val)
        case '>':
            return native_bool_to_boolean_object(left_val > right_val)
        case '==':
            return native_bool_to_boolean_object(left_val == right_val)
        case '!=':
            return native_bool_to_boolean_object(left_val != right_val)
        case _:
            return NULL


def native_bool_to_boolean_object(input: bool) -> object.Boolean:
    if input:
        return TRUE
    return FALSE
