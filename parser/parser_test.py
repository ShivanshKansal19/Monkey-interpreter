import pytest
from my_ast import ast
from lexer import lexer
from my_token.token import *
from . import parser


@pytest.mark.parametrize("input, expected", [
    ("-a * b", "((-a) * b)"),
    ("!-a", "(!(-a))"),
    ("a + b + c", "((a + b) + c)"),
    ("a + b - c", "((a + b) - c)"),
    ("a * b * c", "((a * b) * c)"),
    ("a * b / c", "((a * b) / c)"),
    ("a + b / c", "(a + (b / c))"),
    ("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"),
    ("3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"),
    ("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
    ("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),
    ("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
    ("true", "true"),
    ("false", "false"),
    ("3 > 5 == false", "((3 > 5) == false)"),
    ("3 < 5 == true", "((3 < 5) == true)"),
    ("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"),
    ("(5 + 5) * 2", "((5 + 5) * 2)"),
    ("2 / (5 + 5)", "(2 / (5 + 5))"),
    ("-(5 + 5)", "(-(5 + 5))"),
    ("!(true == true)", "(!(true == true))"),
    ("a + add(b * c) + d", "((a + add((b * c))) + d)"),
    ("add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))",
     "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"),
    ("add(a + b + c * d / f + g)", "add((((a + b) + ((c * d) / f)) + g))"),
])
def test_operator_precedence_parsing(input: str, expected: str) -> None:
    program = create_program_from_input(input)
    actual = str(program)
    assert actual == expected, f"expected={expected}, got={actual}"


@pytest.mark.parametrize("input, operator, integer_value", [
    ("!5;", "!", 5),
    ("-15;", "-", 15),
    ("!true;", "!", True),
    ("!false;", "!", False),
])
def test_prefix_expressions(input: str, operator: str, integer_value: int) -> None:
    program = create_program_from_input(input, 1)
    stmt = program.statements[0]
    exp = assert_expression_statement(stmt)
    assert_prefix_expression(exp, operator, integer_value)


@pytest.mark.parametrize("input, left_value, operator, right_value", [
    ("5 + 5;", 5, "+", 5),
    ("5 - 5;", 5, "-", 5),
    ("5 * 5;", 5, "*", 5),
    ("5 / 5;", 5, "/", 5),
    ("5 > 5;", 5, ">", 5),
    ("5 < 5;", 5, "<", 5),
    ("5 == 5;", 5, "==", 5),
    ("5 != 5;", 5, "!=", 5),
    ("true == true", True, "==", True),
    ("true != false", True, "!=", False),
    ("false == false", False, "==", False),
])
def test_infix_expressions(input: str, left_value: int, operator: str, right_value: int) -> None:
    program = create_program_from_input(input, 1)
    stmt = program.statements[0]
    exp = assert_expression_statement(stmt)
    assert_infix_expression(exp, left_value, operator, right_value)


@pytest.mark.parametrize("input, expected_value", [
    ("5;", 5),
    ("10;", 10),
])
def test_integer_literal_expressions(input: str, expected_value: int) -> None:
    program = create_program_from_input(input, 1)
    stmt = program.statements[0]
    literal = assert_expression_statement(stmt)
    assert_integer_literal(literal, expected_value)


@pytest.mark.parametrize("input, expected_identifier", [
    ("foobar;", "foobar"),
    ("x;", "x"),
])
def test_identifier_expressions(input: str, expected_identifier: str) -> None:
    program = create_program_from_input(input, 1)
    stmt = program.statements[0]
    ident = assert_expression_statement(stmt)
    assert_identifier(ident, expected_identifier)


@pytest.mark.parametrize("input, expected_value", [
    ("true;", True),
    ("false;", False),
])
def test_boolean_expressions(input: str, expected_value: bool) -> None:
    program = create_program_from_input(input, 1)
    stmt = program.statements[0]
    bool = assert_expression_statement(stmt)
    assert_boolean(bool, expected_value)


def test_if_expression1() -> None:
    input = "if (x < y) { x }"
    program = create_program_from_input(input, 1)
    exp = assert_expression_statement(program.statements[0])
    assert isinstance(
        exp, ast.IfExpression), f"exp is not ast.IfExpression. got={type(exp)}"
    assert_infix_expression(exp.condition, "x", "<", "y")
    assert exp.consequence
    assert len(
        exp.consequence.statements) == 1, f"consequence is not 1 statement. got={len(exp.consequence.statements)}"
    consequence = assert_expression_statement(exp.consequence.statements[0])
    assert_identifier(consequence, "x")
    assert exp.alternative is None, f"exp.alternative was not None. got={exp.alternative}"


def test_if_expression2() -> None:
    input = "if (x < y) { x } else { y }"
    program = create_program_from_input(input, 1)
    exp = assert_expression_statement(program.statements[0])
    assert isinstance(
        exp, ast.IfExpression), f"exp is not ast.IfExpression. got={type(exp)}"
    assert_infix_expression(exp.condition, "x", "<", "y")
    assert exp.consequence is not None, "exp.consequence is None"
    assert len(
        exp.consequence.statements) == 1, f"consequence is not 1 statement. got={len(exp.consequence.statements)}"
    consequence = assert_expression_statement(exp.consequence.statements[0])
    assert_identifier(consequence, "x")
    assert exp.alternative is not None, "exp.alternative is None"
    assert len(
        exp.alternative.statements) == 1, f"alternative is not 1 statement. got={len(exp.alternative.statements)}"
    alternative = assert_expression_statement(exp.alternative.statements[0])
    assert_identifier(alternative, "y")


def test_function_literal_parsing() -> None:
    input = "fn(x, y) { x + y; }"
    program = create_program_from_input(input, 1)
    function = assert_expression_statement(program.statements[0])
    assert isinstance(
        function, ast.FunctionLiteral), f"function is not ast.FunctionLiteral. got={type(function)}"
    assert len(
        function.parameters) == 2, f"function literal parameters wrong. want 2, got={len(function.parameters)}"
    assert_identifier(function.parameters[0], "x")
    assert_identifier(function.parameters[1], "y")
    assert function.body is not None, "function.body is None"
    assert len(
        function.body.statements) == 1, f"function body statements wrong. want 1, got={len(function.body.statements)}"
    body_stmt = assert_expression_statement(function.body.statements[0])
    assert_infix_expression(body_stmt, "x", "+", "y")


@pytest.mark.parametrize("input, expected_parameters", [
    ("fn() {};", []),
    ("fn(x) {};", ["x"]),
    ("fn(x, y, z) {};", ["x", "y", "z"]),
])
def test_function_parameter_parsing(input: str, expected_parameters: list[str]) -> None:
    program = create_program_from_input(input, 1)
    function = assert_expression_statement(program.statements[0])
    assert isinstance(
        function, ast.FunctionLiteral), f"function is not ast.FunctionLiteral. got={type(function)}"
    assert len(
        function.parameters) == len(expected_parameters), f"function literal parameters wrong. want {len(expected_parameters)}, got={len(function.parameters)}"
    for i, ident in enumerate(expected_parameters):
        assert_identifier(function.parameters[i], ident)


def test_call_expression_parsing() -> None:
    input = "add(1, 2 * 3, 4 + 5);"
    program = create_program_from_input(input, 1)
    exp = assert_expression_statement(program.statements[0])
    assert isinstance(
        exp, ast.CallExpression), f"exp is not ast.CallExpression. got={type(exp)}"
    assert_identifier(exp.function, "add")
    assert len(
        exp.arguments) == 3, f"wrong length of arguments. got={len(exp.arguments)}"
    assert_literal_expression(exp.arguments[0], 1)
    assert_infix_expression(exp.arguments[1], 2, "*", 3)
    assert_infix_expression(exp.arguments[2], 4, "+", 5)


@pytest.mark.parametrize("input, expected_identifier, expected_value", [
    ("let x = 5;", "x", 5),
    ("let y = true;", "y", True),
    ("let foobar = y;", "foobar", "y"),
])
def test_let_statements(input: str, expected_identifier: str, expected_value: object) -> None:
    program = create_program_from_input(input, 1)
    stmt = assert_let_statement(program.statements[0], expected_identifier)
    print(str(stmt))
    assert_literal_expression(stmt.value, expected_value)


@pytest.mark.parametrize("input, expected_value", [
    ("return 5;", 5),
    ("return true;", True),
    ("return foobar;", "foobar"),
])
def test_return_statements(input: str, expected_value: object) -> None:
    program = create_program_from_input(input, 1)
    stmt = program.statements[0]
    assert isinstance(
        stmt, ast.ReturnStatement), f"stmt not ast.ReturnStatement. got={type(stmt)}"
    assert stmt.token_literal(
    ) == "return", f"stmt.token_literal not 'return'. got='{stmt.token_literal()}'"
    assert_literal_expression(stmt.return_value, expected_value)


# Helper functions for assertions and program creation

def assert_expression_statement(stmt: ast.Statement) -> ast.Expression | None:
    assert isinstance(
        stmt, ast.ExpressionStatement), f"stmt not ast.ExpressionStatement. got={type(stmt)}"
    return stmt.expression


def assert_integer_literal(integ: ast.Expression | None, value: int) -> None:
    assert isinstance(
        integ, ast.IntegerLiteral), f"exp not ast.IntegerLiteral. got={type(integ)}"
    assert integ.value == value, f"integ.value not {value}. got={integ.value}"
    assert integ.token_literal(
    ) == str(value), f"integ.token_literal not {value}. got={integ.token_literal()}"


def assert_identifier(ident: ast.Expression | None, value: str) -> None:
    assert isinstance(
        ident, ast.Identifier), f"exp not ast.Identifier. got={type(ident)}"
    assert ident.value == value, f"ident.value not {value}. got={ident.value}"
    assert ident.token_literal(
    ) == value, f"ident.token_literal not {value}. got={ident.token_literal()}"


def assert_boolean(bool: ast.Expression | None, value: bool) -> None:
    assert isinstance(
        bool, ast.Boolean), f"exp not ast.Boolean. got={type(bool)}"
    assert bool.value == value, f"ident.value not {value}. got={bool.value}"


def assert_literal_expression(exp: ast.Expression | None, expected: object) -> None:
    match expected:
        case bool():
            assert_boolean(exp, expected)
        case int():
            assert_integer_literal(exp, expected)
        case str():
            assert_identifier(exp, expected)
        case _:
            pytest.fail(f"type of exp not handled. got={type(expected)}")


def assert_prefix_expression(exp: ast.Expression | None, operator: str, right: object) -> None:
    assert isinstance(
        exp, ast.PrefixExpression), f"exp not ast.PrefixExpression. got={type(exp)}"
    assert exp.operator == operator, f"exp.operator is not '{operator}'. got={exp.operator}"
    assert_literal_expression(exp.right, right)


def assert_infix_expression(exp: ast.Expression | None, left: object, operator: str, right: object) -> None:
    assert isinstance(
        exp, ast.InfixExpression), f"exp not ast.InfixExpression. got={type(exp)}"
    assert_literal_expression(exp.left, left)
    assert exp.operator == operator, f"exp.operator is not '{operator}'. got={exp.operator}"
    assert_literal_expression(exp.right, right)


def assert_let_statement(stmt: ast.Statement, name: str) -> ast.LetStatement:
    print(str(stmt))
    assert isinstance(
        stmt, ast.LetStatement), f"stmt not ast.LetStatement. got={type(stmt)}"
    assert stmt.token_literal(
    ) == "let", f"stmt.token_literal not 'let'. got='{stmt.token_literal()}'"
    assert stmt.name is not None, "stmt.name is None"
    assert stmt.name.value == name, f"stmt.name.value not '{name}'. got={stmt.name.value}"
    assert stmt.name.token_literal(
    ) == name, f"stmt.name.token_literal() not '{name}'. got={stmt.name.token_literal()}"
    return stmt


def create_program_from_input(input: str, n_statements: int | None = None) -> ast.Program:
    l = lexer.Lexer(input)
    p = parser.Parser(l)
    program = p.parse_program()
    check_parse_errors(p)
    if n_statements is not None:
        assert len(
            program.statements) == n_statements, f"program.statements does not contain {n_statements} statements. got={len(program.statements)}"
    return program


def check_parse_errors(p: parser.Parser) -> None:
    erors = p.Errors()
    if len(erors) == 0:
        return
    print(f"parser has {len(erors)} errors")
    for msg in erors:
        print(f"parser error: {msg}")
    pytest.fail("parse errors encountered")
