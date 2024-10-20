import re


def tokenize(text: str) -> (str, str):
    i, line, output, errors = 0, 1, "", ""
    while i < len(text):
        l_token, line, lexeme, error = scanner(text[i:], line)
        output += lexeme
        errors += error
        i += l_token
    output += "EOF  null"

    return output, errors


def scanner(text: str, line: int) -> (int, bool, str, str):
    lexeme, error = "", ""
    match text:
        case _ if (m := re.match(r"[A-z_][\w]*", text)):
            t = m.group()
            if t in [
                "and",
                "class",
                "else",
                "false",
                "for",
                "fun",
                "if",
                "nil",
                "or",
                "print",
                "return",
                "super",
                "this",
                "true",
                "var",
                "while",
            ]:
                lexeme = f"{t.upper()} {t} null\n"
            else:
                lexeme = f"IDENTIFIER {t} null\n"
        case _ if (m := re.match(r"[\n]+", text)):
            # match newline character(s)
            t = m.group()
            line += len(t)
        case _ if (m := re.match(r"[ \t]+", text)):
            # match contiguous tabs and spaces
            t = m.group()
            pass
        case _ if (m := re.match(r"//.+", text)):
            # match comment
            t = m.group()
        case _ if (m := re.match(r"\"([^\"]*)\"", text)):
            # match strings
            t = m.group()
            lexeme = f"STRING {t} {m.group(1)}\n"
        case _ if (m := re.match(r"\"[^\"\n]*", text)):
            # match unbalanced strings (error)
            t = m.group()
            error = f"[line {line}] Error: Unterminated string.\n"
        case _ if (m := re.match(r"([\d]+)\.?([\d]*)", text)):
            # match number literals
            # handle trailing zeros sensibly
            t = m.group()
            if (fraction := re.sub(r"0+$", r"", f"{m.group(2)}")) == "":
                fraction = "0"
            lexeme = f"NUMBER {t} {m.group(1)}.{fraction}\n"
        case _ if (m := re.match(r"==", text)):
            t = m.group()
            lexeme = f"EQUAL_EQUAL {t} null\n"
        case _ if (m := re.match(r"!=", text)):
            t = m.group()
            lexeme = f"BANG_EQUAL {t} null\n"
        case _ if (m := re.match(r"<=", text)):
            t = m.group()
            lexeme = f"LESS_EQUAL {t} null\n"
        case _ if (m := re.match(r">=", text)):
            t = m.group()
            lexeme = f"GREATER_EQUAL {t} null\n"
        case _ if (m := re.match(r"\(", text)):
            t = m.group()
            lexeme = f"LEFT_PAREN {t} null\n"
        case _ if (m := re.match(r"\)", text)):
            t = m.group()
            lexeme = f"RIGHT_PAREN {t} null\n"
        case _ if (m := re.match(r"{", text)):
            t = m.group()
            lexeme = f"LEFT_BRACE {t} null\n"
        case _ if (m := re.match(r"}", text)):
            t = m.group()
            lexeme = f"RIGHT_BRACE {t} null\n"
        case _ if (m := re.match(r",", text)):
            t = m.group()
            lexeme = f"COMMA {t} null\n"
        case _ if (m := re.match(r"\.", text)):
            t = m.group()
            lexeme = f"DOT {t} null\n"
        case _ if (m := re.match(r"-", text)):
            t = m.group()
            lexeme = f"MINUS {t} null\n"
        case _ if (m := re.match(r"\+", text)):
            t = m.group()
            lexeme = f"PLUS {t} null\n"
        case _ if (m := re.match(r";", text)):
            t = m.group()
            lexeme = f"SEMICOLON {t} null\n"
        case _ if (m := re.match(r"/", text)):
            t = m.group()
            lexeme = f"SLASH {t} null\n"
        case _ if (m := re.match(r"\*", text)):
            t = m.group()
            lexeme = f"STAR {t} null\n"
        case _ if (m := re.match(r"=", text)):
            t = m.group()
            lexeme = f"EQUAL {t} null\n"
        case _ if (m := re.match(r"!", text)):
            t = m.group()
            lexeme = f"BANG {t} null\n"
        case _ if (m := re.match(r"<", text)):
            t = m.group()
            lexeme = f"LESS {t} null\n"
        case _ if (m := re.match(r">", text)):
            t = m.group()
            lexeme = f"GREATER {t} null\n"
        case _ if (m := re.match(r"/", text)):
            t = m.group()
            lexeme = f"SLASH {t} null\n"
        case _:
            t = text[0]
            error = f"[line {line}] Error: Unexpected character: {text[0]}\n"

    return len(t), line, lexeme, error
