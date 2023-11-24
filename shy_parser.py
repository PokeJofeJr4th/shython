"""
# Shython Parser

Parse shython tokens into a syntax tree
"""
# pylint: disable=too-few-public-methods

import lexer


class Operation:
    """
    Any kind of binary operation
    """

    __slots__ = ["left", "right", "operation"]

    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

    def __repr__(self) -> str:
        return f"({repr(self.left)}){self.operation}({repr(self.right)})"


class Block:
    """
    An indented block of code with a qualifier
    """

    __slots__ = ["block_type", "condition", "body"]

    def __init__(self, block_type, condition, body) -> None:
        self.block_type = block_type
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"{self.block_type} {self.condition}: {self.body}"


class FunctionCall:
    """
    Callling a function
    """

    __slots__ = ["function", "argument"]

    def __init__(self, function, argument) -> None:
        self.function = function
        self.argument = argument

    def __repr__(self) -> str:
        return f"{self.function}({self.argument})"


syntax = Operation | FunctionCall | Block | int | str | bool | float | lexer.Identifier


def is_literal(syn):
    """
    Check if a syntax element is a literal value that can be evaluated at compile time
    """
    return isinstance(syn, (int, float, str, bool))


def group_blocks(lines, index=0, indent=0):
    """
    Group levels of indentation
    """
    statements = []
    while index < len(lines):
        line = lines[index]
        line_indent = 0
        for token in line:
            if lexer.compare_symbol(token, "\t"):
                line_indent += 1
            else:
                break
        if line_indent < indent:
            return index - 1, statements
        if line_indent > indent:
            index, statement = group_blocks(lines, index, line_indent)
            statements.append(statement)
        else:
            # line_indent == indent
            statements.append(line[line_indent:])
        index += 1
    return index, statements


def parse_file(lines):
    """
    Parse a file of tokens
    """
    _, lines = group_blocks(lines)
    index = 0
    statements = []
    while index < len(lines):
        index, statement = parse_statement(lines, index)
        statement = optimize_syntax(statement)
        if isinstance(statement, list):
            statements.extend(statement)
        if statement is not None:
            statements.append(statement)
    return statements


BLOCK_TYPES = ["while", "if"]


def parse_statement(lines, index=0):
    """
    Parse a single line of Shython code
    """
    statement = lines[index]
    first_item = statement[0]
    if isinstance(first_item, list):
        raise IndentationError(f"Unexpected indent; {statement}")
    if isinstance(first_item, lexer.Identifier) and first_item.name in BLOCK_TYPES:
        _, condition = make_operation(1, statement)
        body = parse_file(lines[index + 1])
        return index + 2, Block(first_item.name, condition, body)
    if lexer.compare_symbol(first_item, "\n"):
        return index + 1, None
    _, statement = make_operation(0, statement)
    return index + 1, statement


def get_one_item(index: int, tokens: list[lexer.token]) -> tuple[int, syntax]:
    """
    Take the smallest unit of syntax possible
    """
    token: lexer.token = tokens[index]
    if isinstance(token, lexer.Identifier):
        return index + 1, token
    if is_literal(token):
        return index + 1, token  # type: ignore
    raise SyntaxError(f"Invalid token at {index} of {tokens}")


OPERATIONS = [["<", ">", "!", "="], ["+", "-"], ["*", "/", "%"]]


def make_operation(index: int, tokens: list[lexer.token], priority=0):
    """
    Parse a syntax operation
    """
    if priority >= len(OPERATIONS):
        index, left = get_one_item(index, tokens)
        while index < len(tokens) and lexer.compare_symbol(tokens[index], "("):
            index, argument = make_operation(index + 1, tokens)
            index += 1
            left = FunctionCall(left, argument)
        return index, left
    index, left = make_operation(index, tokens, priority + 1)
    operations = OPERATIONS[priority]
    if index >= len(tokens):
        return index, left
    token = tokens[index]
    while isinstance(token, lexer.Symbol) and token.symbol in operations:
        index += 1
        operation = token.symbol
        if lexer.compare_symbol(tokens[index], "="):
            operation += "="
            index += 1
        if operation == "!":
            raise SyntaxError("Invalid operation `!`")
        index, right = make_operation(index, tokens, priority + 1)
        left = Operation(left, operation, right)
        token = tokens[index]
    return index, left


def optimize_syntax(syn: syntax | None) -> syntax | None:
    """
    Optimize the syntax tree
    """
    # pylint: disable=too-many-return-statements,too-many-branches
    if isinstance(syn, Operation):
        syn.left = optimize_syntax(syn.left)
        syn.right = optimize_syntax(syn.right)
        if is_literal(syn.left) and is_literal(syn.right):
            if syn.operation == "+":
                return syn.left + syn.right  # type: ignore
            if syn.operation == "-":
                return syn.left - syn.right  # type: ignore
            if syn.operation == "*":
                return syn.left * syn.right  # type: ignore
            if syn.operation == "/":
                return syn.left / syn.right  # type: ignore
            if syn.operation == "%":
                return syn.left % syn.right  # type: ignore
            if syn.operation == "<":
                return syn.left < syn.right  # type: ignore
            if syn.operation == ">":
                return syn.left > syn.right  # type: ignore
            if syn.operation == "<=":
                return syn.left <= syn.right  # type: ignore
            if syn.operation == ">=":
                return syn.left >= syn.right  # type: ignore
            if syn.operation == "==":
                return syn.left == syn.right
            if syn.operation == "!=":
                return syn.left != syn.right
    return syn
