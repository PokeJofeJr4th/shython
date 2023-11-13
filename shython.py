"""
# Shython

A rudimentary subset of python, implemented in python
"""

import sys

import lexer
import shy_parser
import interpreter


def lex_file(filename):
    """
    Open a file and convert it to tokens
    """
    # pylint: disable=unspecified-encoding
    with open(filename) as file:
        return [lexer.make_tokens(line) for line in file]


def main(filename):
    """
    Run the full Shython pipeline on a given filename
    """
    tokens = lex_file(filename)
    for line in tokens:
        print(line)
    syntax = shy_parser.parse_file(tokens)
    print(syntax)
    interpreter.interpret(syntax)


if __name__ == "__main__":
    main(sys.argv[1])
