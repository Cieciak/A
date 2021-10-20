# A Programming Language

A assembly-like interpreted language.

## Basics

A uses only two data types:
>Fields

>Pointers

### Field:
    Used for storing data, it can't be resized.
    
### Pointer:
    User for moving and operationg on data.
    Can be used on many scopes.

### Keywords:

`field` - Defines field

`pointer` - Defines pointer

`value` - Set value of pointer

`position` - Set the position of pointer

`write` - Write at pointer position

`read` - Read at pointer position

`add` - Add pointer value to pointer position

`eoc` - End of code

### Definitions and syntax:

Field:
```
    field <name> [shape]
```

Pointer:
```
    pointer <name>
```

Label:
```
    label <name>
```

Entry:
```
    entry <name>
```

Jump:
```
    jump <label>
```

If:
```
    jump if <pointer name> true|false <label>

    jump if <pointer name> greater|equal|smaller <pointer name> <label>
```

Scope:
```
    <pointer> @ <field> :
        ...
        ...
    ::
```

## Code samples:

```
field main 10 10
field second 1
pointer dummy

entry begin

dummy @ main:

    global label begin
    dummy position 0 0
    dummy value 1

    write
    add
    read
::

dummy @ second:

    dummy position 0
    write
::
eoc
```