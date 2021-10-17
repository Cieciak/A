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
    tokens = []
    for token in raw_tokens:
        if token == 'field':
            tokens.append(FieldToken())
        elif token == 'pointer':
            tokens.append(PointerToken())
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

    # Final tokens
    final_tokens = []
    while tokens:
        match tokens:
            case [FieldToken(), NameToken(), *_]:
                data = {'name': tokens[1].data}
                del tokens[:2]
                shape = []
                while isinstance(tokens[0], IntToken):
                    shape.append(tokens[0].data)
                    del tokens[0]
                data['shape'] = tuple(shape)
                final_tokens.append(FieldToken(data=data))

            case [PointerToken(), NameToken(), *_]:
                data = {'name': tokens[1].data}
                del tokens[:2]
                final_tokens.append(PointerToken(data=data))

            case [EntryToken(), NameToken(), *_]:
                data = {'name': tokens[1].data}
                del tokens[:2]
                final_tokens.append(EntryToken(data=data))

            case [NameToken(), AtToken(), NameToken(), EnterScopeToken(), *_]:
                data = {'pointer_name': tokens[0].data, 'field_name': tokens[2].data}
                del tokens[:4]
                final_tokens.append(EnterScopeToken(data=data))

            case [NameToken(), ValueToken(), IntToken(), *_]:
                data = {'ponter': tokens[0].data, 'value': tokens[2].data}
                del tokens[:3]
                final_tokens.append(ValueToken(data=data))

            case [NameToken(), PositionToken(), *_]:
                data = {'pointer': tokens[0].data}
                del tokens[:2]
                shape = []
                while isinstance(tokens[0], IntToken):
                    shape.append(tokens[0].data)
                    del tokens[0]
                data['shape'] = tuple(shape)
                final_tokens.append(PositionToken(data=data))

            case [WriteToken(), *_]:
                final_tokens.append(WriteToken())
                del tokens[0]

            case [AddToken(), *_]:
                final_tokens.append(AddToken())
                del tokens[0]

            case [ReadToken(), *_]:
                final_tokens.append(ReadToken())
                del tokens[0]

            case [ExitScopeToken(), *_]:
                final_tokens.append(ExitScopeToken())
                del tokens[0]

            case [NoScopeToken(), EnterScopeToken(), *_]:
                final_tokens.append(NoScopeToken())
                del tokens[:2]

            case [GlobalToken(), LabelToken(), NameToken(), *_]:
                data = {'global': True, 'name': tokens[2].data}
                del tokens[:3]
                final_tokens.append(LabelToken(data=data))

            case [LabelToken(), NameToken(), *_]:
                data = {'global': False, 'name': tokens[1].data}
                del tokens[:2]
                final_tokens.append(LabelToken(data=data))

            case [JumpToken(), NameToken(), *_]:
                data = {'name': tokens[1].data}
                del tokens[:2]
                final_tokens.append(JumpToken(data=data))

            case [JumpToken(), IfToken(), NameToken(), FalseToken() | TrueToken(), NameToken(), *_]:
                data = {'name': tokens[4].data, 'operation': 'check'}
                del tokens[:5]
                final_tokens.append(IfToken(data=data))

            case [JumpToken(), IfToken(), NameToken(), GreaterToken() | EqualToken() | SmallerToken(), NameToken(), NameToken(), *_]:
                data = {'name': tokens[5].data, 'operation': tokens[3].type, 'operand1': tokens[2].data, 'operand2': tokens[4].data}
                del tokens[:6]
                final_tokens.append(IfToken(data=data))

            case [EndOfCodeToken()]:
                del tokens[0]
                final_tokens.append(EndOfCodeToken())

            case _:
                print('Unmathched token', tokens[0])

                del tokens[0]

    return final_tokens

if __name__ == '__main__':
    with open('te.a', 'r') as file:
        text = file.read()

    tokens = tokenize(text)
    for i in tokens:
        print(i)
