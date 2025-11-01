from typing import NewType

TokenType = NewType('TokenType', str)


ILLEGAL = "ILLEGAL"
EOF = "EOF"

# Identifiers + literals
IDENT = "IDENT"  # add, foobar, x, y, ...
INT = "INT"  # 1343456

# Operators
ASSIGN = "="
PLUS = "+"
MINUS = "-"
BANG = "!"
ASTERISK = "*"
SLASH = "/"
LT = "<"
GT = ">"
EQ = "=="
NOT_EQ = "!="


# Delimiters
COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"

# Keywords
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"

keywords: dict[str, TokenType] = {
    "fn": TokenType(FUNCTION),
    "let": TokenType(LET),
    "true": TokenType(TRUE),
    "false": TokenType(FALSE),
    "if": TokenType(IF),
    "else": TokenType(ELSE),
    "return": TokenType(RETURN),
}


def lookup_ident(ident: str) -> TokenType:
    return keywords.get(ident, TokenType(IDENT))


class Token:
    def __init__(self, token_type: TokenType, literal: str) -> None:
        self.type = token_type
        self.literal = literal

    def __repr__(self) -> str:
        return f"Token(Type='{self.type}', Literal='{self.literal}')"
