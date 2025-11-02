import sys
import getpass
import argparse
from repl import repl


def parse_args():
    parser = argparse.ArgumentParser(description="Monkey Programming Language")
    parser.add_argument("source", nargs="?",
                        type=argparse.FileType("r"), default=sys.stdin, help="Source code file to interpret (Optional)")
    parser.add_argument(
        "--mode", choices=["l", "p", "e"], default="e", help="Set the mode of the REPL {l: lex, p: parse, e: evaluate} (default: e)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.source != sys.stdin:
        repl.interpret_file(args.source, sys.stdout, args.mode)
    else:
        print(
            f"Hello {getpass.getuser()}! This is the Monkey programming language!")
        print("Feel free to type in commands")
        repl.start(sys.stdin, sys.stdout, args.mode)

    #     with open(source_code) as f:
    #         repl.interpret_file(f, sys.stdout)
    # else:
    #     print(
    #         f"Hello {getpass.getuser()}! This is the Monkey programming language!")
    #     print("Feel free to type in commands")
    #     repl.start(sys.stdin, sys.stdout)
