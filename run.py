import sys, time
import numpy as np
from A import *

try:
    if sys.argv[2] == 'show':
        show = True
    else:
        show = False
except:
    show = False

def make_args_int(token, labels):
    data = token.data
    if token.data:
        try:
            data = [int(x) for x in token.data]
        except:
            data = [labels[token.data[0]]]
    return Token(token.type, data)

code_file = sys.argv[1]
code = open(code_file, 'r').read()
lexer = Lexer(code)

tokens, error, *labels = lexer.tokenize()

if error: print(error)
if not error:
    running = True
    index = 0
    pointer = None
    value = None
    saved = None
    while running:
        operator = make_args_int(tokens[index], labels[0])
        if operator.type == T_DEF:
            memory = np.zeros(operator.data)
        elif operator.type == T_POS:
            pointer = np.array(operator.data)
        elif operator.type == T_PSV:
            value = operator.data[0]
        elif operator.type == T_POW:
            memory[tuple(pointer)] = value
        elif operator.type == T_POR:
            value = memory[tuple(pointer)]
        elif operator.type == T_NOP:
            pass
        elif operator.type == T_INP:
            value = ord(input()[0])
        elif operator.type == T_PRT:
            print(chr(int(value)), end='')
        elif operator.type == T_ADD:
            memory[tuple(pointer)] += value
        elif operator.type == T_SUB:
            memory[tuple(pointer)] -= value
        elif operator.type == T_MUL:
            memory[tuple(pointer)] *= value
        elif operator.type == T_DIV:
            memory[tuple(pointer)] /= value
        elif operator.type == T_JUM:
            index = operator.data[0] - 1
        elif operator.type == T_IFZ:
            if value == 0:
                index = operator.data[0] - 1
        elif operator.type == T_IFS:
            if value < memory(tuple(pointer)):
                index = operator.data[0] - 1 
        elif operator.type == T_IFE:
            if value == memory(tuple(pointer)):
                index = operator.data[0] - 1 
        elif operator.type == T_IFG:
            if value > memory(tuple(pointer)):
                index = operator.data[0] - 1
        elif operator.type == T_SAV:
            saved = index
        elif operator.type == T_JSV:
            index = saved - 1
        elif operator.type == T_CAL:
            saved = index + 1
            index = operator.data[0] - 1

        index += 1
        if index == len(tokens):
            running = False

if not error and show:
    print()
    print(memory)
    print(tokens)
    print(pointer)
    print(value)
    print(labels)
    
print()