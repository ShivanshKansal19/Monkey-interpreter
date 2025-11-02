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
    token.EQ: EQUALS,
    token.NOT_EQ: EQUALS,
    token.LT: LESSGREATER,
    token.GT: LESSGREATER,
    token.PLUS: SUM,
    token.MINUS: SUM,
    token.SLASH: PRODUCT,
    token.ASTERISK: PRODUCT,
    token.LPAREN: CALL,
}

prefix_parse_fn = Callable[[], ast.Expression | None]
infix_parse_fn = Callable[[ast.Expression], ast.Expression]


class Parser:
    def __init__(self, l: lexer.Lexer) -> None:
        self.l = l
        self.errors: list[str] = []

        self.cur_token: token.Token = self.l.next_token()
        self.peek_token: token.Token = self.l.next_token()

        self.prefix_parse_fns: dict[token.TokenType, prefix_parse_fn] = {
            token.IDENT: self.parse_identifier,
            token.INT: self.parse_integer_literal,
            token.MINUS: self.parse_prefix_expression,
            token.BANG: self.parse_prefix_expression,
            token.LPAREN: self.parse_grouped_expression,
            token.FUNCTION: self.parse_function_literal,
            token.TRUE: self.parse_boolean,
            token.FALSE: self.parse_boolean,
            token.IF: self.parse_if_expression,
        }
        self.infix_parse_fns: dict[token.TokenType, infix_parse_fn] = {
            token.PLUS: self.parse_infix_expression,
            token.MINUS: self.parse_infix_expression,
            token.SLASH: self.parse_infix_expression,
            token.ASTERISK: self.parse_infix_expression,
            token.EQ: self.parse_infix_expression,
            token.NOT_EQ: self.parse_infix_expression,
            token.LT: self.parse_infix_expression,
            token.GT: self.parse_infix_expression,
            token.LPAREN: self.parse_call_expression,
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
        if self.peek_token_is(token.SEMICOLON):
            self.next_token()
        return stmt

    def parse_expression(self, precedence: int) -> ast.Expression | None:
        prefix = self.prefix_parse_fns.get(self.cur_token.type)
        if prefix is None:
            self.no_prefix_parse_error(self.cur_token.type)
            return None
        left_exp = prefix()
        while not self.peek_token_is(token.SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns.get(self.peek_token.type)
            if infix is None:
                return left_exp
            self.next_token()
            if left_exp is None:
                return None
            left_exp = infix(left_exp)
        return left_exp

    def parse_prefix_expression(self) -> ast.Expression:
        expression = ast.PrefixExpression(
            self.cur_token, self.cur_token.literal)
        self.next_token()
        expression.right = self.parse_expression(PREFIX)
        return expression

    def parse_infix_expression(self, left: ast.Expression) -> ast.Expression:
        expression = ast.InfixExpression(
            self.cur_token, left, self.cur_token.literal)
        precedence = self.cur_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)
        return expression

    def parse_integer_literal(self) -> ast.IntegerLiteral | None:
        try:
            value = int(self.cur_token.literal)
        except Exception:
            msg = f"could not parse {self.cur_token.literal} as integer"
            self.errors.append(msg)
            return None
        lit = ast.IntegerLiteral(self.cur_token, value)
        return lit

    def parse_call_expression(self, function: ast.Expression) -> ast.CallExpression:
        exp = ast.CallExpression(self.cur_token, function)
        exp.arguments = self.parse_call_arguments()
        return exp

    def parse_call_arguments(self) -> list[ast.Expression]:
        args = []
        if self.peek_token_is(token.RPAREN):
            self.next_token()
            return args
        self.next_token()
        args.append(self.parse_expression(LOWEST))
        while self.peek_token_is(token.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(LOWEST))
        if not self.expect_peek(token.RPAREN):
            return []
        return args

    def parse_identifier(self) -> ast.Identifier:
        return ast.Identifier(self.cur_token, self.cur_token.literal)

    def parse_grouped_expression(self) -> ast.Expression | None:
        self.next_token()
        exp = self.parse_expression(LOWEST)
        if not self.expect_peek(token.RPAREN):
            return None
        return exp

    def parse_function_literal(self) -> ast.FunctionLiteral | None:
        lit = ast.FunctionLiteral(self.cur_token)
        if not self.expect_peek(token.LPAREN):
            return None
        lit.parameters = self.parse_function_parameters()
        if not self.expect_peek(token.LBRACE):
            return None
        lit.body = self.parse_block_statement()
        return lit

    def parse_function_parameters(self) -> list[ast.Identifier]:
        identifiers: list[ast.Identifier] = []
        if self.peek_token_is(token.RPAREN):
            self.next_token()
            return identifiers
        self.next_token()
        ident = ast.Identifier(self.cur_token, self.cur_token.literal)
        identifiers.append(ident)
        while self.peek_token_is(token.COMMA):
            self.next_token()
            self.next_token()
            ident = ast.Identifier(self.cur_token, self.cur_token.literal)
            identifiers.append(ident)
        if not self.expect_peek(token.RPAREN):
            return []
        return identifiers

    def parse_boolean(self) -> ast.Boolean:
        return ast.Boolean(self.cur_token, self.cur_token_is(token.TRUE))

    def parse_if_expression(self) -> ast.IfExpression | None:
        expression = ast.IfExpression(self.cur_token)
        if not self.expect_peek(token.LPAREN):
            return None
        self.next_token()
        expression.condition = self.parse_expression(LOWEST)
        if not self.expect_peek(token.RPAREN):
            return None
        if not self.expect_peek(token.LBRACE):
            return None
        expression.consequence = self.parse_block_statement()
        if self.peek_token_is(token.ELSE):
            self.next_token()
            if not self.expect_peek(token.LBRACE):
                return None
            expression.alternative = self.parse_block_statement()
        return expression

    def parse_block_statement(self) -> ast.BlockStatement:
        block = ast.BlockStatement(self.cur_token)
        self.next_token()
        while not self.cur_token_is(token.RBRACE) and not self.cur_token_is(token.EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                block.statements.append(stmt)
            self.next_token()
        return block

    def parse_let_statement(self) -> ast.LetStatement | None:
        stmt = ast.LetStatement(self.cur_token)
        if not self.expect_peek(token.IDENT):
            return None
        stmt.name = ast.Identifier(self.cur_token, self.cur_token.literal)
        if not self.expect_peek(token.ASSIGN):
            return None
        self.next_token()
        stmt.value = self.parse_expression(LOWEST)
        if self.peek_token_is(token.SEMICOLON):
            self.next_token()
        return stmt

    def parse_return_statement(self) -> ast.ReturnStatement:
        stmt = ast.ReturnStatement(self.cur_token)
        self.next_token()
        stmt.return_value = self.parse_expression(LOWEST)
        if self.peek_token_is(token.SEMICOLON):
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
