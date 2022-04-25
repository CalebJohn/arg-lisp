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

    # the purpose of this test is actually to ensure it parsed
    assert repr(parsed) == "{and: 4, add: 6}"

def test_parser_long():
    parsed = parse(fib, base_fun_table())

    assert repr(parsed) == "{fn: ['n'], on: {if: {is: n, lessthan: 2}, then: n, else: {add: {fib: {subtract: 1, from: n}}, and: {fib: {subtract: 2, from: n}}}}}"

def test_parser_non_unique_func():
    parsed = parse("is:4 lessthan:6", base_fun_table())
    assert repr(parsed) == "{is: 4, lessthan: 6}"
    parsed = parse("is:4 greaterthan:6", base_fun_table())
    assert repr(parsed) == "{is: 4, greaterthan: 6}"

def test_parser_no_func():
    # TODO: This should be a specific exception
    with pytest.raises(ParsingError):
        parsed = parse("is:4 notacondition:6", base_fun_table())

def test_simple_parser():
    simple_fib = """
    {fn:{fib:n} on:{if: {is:n lessthan:2} then:n else:{add:{fib:{subtract:1 from:n}} and:{fib:{subtract:2 from:n}}}}}
    """

    simple_parsed = parse(simple_fib, base_fun_table())
    parsed = parse(fib, base_fun_table())

    assert repr(simple_parsed) == repr(parsed)

