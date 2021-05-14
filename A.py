from numpy import zeros

####################
##
## TOKENS
##
####################

# System
T_DEF = 'DEFINE'
T_NOP = 'NO OPERATION'

# Pointer ops
T_POS = 'POINTER SET POSITION'
T_PSV = 'POINTER SET VALUE'
T_POW = 'POINTER WRITE CELL'
T_POS = 'POINTER READ CELL'

# User IO
T_INP = 'USER INPUT'
T_PRT = 'PRINT'

# Math
T_ADD = 'ADD'
T_SUB = 'SUBTRACT'
T_MUL = 'MULTIPLY'
T_DIV = 'DIVIDE'

# Jumps
T_JUM = 'JUMP'
T_IFZ = 'JUMP IF ZERO'
T_IFS = 'JUMP IF SMALLER'
T_IFE = 'JUMP IF EQUAL'
T_IFG = 'JUMP IF GREATER'

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
        error = None
        while self.current_instruction:
            operator, *args = self.current_instruction.split(' ')
            if operator == 'def':
                if args == []:
                    error = Error('Missing Args', '\"DEFINE\" operator should have at least one argument')
                else:
                    tokens.append(Token(T_DEF, args))
            elif operator == 'psp':
                if args == []:
                    error = Error('Missing Args', '\"SET POINTER POSITION\" operator should have at least one argument')
                else:
                    tokens.append(Token(T_POS, args))
            elif operator == 'psv':
                if len(args) != 1:
                    error = Error('Argument Amount', '\"POINTER SET VALUE\" opertator should have one argument')
                else:
                    tokens.append(Token(T_PSV, args))
            elif operator == 'pow':
                if args:
                    error = Error('Excess Arument Error', '\"POINTER WRITE CELL\" operator should have no aguments')
                else:
                    tokens.append(Token(T_POW))
            elif operator == 'por':
                if args:
                    error = Error('Excess Arument Error', '\"POINTER READ CELL\" operator should have no aguments')
                else:
                    tokens.append(Token(T_POS))
            elif operator == 'nul':
                tokens.append(Token(T_NOP))
            elif operator == 'inp':
                if args:
                    error = Error('Excess Arument Error', '\"INPUT\" operator should have no aguments')
                else:
                    tokens.append(Token(T_INP))
            elif operator == 'ptr':
                if args:
                    error = Error('Excess Arument Error', '\"PRINT\" operator should have no aguments')
                else:
                    tokens.append(Token(T_PRT))
            elif operator == 'add':
                if args:
                    error = Error('Excess Arument Error', '\"ADD\" operator should have no aguments')
                else:
                    tokens.append(Token(T_ADD))
            elif operator == 'sub':
                if args:
                    error = Error('Excess Arument Error', '\"SUBTRACT\" operator should have no aguments')
                else:
                    tokens.append(Token(T_SUB))
            elif operator == 'mul':
                if args:
                    error = Error('Excess Arument Error', '\"MULTIPLY\" operator should have no aguments')
                else:
                    tokens.append(Token(T_MUL))
            elif operator == 'div':
                if args:
                    error = Error('Excess Arument Error', '\"DIVIDE\" operator should have no aguments')
                else:
                    tokens.append(Token(T_DIV))
            elif operator == 'jmp':
                if args == []:
                    error = Error('Missing Args', '\"JUMP\" operator should have at least one argument')
                else:
                    tokens.append(Token(T_JUM, args))
            elif operator == 'ifz':
                if args == []:
                    error = Error('Missing Args', '\"IF ZERO\" operator should have at least one argument')
                else:
                    tokens.append(Token(T_IFZ, args))
            elif operator == 'ifs':
                if args == []:
                    error = Error('Missing Args', '\"IF SMALLER\" operator should have at least one argument')
                else:
                    tokens.append(Token(T_IFS, args))
            elif operator == 'ife':
                if args == []:
                    error = Error('Missing Args', '\"IF EQUAL\" operator should have at least one argument')
                else:
                    tokens.append(Token(T_IFE, args))
            elif operator == 'ifg':
                if args == []:
                    error = Error('Missing Args', '\"IF GREATER\" operator should have at least one argument')
                else:
                    tokens.append(Token(T_IFG, args))
            self.advance()
        return tokens, error

