from my_ast import ast
from lexer import lexer
from my_token import token

class Parser:
    def __init__(self, l: lexer.Lexer) -> None:
        self.l = l
        self.cur_token: token.Token = self.l.next_token()
        self.peek_token: token.Token = self.l.next_token()
        self.errors:list[str]=[]

    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()

    def parse_program(self)->ast.Program:
        program=ast.Program()

        while self.cur_token.type!=token.EOF:
            stmt=self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()
        
        return program
    
    def parse_statement(self)->ast.Statement|None:
        match self.cur_token.type:
            case token.LET: return self.parse_let_statement()
            case token.RETURN:return self.parse_return_statement()
            case _:return None
    
    def parse_let_statement(self)->ast.LetStatement|None:
        stmt=ast.LetStatement(self.cur_token)
        if not self.expect_peek(token.TokenType(token.IDENT)):
            return None
        stmt.name=ast.Identifier(self.cur_token,self.cur_token.literal)
        if not self.expect_peek(token.TokenType(token.ASSIGN)):
            return None
        while not self.cur_token_is(token.TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt
    
    def parse_return_statement(self)->ast.ReturnStatement|None:
        stmt=ast.ReturnStatement(self.cur_token)
        while not self.cur_token_is(token.TokenType(token.SEMICOLON)):
            self.next_token()
        return stmt

    def cur_token_is(self,t:token.TokenType)->bool:
        return self.cur_token.type==t

    def peek_token_is(self,t:token.TokenType)->bool:
        return self.peek_token.type==t

    def expect_peek(self,t:token.TokenType)->bool:
        if self.peek_token_is(t):
            self.next_token()
            return True
        else:
            self.peek_error(t)
            return False

    def Errors(self)->list[str]:
        return self.errors
    
    def peek_error(self,t:token.TokenType)->None:
        msg=f"expected next token to be {t}, got {self.peek_token.type} instead"
        self.errors.append(msg)