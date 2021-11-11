# A Programming Language

A assembly-like interpreted language.

## Basics

A uses only two data types:
>Fields

>Pointers

### Field:
    Used for storing data, it can't be resized. But it can be of any size and order.
    
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

`in` - Get data from a user

`out` - Return data to a user

### Directives:

`insert` - Insert A code from other file

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

In:
```
    in <type>
```

Out:
```
    out <object> <type>
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

Inserting `A` file:
```
    insert "<filename.a>"
```

## Code samples:

```
field main 10 10        - Define field main with size of 10x10 
field second 1          - Define field second with size of 1
pointer dummy           - Define pointer dummy

entry begin             - Jump to entry point

dummy @ main:           - Scope entry

    global label begin  - Global label
    dummy position 0 0  - Set dummy position to cell (0,0)
    dummy value 1       - Set dummy value to 1

    write
    add
    read
::                      - Exit dummy @ main scope

dummy @ second:

    dummy position 0
    write
::
eoc                     - Finish code
```
* And no, that's not how comments work in `A`.
  In fact it doesn't have comments. 