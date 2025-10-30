from my_token.token import *


class Lexer:
    def __init__(self, input: str) -> None:
        self.input = input
        self.position = 0
        self.read_position = 0
        self.ch = ''
        self.read_char()

    def read_char(self) -> None:
        if self.read_position >= len(self.input):
            self.ch = ''
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self) -> str:
        if self.read_position >= len(self.input):
            return ''
        else:
            return self.input[self.read_position]

    def next_token(self) -> Token:
        self.skip_whitespace()
        match self.ch:
            # Operators
            case '=':
                if self.peek_char() == '=':
                    ch = self.ch
                    self.read_char()
                    tok = Token(TokenType(EQ), ch+self.ch)
                else:
                    tok = Token(TokenType(ASSIGN), self.ch)
            case '+': tok = Token(TokenType(PLUS), self.ch)
            case '-': tok = Token(TokenType(MINUS), self.ch)
            case '!':
                if self.peek_char() == '=':
                    ch = self.ch
                    self.read_char()
                    tok = Token(TokenType(NOT_EQ), ch+self.ch)
                else:
                    tok = Token(TokenType(BANG), self.ch)
            case '*': tok = Token(TokenType(ASTERISK), self.ch)
            case '/': tok = Token(TokenType(SLASH), self.ch)
            case '<': tok = Token(TokenType(LT), self.ch)
            case '>': tok = Token(TokenType(GT), self.ch)
            # Delimiters
            case ';': tok = Token(TokenType(SEMICOLON), self.ch)
            case ',': tok = Token(TokenType(COMMA), self.ch)
            case '(': tok = Token(TokenType(LPAREN), self.ch)
            case ')': tok = Token(TokenType(RPAREN), self.ch)
            case '{': tok = Token(TokenType(LBRACE), self.ch)
            case '}': tok = Token(TokenType(RBRACE), self.ch)
            # EOF
            case '': tok = Token(TokenType(EOF), '')
            case _:
                if self.ch.isalpha() or self.ch == '_':
                    literal = self.read_identifier()
                    token_type = lookup_ident(literal)
                    tok = Token(token_type, literal)
                    return tok
                elif self.ch.isdigit():
                    tok = Token(TokenType(INT), self.read_number())
                    return tok
                else:
                    tok = Token(TokenType(ILLEGAL), self.ch)
        self.read_char()
        return tok

    def read_identifier(self) -> str:
        position = self.position
        while self.ch.isalpha() or self.ch == '_':
            self.read_char()
        return self.input[position:self.position]

    def read_number(self) -> str:
        position = self.position
        while self.ch.isdigit():
            self.read_char()
        return self.input[position:self.position]

    def skip_whitespace(self) -> None:
        while self.ch and self.ch in ' \t\n\r':
            self.read_char()
