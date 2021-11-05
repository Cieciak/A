from typing import List
from tokens import *

def parse_file(path: str) -> List[str]:
    '''Parse lines from a file'''
    clear_lines: List[str] = []
    with open(path, 'r') as file:
        lines = file.read().splitlines()
        for line in lines:
            if line.startswith('insert '):
                clear_lines.extend(parse_file(line[8:-1]))
            elif line:
                clear_lines.append(line.strip())
    return clear_lines

def separate_tokens(lines: List[str]) -> List[str]:
    '''Get separate tokens'''
    out: List[str] = []
    for line in lines:
        for token in line.split(' '):
            if token.endswith(':') and not token == '::':
                out.extend([token[:-1], ':'])
            else:
                out.append(token)
    return out

def tokenize(path: str, loud: int = 0) -> List[Token]:

    # Clean lines and prepare for tokenization
    response = parse_file(path)
    raw_tokens = separate_tokens(response)

    if loud & 0b1: [print(token) for token in raw_tokens]

    # Pretokenize
    tokens: List[Token] = []
    for token in raw_tokens:
        try:
            tokens.append(DICT[token]())
        except KeyError:
            if token.isdigit(): tokens.append(IntToken(data=int(token)))
            else: tokens.append(NameToken(data=token))

    if loud & 0b10: [print(token) for token in tokens]

    # Final tokens
    CURRENT_SCOPE = None
    CURRENT_POINT = None
    SCOPE_INDEX = 0
    SCOPE_ID = 0
    final_tokens = []
    global_labels = {}
    while tokens:
        match tokens:
            case [FieldToken(), NameToken(), *_]:

                data = {
                    'name': tokens[1].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:2]
                shape = []
                while isinstance(tokens[0], IntToken):
                    shape.append(tokens[0].data)
                    del tokens[0]
                data['shape'] = tuple(shape)
                final_tokens.append(FieldToken(data=data))

            case [PointerToken(), NameToken(), *_]:
                data = {
                    'name': tokens[1].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:2]
                final_tokens.append(PointerToken(data=data))

            case [EntryToken(), NameToken(), *_]:
                data = {
                    'name': tokens[1].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:2]
                final_tokens.append(EntryToken(data=data))

            case [NameToken(), AtToken(), NameToken(), EnterScopeToken(), *_]:
                CURRENT_POINT = tokens[0].data
                CURRENT_SCOPE = tokens[2].data
                SCOPE_ID += 1
                data = {
                    'name': SCOPE_ID,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:4]
                final_tokens.append(EnterScopeToken(data=data))
                #SCOPE_INDEX = -1

            case [NameToken(), ValueToken(), IntToken(), *_]:
                data = {
                    'value': tokens[2].data,
                    'pointer': tokens[0].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT
                    }
                }
                del tokens[:3]
                final_tokens.append(ValueToken(data=data))

            case [NameToken(), PositionToken(), *_]:
                data = {
                    'pointer': tokens[0].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:2]
                shape = []
                while isinstance(tokens[0], IntToken):
                    shape.append(tokens[0].data)
                    del tokens[0]
                data['shape'] = tuple(shape)
                final_tokens.append(PositionToken(data=data))

            case [WriteToken(), *_]:
                data = {
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                final_tokens.append(WriteToken(data=data))
                del tokens[0]

            case [AddToken(), *_]:
                data = {
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                final_tokens.append(AddToken(data=data))
                del tokens[0]

            case [ReadToken(), *_]:
                data = {
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                final_tokens.append(ReadToken(data=data))
                del tokens[0]

            case [ExitScopeToken(), *_]:
                CURRENT_SCOPE = None
                CURRENT_POINT = None
                data = {
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                final_tokens.append(ExitScopeToken(data=data))
                del tokens[0]

            case [NoScopeToken(), EnterScopeToken(), *_]:
                CURRENT_SCOPE = None
                CURRENT_POINT = None
                SCOPE_ID += 1
                data = {
                    'name': SCOPE_ID,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                final_tokens.append(NoScopeToken(data=data))
                del tokens[:2]

            case [GlobalToken(), LabelToken(), NameToken(), *_]:
                data = {
                    'global': True,
                    'name': tokens[2].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                global_labels[data['name']] = data
                del tokens[:3]
                final_tokens.append(LabelToken(data=data))

            case [LabelToken(), NameToken(), *_]:
                data = {
                    'global': False,
                    'name': tokens[1].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:2]
                global_labels[data['name']] = data
                final_tokens.append(LabelToken(data=data))

            case [JumpToken(), NameToken(), *_]:
                data = {
                    'name': tokens[1].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:2]
                final_tokens.append(JumpToken(data=data))

            case [JumpToken(), IfToken(), NameToken(), FalseToken() | TrueToken(), NameToken(), *_]:
                data = {
                    'name': tokens[2].data,
                    'operation': 'check',
                    'label': tokens[4].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:5]
                final_tokens.append(IfToken(data=data))

            case [JumpToken(), IfToken(), NameToken(), GreaterToken() | EqualToken() | SmallerToken(), NameToken(), NameToken(), *_]:
                data = {
                    'name': tokens[2].data,
                    'operation': tokens[3].type,
                    'operand1': tokens[2].data,
                    'operand2': tokens[4].data,
                    'label': tokens[5].data,
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[:6]
                final_tokens.append(IfToken(data=data))

            case [EndOfCodeToken()]:
                data = {
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[0]
                final_tokens.append(EndOfCodeToken(data=data))

            case [OutputToken(), *_]:
                data = {
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[0]
                final_tokens.append(OutputToken(data=data))

            case [InputToken(), *_]:
                data = {
                    'scope': {
                        'index': SCOPE_INDEX,
                        'name': CURRENT_SCOPE,
                        'pointer': CURRENT_POINT,
                    }
                }
                del tokens[0]
                final_tokens.append(InputToken(data=data))

            case _:
                print('Unmathched token', tokens[0])

                del tokens[0]

        SCOPE_INDEX += 1

    if loud & 0b100: [print(token) for token in final_tokens]

    return final_tokens, global_labels

if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]

    response = tokenize(file_name, loud=7)
    print(response[1])