import sys
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
            elif token == "\n":
                line += 1
            # elif (
            #     token == "="
            #     and (i + 1) < len(file_contents)
            #     and file_contents[i : i + 2] == "=="
            # ):
            #     res, _ = scanner(file_contents[i : i + 2])
            #     output = output + res if res != "" else output
            #     i += 2
            #     continue
            # elif (
            #     token == "!"
            #     and (i + 1) < len(file_contents)
            #     and file_contents[i : i + 2] == "!="
            # ):
            #     res, _ = scanner(file_contents[i : i + 2])
            #     output = output + res if res != "" else output
            #     i += 2
            #     continue
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
