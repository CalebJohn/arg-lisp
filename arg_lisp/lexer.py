from collections import deque
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class SourcePoint:
    line: int
    column: int

class TokenType(str, Enum):
    col = "colon"
    lis = "list"
    bol = "boolean"
    str = "string"
    num = "number"
    ide = "identifier"
    err = "error"

@dataclass(frozen=True)
class Token:
    value: str
    start: SourcePoint
    end: SourcePoint

    def __repr__(self):
        return self.value

    @property
    def type(self) -> TokenType:
        if self.value == ':':
            return TokenType.col
        elif self.value == '{' or self.value == '}':
            return TokenType.lis
        elif self.value[0] == '#':
            return TokenType.bol
        elif self.value[0] == '"':
            return TokenType.str
        elif self.value[0].isdigit():
            return TokenType.num
        else:
            return TokenType.ide


def tokenize(program: str) -> deque[Token]:
    tokens = deque()
    i = -1
    in_string = False
    line, col = 0, -1
    current_token = Token(value="", start=SourcePoint(0, 0), end=SourcePoint(0, 0))
    while i < len(program) -1:
        i += 1
        col += 1
        char = program[i]
        loc = SourcePoint(line=line, column=col)
        if in_string:
            current_token = Token(value=current_token.value+char, start=current_token.start, end=loc)
            if char == '"':
                in_string = False
        else:
            if char.isspace():
                if current_token.value:
                    loc = SourcePoint(line=line, column=col+1)
                    tokens.append(current_token)
                    current_token = Token(value="", start=loc, end=loc)
                # Sorry windows users :(
                if char == '\n':
                    col = -1
                    line += 1
                continue
            elif char == '"':
                in_string = True
            elif char == ':' or char == "{" or char == "}":
                if current_token.value:
                    tokens.append(current_token)
                    next_loc = SourcePoint(line=line, column=col+1)
                    current_token = Token(value="", start=next_loc, end=next_loc)
                tokens.append(Token(value=char, start=loc, end=loc))
            else:
                current_token = Token(value=current_token.value+char, start=current_token.start, end=loc)

    if current_token.value:
        tokens.append(current_token)

    return tokens


