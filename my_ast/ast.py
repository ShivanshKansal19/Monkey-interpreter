from my_token import token


class Node:
    def __str__(self) -> str:
        return ''

    def token_literal(self) -> str:
        raise NotImplementedError()


class Statement(Node):
    def __str__(self) -> str:
        return 'Statement'

    def statement_node(self) -> None:
        pass


class Expression(Node):
    def __str__(self) -> str:
        return 'Expression'

    def expression_node(self) -> None:
        pass


class ExpressionStatement(Statement):
    def __init__(self, token: token.Token, expression: Expression | None = None) -> None:
        self.token = token
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression) if self.expression else ''


class IntegerLiteral(Expression):
    def __init__(self, token: token.Token, value: int | None = None) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return self.token.literal

    def token_literal(self) -> str:
        return self.token.literal


class Identifier(Expression):
    def __init__(self, token: token.Token, value: str) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return self.value

    def token_literal(self) -> str:
        return self.token.literal


class LetStatement(Statement):
    def __init__(self, token: token.Token, name: Identifier | None = None, value: Expression | None = None) -> None:
        self.token = token
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.name)} = {str(self.value) if self.value else ''};"

    def token_literal(self) -> str:
        return self.token.literal


class ReturnStatement(Statement):
    def __init__(self, token: token.Token, return_value: Expression | None = None) -> None:
        self.token = token
        self.return_value = return_value

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.return_value) if self.return_value else ''};"

    def token_literal(self) -> str:
        return self.token.literal


class Program(Node):
    def __init__(self, stmts: list[Statement] | None = None) -> None:
        self.statements: list[Statement] = stmts if stmts is not None else []

    def __str__(self) -> str:
        return '\n'.join([str(s) for s in self.statements])

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""
