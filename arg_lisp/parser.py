from pprint import pprint

if __name__ == "__main__":
    from lexer import tokenize
else:
    from .lexer import tokenize

def parse(program):
    return parse_tokens(tokenize(program))

def parse_tokens(tokens):
    if len(tokens) == 0:
        raise SyntaxError("Unexpected EOF")
    print(tokens)

    token = tokens.pop(0)
    if token == "{":
        l = []
        while tokens[0] != "}":
            l.append(parse_tokens(tokens))
        tokens.pop(0) # remove the }
        return l
    if token == "}":
        # TODO: Incorporate line and char
        raise SyntaxError("Unexpected {")
    if ":" in token: # parse arguments
        name, arg = token.split(":")
        if arg.startswith("{"):
            tokens.insert(0, arg)
            arg = parse_tokens(tokens)
        return {"name":name, "arg":arg}

    return atom(token)

def atom(token):
    return token

def func(token):
    pass

# print(parse('{do body:other_func once:1 told:print me:"something"}'))
pprint(parse('''
{repeat times:10 on:{
	print value:'Hello';
        print value:'World'
}}
'''))
