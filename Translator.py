import A, sys

def parse_paths(path):
    to_analyze = path.split('\\')[:-1]
    out = ''
    for i in to_analyze:
        out += i + '/'
    return out

def convert_to_int(token):
    out = []
    for val in token.data:
        out.append(int(val))
    token.data = tuple(out) 
    return token.data

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

translator_path = parse_paths(sys.argv[0])
a_code_grammar_path = parse_paths(sys.argv[0]).replace('\\', '/') + 't'
input_file_path = sys.argv[1].replace('\\', '/')
output_file_path = sys.argv[1].split('.')[0].replace('\\', '/') + '.asm'

# Show all important paths to user
# print('')
# print(f'Translator path: {translator_path}, (folder)')
# print(f'A Grammar: {a_code_grammar_path}, (file) ')
# print(f'Input file path: {input_file_path}, (file)')
# print(f'Output file path: {output_file_path}, (file)')
# print('')

# Read file cointainig A code
with open(input_file_path, 'r') as file:
    code_string = file.read()

# Get the base assembly code
with open(a_code_grammar_path, 'r') as file:
    base_code = file.read()

lexer = A.Lexer(code_string)
tokens, error = lexer.analyze_code()

if error: 
    print(error)
    quit()

# Get memory shape and size and set all of data to int
memory_shape = []
memory_size = 1
for token in tokens:
    if token.type == A.T_NUL:
        token.data = None
    elif token.type == A.T_DEF:
        for length in token.data:
            memory_shape.append(int(length))
            memory_size *= int(length)
    
    if token.data:
        final_data = []
        for element in token.data:
            final_data.append(int(element))
        token.data = tuple(final_data)
memory_shape = tuple(memory_shape)

translation_table = {}
j = 0
i = -2
for token in tokens:
    translation_table[j] = i
    if token.data:
        i += 1
    i += 1
    j += 1

for token in tokens:

    # Pointer set position
    if token.type == A.T_PSE:
        token.data = calc_position(token, memory_shape)
    
    # Jumps
    elif token.type in [A.T_JIS, A.T_JIZ, A.T_JUM, A.T_JUS]:
        token.data = translation_table[token.data[0]]
    
    elif token.data:
        token.data = token.data[0]

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

out = ''
for token in tokens:
    out += token.type
    if token.data: out += ', ' + str(token.data)
    out += ', '
out = out[:-2]

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

with open(output_file_path, 'w') as file:
    file.write(main_code)