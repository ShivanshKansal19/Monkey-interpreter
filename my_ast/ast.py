from my_token import token
from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass


class Statement(Node):
    def __init__(self) -> None:
        self.token: token.Token

    def token_literal(self) -> str:
        return self.token.literal


class Expression(Node):
    def __init__(self) -> None:
        self.token: token.Token

    def token_literal(self) -> str:
        return self.token.literal


class PrefixExpression(Expression):
    def __init__(self, token: token.Token, operator: str, right: Expression | None = None) -> None:
        self.token = token
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"({self.operator}{str(self.right)})"


class InfixExpression(Expression):
    def __init__(self, token: token.Token, left: Expression | None, operator: str, right: Expression | None = None) -> None:
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"({str(self.left)} {self.operator} {str(self.right)})"


class ExpressionStatement(Statement):
    def __init__(self, token: token.Token, expression: Expression | None = None) -> None:
        self.token = token
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)+';\n' if self.expression is not None else ';\n'


class IntegerLiteral(Expression):
    def __init__(self, token: token.Token, value: int) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return self.token.literal


class Identifier(Expression):
    def __init__(self, token: token.Token, value: str) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return self.value


class Boolean(Expression):
    def __init__(self, token: token.Token, value: bool) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return self.token.literal


class BlockStatement(Statement):
    def __init__(self, token: token.Token, statements: list[Statement] | None = None) -> None:
        self.token = token
        self.statements = statements if statements is not None else []

    def __str__(self) -> str:
        return '{\n\t'+'\t'.join(map(str, self.statements))+'}'


class IfExpression(Expression):
    def __init__(self, token: token.Token, condition: Expression | None = None, consequence: BlockStatement | None = None, alternative: BlockStatement | None = None) -> None:
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self) -> str:
        return f"if {str(self.condition)} {str(self.consequence)}\n{'else '+ str(self.alternative) if self.alternative is not None else ''}"


class FunctionLiteral(Expression):
    def __init__(self, token: token.Token, parameters: list[Identifier] | None = None, body: BlockStatement | None = None) -> None:
        self.token = token
        self.parameters = parameters if parameters is not None else []
        self.body = body

    def __str__(self) -> str:
        params = ', '.join([str(p) for p in self.parameters])
        return f"{self.token_literal()}({params}) {str(self.body)}"


class CallExpression(Expression):
    def __init__(self, token: token.Token, function: Expression | None = None, arguments: list[Expression] | None = None) -> None:
        self.token = token
        self.function = function
        self.arguments = arguments if arguments is not None else []

    def __str__(self) -> str:
        args = ', '.join([str(a) for a in self.arguments])
        return f"{str(self.function)}({args})"


class LetStatement(Statement):
    def __init__(self, token: token.Token, name: Identifier | None = None, value: Expression | None = None) -> None:
        self.token = token
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.name)} = {str(self.value) if self.value is not None else 'None'};\n"


class ReturnStatement(Statement):
    def __init__(self, token: token.Token, return_value: Expression | None = None) -> None:
        self.token = token
        self.return_value = return_value

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.return_value) if self.return_value is not None else 'None'};\n"


class Program(Node):
    def __init__(self, stmts: list[Statement] | None = None) -> None:
        self.statements: list[Statement] = stmts if stmts is not None else []

    def __str__(self) -> str:
        return ''.join([str(s) for s in self.statements])

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""
