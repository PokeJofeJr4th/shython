"""
# Shython Interpreter

Run Shython code that's been parsed already
"""

import lexer
import shy_parser


def interpret(source):
    """
    Interpret a whole program
    """
    variables = {"print": print, "int": int, "input": input, "chr": chr}
    inner_interpret(source, variables)


def inner_interpret(lines, variables):
    """
    Interpret a block of code
    """
    index = 0
    while index < len(lines):
        syntax = lines[index]
        interpret_syntax(syntax, variables)
        index += 1


COMPARISON_OPERATIONS = ["==", "<", "<=", ">", ">=", "!="]


def interpret_syntax(syntax, variables):
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    """
    Evaluate a single syntax element
    """
    if isinstance(syntax, shy_parser.Operation):
        operation = syntax.operation
        if (
            operation == "="
            or len(operation) == 2
            and operation not in COMPARISON_OPERATIONS
        ):
            value = interpret_syntax(syntax.right, variables)
            if not isinstance(syntax.left, lexer.Identifier):
                raise SyntaxError(
                    f"Can't assign to {syntax.left}; must be an identifier"
                )
            if operation == "=":
                variables[syntax.left.name] = value
            elif operation == "+=":
                variables[syntax.left.name] += value
            elif operation == "-=":
                variables[syntax.left.name] -= value
            elif operation == "*=":
                variables[syntax.left.name] *= value
            elif operation == "/=":
                variables[syntax.left.name] /= value
            elif operation == "%=":
                variables[syntax.left.name] %= value
            return None

        left = interpret_syntax(syntax.left, variables)
        right = interpret_syntax(syntax.right, variables)
        if operation == "==":
            return left == right
        if operation == "<":
            return left < right
        if operation == ">":
            return left > right
        if operation == "<=":
            return left <= right
        if operation == ">=":
            return left >= right
        if operation == "!=":
            return left != right
        if operation == "+":
            return left + right
        if operation == "-":
            return left - right
        if operation == "*":
            return left * right
        if operation == "/":
            return left / right
        if operation == "%":
            return left % right
        raise SyntaxError(f"Invalid operation: {operation}; {syntax}")
    if isinstance(syntax, shy_parser.Block):
        if syntax.block_type == "while":
            while interpret_syntax(syntax.condition, variables):
                inner_interpret(syntax.body, variables)
        elif syntax.block_type == "if":
            if interpret_syntax(syntax.condition, variables):
                inner_interpret(syntax.body, variables)
        else:
            raise SyntaxError(f"Invalid Block Type: {syntax.block_type}")
        return None
    if isinstance(syntax, shy_parser.FunctionCall):
        function = interpret_syntax(syntax.function, variables)
        argument = interpret_syntax(syntax.argument, variables)
        # print(syntax, syntax.function, syntax.argument, function, argument)
        return function(argument)
    if isinstance(syntax, lexer.Identifier):
        return variables[syntax.name]
    if isinstance(syntax, int):
        return syntax
    raise SyntaxError(f"Invalid Syntax: {syntax}")
