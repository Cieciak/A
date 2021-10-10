from enum import Enum
from typing import List

class TokenType(Enum):
    # Keywords
    eoc = 'END OF CODE'
    sce = 'SCOPE ENTRY'
    scx = 'SCOPE EXIT'
    at = '@'
    value = 'VALUE'
    position = 'POSITION'
    write = 'WRITE'
    add = 'ADD'
    read = 'READ'
    noscope = 'NO FIELD'
    entry = 'ENTRY'
    label = 'LABEL'
    globa = 'GLOBAL'
    jump = 'JUMP'
    iF = 'IF'
    greater = 'GREATER'
    smaller = 'SMALLER'
    equal = 'EQUAL'

    # Data structures
    field = 'FIELD'
    pointer = 'POINTER'
    
    # Data types
    int = 'INTEGER'
    float = 'FLOAT'
    name = 'NAME'

    # Data values
    true = 'True'
    false = 'False'

class Token:

    def __init__(self, type, data = None) -> None:
        self.type = type
        self.data = data

    def __repr__(self) -> str:
        out = f'{self.type}'
        if self.data: out += f': {self.data}'
        return out

def tokenize(text: str) -> List[Token]:
    clear_lines = [x.strip() for x in text.splitlines() if x]
    raw_tokens = []
    for line in clear_lines:
        for token in line.split(' '):
            if token.endswith(':') and not token == '::':
                raw_tokens.extend([token[:-1], ':'])
            else:
                raw_tokens.append(token)

    print(raw_tokens)
    tokens = [] 
    for token in raw_tokens:
        if token == 'field':
            tokens.append(Token(TokenType.field))
        elif token == 'pointer':
            tokens.append(Token(TokenType.pointer))
        elif token == '@':
            tokens.append(Token(TokenType.at))
        elif token == ':':
            tokens.append(Token(TokenType.sce))
        elif token == '::':
            tokens.append(Token(TokenType.scx))
        elif token == 'value':
            tokens.append(Token(TokenType.value))
        elif token == 'position':
            tokens.append(Token(TokenType.position))
        elif token == 'write':
            tokens.append(Token(TokenType.write))
        elif token == 'add':
            tokens.append(Token(TokenType.add))
        elif token == 'read':
            tokens.append(Token(TokenType.read))
        elif token == 'eoc':
            tokens.append(Token(TokenType.eoc))
        elif token == 'noscope':
            tokens.append(Token(TokenType.noscope))
        elif token == 'entry':
            tokens.append(Token(TokenType.entry))
        elif token == 'label':
            tokens.append(Token(TokenType.label))
        elif token == 'global':
            tokens.append(Token(TokenType.globa))
        elif token == 'if':
            tokens.append(Token(TokenType.iF))
        elif token == 'jump':
            tokens.append(Token(TokenType.jump))
        elif token == 'greater':
            tokens.append(Token(TokenType.greater))
        elif token == 'smaller':
            tokens.append(Token(TokenType.smaller))
        elif token == 'equal':
            tokens.append(Token(TokenType.equal))
        elif token == 'true':
            tokens.append(Token(TokenType.true))
        elif token == 'false':
            tokens.append(Token(TokenType.false))

    return tokens

if __name__ == '__main__':
    with open('test.a', 'r') as file:
        text = file.read()

    tokens = tokenize(text)
    for i in tokens:
        print(i)
