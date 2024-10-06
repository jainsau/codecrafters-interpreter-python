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
        for token in file_contents:
            if token == "\n":
                line += 1
            else:
                res, err = scanner(token)
                output = output + res if res != "" else output
                errors = errors + f"[line {line}] {err}" if err != "" else errors
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
