import sys
import argparse
from app.scanner import Scanner
from app.parser import Parser
from app.ast_printer import AstPrinter


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Lox parser")

    # Add arguments
    parser.add_argument("command", choices=["tokenize", "parse"], help="Command")
    parser.add_argument("filename", type=str, help="Sourcefile")

    # Parse arguments
    args = parser.parse_args()

    with open(args.filename) as file:
        file_contents = file.read()

    if file_contents:
        s = Scanner(file_contents)
        tokens, errors = s.tokens
        if args.command == "tokenize":
            for token in tokens:
                print(token)
            print("EOF  null")
            for error in errors:
                print(error, file=sys.stderr)
            if errors:
                exit(65)
        else:
            t = Parser(tokens)
            p = AstPrinter()
            print(p.print(t.expression()))
    else:
        print("EOF  null")


if __name__ == "__main__":
    main()
