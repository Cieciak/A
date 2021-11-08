from typing import Any, Dict, List
import A, sys
from tokens import *

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

FIELDS: Dict[str, Field] = {}
POINTERS: Dict[str, Pointer] = {}

running = True
index = 0
while running:
    token = tokens[index]
    match token:
        case FieldToken():
            FIELDS[token.data['name']] = Field(size=token.data['shape'])
        case PointerToken():
            POINTERS[token.data['name']] = Pointer()
        case EntryToken():
            index = glabels[token.data['name']]['scope']['index']

        case PositionToken():
            POINTERS[token.data['pointer']].set_pos(token.data['shape'])

        case ValueToken():
            POINTERS[token.data['pointer']].set_val(token.data['value'])

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
            try:
                field = FIELDS[token.data['object']]
                if token.data['type'] == str:
                    print(''.join([chr(x) for x in field.data()]))
                elif token.data['type'] ==  int:
                    print(' '.join([str(x) for x in field.data()]))
            except KeyError:
                pointer = POINTERS[token.data['object']]
                if token.data['type'] == str:
                    print(chr(pointer.value))
                elif token.data['type'] == int:
                    print(pointer.value)



        case InputToken():
            p = POINTERS[token.data['scope']['pointer']]
            FIELDS[token.data['scope']['name']].transmit(input(), p.position)


    index += 1

#print(FIELDS)