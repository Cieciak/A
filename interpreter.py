from typing import Any, Dict, List, Tuple
import A, sys
from tokens import *

def construct_index(tuple: Tuple[int], shape: Tuple[int]) -> int:
    '''Returns tuple casted onto shape of field'''
    shape = (1, ) + shape
    index = 0
    for value, size in zip(tuple, shape):
        index += value * size
    return index


class Field:

    def __init__(self, size) -> None:
        self.size = size
        self.__content = [0]
        for i in size:
            self.__content = self.__content * i

    def setitem(self, index, value):
        o = 1
        for i in tuple(index):
            o *= i
        self.__content[o] = value

    def getitem(self, index):
        o = 1
        for i in tuple(index):
            o *= i
        return self.__content[o]

    def __repr__(self) -> str:
        out = [str(x) for x in self.__content]
        return ' '.join(out)

    def transmit(self, data: str | List[int | float], begin):
        start = 1
        for i in begin:
            start *= i
        length = len(data)
        for i in range(length):
            self.__content[start + i] = data[i]

    def data(self) -> List[int | float]:
        return self.__content

class Pointer:

    def __init__(self) -> None:
       self.position = None
       self.value = None

    def __repr__(self) -> str:
        return f'{self.position}, {self.value}'

    def set_val(self, value):
        self.value = value

    def set_pos(self, position):
        self.position = position 

file_name = sys.argv[1]
tokens, glabels = A.tokenize(file_name)

FIELDS: Dict[str, Field] = {}     # Dictionary of fields
POINTERS: Dict[str, Pointer] = {} # Dictionary of pointers

running = True
index = 0 # Line index
while running:
    token = tokens[index]
    match token:

        case FieldToken():
            # Field declaration
            FIELDS[token.data['name']] = Field(size=token.data['shape'])

        case PointerToken():
            # Pointer declaration
            POINTERS[token.data['name']] = Pointer()

        case EntryToken():
            # Jump to entry
            index = glabels[token.data['name']]['scope']['index']

        case PositionToken():
            if token.data['pointer'] == token.data['scope']['pointer']:
                POINTERS[token.data['pointer']].set_pos(token.data['shape'])
            else:
                print('Wrong pointer')

        case ValueToken():
            if token.data['pointer'] == token.data['scope']['pointer']:
                POINTERS[token.data['pointer']].set_val(token.data['value'])
            else:
                print('Wrong pointer')

        case AddToken():
            f = FIELDS[token.data['scope']['name']]
            p = POINTERS[token.data['scope']['pointer']]
            f.setitem(p.position, p.value + f.getitem(p.position))

        case ReadToken():
            f = FIELDS[token.data['scope']['name']]
            p = POINTERS[token.data['scope']['pointer']]
            p.value = f.getitem(p.position)

        case WriteToken():
            f = FIELDS[token.data['scope']['name']]
            p = POINTERS[token.data['scope']['pointer']]
            f.setitem(p.position, p.value)

        case JumpToken():
            f = FIELDS[token.data['scope']['name']]
            p = POINTERS[token.data['scope']['pointer']]
            l = glabels[token.data['name']]
            if l['global']: index = l['scope']['index']
            elif l['scope']['name'] == token.data['scope']['name']:
                index = l['scope']['index']

        case IfToken():
            p = POINTERS[token.data['scope']['pointer']]
            l = glabels[token.data['label']]
            match token.data['operation']:
                case 'check':
                    if p.value: index = l['scope']['index']
                    
                case TokenType.greater:
                    one = POINTERS[token.data['operand1']]
                    two = POINTERS[token.data['operand2']]

                    if one.value > two.value: index = l['scope']['index']

                case TokenType.equal:
                    one = POINTERS[token.data['operand1']]
                    two = POINTERS[token.data['operand2']]

                    if one.value == two.value: index = l['scope']['index']

                case TokenType.smaller:
                    one = POINTERS[token.data['operand1']]
                    two = POINTERS[token.data['operand2']]

                    if one.value < two.value: index = l['scope']['index']
   
        case EndOfCodeToken():
            running = False

        case OutputToken():
            if token.data['object'] == token.data['scope']['name']:
                # Print field
                to_cast = FIELDS[token.data['object']].data()
                if token.data['type'] == str:
                    # Output as a string
                    print(''.join([chr(n) for n in to_cast]), end='')

                elif token.data['type'] == int:
                    # Output as a list of numbers
                    print(' '.join([str(n) for n in to_cast]), end='')

            elif token.data['object'] == token.data['scope']['pointer']:
                # Print pointer
                to_cast = POINTERS[token.data['object']].value
                if token.data['type'] == str:
                    # Output as a string
                    print(chr(to_cast), end='')
                elif token.data['type'] == int:
                    # Output as a number
                    print(str(to_cast), end='')

            else:
                print('You are in different scopes')

        case InputToken():
            # Take input from a user and transmit it on a scope field
            pointer = POINTERS[token.data['scope']['pointer']]
            field = FIELDS[token.data['scope']['name']]

            if token.data['type'] == str:
                # Ask for input as string
                to_cast = [ord(char) for char in input()]

            elif token.data['type'] == int:
                # Ask for input as integer
                to_cast = [int(input())]

            else:
                print('How?')
            
            field.transmit(to_cast, pointer.position)

    index += 1
