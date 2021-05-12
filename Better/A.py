from os import error
from numpy import zeros

####################
##
## TOKENS
##
####################

T_DEF = 'DEFINE'

class Error:
    
    def __init__(self, type_, details = None):
        self.type = type_
        self.details = details
    
    def __repr__(self):
        result = f'{self.type} Error'
        if self.details: result += f': {self.details}'
        return result

class Token:

    def __init__(self, _type, data=None):
        self.type = _type
        self.data = data

    def __repr__(self):
        out = self.type
        if self.data: out += f':{self.data}'
        return out

class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos_in_code = -1
        self.current_instruction = None
        self.prepare_code()
        self.advance()

    def prepare_code(self):
        to_analyze = self.text.replace('|', '\n').split('\n')
        analyzed = []
        for line in to_analyze:
            analyzed.append(line.strip())
        self.code = analyzed

    def advance(self):
        self.pos_in_code += 1
        self.current_instruction = self.code[self.pos_in_code] if self.pos_in_code < len(self.code) else None

    def tokenize(self):
        tokens = []
        while self.current_instruction:
            operator, *args = self.current_instruction.split(' ')
            if operator == 'def':
                if args == []:
                    error = Error('Missing Args', 'DEFINE operator should have at least one argument')
                else:
                    tokens.append(Token(T_DEF, args))
            self.advance()
        return tokens, error

lexer = Lexer(' def | pos 10 |  por| pow')
tokens, error = lexer.tokenize()

if error: print(error)
if not error: print(tokens)