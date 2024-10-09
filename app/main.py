import sys
import re
from app.scanner import scanner


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Uncomment this block to pass the first stage
    if file_contents:
        line, output, errors = 1, "", ""
        i = 0
        while i < len(file_contents):
            token = file_contents[i]
            if (i + 1) < len(file_contents) and file_contents[i : i + 2] in [
                "==",
                "!=",
                "<=",
                ">=",
            ]:
                res, _ = scanner(file_contents[i : i + 2])
                output = output + res if res != "" else output
                i += 2
                continue
            elif (i + 1) < len(file_contents) and file_contents[i : i + 2] == "//":
                while i < len(file_contents) and file_contents[i] != "\n":
                    i += 1
                line += 1
            elif token == "\n":
                line += 1
            elif token in [" ", "\t"]:
                pass
            elif token == '"':
                res, err = "", ""
                i += 1
                while True:
                    if i == len(file_contents) or file_contents[i] == "\n":
                        res, err = "", f"[line {line}] Error: Unterminated string.\n"
                        line += 1
                        break
                    elif file_contents[i] == '"':
                        break
                    else:
                        res += file_contents[i]
                    i += 1
                errors += err
                output = output + f'STRING "{res}" {res}\n' if res != "" else output
            elif token in "0123456789":
                res = token
                i += 1
                while i < len(file_contents):
                    if file_contents[i] in ".0123456789":
                        res += file_contents[i]
                    else:
                        break
                    i += 1
                if "." in res:
                    res_ = res
                    # drop extra zeros past decimal
                    while res.endswith("0"):
                        res = res[:-1]
                    if res.endswith("."):
                        res += "0"
                    output = output + f"NUMBER {res_} {res}\n"
                else:
                    output = output + f"NUMBER {res} {res}.0\n"
                continue
            elif re.search("[A-z_]", token):
                res = re.search("^[A-z_][A-z_0-9]*", file_contents[i:]).group()
                output += f"IDENTIFIER {res} null\n"
                i += len(res)
                continue
            else:
                res, err = scanner(token)
                output = output + res if res != "" else output
                errors = errors + f"[line {line}] {err}" if err != "" else errors
            i += 1
        output += "EOF  null"
        print(errors, file=sys.stderr)
        print(output)
        if errors != "":
            exit(65)
    else:
        print(
            "EOF  null"
        )  # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
