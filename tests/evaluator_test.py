from lexer import lexer
from object import object
from parser import parser
from evaluator import evaluator
import pytest


@pytest.mark.parametrize('input, expected', [
    ("5", 5),
    ("10", 10),
])
def test_eval_integer_expression(input: str, expected: int) -> None:
    evaluated = eval_input(input)
    assert_integer_object(evaluated, expected)


def eval_input(input: str) -> object.Object | None:
    l = lexer.Lexer(input)
    p = parser.Parser(l)
    program = p.parse_program()
    return evaluator.eval(program)


def assert_integer_object(obj: object.Object | None, expected: int):
    assert obj is not None, "object is None"
    assert isinstance(
        obj, object.Integer), f"object is not Integer. got={obj.type()} instead"
    assert obj.value == expected, f"object has wrong value. got={obj.value}, want={expected}"
