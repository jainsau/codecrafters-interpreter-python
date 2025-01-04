import sys
import argparse
from app.scanner import Scanner
from app.parser import Parser
from app.ast_printer import AstPrinter
from app.interpreter import Interpreter


def main():
    # Create the parser
    ap = argparse.ArgumentParser(description="Lox parser")

    # Add arguments
    ap.add_argument(
        "command", choices=["tokenize", "parse", "evaluate"], help="Command"
    )
    ap.add_argument("filename", type=str, help="Sourcefile")

    # Parse arguments
    args = ap.parse_args()

    with open(args.filename) as file:
        file_contents = file.read()

    if file_contents:
        tokens, errors = Scanner(file_contents).tokens
        had_error, expr = Parser(tokens).parse()

        if args.command == "tokenize":
            for token in tokens:
                print(token)
            for error in errors:
                print(error, file=sys.stderr)
        elif args.command == "parse":
            if had_error:
                exit(65)
            if expr:
                print(AstPrinter().print(expr))
        else:
            o = Interpreter().evaluate(expr)
            if o is None:
                print("nil")
            elif o is True:
                print("true")
            elif o is False:
                print("false")
            else:
                print(o)
        if errors:
            exit(65)
    else:
        print("EOF  null")


if __name__ == "__main__":
    main()
