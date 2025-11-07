from object import object
from my_ast import ast

NULL = object.Null()
TRUE = object.Boolean(True)
FALSE = object.Boolean(False)


def eval(node: ast.Node | None) -> object.Object:
    match node:
        # Statements
        case ast.Program():
            return eval_program(node)
        case ast.ExpressionStatement():
            return eval(node.expression)
        case ast.BlockStatement():
            return eval_block_statement(node)
        case ast.ReturnStatement():
            val = eval(node.return_value)
            if is_error(val):
                return val
            return object.ReturnValue(val)

        # Expressions
        case ast.IntegerLiteral():
            return object.Integer(node.value)
        case ast.Boolean():
            return native_bool_to_boolean_object(node.value)
        case ast.PrefixExpression():
            right = eval(node.right)
            if is_error(right):
                return right
            return eval_prefix_expression(node.operator, right)
        case ast.InfixExpression():
            left = eval(node.left)
            if is_error(left):
                return left
            right = eval(node.right)
            if is_error(right):
                return right
            return eval_infix_expression(node.operator, left, right)
        case ast.IfExpression():
            return eval_if_expression(node)
        case _:
            return NULL


def eval_program(stmts: ast.Program) -> object.Object:
    result = NULL
    for stmt in stmts.statements:
        result = eval(stmt)
        match result:
            case object.ReturnValue():
                return result.value
            case object.Error():
                return result
    return result


def eval_block_statement(block: ast.BlockStatement) -> object.Object:
    result = NULL
    for stmt in block.statements:
        result = eval(stmt)
        rt = result.type()
        if rt == object.RETURN_VALUE_OBJ or rt == object.ERROR_OBJ:
            return result
    return result


def eval_prefix_expression(operator: str, right: object.Object) -> object.Object:
    match operator:
        case '!':
            return eval_bang_operator_expression(right)
        case '-':
            return eval_minus_prefix_operator_expression(right)
        case _:
            return object.Error(f"unknown operator: {operator}{right.type()}")


def eval_bang_operator_expression(right: object.Object) -> object.Object:
    if is_truthy(right):
        return FALSE
    else:
        return TRUE


def eval_minus_prefix_operator_expression(right: object.Object) -> object.Object:
    if not isinstance(right, object.Integer):
        return object.Error(f"unknown operator: -{right.type()}")
    value = right.value
    return object.Integer(-value)


def eval_infix_expression(operator: str, left: object.Object, right: object.Object) -> object.Object:
    if isinstance(left, object.Integer) and isinstance(right, object.Integer):
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)
    elif left.type() != right.type():
        return object.Error(f"type mismatch: {left.type()} {operator} {right.type()}")
    else:
        return object.Error(f"unknown operator: {left.type()} {operator} {right.type()}")


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
            return object.Error(f"unknown operator: {left.type()} {operator} {right.type()}")


def eval_if_expression(ie: ast.IfExpression) -> object.Object:
    condition = eval(ie.condition)
    if is_error(condition):
        return condition
    if is_truthy(condition):
        return eval(ie.consequence)
    elif ie.alternative is not None:
        return eval(ie.alternative)
    else:
        return NULL


def is_truthy(obj: object.Object) -> bool:
    if obj is NULL:
        return False
    elif obj is TRUE:
        return True
    elif obj is FALSE:
        return False
    else:
        return True


def native_bool_to_boolean_object(input: bool) -> object.Boolean:
    if input:
        return TRUE
    return FALSE


def is_error(obj: object.Object) -> bool:
    return obj.type() == object.ERROR_OBJ
