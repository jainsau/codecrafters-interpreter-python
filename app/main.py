from app.lox import Lox
from argparse import ArgumentParser
from app.parser import Parser
from app.ast_printer import AstPrinter
from app.interpreter import Interpreter
from app.scanner import ValidToken
from typing import List


def print_tokens(tokens: List[ValidToken]) -> List[ValidToken]:
    for token in tokens:
        print(token)
    if Lox.had_error:
        exit(65)


def print_expr(tokens: List[ValidToken]) -> None:
    parser = Parser(tokens)
    expr = parser.expr()
    printer = AstPrinter()

    if Lox.had_error:
        exit(65)
    print(printer.print(expr))


def evaluate_expr(tokens: List[ValidToken]) -> None:
    parser = Parser(tokens)
    expr = parser.expr()
    interpreter = Interpreter()

    if Lox.had_error:
        exit(65)
    interpreter.interpret_expr(expr)


def main():
    # Create the parser
    parser = ArgumentParser(description="Lox parser")

    # Add arguments
    parser.add_argument(
        "command", choices=["tokenize", "parse", "evaluate", "run"], help="Command"
    )
    parser.add_argument("filename", type=str, help="Sourcefile")

    # Parse arguments
    args = parser.parse_args()

    source = Lox.read_file(args.filename)
    tokens = Lox.tokenize(source)

    if args.command == "tokenize":
        print_tokens(tokens)
    if args.command == "parse":
        print_expr(tokens)
    if args.command == "evaluate":
        evaluate_expr(tokens)
    if args.command == "run":
        Lox.run_file(args.filename)


if __name__ == "__main__":
    main()
