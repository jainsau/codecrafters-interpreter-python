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
            return "COMMA , null\n"
        case ".":
            return "DOT . null\n"
        case "-":
            return "MINUS - null\n"
        case "+":
            return "PLUS + null\n"
        case ";":
            return "SEMICOLON ; null\n"
        case "/":
            return "SLASH / null\n"
        case "*":
            return "STAR * null\n"

    raise NotImplementedError("Unrecognized token")
