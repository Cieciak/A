from typing import List
from tokens import *

def tokenize(text: str) -> List[Token]:

    # Clean lines and prepare for tokenization
    clear_lines = [x.strip() for x in text.splitlines() if x]
    raw_tokens = []
    for line in clear_lines:
        for token in line.split(' '):
            if token.endswith(':') and not token == '::':
                raw_tokens.extend([token[:-1], ':'])
            else:
                raw_tokens.append(token)

    # Pretokenize
    print(raw_tokens)
    tokens = [] 
    for token in raw_tokens:
        if token == 'field':
            tokens.append(FieldToken())
        elif token == 'pointer':
            tokens.append(PointerToken)
        elif token == '@':
            tokens.append(AtToken())
        elif token == ':':
            tokens.append(EnterScopeToken())
        elif token == '::':
            tokens.append(ExitScopeToken())
        elif token == 'value':
            tokens.append(ValueToken())
        elif token == 'position':
            tokens.append(PositionToken())
        elif token == 'write':
            tokens.append(WriteToken())
        elif token == 'add':
            tokens.append(AddToken())
        elif token == 'read':
            tokens.append(ReadToken())
        elif token == 'eoc':
            tokens.append(EndOfCodeToken())
        elif token == 'noscope':
            tokens.append(NoScopeToken())
        elif token == 'entry':
            tokens.append(EntryToken())
        elif token == 'label':
            tokens.append(LabelToken())
        elif token == 'global':
            tokens.append(GlobalToken())
        elif token == 'if':
            tokens.append(IfToken())
        elif token == 'jump':
            tokens.append(JumpToken())
        elif token == 'greater':
            tokens.append(GreaterToken())
        elif token == 'smaller':
            tokens.append(SmallerToken())
        elif token == 'equal':
            tokens.append(EqualToken())
        elif token == 'true':
            tokens.append(TrueToken())
        elif token == 'false':
            tokens.append(FalseToken())

        elif token.isdigit(): tokens.append(IntToken(data=int(token)))
        else: tokens.append(NameToken(data=token))

    final_tokens = []
    while tokens:
        match tokens:
            case [FieldToken(), *_]:
                print('Found field declaration!')

        tokens.pop(0)

    return final_tokens

if __name__ == '__main__':
    with open('test.a', 'r') as file:
        text = file.read()

    tokens = tokenize(text)
    for i in tokens:
        print(i)
