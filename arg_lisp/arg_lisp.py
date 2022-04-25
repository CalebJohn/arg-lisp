from collections import deque
from dataclasses import dataclass
from itertools import permutations
from enum import Enum
import re


class TokenType(str, Enum):
    ide = "identifier"
    col = "colon"
    lis = "list"
    num = "number"
    str = "string"
    bol = "boolean"
    err = "error"


@dataclass(frozen=True)
class Token:
    value: str
    type: TokenType

    def __repr__(self):
        return self.value


class SymbolType(str, Enum):
    fun = "function"
    sym = "symbol"


@dataclass
class Symbol:
    value: str
    type: SymbolType


def base_fun_table():
    return make_trie([
        {"let", "be"},
        {"multiply", "by"},
        {"add", "and"},
        {"subtract", "from"},
        {"divide", "by"},
        {"fn", "on"},
        {"is", "lessthan"},
        {"is", "greaterthan"},
        {"if", "then", "else"},
        ])

Trie = dict[str, 'Trie']

def make_trie(functions: list[set[str]]) -> Trie:
    trie = {}
    for func in functions:
        add_func(func, trie)

    return trie

def add_func(func: str, trie: Trie):
    for f in permutations(func):
        index = trie
        for g in f:
            index = index.setdefault(g, {})

def parse(
    tokens: deque[Token], fun_trie: Trie, symbol_table: set = None
) -> dict | Token:
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
        raise Exception(f"Parse got bad input {tkn}")

    if tkn.value not in fun_trie:
        raise Exception(f"Unknown function {tkn.value}")

    if tokens.popleft().type is not TokenType.col:
        raise Exception(
            f"Function name must be followed by a colon, then argument in {tkn.value}"
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
        add_func(names, fun_trie)
        for a in args:
            symbol_table.add(a)
        # TODO: use a proper data storage class
        hack_token = Token(value=str(args), type=TokenType.lis)
        arguments = {tkn: hack_token}
    else:
        arguments = {tkn: parse(tokens, fun_trie, symbol_table)}

    # Map out the arguments to the current function
    current_index = fun_trie[tkn.value]
    while options := current_index:
        arg = tokens.popleft()
        if arg.value not in options:
            raise Exception(f"Expected argument to be in {options}: got {arg.value}")

        if tokens.popleft().type is not TokenType.col:
            raise Exception(
                f"Arg name must be followed by a colon, then argument in {tkn.value} {arg}"
            )
        value = parse(tokens, fun_trie, symbol_table)

        arguments[arg] = value
        current_index = current_index[arg.value]

    # Ignore trailing }
    if len(tokens) > 0 and tokens[0].type == TokenType.lis:
        tokens.popleft()

    return arguments


# Simple function to parse {things:like th:is}
def parse_fn_arguments(tokens: deque[Token]) -> tuple[list, list]:
    if tokens.popleft().type is not TokenType.lis:
        raise Exception("fn takes a mapping of names to variables")

    names = []
    arguments = []
    while (nxt := tokens.popleft()).type != TokenType.lis:
        arg_name = nxt.value
        if tokens.popleft().type is not TokenType.col:
            raise Exception(
                f"Arg name must be followed by a colon, then argument for {arg_name}"
            )
        arg_value = tokens.popleft().value

        # The parser only cares about the external argument name (for now)
        names.append(arg_name)
        arguments.append(arg_value)

    return names, arguments


def eat_token(inp: str) -> tuple[Token, str]:
    inp = inp.strip()
    if inp[0] == ":":
        return Token(value=":", type=TokenType.col), inp[1:]
    if inp[0] == "{" or inp[0] == "}":
        return Token(value=inp[0], type=TokenType.lis), inp[1:]
    # if inp[0] == '"':
    #     # TODO: string parsing
    #     pass
    # if inp[0] == "#":
    #     # TODO: Booleans
    #     pass

    broken = re.split(r"[:\s{;}]", inp)

    if inp[0].isdigit():
        return Token(value=broken[0], type=TokenType.num), inp[len(broken[0]) :]
    if inp[0].isalnum():
        return Token(value=broken[0], type=TokenType.ide), inp[len(broken[0]) :]

    return Token(value=f"Unknown token: {inp[0]}", type=TokenType.err), ""


def tokenize(inp: str) -> deque[Token]:
    tokens = deque()
    while inp:
        token, inp = eat_token(inp)
        tokens.append(token)

    return tokens
