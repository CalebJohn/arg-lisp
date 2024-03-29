from arg_lisp.functions import base_fun_table
from arg_lisp.parser import parse, ParsingError
import pytest

fib = """
fn:{fib:n} on:
    if: is:n lessthan:2 then:
        n
    else:
        add:fib:subtract:1 from:n and:fib:subtract:2 from:n
"""


def test_parser():
    parsed = parse("add:4 and:6", base_fun_table())

    assert repr(parsed) == "{add: 4, and: 6}"

def test_parser_reverse():
    parsed = parse("and:4 add:6", base_fun_table())

    assert repr(parsed) == "{and: 4, add: 6}"

def test_parser_long():
    parsed = parse(fib, base_fun_table())

    assert repr(parsed) == "{fn: ['n'], on: {if: {is: n, lessthan: 2}, then: n, else: {add: {fib: {subtract: 1, from: n}}, and: {fib: {subtract: 2, from: n}}}}}"

def test_parser_non_unique_func():
    parsed = parse("is:4 lessthan:6", base_fun_table())
    assert repr(parsed) == "{is: 4, lessthan: 6}"
    parsed = parse("is:4 greaterthan:6", base_fun_table())
    assert repr(parsed) == "{is: 4, greaterthan: 6}"

def test_parser_ambiguous_func():
    fun_table = base_fun_table()
    fun_table.add_func({"is"})
    with pytest.raises(ParsingError):
        parsed = parse("if:is:4 then:7 else:5", fun_table)

    parsed = parse("if:{is:4} then:7 else:5", fun_table)
    assert repr(parsed) == "{if: {is: 4}, then: 7, else: 5}"

def test_parser_unknown_arg():
    with pytest.raises(ParsingError):
        parsed = parse("is:4 notacondition:6", base_fun_table())

def test_parser_missing_arg():
    with pytest.raises(ParsingError):
        parsed = parse("if:3 then:4", base_fun_table())

def test_simple_parser():
    simple_fib = """
    {fn:{fib:n} on:{if: {is:n lessthan:2} then:n else:{add:{fib:{subtract:1 from:n}} and:{fib:{subtract:2 from:n}}}}}
    """

    simple_parsed = parse(simple_fib, base_fun_table())
    parsed = parse(fib, base_fun_table())

    assert repr(simple_parsed) == repr(parsed)

