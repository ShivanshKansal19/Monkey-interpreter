import sys
import getpass
from repl import repl

if __name__ == "__main__":
    print(f"Hello {getpass.getuser()}! This is the Monkey programming language!")
    print("Feel free to type in commands")
    repl.start(sys.stdin, sys.stdout)
