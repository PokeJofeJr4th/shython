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
        self.name: str = str(name)

    def __repr__(self) -> str:
        return self.name


class Symbol:
    """
    A token representing a miscellaneous symbol
    """

    __slots__ = ["symbol"]

    def __init__(self, symbol: str):
        self.symbol: str = symbol

    def __repr__(self) -> str:
        return repr(self.symbol)


token = Identifier | Symbol | int


ASCII_A = ord("A")
ASCII_Z = ord("Z")
ASCII_A_LOWER = ord("a")
ASCII_Z_LOWER = ord("z")
ASCII_0 = ord("0")
ASCII_9 = ord("9")


def compare_symbol(token: token, compare: str) -> bool:
    """
    Check if a symbol matches a certain string
    """
    if not isinstance(token, Symbol):
        return False
    return token.symbol == compare


def is_alphabetic(c: str) -> bool:
    """
    check if a character is a letter or "_"
    """
    return (
        ASCII_A <= ord(c) <= ASCII_Z
        or ASCII_A_LOWER <= ord(c) <= ASCII_Z_LOWER
        or c == "_"
    )


def is_numeric(c: str) -> bool:
    """
    check if a character is a number
    """
    return ASCII_0 <= ord(c) <= ASCII_9


def is_alphanumeric(c: str) -> bool:
    """
    check if a character is a letter, "_", or number
    """
    return is_alphabetic(c) or is_numeric(c)


def is_token(c: str) -> bool:
    """
    Check if a character is a symbol
    """
    return (
        33 <= ord(c) <= 47
        or 58 <= ord(c) <= 64
        or 91 <= ord(c) <= 96
        or 123 <= ord(c) <= 126
    )


def make_tokens(a_string: str) -> list[token]:
    """
    Turn a string into a list of tokens
    """
    index: int = 0
    length: int = len(a_string)
    tokens: list[token] = []
    while index < length:
        character: str = a_string[index]
        if is_alphabetic(character):
            identifier_buffer: str = character
            index += 1
            while index < length and is_alphanumeric(a_string[index]):
                identifier_buffer += a_string[index]
                index += 1
            tokens.append(Identifier(identifier_buffer))
        elif is_numeric(character):
            int_buffer: str = character
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
