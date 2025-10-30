import pytest
from my_ast import ast
from lexer import lexer
from . import parser

def test_let_statements()->None:
    input="""
let x = 5;
let y = 10;
let foobar = 838383;
"""
    expected_identifiers=["x","y","foobar"]
    l = lexer.Lexer(input)
    p = parser.Parser(l)
    program = p.parse_program()
    check_parse_errors(p)
    assert len(program.statements) == 3, f"program.statements does not contain 3 statements. got={len(program.statements)}"

    for i, ident in enumerate(expected_identifiers):
        stmt = program.statements[i]
        assert isinstance(stmt, ast.LetStatement), f"stmt not ast.LetStatement. got={type(stmt)}"
        assert stmt.token_literal() == "let", f"stmt.token_literal not 'let'. got='{stmt.token_literal()}'"
        assert stmt.name is not None, "stmt.name is None"
        assert stmt.name.value == ident, f"stmt.name.value not '{ident}'. got={stmt.name.value}"
        assert stmt.name.token_literal() == ident, f"stmt.name.token_literal() not '{ident}'. got={stmt.name.token_literal()}"

def test_return_statements()->None:
    input="""
return 5;
return 10;
return 993322;
"""
    l = lexer.Lexer(input)
    p = parser.Parser(l)
    program = p.parse_program()
    check_parse_errors(p)
    assert len(program.statements) == 3, f"program.statements does not contain 3 statements. got={len(program.statements)}"

    for stmt in program.statements:
        assert isinstance(stmt, ast.ReturnStatement), f"stmt not ast.ReturnStatement. got={type(stmt)}"
        assert stmt.token_literal() == "return", f"stmt.token_literal not 'return'. got='{stmt.token_literal()}'"


def check_parse_errors(p: parser.Parser) -> None:
    erors=p.Errors()
    if len(erors)==0:
        return
    print(f"parser has {len(erors)} errors")
    for msg in erors:
        print(f"parser error: {msg}")
    pytest.fail("parse errors encountered")