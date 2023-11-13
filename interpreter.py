import lexer
import shy_parser


def interpret(source):
    variables = {"print": print}
    inner_interpret(source, variables)


def inner_interpret(lines, variables):
    index = 0
    while index < len(lines):
        syntax = lines[index]
        interpret_syntax(syntax, variables)
        index += 1


def interpret_syntax(syntax, variables):
    if isinstance(syntax, shy_parser.Operation):
        operation = syntax.operation
        if operation == "=" or len(operation) == 2:
            value = interpret_syntax(syntax.right, variables)
            if not isinstance(syntax.left, lexer.Identifier):
                raise SyntaxError(
                    f"Can't assign to {syntax.left}; must be an identifier"
                )
            if operation == "=":
                variables[syntax.left.name] = value
            elif operation == "+=":
                variables[syntax.left.name] += value
        else:
            left = interpret_syntax(syntax.left, variables)
            right = interpret_syntax(syntax.right, variables)
            if operation == "<":
                return left < right
    elif isinstance(syntax, shy_parser.Block):
        if syntax.block_type == "while":
            while interpret_syntax(syntax.condition, variables):
                inner_interpret(syntax.body, variables)
        else:
            raise SyntaxError(f"Invalid Block Type: {syntax.block_type}")
    elif isinstance(syntax, shy_parser.FunctionCall):
        function = interpret_syntax(syntax.function, variables)
        argument = interpret_syntax(syntax.argument, variables)
        return function(argument)
    elif isinstance(syntax, lexer.Identifier):
        return variables[syntax.name]
    elif isinstance(syntax, int):
        return syntax
    else:
        raise SyntaxError(f"Invalid Syntax: {syntax}")
