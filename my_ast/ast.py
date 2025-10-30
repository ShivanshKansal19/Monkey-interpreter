from my_token import token

class Node:
    def token_literal(self) -> str:
        raise NotImplementedError()

class Statement(Node):
    def statement_node(self) -> None:
        pass

class Expression(Node):
    def expression_node(self) -> None:
        pass

class Identifier(Expression):
    def __init__(self, token:token.Token, value:str) -> None:
        self.token=token
        self.value=value
    def token_literal(self)->str:
        return self.token.literal

class LetStatement(Statement):
    def __init__(self, token:token.Token) -> None:
        self.token=token
        self.name: Identifier|None =None
        self.value: Expression|None =None
    def token_literal(self)->str:
        return self.token.literal

class ReturnStatement(Statement):
    def __init__(self, token:token.Token) -> None:
        self.token=token
        self.return_value: Expression|None =None
    def token_literal(self)->str:
        return self.token.literal

class Program(Node):
    def __init__(self) -> None:
        self.statements: list[Statement] = []
    def token_literal(self)->str:
        if len(self.statements)>0:
            return self.statements[0].token_literal()
        else:
            return ""
        