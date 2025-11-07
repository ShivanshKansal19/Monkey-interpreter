from lexer import lexer
from object import object, environment
from parser import parser
from evaluator import evaluator
import pytest


@pytest.mark.parametrize('input, expected', [
    ("5", 5),
    ("10", 10),
    ("-5", -5),
    ("-10", -10),
    ("5 + 5 + 5 + 5 - 10", 10),
    ("2 * 2 * 2 * 2 * 2", 32),
    ("5 + 5 + 5 + 5 - 10", 10),
    ("2 * 2 * 2 * 2 * 2", 32),
    ("-50 + 100 + -50", 0),
    ("5 * 2 + 10", 20),
    ("5 + 2 * 10", 25),
    ("20 + 2 * -10", 0),
    ("50 / 2 * 2 + 10", 60),
    ("2 * (5 + 10)", 30),
    ("3 * 3 * 3 + 10", 37),
    ("3 * (3 * 3) + 10", 37),
    ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
])
def test_eval_integer_expression(input: str, expected: int) -> None:
    evaluated = eval_input(input)
    assert_integer_object(evaluated, expected)


@pytest.mark.parametrize('input, expected', [
    ("true", True),
    ("false", False),
    ("1 < 2", True),
    ("1 > 2", False),
    ("1 < 1", False),
    ("1 > 1", False),
    ("1 == 1", True),
    ("1 != 1", False),
    ("1 == 2", False),
    ("1 != 2", True),
])
def test_eval_boolean_expression(input: str, expected: bool) -> None:
    evaluated = eval_input(input)
    assert_boolean_object(evaluated, expected)


@pytest.mark.parametrize('input, expected', [
    ("!true", False),
    ("!false", True),
    ("!5", False),
    ("!!true", True),
    ("!!false", False),
    ("!!5", True),
    ("true == true", True),
    ("false == false", True),
    ("true == false", False),
    ("true != false", True),
    ("false != true", True),
    ("(1 < 2) == true", True),
    ("(1 < 2) == false", False),
    ("(1 > 2) == true", False),
    ("(1 > 2) == false", True),
])
def test_bang_operator(input: str, expected: bool) -> None:
    evaluated = eval_input(input)
    assert_boolean_object(evaluated, expected)


@pytest.mark.parametrize('input, expected', [
    ("if (true) { 10 }", 10),
    ("if (false) { 10 }", None),
    ("if (1) { 10 }", 10),
    ("if (1 < 2) { 10 }", 10),
    ("if (1 > 2) { 10 }", None),
    ("if (1 > 2) { 10 } else { 20 }", 20),
    ("if (1 < 2) { 10 } else { 20 }", 10),
])
def test_eval_if_else_expressions(input: str, expected: int) -> None:
    evaluated = eval_input(input)
    if expected is None:
        assert_null_object(evaluated)
    else:
        assert_integer_object(evaluated, expected)


@pytest.mark.parametrize('input, expected', [
    ("return 10;", 10),
    ("return 10; 9;", 10),
    ("return 2 * 5; 9;", 10),
    ("9; return 2 * 5; 9;", 10),
    ('''
    if (10 > 1) {
        if (10 > 1) {
            return 10;
        }
        return 1;
    }
    ''', 10),
])
def test_return_statements(input: str, expected: int) -> None:
    evaluated = eval_input(input)
    assert_integer_object(evaluated, expected)


@pytest.mark.parametrize('input, expected', [
    ("let a = 5; a;", 5),
    ("let a = 5 * 5; a;", 25),
    ("let a = 5; let b = a; b;", 5),
    ("let a = 5; let b = a; let c = a + b + 5; c;", 15),
])
def test_let_statements(input: str, expected: int) -> None:
    evaluated = eval_input(input)
    assert_integer_object(evaluated, expected)


def test_function_object() -> None:
    input = "fn(x) { x + 2; };"
    evaluated = eval_input(input)
    assert isinstance(
        evaluated, object.Function), f"object is not Function. got={type(evaluated)}({evaluated.__dict__}) instead"
    assert len(
        evaluated.parameters) == 1, f"function has wrong parameters. Parameters={evaluated.parameters}"
    assert str(
        evaluated.parameters[0]) == "x", f"parameter is not 'x'. got={str(evaluated.parameters[0])}"
    expected_body = "(x + 2)"
    assert str(
        evaluated.body) == expected_body, f"body is not {expected_body}. got={evaluated.body}"


@pytest.mark.parametrize('input, expected', [
    ("let identity = fn(x) { x; }; identity(5);", 5),
    ("let identity = fn(x) { return x; }; identity(5);", 5),
    ("let double = fn(x) { x * 2; }; double(5);", 10),
    ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
    ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
    ("fn(x) { x; }(5)", 5),
])
def test_function_application(input: str, expected: int) -> None:
    evaluated = eval_input(input)
    assert_integer_object(evaluated, expected)


@pytest.mark.parametrize('input, expected_message', [
    ("5 + true;", "type mismatch: INTEGER + BOOLEAN"),
    ("5 + true; 5;", "type mismatch: INTEGER + BOOLEAN"),
    ("-true", "unknown operator: -BOOLEAN"),
    ("true + false;", "unknown operator: BOOLEAN + BOOLEAN"),
    ("5; true + false; 5", "unknown operator: BOOLEAN + BOOLEAN"),
    ("if (10 > 1) { true + false; }", "unknown operator: BOOLEAN + BOOLEAN"),
    ('''
    if (10 > 1) { 
        if (10 > 1) {
            return true + false;
        }
        return 1;
    }
    ''', "unknown operator: BOOLEAN + BOOLEAN"),
    ("foobar", "identifier not found: foobar"),
])
def test_error_handling(input: str, expected_message: str) -> None:
    evaluated = eval_input(input)
    assert isinstance(
        evaluated, object.Error), f"object is not Error. got={type(evaluated)}({evaluated.__dict__}) instead"
    assert evaluated.message == expected_message, f"wrong error message. expected={expected_message}, got={evaluated.message}"


# Helper functions

def assert_null_object(obj: object.Object | None) -> None:
    assert isinstance(
        obj, object.Null), f"object is not Null. got={type(obj)}({obj.__dict__}) instead"


def assert_integer_object(obj: object.Object | None, expected: int) -> None:
    assert isinstance(
        obj, object.Integer), f"object is not Integer. got={type(obj)}({obj.__dict__}) instead"
    assert obj.value == expected, f"object has wrong value. got={obj.value}, want={expected}"


def assert_boolean_object(obj: object.Object | None, expected: int) -> None:
    assert isinstance(
        obj, object.Boolean), f"object is not Boolean. got={type(obj)}({obj.__dict__}) instead"
    assert obj.value == expected, f"object has wrong value. got={obj.value}, want={expected}"


def eval_input(input: str) -> object.Object | None:
    l = lexer.Lexer(input)
    p = parser.Parser(l)
    program = p.parse_program()
    env = environment.Environment()
    return evaluator.eval(program, env)
