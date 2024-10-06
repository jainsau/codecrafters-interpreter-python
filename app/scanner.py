def scanner(c: str) -> str:
    match c:
        case "(":
            return "LEFT_PAREN ( null\n"
        case ")":
            return "RIGHT_PAREN ) null\n"
        case "{":
            return "LEFT_BRACE { null\n"
        case "}":
            return "RIGHT_BRACE } null\n"
        case ",":
            return "COMMA , null"
        case ".":
            return "DOT . null"
        case "-":
            return "MINUS - null"
        case "+":
            return "PLUS + null"
        case ";":
            return "SEMICOLON ; null"
        case "/":
            return "SLASH / null"
        case "*":
            return "STAR * null"

    raise NotImplementedError("Unrecognized token")
