from typing import TextIO
from lexer import lexer
from parser import parser
from my_token import token
from my_ast import ast

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
    # out.write(str(program))
    print_parse_tree(out, program)


def print_parser_errors(out: TextIO, errors: list[str]) -> None:
    out.write(MONKEY_FACE)
    out.write("Woops! We ran into some monkey business here!\n")
    out.write("Parser errors:\n")
    for msg in errors:
        out.write(f"\t{msg}\n")


def print_parse_tree(out: TextIO, node: ast.Node, indent_width: int = 4, line_space: int = 1) -> None:
    if node is None:
        return

    def _write_line(node: ast.Node, indent: str = '', name: str = '') -> None:
        class_name = type(node).__name__
        if isinstance(node, ast.Program):
            class_name = f"\033[0;91m{class_name}\033[0m"
        elif isinstance(node, (ast.IntegerLiteral, ast.Boolean)):
            class_name = f"\033[0;92m{class_name} (\033[0;33m{str(node.value)}\033[0;92m)\033[0m"
        elif isinstance(node, ast.Identifier):
            class_name = f"\033[0;94m{class_name} (\033[0;33m'{node.value}'\033[0;94m)\033[0m"
        elif isinstance(node, (ast.PrefixExpression, ast.InfixExpression)):
            class_name = f"\033[0;95m{class_name} (\033[0;33m'{node.operator}'\033[0;95m)\033[0m"
        elif isinstance(node, ast.Statement):
            class_name = f"\033[0;96m{class_name}\033[0m"
        else:
            class_name = f"\033[0;93m{class_name}\033[0m"
        name = f"\033[3;90m{name}\033[0m: " if name else ""
        out.write(indent + name + class_name + "\n")

    def _print_parse_tree(parent: ast.Node, indent: str = '') -> None:
        items = [item for item in parent.__dict__.items(
        ) if item[1] is not None and item[0] != 'token']

        for i, (name, child) in enumerate(items):
            symbol = "└" if i == len(items) - 1 else "├"
            new_indent = " " * \
                (indent_width + 1) if i == len(items) - \
                1 else "│" + " " * indent_width

            if isinstance(child, list):
                for j in range(len(child)):
                    symbol = "└" if i == len(
                        items) - 1 and j == len(child) - 1 else "├"
                    new_indent = " " * \
                        (indent_width + 1) if i == len(items)-1 and j == len(child) - \
                        1 else "│" + " " * indent_width

                    item = child[j]
                    if isinstance(item, ast.Node):
                        for _ in range(line_space):
                            out.write(indent + "│" + " " * indent_width + '\n')
                        _write_line(item, indent + symbol +
                                    "─" * indent_width, f"{name}[{j}]")
                        _print_parse_tree(
                            item, indent + new_indent)

            elif isinstance(child, ast.Node):
                for _ in range(line_space):
                    out.write(indent + "│" + " " * indent_width + '\n')
                _write_line(child, indent + symbol + "─" * indent_width, name)
                _print_parse_tree(child, indent + new_indent)

    _write_line(node)
    _print_parse_tree(node)
