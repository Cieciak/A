from os import error
import sys, A

code_file = sys.argv[1]
code = open(code_file, 'r').read()
lexer = A.Lexer(code)

tokens, error = lexer.tokenize()

if error: print(error)
if not error:
    