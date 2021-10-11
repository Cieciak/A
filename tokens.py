from enum import Enum

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

    def __init__(self, typ = TokenType, data = None) -> None:
        self.type = typ
        self.data = data

    def __repr__(self) -> str:
        out = f'{self.type}'
        if self.data: out += f': {self.data}'
        return out

class EndOfCodeToken(Token):

    def __init__(self, typ = TokenType.eoc, data=None) -> None:
        super().__init__(typ, data=data)

class EnterScopeToken(Token):

    def __init__(self, typ=TokenType.sce, data=None) -> None:
        super().__init__(typ=typ, data=data)

class ExitScopeToken(Token):

    def __init__(self, typ=TokenType.scx, data=None) -> None:
        super().__init__(typ=typ, data=data)

class AtToken(Token):

    def __init__(self, typ=TokenType.at, data=None) -> None:
        super().__init__(typ=typ, data=data)

class ValueToken(Token):

    def __init__(self, typ=TokenType.value, data=None) -> None:
        super().__init__(typ=typ, data=data)

class PositionToken(Token):

    def __init__(self, typ=TokenType.position, data=None) -> None:
        super().__init__(typ=typ, data=data)

class WriteToken(Token):

    def __init__(self, typ=TokenType.write, data=None) -> None:
        super().__init__(typ=typ, data=data)

class AddToken(Token):

    def __init__(self, typ=TokenType.add, data=None) -> None:
        super().__init__(typ=typ, data=data)

class ReadToken(Token):

    def __init__(self, typ=TokenType.read, data=None) -> None:
        super().__init__(typ=typ, data=data)

class NoScopeToken(Token):

    def __init__(self, typ=TokenType.noscope, data=None) -> None:
        super().__init__(typ=typ, data=data)

class EntryToken(Token):

    def __init__(self, typ=TokenType.entry, data=None) -> None:
        super().__init__(typ=typ, data=data)

class LabelToken(Token):

    def __init__(self, typ=TokenType.label, data=None) -> None:
        super().__init__(typ=typ, data=data)

class GlobalToken(Token):

    def __init__(self, typ=TokenType.globa, data=None) -> None:
        super().__init__(typ=typ, data=data)

class JumpToken(Token):

    def __init__(self, typ=TokenType.jump, data=None) -> None:
        super().__init__(typ=typ, data=data)

class IfToken(Token):

    def __init__(self, typ=TokenType.iF, data=None) -> None:
        super().__init__(typ=typ, data=data)

class GreaterToken(Token):

    def __init__(self, typ=TokenType.greater, data=None) -> None:
        super().__init__(typ=typ, data=data)

class EqualToken(Token):

    def __init__(self, typ=TokenType.equal, data=None) -> None:
        super().__init__(typ=typ, data=data)
    
class SmallerToken(Token):

    def __init__(self, typ=TokenType.smaller, data=None) -> None:
        super().__init__(typ=typ, data=data)


class PointerToken(Token):

    def __init__(self, typ=TokenType.pointer, data=None) -> None:
        super().__init__(typ=typ, data=data)

class FieldToken(Token):

    def __init__(self, typ=TokenType.field, data=None) -> None:
        super().__init__(typ=typ, data=data)


class IntToken(Token):

    def __init__(self, typ=TokenType.int, data=None) -> None:
        super().__init__(typ=typ, data=data)

class NameToken(Token):

    def __init__(self, typ=TokenType.name, data=None) -> None:
        super().__init__(typ=typ, data=data)

class FloatToken(Token):

    def __init__(self, typ=TokenType.float, data=None) -> None:
        super().__init__(typ=typ, data=data)


class TrueToken(Token):
    
    def __init__(self, typ=TokenType.true, data=None) -> None:
        super().__init__(typ=typ, data=data)

class FalseToken(Token):
    
    def __init__(self, typ=TokenType.false, data=None) -> None:
        super().__init__(typ=typ, data=data)