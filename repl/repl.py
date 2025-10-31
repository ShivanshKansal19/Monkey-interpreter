from typing import TextIO
from lexer import lexer
from my_token import token

prompt = ">>"


def start(inp: TextIO, out: TextIO) -> None:
    while True:
        out.write(prompt)
        out.flush()
        line = inp.readline().strip()
        if not line:
            break
        l = lexer.Lexer(line)
        tok = l.next_token()
        while tok.type != token.EOF:
            out.write(f"{tok}\n")
            tok = l.next_token()


def interpret_file(file: TextIO, out: TextIO) -> None:
    for line in file:
        if not line:
            break
        l = lexer.Lexer(line)
        tok = l.next_token()
        while tok.type != token.EOF:
            out.write(f"{tok}\n")
            tok = l.next_token()
