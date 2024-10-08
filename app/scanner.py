def scanner(c: str) -> str:
    match c:
        case "(":
            return "LEFT_PAREN ( null\n", ""
        case ")":
            return "RIGHT_PAREN ) null\n", ""
        case "{":
            return "LEFT_BRACE { null\n", ""
        case "}":
            return "RIGHT_BRACE } null\n", ""
        case ",":
            return "COMMA , null\n", ""
        case ".":
            return "DOT . null\n", ""
        case "-":
            return "MINUS - null\n", ""
        case "+":
            return "PLUS + null\n", ""
        case ";":
            return "SEMICOLON ; null\n", ""
        case "/":
            return "SLASH / null\n", ""
        case "*":
            return "STAR * null\n", ""
        case "=":
            return "EQUAL = null\n", ""
        case "==":
            return "EQUAL_EQUAL == null\n", ""
        case "!":
            return "BANG ! null\n", ""
        case "!=":
            return "BANG_EQUAL != null\n", ""
        case "<":
            return "LESS < null\n", ""
        case ">":
            return "GREATER > null\n", ""
        case "<=":
            return "LESS_EQUAL <= null\n", ""
        case ">=":
            return "GREATER_EQUAL >= null\n", ""
        case "/":
            return "SLASH / null\n", ""
        case _:
            return "", f"Error: Unexpected character: {c}\n"
