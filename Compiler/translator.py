import A, sys

# Get two init paths
exec_file_path = sys.argv[0]
try:
    input_file_path = sys.argv[1]
except IndexError:
    print('No file input file detected')
    sys.exit()

# Options
silent = False
inside = False

if len(sys.argv) > 2:
    rest = sys.argv[2:]
    if '-s' in rest:
        rest.remove('-s')
        silent = True
    if '-i' in rest:
        rest.remove('-i')
        inside = True
    
    if rest:
        print(f'Unknown parameter {rest}')

def get_folder_of_file(path):
    '''Returns path to a folder containig inputed file'''
    to_analyze = path.split('\\')
    out = ''
    for i in to_analyze[:-1]:
        out += i + '\\'
    return out

def calc_position(token, shape):
    vec = token.data
    val = 0
    for i in range(len(shape)):
        if not i: val = vec[0]
        else: val += shape[i - 1] * vec[i]
    return val

def split_list(data, length):
    out = []
    t = []
    for i in data:
        if len(t) == length:
            out.append(t)
            t = []
        t.append(i)
    out.append(t)
    return out

# Get dir of both files
exec_file_dir = get_folder_of_file(exec_file_path)
input_file_dir = get_folder_of_file(input_file_path)

# Grammar path
grammar = exec_file_dir + 'Grammar.ad'

# Output path
asm_file_path = input_file_path.split('.')[0] + '.asm'

# Load other important files
try:
    with open(input_file_path, 'r') as file:
        code_string = file.read()
except FileNotFoundError:
    print(f'Could not open file with path \'{input_file_path}\'')
    sys.exit()

try:
    with open(grammar, 'r') as file:
        base_code = file.read()
except:
    print(f'Could not find grammar file')
    sys.exit()

# Init print
if not silent:
    print('')
    print('Init values:')
    print(f'Compiler path: {exec_file_path}')
    print(f'Grammar path: {grammar}')
    print(f'Input file path: {input_file_path}')
    print(f'Ouput file path: {asm_file_path}')

# Procces file
lexer = A.Lexer(code_string)
tokens, error = lexer.analyze_code()

# Quit if error
if error:
    print(error)
    sys.exit()

# Show tokens
if not silent:
    print()
    print(f'Tokens found: {tokens}')

# Token normalization
memory_shape = []
memory_size = 1
for token in tokens:
    # Delete comments
    if token.type == A.T_NUL:
        token.data = None

    # Define proc
    elif token.type == A.T_DEF:
        for size in token.data:
            memory_shape.append(int(size))
            memory_size *= int(size)

    if token.data:
        final_data = []
        for element in token.data:
            final_data.append(int(element))
        token.data = tuple(final_data)
memory_shape = tuple(memory_shape)

if not silent and inside:
    print()
    print(f'Corrected tokens: {tokens}')
    print(f'Shape of program memory: {memory_shape}')
    print(f'Size of memory program: {memory_size}')

# Creating translation table
translation_table = {}
j = 0
i = -2
for token in tokens:
    translation_table[j] = i
    if token.data:
        i += 1
    i += 1
    j += 1

if not silent and inside:
    print()
    print(f'Translation table: {translation_table}')

# Further token analysys
for token in tokens:

    # Pointer set position
    if token.type == A.T_PSE:
        token.data = calc_position(token, memory_shape)
    
    # Jumps
    elif token.type in [A.T_JIS, A.T_JIZ, A.T_JUM, A.T_JUS]:
        token.data = translation_table[token.data[0]]
    
    elif token.data:
        token.data = token.data[0]

if not silent and inside:
    print()
    print(f'Tokens: {tokens[1:]}')

# Translate
for token in tokens:
    if token.type == A.T_NUL:
        token.type = '00h'
    elif token.type == A.T_PSE:
        token.type = '01h'
    elif token.type == A.T_PSW:
        token.type = '02h'
    elif token.type == A.T_PWR:
        token.type = '03h'
    elif token.type == A.T_PRD:
        token.type = '04h'
    elif token.type == A.T_PRI:
        token.type = '05h'
    elif token.type == A.T_INP:
        token.type = '06h'
    elif token.type == A.T_ADD:
        token.type = '07h'
    elif token.type == A.T_SUB:
        token.type = '08h'
    elif token.type == A.T_MUL:
        token.type = '09h'
    elif token.type == A.T_DIV:
        token.type = '0Ah'
    elif token.type == A.T_JIZ:
        token.type = '0Bh'
    elif token.type == A.T_JIS:
        token.type = '0Ch'
    elif token.type == A.T_JUM:
        token.type = '0Dh'
tokens = tokens[1:]

if not silent and inside:
    print()
    print(f'Translated tokens: {tokens[1:]}')

# String
out = ''
for token in tokens:
    out += token.type
    if token.data: out += ', ' + str(token.data)
    out += ', '
out = out[:-2]

if not silent and inside:
    print()
    print(f'String: {out}')

instructions = split_list(tokens, 16)
g = ''
j = 1
for tokens in instructions:
    out = ''
    for token in tokens:
        out += token.type
        if token.data != None: out += ', ' + str(token.data)
        out += ', '
    out = out[:-2] + f'\ninstructions{j} db '
    g += out
    j += 1 
g = g[:-18]

main_code = base_code.replace('ext_mem_size_here', str(memory_size)).replace('instructions_here', g)

with open(asm_file_path, 'w') as file:
    file.write(main_code)

if not silent:
    print('Finished succesfully')