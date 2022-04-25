from itertools import permutations
from collections.abc import Iterable
from typing import Any


class Trie(dict):
    def __init__(self, func_table: Iterable[Iterable[Any]] = []):
        for func in func_table:
            self.add_func(func)

    def add_func(self, func: Iterable[str]):
        for f in permutations(func):
            index = self
            for g in f:
                index = index.setdefault(g, Trie())

