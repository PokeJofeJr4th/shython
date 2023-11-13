"""
# Shython Lexer

Turns a list of file lines into a list of tokens
"""
# pylint: disable=too-few-public-methods


class Identifier:
    """
    A token representing an identifier
    """

    __slots__ = ["name"]

    def __init__(self, name):
        self.name = str(name)

    def __repr__(self):
        return self.name


class Symbol:
    """
    A token representing a miscellaneous symbol
    """

    __slots__ = ["symbol"]

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return repr(self.symbol)


def compare_token(token, compare):
    """
    Check if a symbol matches a certain string
    """
    if not isinstance(token, Symbol):
        return False
    return token.symbol == compare


ASCII_A = ord("A")
ASCII_Z = ord("Z")
ASCII_A_LOWER = ord("a")
ASCII_Z_LOWER = ord("z")
ASCII_0 = ord("0")
ASCII_9 = ord("9")


def is_alphabetic(a_char):
    """
    check if a character is a letter or "_"
    """
    return (
        ASCII_A <= ord(a_char) <= ASCII_Z
        or ASCII_A_LOWER <= ord(a_char) <= ASCII_Z_LOWER
        or a_char == "_"
    )


def is_numeric(a_char):
    """
    check if a character is a number
    """
    return ASCII_0 <= ord(a_char) <= ASCII_9


def is_alphanumeric(a_char):
    """
    check if a character is a letter, "_", or number
    """
    return is_alphabetic(a_char) or is_numeric(a_char)


def is_token(a_char):
    """
    Check if a character is a symbol
    """
    return (
        33 <= ord(a_char) <= 47
        or 58 <= ord(a_char) <= 64
        or 91 <= ord(a_char) <= 96
        or 123 <= ord(a_char) <= 126
    )


def make_tokens(a_string):
    """
    Turn a string into a list of tokens
    """
    index = 0
    length = len(a_string)
    tokens = []
    while index < length:
        character = a_string[index]
        if is_alphabetic(character):
            identifier_buffer = character
            index += 1
            while index < length and is_alphanumeric(a_string[index]):
                identifier_buffer += a_string[index]
                index += 1
            tokens.append(Identifier(identifier_buffer))
        elif is_numeric(character):
            int_buffer = character
            index += 1
            while index < length and is_numeric(a_string[index]):
                int_buffer += a_string[index]
                index += 1
            tokens.append(int(int_buffer))
        elif is_token(character) or character == "\n" or character == "\t":
            tokens.append(Symbol(character))
            index += 1
        elif character == " ":
            if a_string[index : index + 4] == "    ":
                tokens.append(Symbol("\t"))
                index += 4
            else:
                index += 1
        else:
            raise SyntaxError("Unexpected Character", character)
    return tokens
