from arg_lisp.parser import base_fun_table, parse, tokenize, make_trie
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
    assert to_string(tokenize("add:4 and:6")) == "add : 4 and : 6"

def test_tokenize_long():
    tokens = tokenize(fib)

    assert len(tokens) == 42

def test_parser():
    parsed = parse(tokenize("add:4 and:6"), base_fun_table())

    assert repr(parsed) == "{add: 4, and: 6}"

def test_parser_reverse():
    parsed = parse(tokenize("and:4 add:6"), base_fun_table())

    # the purpose of this test is actually to ensure it parsed
    assert repr(parsed) == "{and: 4, add: 6}"

def test_parser_long():
    tokens = tokenize(fib)
    parsed = parse(tokens, base_fun_table())

    assert repr(parsed) == "{fn: ['n'], on: {if: {is: n, lessthan: 2}, then: n, else: {add: {fib: {subtract: 1, from: n}}, and: {fib: {subtract: 2, from: n}}}}}"

def test_parser_non_unique_func():
    parsed = parse(tokenize("is:4 lessthan:6"), base_fun_table())
    assert repr(parsed) == "{is: 4, lessthan: 6}"
    parsed = parse(tokenize("is:4 greaterthan:6"), base_fun_table())
    assert repr(parsed) == "{is: 4, greaterthan: 6}"

def test_parser_no_func():
    # TODO: This should be a specific exception
    with pytest.raises(Exception):
        parsed = parse(tokenize("is:4 notacondition:6"), base_fun_table())


def test_simple_parser():
    simple_fib = """
    {fn:{fib:n} on:{if: {is:n lessthan:2} then:n else:{add:{fib:{subtract:1 from:n}} and:{fib:{subtract:2 from:n}}}}}
    """

    simple_parsed = parse(tokenize(simple_fib), base_fun_table())
    tokens = tokenize(fib)
    parsed = parse(tokens, base_fun_table())

    assert repr(simple_parsed) == repr(parsed)

def test_trie_simple():
    trie = make_trie([[1, 2, 3]])

    assert trie == {1: {2: {3: {}}, 3: {2: {}}}, 2: {1: {3: {}}, 3: {1: {}}}, 3: {1: {2: {}}, 2: {1: {}}}}

def test_trie_2_rows():
    trie = make_trie([[1, 2, 3], [3, 4, 5]])

    assert trie == {1: {2: {3: {}}, 3: {2: {}}}, 2: {1: {3: {}}, 3: {1: {}}}, 3: {1: {2: {}}, 2: {1: {}}, 4: {5: {}}, 5: {4: {}}}, 4: {3: {5: {}}, 5: {3: {}}}, 5: {3: {4: {}}, 4: {3: {}}}}
