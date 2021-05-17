import sys
import numpy as np
from A import *

def make_args_int(token):
    data = token.data
    if token.data:
        data = [int(x) for x in token.data]
    return Token(token.type, data)

code_file = sys.argv[1]
code = open(code_file, 'r').read()
lexer = Lexer(code)

tokens, error = lexer.tokenize()

if error: print(error)
if not error:
    running = True
    index = 0
    pointer = None
    value = None
    while running:
        operator = make_args_int(tokens[index])
        if operator.type == T_DEF:
            memory = np.zeros(operator.data)
        elif operator.type == T_POS:
            pointer = operator.data
        elif operator.type == T_PSV:
            value = operator.data[0]
        elif operator.type == T_POW:
            memory[pointer] = value
        elif operator.type == T_POR:
            value = memory[pointer]
        elif operator.type == T_INP:
            value = ord(input()[0])
        elif operator.type == T_PRT:
            print(chr(int(value[0])), end='')
        elif operator.type == T_ADD:
            memory[pointer] += value
        elif operator.type == T_SUB:
            memory[pointer] -= value
        elif operator.type == T_MUL:
            memory[pointer] *= value
        elif operator.type == T_DIV:
            memory[pointer] /= value
        elif operator.type == T_JUM:
            index = operator.data[0] - 1
        elif operator.type == T_IFZ:
            if not value:
                index = operator.data[0] - 1
        elif operator.type == T_IFS:
            if value < memory[pointer]:
                index = operator.data[0] - 1
        elif operator.type == T_IFE:
            if value == memory[pointer]:
                index = operator.data[0] - 1
        elif operator.type == T_IFG:
            if value > memory[pointer]:
                index = operator.data[0] - 1

        index += 1
        if index == len(tokens):
            running = False

if not error: 
    print(memory)
    print(tokens)