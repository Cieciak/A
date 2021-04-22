import sys, os

a = '''
# Imports
from numpy import zeros

# Tokens

T_DEF = 'DEFINE'
T_PSE = 'POINTER_SET'
T_PRD = 'POINTER_READ'
T_PWR = 'POINTER_WRITE'
T_SME = 'SHOW_MEMORY'
T_PSW = 'POINTER_SET_VALUE'

T_ADD = 'ADD'
T_SUB = 'SUB'
T_MUL = 'MUL'
T_DIV = 'DIV'

T_JUM = 'JUMP'
T_JIZ = 'JUMP_IF_ZERO'
T_JIS = 'JUMP_IF_SMALLER'
T_JUS = 'JUMP_TO_SAVED'

T_PRI = 'PRINT'
T_PRC = 'PRINT_CHAR'

T_INP = 'INPUT'
T_INC = 'INPUT_CHAR'

T_NUL = 'NULL'
T_SAV = 'SAVE'


# System func
def create_grid(size):
    return zeros(size, dtype='float64')

# Fixed
def pick_arguments(string):
    data = string.split(' ')[1:] if string.split(' ')[1:] else None
    if data: return [arg for arg in data if arg != '']

def list_check(list_one, list_two):
    for x, y in zip(list_one, list_two):
        if x > y - 1: return 1
    return 0

# Token
class Token:

    def __init__(self, type_, data = None):
        self.type = type_
        self.data = data
    
    def __repr__(self):
        return f'{self.type}:{self.data}' if self.data else f'{self.type}'

# Pointer

class Pointer:

    def __init__(self):
        self.pos = None
        self.val = None
        self.save = None

# Error
class Error:
    
    def __init__(self, type_, place = None, details = None):
        self.type = type_
        self.details = details
        self.place = place
    
    def __repr__(self):
        result = f'{self.type} Error'
        if self.details: result += f': {self.details}'
        if self.place != None: result += f'\\n    At line {self.place}'
        return result

class IllegalCharacterError(Error):
    
    def __init__(self, character):
        super().__init__('Illegal Character',details = f'Illegal character \\'{character}\\' found')

class SyntaxError(Error):

    def __init__(self, place = None, details = None):
        super().__init__('Syntax', place = place, details = details)

class BadAgrsError(Error):

    def __init__(self, place = None, details = None):
        super().__init__('Bad Argument', place = place, details = details)

class UserInputError(Error):

    def __init__(self, place = None, details = None):
        super().__init__('User Input', place = place, details = details)

class MathError(Error):

    def __init__(self, place = None, details = None):
        super().__init__('Math', place = place, details = details)


# Lexer
class Lexer:

    def __init__(self, code):
        self.code = code.replace('|', '\\n').split('\\n')
        self.pos_in_code = -1
        self.current_instr = None
        self.infunc = False
        self.advance()
    
    def advance(self):
        self.pos_in_code += 1
        self.current_instr = self.code[self.pos_in_code] if self.pos_in_code < len(self.code) else None

    def analyze_code(self):
        self.tokens = []
        while self.current_instr != None:
            if self.current_instr.startswith('def'):
                self.tokens.append(Token(T_DEF, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('pos'):
                self.tokens.append(Token(T_PSE, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('pow'):
                self.tokens.append(Token(T_PWR, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('por'):
                self.tokens.append(Token(T_PRD, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('mem'):
                self.tokens.append(Token(T_SME, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('psv'):
                self.tokens.append(Token(T_PSW, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('add'):
                self.tokens.append(Token(T_ADD, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('sub'):
                self.tokens.append(Token(T_SUB, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('mul'):
                self.tokens.append(Token(T_MUL, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('div'):
                self.tokens.append(Token(T_DIV, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('jum'):
                self.tokens.append(Token(T_JUM, pick_arguments(self.current_instr)))
                self.advance()
            
            elif self.current_instr.startswith('ifz'):
                self.tokens.append(Token(T_JIZ, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('prt'):
                self.tokens.append(Token(T_PRI, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('prc'):
                self.tokens.append(Token(T_PRC, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('ifs'):
                self.tokens.append(Token(T_JIS, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('nul'):
                self.tokens.append(Token(T_NUL, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('inp'):
                self.tokens.append(Token(T_INP, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('inc'):
                self.tokens.append(Token(T_INC, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('jus'):
                self.tokens.append(Token(T_JUS, pick_arguments(self.current_instr)))
                self.advance()

            elif self.current_instr.startswith('sav'):
                self.tokens.append(Token(T_SAV, pick_arguments(self.current_instr)))
                self.advance()     

            else:
                self.error = IllegalCharacterError(self.current_instr)
                return [], self.error
        
        return self.tokens, None

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos_in_token = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos_in_token += 1
        self.current_token = self.tokens[self.pos_in_token] if self.pos_in_token < len(self.tokens) else None

    def run(self):
        self.pointer = Pointer()
        response = []

        while self.current_token != None:
            token = self.current_token

            #   System
            # Define field
            if token.type == T_DEF:
                if not token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} got no arguments')
                try: size = [int(x) for x in token.data]
                except ValueError: return [], BadAgrsError(self.pos_in_token, f'Bad argument for {token.type} found')
                self.memory = create_grid(size)
                self.advance()

            # Show Memory
            elif token.type == T_SME:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                response.append(self.memory.copy())
                self.advance()

            # Print
            elif token.type == T_PRI:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                response.append(self.pointer.val)
                self.advance()

            # Print character
            elif token.type == T_PRC:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                response.append(chr(self.pointer.val))
                self.advance()

            # Input number to pointer
            elif token.type == T_INP:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                try: self.pointer.val = int(input('Input:'))
                except ValueError: return [], UserInputError(self.pos_in_token, f'Bad value inserted by user')
                self.advance()

            # Input character to pointer
            elif token.type == T_INC:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                self.pointer.val = ord(input('Input:')[0])
                self.advance()

            # Save pos
            elif token.type == T_SAV:
                self.pointer.save = self.pos_in_token
                self.advance()

            # No op
            elif token.type == T_NUL:
                self.advance()

            #   Pointer
            # Set position
            elif token.type == T_PSE:
                if len(token.data) != len(self.memory.shape): return [], SyntaxError(self.pos_in_token, f'Mismatch in dimensions')
                try: 
                    if list_check([int(x) for x in token.data], self.memory.shape): return [], Error('Index', self.pos_in_token, 'Index is too big')
                    self.pointer.pos = tuple([int(x) for x in token.data])
                except ValueError: return [], BadAgrsError(self.pos_in_token, f'Bad argument for {token.type} found')
                self.advance()

            # Set pointer value
            elif token.type == T_PSW:
                if len(token.data) > 1: return [], SyntaxError(self.pos_in_token, 'Cannot insert two valuses to one cell')
                try: self.pointer.val = int(token.data[0])
                except ValueError: return [], BadAgrsError(self.pos_in_token, f'Bad argument for {token.type} found')
                self.advance()

            # Pointer write value to memory
            elif token.type == T_PWR:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                self.memory[self.pointer.pos] = self.pointer.val
                self.advance()

            # Pointer read value from memory
            elif token.type == T_PRD:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                self.pointer.val = self.memory[self.pointer.pos] 
                self.advance()

            #   Math
            # Add value of the pointer to cell in memory
            elif token.type == T_ADD:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                self.memory[self.pointer.pos] += self.pointer.val
                self.advance()

            # Subtract value of the pointer from cell in memory
            elif token.type == T_SUB:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                self.memory[self.pointer.pos] -= self.pointer.val
                self.advance()

            # Multiply value in memory by pointer 
            elif token.type == T_MUL:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                self.memory[self.pointer.pos] *= self.pointer.val
                self.advance()

            # Divide value in memory by pointer
            elif token.type == T_DIV:
                if token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                if not self.pointer.val: return [], MathError(self.pos_in_token, 'Division by 0')
                self.memory[self.pointer.pos] = self.memory[self.pointer.pos] / self.pointer.val
                self.advance()

            #   Conditionals
            # Jump to line in code
            elif token.type == T_JUM:
                if not token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                try: self.pos_in_token = int(token.data[0]) - 1
                except ValueError: return [], BadAgrsError(self.pos_in_token, f'{token.type} got bad argument')
                self.advance()

            # Jump if pointer value is 0
            elif token.type == T_JIZ:
                if not token.data: return [], SyntaxError(self.pos_in_token, f'{token.type} has no arguments')
                if not self.pointer.val: 
                    try: self.pos_in_token = int(token.data[0]) - 1
                    except ValueError: return [], BadAgrsError(self.pos_in_token, f'{token.type} got bad argument')
                self.advance()

            # Jump if pointer is smaller
            elif token.type == T_JIS:
                if not token.data: return [], SyntaxError(f'{token.type} has no arguments')
                if self.pointer.val < self.memory[self.pointer.pos]: 
                    try: self.pos_in_token = int(token.data[0]) - 1
                    except ValueError: return [], BadAgrsError(self.pos_in_token, f'{token.type} got bad argument')
                self.advance()

            # Jump to saved pos + 1
            elif token.type == T_JUS:
                self.pos_in_token = self.pointer.save + 1
                self.advance()


        return response, None
'''


# Check for file
try:
    file_name = sys.argv[1]
    file = open(file_name)
except:
    input('No file found.')
    sys.exit()

real_file_name = file_name.split('.')[0]
cut_file_name = real_file_name.split('\\')[-1]
folder = (real_file_name + '\\').replace('\\\\', '\\')


code = file.read().replace('\n', '|')

imports = '\n'

code_str = 'data = ' + f'\'{code}\''

main = a + '''
lexer = Lexer(data)
tokens, error = lexer.analyze_code()

if error: print(error)
else:
    parser = Parser(tokens)
    out, error = parser.run()

    if error: print(error)
    else:
        for i in out:
            print(i, '\\n')
input()'''

try:
    os.mkdir(folder)
except:
    pass

# Copy A grammar

file = open(f'{folder + cut_file_name}.py', 'w')
file.write(imports)
file.write('\n')
file.write(code_str)
file.write('\n')
file.write(main)
file.close()

os.system(f'pyinstaller --onefile --distpath={folder} --workpath={folder}\\work --specpath={folder}\\work {folder + cut_file_name}.py')
os.remove(f'{folder + cut_file_name}.py')