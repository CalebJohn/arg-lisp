from arg_lisp.lexer import tokenize, SourcePoint, TokenType, Token
import pytest

fib = """
fn:{fib:n} on:
    if: is:n lessthan:2 then:
        n
    else:
        add:fib:subtract:1 from:n and:fib:subtract:2 from:n
"""

def to_string(tokens):
    return ' '.join(t.value for t in tokens)

def test_tokenize():
    tokens = tokenize("add:4 and:6")
    assert to_string(tokens) == "add : 4 and : 6"
    assert tokens[3].start.column == 6
    assert tokens[3].end.column == 8
    assert tokens[4].start.column == 9
    assert tokens[4].end.column == 9
    assert tokens[-1].start.column == 10

def test_tokenize_long():
    tokens = tokenize(fib)

    assert len(tokens) == 42
    assert tokens[-1].start.column == 58
    assert tokens[-1].start.line == 5
    assert tokens[-1].end.column == 58

def test_token_types():
    loc = SourcePoint(line=0, column=0)
    assert Token(value=':', start=loc, end=loc).type == TokenType.col
    assert Token(value='}', start=loc, end=loc).type == TokenType.lis
    assert Token(value='{', start=loc, end=loc).type == TokenType.lis
    assert Token(value='#t', start=loc, end=loc).type == TokenType.bol
    assert Token(value='"hello world"', start=loc, end=loc).type == TokenType.str
    assert Token(value='123.45', start=loc, end=loc).type == TokenType.num
    assert Token(value='call', start=loc, end=loc).type == TokenType.ide

def test_mixed_parens():
    tokens = tokenize("if:{is:4} then:7")

    assert tokens[1].start.column == 2
    assert to_string(tokens) == "if : { is : 4 } then : 7"
