from my_ast import ast
from lexer import lexer
from my_token import token
from my_token.token import TokenType
from typing import Callable

LOWEST = 1
EQUALS = 2  # ==
LESSGREATER = 3  # > or <
SUM = 4  # +
PRODUCT = 5  # *
PREFIX = 6  # -X or !X
CALL = 7  # myFunction(X)

precedences: dict[TokenType, int] = {
    TokenType(token.EQ): EQUALS,
    TokenType(token.NOT_EQ): EQUALS,
    TokenType(token.LT): LESSGREATER,
    TokenType(token.GT): LESSGREATER,
    TokenType(token.PLUS): SUM,
    TokenType(token.MINUS): SUM,
    TokenType(token.SLASH): PRODUCT,
    TokenType(token.ASTERISK): PRODUCT,
}

prefix_parse_fn = Callable[[], ast.Expression | None]
infix_parse_fn = Callable[[ast.Expression | None], ast.Expression]


class Parser:
    def __init__(self, l: lexer.Lexer) -> None:
        self.l = l
        self.errors: list[str] = []

        self.cur_token: token.Token = self.l.next_token()
        self.peek_token: token.Token = self.l.next_token()

        self.prefix_parse_fns: dict[TokenType, prefix_parse_fn] = {
            TokenType(token.IDENT): self.parse_identifier,
            TokenType(token.INT): self.parse_integer_literal,
            TokenType(token.MINUS): self.parse_prefix_expression,
            TokenType(token.BANG): self.parse_prefix_expression,
            TokenType(token.LPAREN): self.parse_grouped_expression,
            TokenType(token.TRUE): self.parse_boolean,
            TokenType(token.FALSE): self.parse_boolean,
        }
        self.infix_parse_fns: dict[TokenType, infix_parse_fn] = {
            TokenType(token.PLUS): self.parse_infix_expression,
            TokenType(token.MINUS): self.parse_infix_expression,
            TokenType(token.SLASH): self.parse_infix_expression,
            TokenType(token.ASTERISK): self.parse_infix_expression,
            TokenType(token.EQ): self.parse_infix_expression,
            TokenType(token.NOT_EQ): self.parse_infix_expression,
            TokenType(token.LT): self.parse_infix_expression,
            TokenType(token.GT): self.parse_infix_expression,
        }

    def register_prefix(self, token_type: TokenType, fn: prefix_parse_fn) -> None:
        self.prefix_parse_fns[token_type] = fn

    def register_infix(self, token_type: TokenType, fn: infix_parse_fn) -> None:
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
        if self.peek_token_is(TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt

    def parse_expression(self, precedence: int) -> ast.Expression | None:
        prefix = self.prefix_parse_fns.get(self.cur_token.type)
        if prefix is None:
            self.no_prefix_parse_error(self.cur_token.type)
            return None
        left_exp = prefix()
        while not self.peek_token_is(TokenType(token.SEMICOLON)) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if infix is None:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        return left_exp

    def parse_prefix_expression(self) -> ast.Expression:
        expression = ast.PrefixExpression(
            self.cur_token, self.cur_token.literal)
        self.next_token()
        expression.right = self.parse_expression(PREFIX)
        return expression

    def parse_infix_expression(self, left: ast.Expression | None) -> ast.Expression:
        expression = ast.InfixExpression(
            self.cur_token, left, self.cur_token.literal)
        precedence = self.cur_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)
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

    def parse_grouped_expression(self) -> ast.Expression | None:
        self.next_token()
        exp = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType(token.RPAREN)):
            return None
        return exp

    def parse_boolean(self) -> ast.Boolean:
        return ast.Boolean(self.cur_token, self.cur_token_is(TokenType(token.TRUE)))

    def parse_let_statement(self) -> ast.LetStatement | None:
        stmt = ast.LetStatement(self.cur_token)
        if not self.expect_peek(TokenType(token.IDENT)):
            return None
        stmt.name = ast.Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(TokenType(token.ASSIGN)):
            return None
        self.next_token()
        stmt.value = self.parse_expression(LOWEST)
        if self.peek_token_is(TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt

    def parse_return_statement(self) -> ast.ReturnStatement | None:
        stmt = ast.ReturnStatement(self.cur_token)
        self.next_token()
        stmt.return_value = self.parse_expression(LOWEST)
        if self.peek_token_is(TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt

    def cur_token_is(self, t: TokenType) -> bool:
        return self.cur_token.type == t

    def peek_token_is(self, t: TokenType) -> bool:
        return self.peek_token.type == t

    def expect_peek(self, t: TokenType) -> bool:
        if self.peek_token_is(t):
            self.next_token()
            return True
        else:
            self.peek_error(t)
            return False

    def cur_precedence(self) -> int:
        return precedences.get(self.cur_token.type, LOWEST)

    def peek_precedence(self) -> int:
        return precedences.get(self.peek_token.type, LOWEST)

    # Errors

    def Errors(self) -> list[str]:
        return self.errors

    def peek_error(self, t: TokenType) -> None:
        msg = f"expected next token to be {t}, got {self.peek_token.type} instead"
        self.errors.append(msg)

    def no_prefix_parse_error(self, t: TokenType) -> None:
        msg = f"no prefix parse function for {t} found"
        self.errors.append(msg)
