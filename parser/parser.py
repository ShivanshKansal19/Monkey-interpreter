from my_ast import ast
from lexer import lexer
from my_token import token
from typing import Callable

LOWEST = 1
EQUALS = 2  # ==
LESSGREATER = 3  # > or <
SUM = 4  # +
PRODUCT = 5  # *
PREFIX = 6  # -X or !X
CALL = 7  # myFunction(X)

prefix_parse_fn = Callable[[], ast.Expression | None]
infix_parse_fn = Callable[[ast.Expression], ast.Expression]


class Parser:
    def __init__(self, l: lexer.Lexer) -> None:
        self.l = l
        self.errors: list[str] = []

        self.cur_token: token.Token = self.l.next_token()
        self.peek_token: token.Token = self.l.next_token()

        self.prefix_parse_fns: dict[token.TokenType, prefix_parse_fn] = {}
        self.register_prefix(token.TokenType(
            token.IDENT), self.parse_identifier)
        self.register_prefix(token.TokenType(token.INT),
                             self.parse_integer_literal)
        self.register_prefix(token.TokenType(token.BANG),
                             self.parse_prefix_expression)
        self.register_prefix(token.TokenType(token.MINUS),
                             self.parse_prefix_expression)
        self.infix_parse_fns: dict[token.TokenType, infix_parse_fn] = {}

    def register_prefix(self, token_type: token.TokenType, fn: prefix_parse_fn) -> None:
        self.prefix_parse_fns[token_type] = fn

    def register_infix(self, token_type: token.TokenType, fn: infix_parse_fn) -> None:
        self.infix_parse_fns[token_type] = fn

    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()

    def parse_program(self) -> ast.Program:
        program = ast.Program()

        while self.cur_token.type != token.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()

        return program

    def parse_statement(self) -> ast.Statement | None:
        match self.cur_token.type:
            case token.LET: return self.parse_let_statement()
            case token.RETURN: return self.parse_return_statement()
            case _: return self.parse_expression_statement()

    def parse_expression_statement(self) -> ast.ExpressionStatement:
        stmt = ast.ExpressionStatement(self.cur_token)
        stmt.expression = self.parse_expression(LOWEST)
        if self.peek_token_is(token.TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt

    def parse_expression(self, precedence: int) -> ast.Expression | None:
        prefix = self.prefix_parse_fns.get(self.cur_token.type)
        if prefix is None:
            self.no_prefix_parse_error(self.cur_token.type)
            return None
        left_exp = prefix()
        return left_exp

    def parse_prefix_expression(self) -> ast.Expression:
        expression = ast.PrefixExpression(
            self.cur_token, self.cur_token.literal)
        self.next_token()
        expression.right = self.parse_expression(PREFIX)
        return expression

    def parse_integer_literal(self) -> ast.IntegerLiteral | None:
        lit = ast.IntegerLiteral(self.cur_token)
        try:
            value = int(self.cur_token.literal)
        except Exception:
            msg = f"could not parse {self.cur_token.literal} as integer"
            self.errors.append(msg)
            return None
        lit.value = value
        return lit

    def parse_identifier(self) -> ast.Identifier:
        return ast.Identifier(self.cur_token, self.cur_token.literal)

    def parse_let_statement(self) -> ast.LetStatement | None:
        stmt = ast.LetStatement(self.cur_token)
        if not self.expect_peek(token.TokenType(token.IDENT)):
            return None
        stmt.name = ast.Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(token.TokenType(token.ASSIGN)):
            return None
        while not self.cur_token_is(token.TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt

    def parse_return_statement(self) -> ast.ReturnStatement | None:
        stmt = ast.ReturnStatement(self.cur_token)
        while not self.cur_token_is(token.TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt

    def cur_token_is(self, t: token.TokenType) -> bool:
        return self.cur_token.type == t

    def peek_token_is(self, t: token.TokenType) -> bool:
        return self.peek_token.type == t

    def expect_peek(self, t: token.TokenType) -> bool:
        if self.peek_token_is(t):
            self.next_token()
            return True
        else:
            self.peek_error(t)
            return False

    # Errors

    def Errors(self) -> list[str]:
        return self.errors

    def peek_error(self, t: token.TokenType) -> None:
        msg = f"expected next token to be {t}, got {self.peek_token.type} instead"
        self.errors.append(msg)

    def no_prefix_parse_error(self, t: token.TokenType) -> None:
        msg = f"no prefix parse function for {t} found"
        self.errors.append(msg)
