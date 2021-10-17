from typing import List
import A
from tokens import *

class Field:

    def __init__(self, shape, name) -> None:
        self.size = 1
        self.name = name
        for i in shape:
            self.size *= i

        self.content = [0] * self.size

    def __getitem__(self, index):
        return self.content[(index)]

    def __repr__(self) -> str:
        return f'{self.content}'

class Pointer:

    def __init__(self, name) -> None:
        self.position = None
        self.value = None
        self.name = name

    def set_position(self, place):
        self.position = place

    def set_value(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

class Scope:

    def __init__(self, name: str, tokens) -> None:
        self.name = name
        self.code = tokens
        self.labels: List = []

    def __repr__(self) -> str:
        header = str(self.name) + ':\n'
        labels = '    labels:\n        ' + '\n        '.join([str(x) for x in self.labels])
        code = '\n    tokens:\n        ' + '\n        '.join([str(x) for x in self.code])

        return header + labels + code

    def add_label(self, label):
        self.labels.append(label)

with open(input('File: '), 'r') as file:
    text = file.read()
    file.close()

tokens = A.tokenize(text)

CURRENT_SCOPE = None
CURRENT_POINTER = None
SCOPES: List[Scope] = []

GLOBAL_LABELS = []

code_tokens: List[Token] = []
while tokens:
    token = tokens.pop(0)

    data = token.data
    if data == None:
        data = {}

    data['scope'] = CURRENT_SCOPE
    data['pointer'] = CURRENT_POINTER
    token.data = data

    if isinstance(token, EnterScopeToken):
        CURRENT_POINTER = token.data['pointer_name']
        CURRENT_SCOPE = token.data['field_name']
    elif isinstance(token, ExitScopeToken):
        CURRENT_SCOPE = CURRENT_POINTER = None

    code_tokens.append(token)

scope = None
point = None

scope_list = []

for token in code_tokens:

    if scope == token.data['scope']:
        scope_list.append(token)
    else:
        SCOPES.append(Scope(scope, scope_list))
        scope_list = []

    scope = token.data['scope']

for token in code_tokens:

    if isinstance(token, LabelToken):
        pass

SCOPES[0].labels.append('a')

for i in SCOPES:
    print(i)