import lexer


class Operation:
    __slots__ = ["left", "right", "operation"]

    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

    def __repr__(self) -> str:
        return f"({repr(self.left)}){self.operation}({repr(self.right)})"


class Block:
    __slots__ = ["block_type", "condition", "body"]

    def __init__(self, block_type, condition, body) -> None:
        self.block_type = block_type
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"{self.block_type} {self.condition}: {self.body}"


class FunctionCall:
    __slots__ = ["function", "argument"]

    def __init__(self, function, argument) -> None:
        self.function = function
        self.argument = argument

    def __repr__(self) -> str:
        return f"{self.function}({self.argument})"


def is_literal(syntax):
    return (
        isinstance(syntax, int)
        or isinstance(syntax, float)
        or isinstance(syntax, str)
        or isinstance(syntax, bool)
    )


def group_blocks(lines, index=0, indent=0):
    statements = []
    while index < len(lines):
        line = lines[index]
        line_indent = 0
        for token in line:
            if lexer.compare_token(token, "\t"):
                line_indent += 1
            else:
                break
        if line_indent < indent:
            return index - 1, statements
        elif line_indent > indent:
            index, statement = group_blocks(lines, index, line_indent)
            statements.append(statement)
        else:
            # line_indent == indent
            statements.append(line[line_indent:])
        index += 1
    return index, statements


def parse_file(lines):
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
    statement = lines[index]
    first_item = statement[0]
    if isinstance(first_item, list):
        raise IndentationError(f"Unexpected indent; {statement}")
    elif isinstance(first_item, lexer.Identifier) and first_item.name in BLOCK_TYPES:
        _, condition = make_operation(1, statement)
        body = parse_file(lines[index + 1])
        return index + 2, Block(first_item.name, condition, body)
    elif lexer.compare_token(first_item, "\n"):
        return index + 1, None
    else:
        _, statement = make_operation(0, statement)
        return index + 1, statement


def get_one_item(index, tokens):
    token = tokens[index]
    if isinstance(token, lexer.Identifier):
        return index + 1, token
    elif isinstance(token, int):
        return index + 1, token
    else:
        raise SyntaxError(f"Invalid token at {index} of {tokens}")


OPERATIONS = [["<", ">", "!", "="], ["+", "-"], ["*", "/", "%"]]


def make_operation(index, tokens, priority=0):
    if priority >= len(OPERATIONS):
        index, left = get_one_item(index, tokens)
        while index < len(tokens) and lexer.compare_token(tokens[index], "("):
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
        if lexer.compare_token(tokens[index], "="):
            operation += "="
            index += 1
        if operation == "!":
            raise SyntaxError("Invalid operation `!`")
        index, right = make_operation(index, tokens, priority + 1)
        left = Operation(left, operation, right)
        token = tokens[index]
    return index, left


def optimize_syntax(syntax):
    if isinstance(syntax, Operation):
        syntax.left = optimize_syntax(syntax.left)
        syntax.right = optimize_syntax(syntax.right)
        if is_literal(syntax.left) and is_literal(syntax.right):
            if syntax.operation == "+":
                return syntax.left + syntax.right
            elif syntax.operation == "-":
                return syntax.left - syntax.right
            elif syntax.operation == "*":
                return syntax.left * syntax.right
            elif syntax.operation == "/":
                return syntax.left / syntax.right
            elif syntax.operation == "%":
                return syntax.left % syntax.right
            elif syntax.operation == "<":
                return syntax.left < syntax.right
            elif syntax.operation == ">":
                return syntax.left > syntax.right
            elif syntax.operation == "<=":
                return syntax.left <= syntax.right
            elif syntax.operation == ">=":
                return syntax.left >= syntax.right
            elif syntax.operation == "==":
                return syntax.left == syntax.right
            elif syntax.operation == "!=":
                return syntax.left != syntax.right
    return syntax
