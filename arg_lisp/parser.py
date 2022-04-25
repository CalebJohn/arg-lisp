from collections import deque
from .lexer import Token, TokenType, SourcePoint, tokenize
from .trie import Trie
from typing import Union

AST = dict[Token, Union['AST', Token]]


class ParsingError(SyntaxError):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(message)


def parse_tokens(
    tokens: deque[Token], fun_trie: Trie, symbol_table: set = None
) -> Union[AST, Token]:
    if symbol_table is None:
        symbol_table = set()

    tkn = tokens.popleft()

    if tkn.type == TokenType.num or tkn.value in symbol_table:
        return tkn

    # Ignore surrounding {
    if tkn.type == TokenType.lis:
        tkn = tokens.popleft()

    # Error condition checking
    if tkn.type not in [TokenType.ide, TokenType.num]:
        raise ParsingError(tkn, "Parse got bad input")

    if tkn.value not in fun_trie:
        raise ParsingError(tkn, "Unknown function")

    col_token = tokens.popleft()
    if col_token.type is not TokenType.col:
        print(col_token.start)
        raise ParsingError(col_token,
            f"Function name ({tkn.value}) must be followed by a colon, then argument"
        )

    # Special forms
    # These are special cases where it's useful to parse them differently
    # These are only needed for the braceless ({/}) syntax
    if tkn.value == "let":
        arg = tokens.popleft()
        arguments = {tkn: arg}
        symbol_table.add(arg.value)
    elif tkn.value == "fn":
        names, args = parse_fn_arguments(tokens)
        # TODO: ensure names, is not a subset of any other function
        # also, no function is  asubset of names
        fun_trie.add_func(names)
        for a in args:
            symbol_table.add(a)
        # TODO: use a proper data storage class
        loc = SourcePoint(line=-1, column=-1)
        hack_token = Token(value=str(args), start=loc, end=loc)
        arguments = {tkn: hack_token}
    else:
        arguments = {tkn: parse_tokens(tokens, fun_trie, symbol_table)}

    # Map out the arguments to the current function
    current_index = fun_trie[tkn.value]
    while options := current_index:
        arg = tokens.popleft()
        if arg.value not in options:
            raise ParsingError(arg, f"Expected argument to be in {options}, this could be an ambiguous function call, try wrapping it in {}")

        if tokens.popleft().type is not TokenType.col:
            raise ParsingError(arg,
                f"Arg name must be followed by a colon, then argument in {tkn.value}"
            )
        value = parse_tokens(tokens, fun_trie, symbol_table)

        arguments[arg] = value
        current_index = current_index[arg.value]

    # Ignore trailing }
    if len(tokens) > 0 and tokens[0].type == TokenType.lis:
        tokens.popleft()

    return arguments


# Simple function to parse {things:like th:is}
def parse_fn_arguments(tokens: deque[Token]) -> tuple[list, list]:
    lis_token = tokens.popleft()
    if lis_token.type is not TokenType.lis:
        raise ParsingError(lis_token, "fn takes a mapping of names to variables")

    names = []
    arguments = []
    while (nxt := tokens.popleft()).type != TokenType.lis:
        arg_name = nxt.value
        if tokens.popleft().type is not TokenType.col:
            raise ParsingError(nxt,
                "Arg name must be followed by a colon, then argument"
            )
        arg_value = tokens.popleft().value

        # The parser only cares about the external argument name (for now)
        names.append(arg_name)
        arguments.append(arg_value)

    return names, arguments

def parse(program: str, fun_trie: Trie) -> Union[AST, Token]:
    tokens = tokenize(program)

    try:
        ast = parse_tokens(tokens, fun_trie)
    except ParsingError as pe:
        # Intercept the error and make it a bit nicer
        prgm = program.split("\n")
        token = pe.token
        error_line = prgm[token.start.line]
        pointer = "^".rjust(token.start.column + 1)
        message = pe.message.rjust(len(pe.message) // 2 + token.start.column)
        m = f"\n{error_line}\n{pointer}\n{message}"
        raise ParsingError(token, m)

    return ast

