import sys

import lexer
import shy_parser
import interpreter


def lex_file(filename):
    with open(filename) as file:
        return [lexer.make_tokens(line) for line in file]


def main(filename):
    tokens = lex_file(filename)
    for line in tokens:
        print(line)
    syntax = shy_parser.parse_file(tokens)
    print(syntax)
    interpreter.interpret(syntax)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
