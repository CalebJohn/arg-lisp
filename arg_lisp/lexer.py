from collections import namedtuple
from typing import List

Source = namedtuple('Source', 'line column')
# Token = namedtuple('Token', 'value source', defaults = [Source(0,0)])

class Token:
    def __init__(self, value: str, source: Source = Source(0, 0)):
        self.value = value
        self.source = source
    def __repr__(self):
        return str(self.value)

# def eat_whitespace(src: List[str], ch:int, ln:int) -> Tuple[int, int]:
#     while src[ln][ch].isspace():
#         if ch == len(src[ln]) - 1:
#             ch = 0
#             ln += 1
#         elif ch < len(src[ln]):
#             ch += 1

#     return ch, ln

# def eat_until_whitespace(src: List[str], ch:int, ln:int) -> Tuple[Token, int, int]:
#     characters = []
#     start = Source(ch, ln)
#     while not src[ln][ch].isspace():
#         characters.append(src[ln][ch])
#         if ch == len(src[ln]) - 1:
#             ch = 0
#             ln += 1
#         elif ch < len(src[ln]):
#             ch += 1

#     return Token(''.join(characters), start), ch, ln


# def lexer(source: str) -> List[str]:
#     char = 0
#     line = 0
#     src = source.split('\n')
#     tokens = []
#     while line <= len(src) and char < len(src[line]):
#         char, line = eat_whitespace(src, char, line)
#         token, char, line = eat_until_whitespace(src, char, line)
#         tokens.append(token)

#     if line < len(src):
#         print("ERROR IN THE LEXER, reached end of line before the end of document")

#     print(char, line)

# lexer('   hello\n\tvalue:world')

# For now the parser is whats important so we're going to move ahead with the simplest tokenizer
# TODO: Add debug symbols to tokens
def tokenize(source: str) -> List[str]:
    # Courtesy of: http://norvig.com/lispy.html
    tokens = source.replace('{', ' { ').replace('}', ' } ').replace(';', '; ').replace(': {', ':{').split()
    # return [Token(t) for t in tokens]
    return tokens

        

