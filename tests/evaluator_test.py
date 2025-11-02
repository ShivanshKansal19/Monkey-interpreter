from lexer import lexer
from object import object
from parser import parser
from evaluator import evaluator
import pytest


@pytest.mark.parametrize('input, expected', [
    ("5", 5),
    ("10", 10),
    ("-5", -5),
    ("-10", -10),
])
def test_eval_integer_expression(input: str, expected: int) -> None:
    evaluated = eval_input(input)
    assert_integer_object(evaluated, expected)


@pytest.mark.parametrize('input, expected', [
    ("true", True),
    ("false", False),
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
])
def test_bang_operator(input: str, expected: bool) -> None:
    evaluated = eval_input(input)
    assert_boolean_object(evaluated, expected)


def eval_input(input: str) -> object.Object | None:
    l = lexer.Lexer(input)
    p = parser.Parser(l)
    program = p.parse_program()
    return evaluator.eval(program)


def assert_integer_object(obj: object.Object | None, expected: int) -> None:
    assert isinstance(
        obj, object.Integer), f"object is not Integer. got={type(obj)} instead"
    assert obj.value == expected, f"object has wrong value. got={obj.value}, want={expected}"


def assert_boolean_object(obj: object.Object | None, expected: int) -> None:
    assert isinstance(
        obj, object.Boolean), f"object is not Boolean. got={type(obj)} instead"
    assert obj.value == expected, f"object has wrong value. got={obj.value}, want={expected}"
