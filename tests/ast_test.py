from my_ast.ast import *
from my_token import token


def test_str():
    program = Program([
        LetStatement(
            token.Token(token.LET, "let"),
            Identifier(token.Token(token.IDENT, "myVar"), "myVar"),
            Identifier(token.Token(token.IDENT, "anotherVar"), "anotherVar")
        )
    ])

    assert str(program) == "let myVar = anotherVar;\n"
