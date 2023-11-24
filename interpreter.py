"""
# Shython Interpreter

Run Shython code that's been parsed already
"""
from typing import Callable
import lexer
import shy_parser

shython_value = int | float | str | Callable | type | None | bool


def interpret(source: list):
    """
    Interpret a whole program
    """
    variables: dict[str, shython_value] = {
        "print": print,
        "int": int,
        "input": input,
        "chr": chr,
        "True": True,
        "False": False,
    }
    inner_interpret(source, variables)


def inner_interpret(lines: list, variables: dict[str, shython_value]):
    """
    Interpret a block of code
    """
    index = 0
    while index < len(lines):
        syntax = lines[index]
        interpret_syntax(syntax, variables)
        index += 1


ASSIGNMENT_OPERATIONS: list[str] = ["=", "+=", "-=", "*=", "/=", "%="]


def interpret_syntax(syntax, variables: dict[str, shython_value]) -> shython_value:
    # pylint: disable=too-many-return-statements,too-many-branches
    """
    Evaluate a single syntax element
    """
    if isinstance(syntax, shy_parser.Operation):
        operation: str = syntax.operation
        if operation in ASSIGNMENT_OPERATIONS:
            value = interpret_syntax(syntax.right, variables)
            if not isinstance(syntax.left, lexer.Identifier):
                raise SyntaxError(
                    f"Can't assign to {syntax.left}; must be an identifier"
                )
            if operation == "=":
                variables[syntax.left.name] = value
            elif operation == "+=":
                variables[syntax.left.name] += value  # type: ignore
            elif operation == "-=":
                variables[syntax.left.name] -= value  # type: ignore
            elif operation == "*=":
                variables[syntax.left.name] *= value  # type: ignore
            elif operation == "/=":
                variables[syntax.left.name] /= value  # type: ignore
            elif operation == "%=":
                variables[syntax.left.name] %= value  # type: ignore
            return None

        left = interpret_syntax(syntax.left, variables)
        right = interpret_syntax(syntax.right, variables)
        if operation == "==":
            return left == right
        if operation == "<":
            return left < right  # type: ignore
        if operation == ">":
            return left > right  # type: ignore
        if operation == "<=":
            return left <= right  # type: ignore
        if operation == ">=":
            return left >= right  # type: ignore
        if operation == "!=":
            return left != right
        if operation == "+":
            return left + right  # type: ignore
        if operation == "-":
            return left - right  # type: ignore
        if operation == "*":
            return left * right  # type: ignore
        if operation == "/":
            return left / right  # type: ignore
        if operation == "%":
            return left % right  # type: ignore
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
        return function(argument)  # type: ignore
    if isinstance(syntax, lexer.Identifier):
        return variables[syntax.name]
    if isinstance(syntax, int):
        return syntax
    raise SyntaxError(f"Invalid Syntax: {syntax}")
