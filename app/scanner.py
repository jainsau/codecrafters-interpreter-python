def scanner(c: str) -> str:
    match c:
        case "(":
            return "LEFT_PAREN ( null\n"
        case ")":
            return "RIGHT_PAREN ) null\n"
        case "{":
            return "LEFT_BRACE ( null\n"
        case "}":
            return "RIGHT_BRACE ) null\n"
    raise NotImplementedError("Unrecognized token")
