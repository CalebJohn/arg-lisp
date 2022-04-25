from arg_lisp.trie import Trie


def test_trie_simple():
    trie = Trie([[1, 2, 3]])

    assert trie == {1: {2: {3: {}}, 3: {2: {}}}, 2: {1: {3: {}}, 3: {1: {}}}, 3: {1: {2: {}}, 2: {1: {}}}}

def test_trie_2_rows():
    trie = Trie([[1, 2, 3], [3, 4, 5]])

    assert trie == {1: {2: {3: {}}, 3: {2: {}}}, 2: {1: {3: {}}, 3: {1: {}}}, 3: {1: {2: {}}, 2: {1: {}}, 4: {5: {}}, 5: {4: {}}}, 4: {3: {5: {}}, 5: {3: {}}}, 5: {3: {4: {}}, 4: {3: {}}}}