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
                    tok = Token(EQ, ch+self.ch)
                else:
                    tok = Token(ASSIGN, self.ch)
            case '+': tok = Token(PLUS, self.ch)
            case '-': tok = Token(MINUS, self.ch)
            case '!':
                if self.peek_char() == '=':
                    ch = self.ch
                    self.read_char()
                    tok = Token(NOT_EQ, ch+self.ch)
                else:
                    tok = Token(BANG, self.ch)
            case '*': tok = Token(ASTERISK, self.ch)
            case '/': tok = Token(SLASH, self.ch)
            case '<': tok = Token(LT, self.ch)
            case '>': tok = Token(GT, self.ch)
            # Delimiters
            case ';': tok = Token(SEMICOLON, self.ch)
            case ',': tok = Token(COMMA, self.ch)
            case '(': tok = Token(LPAREN, self.ch)
            case ')': tok = Token(RPAREN, self.ch)
            case '{': tok = Token(LBRACE, self.ch)
            case '}': tok = Token(RBRACE, self.ch)
            # EOF
            case '': tok = Token(EOF, '')
            case _:
                if self.ch.isalpha() or self.ch == '_':
                    literal = self.read_identifier()
                    token_type = lookup_ident(literal)
                    tok = Token(token_type, literal)
                    return tok
                elif self.ch.isdigit():
                    tok = Token(INT, self.read_number())
                    return tok
                else:
                    tok = Token(ILLEGAL, self.ch)
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
