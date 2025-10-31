from typing import TextIO
from lexer import lexer
from parser import parser
from my_token import token

MONKEY_FACE = r'''            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"""""""-./, -' /
   ''-' /_   ^ ^   _\ '-''
       |  \._   _./  |
       \   \ '~' /   /
        '._ '-=-' _.'
           '-----'
'''


prompt = ">>"


def start(inp: TextIO, out: TextIO) -> None:
    while True:
        out.write(prompt)
        out.flush()
        line = inp.readline().strip()
        if not line:
            break
        print_parsed_program(out, line)


def interpret_file(file: TextIO, out: TextIO) -> None:
    source = file.read()
    print_parsed_program(out, source)


def print_lexer_tokens(out: TextIO, source: str) -> None:
    l = lexer.Lexer(source)
    tok = l.next_token()
    while tok.type != token.EOF:
        out.write(f"{tok}\n")
        tok = l.next_token()


def print_parsed_program(out: TextIO, source: str) -> None:
    l = lexer.Lexer(source)
    p = parser.Parser(l)
    program = p.parse_program()
    if len(p.errors) != 0:
        print_parser_errors(out, p.errors)
        return
    out.write(str(program))


def print_parser_errors(out: TextIO, errors: list[str]) -> None:
    out.write(MONKEY_FACE)
    out.write("Woops! We ran into some monkey business here!\n")
    out.write("Parser errors:\n")
    for msg in errors:
        out.write(f"\t{msg}\n")
