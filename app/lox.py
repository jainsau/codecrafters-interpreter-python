from app.parser import Parser
from app.scanner import Scanner, ValidToken, ValidTokenType
from app.interpreter import Interpreter
from app.error import RuntimeError_
from sys import stderr
from typing import List


class Lox:
    _interpreter: Interpreter = Interpreter()
    had_error: bool = False
    had_runtime_error: bool = False

    @staticmethod
    def read_file(path: str) -> str:
        with open(path) as file:
            source = file.read()
        return source

    @staticmethod
    def tokenize(source: str) -> List[ValidToken]:
        scanner = Scanner(source)
        tokens = scanner.scan()

        return tokens

    @staticmethod
    def parse(tokens: List[ValidToken]) -> None:
        parser = Parser(tokens)
        statements = parser.parse()

        return statements

    @classmethod
    def run_file(cls, path: str) -> None:
        source = cls.read_file(path)
        cls.run(source)

        if cls.had_error:
            exit(65)

        if cls.had_runtime_error:
            exit(70)

    @classmethod
    def run(cls, source: str) -> None:
        tokens = cls.tokenize(source)
        statements = cls.parse(tokens)

        if cls.had_error:
            return

        cls._interpreter.interpret(statements)

    @classmethod
    def error1(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def error2(cls, token: ValidToken, message: str):
        if token.type == ValidTokenType.EOF:
            cls.report(token.line, " at end", message)
        else:
            cls.report(token.line, f" at '{token.lexeme}'", message)

    @classmethod
    def report(cls, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=stderr)
        cls.had_error = True

    @staticmethod
    def runtime_error(error: RuntimeError_) -> None:
        print(f"{error.args[0]}\n[line {error.token.line}]", file=stderr)
        exit(70)
