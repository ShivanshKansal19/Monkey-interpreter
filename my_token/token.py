from typing import NewType

TokenType = NewType('TokenType', str)


ILLEGAL = TokenType("ILLEGAL")
EOF = TokenType("EOF")

# Identifiers + literals
IDENT = TokenType("IDENT")  # add, foobar, x, y, ...
INT = TokenType("INT")  # 1343456

# Operators
ASSIGN = TokenType("=")
PLUS = TokenType("+")
MINUS = TokenType("-")
BANG = TokenType("!")
ASTERISK = TokenType("*")
SLASH = TokenType("/")
LT = TokenType("<")
GT = TokenType(">")
EQ = TokenType("==")
NOT_EQ = TokenType("!=")


# Delimiters
COMMA = TokenType(",")
SEMICOLON = TokenType(";")
LPAREN = TokenType("(")
RPAREN = TokenType(")")
LBRACE = TokenType("{")
RBRACE = TokenType("}")

# Keywords
FUNCTION = TokenType("FUNCTION")
LET = TokenType("LET")
TRUE = TokenType("TRUE")
FALSE = TokenType("FALSE")
IF = TokenType("IF")
ELSE = TokenType("ELSE")
RETURN = TokenType("RETURN")

keywords: dict[str, TokenType] = {
    "fn": FUNCTION,
    "let": LET,
    "true": TRUE,
    "false": FALSE,
    "if": IF,
    "else": ELSE,
    "return": RETURN,
}


def lookup_ident(ident: str) -> TokenType:
    return keywords.get(ident, IDENT)


class Token:
    def __init__(self, token_type: TokenType, literal: str) -> None:
        self.type = token_type
        self.literal = literal

    def __repr__(self) -> str:
        return f"Token(Type='{self.type}', Literal='{self.literal}')"
