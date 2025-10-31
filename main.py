import sys
import getpass
from repl import repl

if __name__ == "__main__":
    if len(sys.argv) > 1:
        source_code = sys.argv[1]
        with open(source_code) as f:
            repl.interpret_file(f, sys.stdout)
    else:
        print(
            f"Hello {getpass.getuser()}! This is the Monkey programming language!")
        print("Feel free to type in commands")
        repl.start(sys.stdin, sys.stdout)
