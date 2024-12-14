import sys
import argparse
from app.scanner import Scanner
from app.parser import Parser
from app.ast_printer import AstPrinter


def main():
    # Create the parser
    ap = argparse.ArgumentParser(description="Lox parser")

    # Add arguments
    ap.add_argument("command", choices=["tokenize", "parse"], help="Command")
    ap.add_argument("filename", type=str, help="Sourcefile")

    # Parse arguments
    args = ap.parse_args()

    with open(args.filename) as file:
        file_contents = file.read()

    if file_contents:
        s = Scanner(file_contents)
        tokens, errors = s.tokens
        if args.command == "tokenize":
            for token in tokens:
                print(token)
            for error in errors:
                print(error, file=sys.stderr)
        else:
            p = Parser(tokens)
            had_error, expr = p.parse()
            if had_error:
                exit(65)
            if expr:
                print(AstPrinter().print(expr))
        if errors:
            exit(65)
    else:
        print("EOF  null")


if __name__ == "__main__":
    main()
