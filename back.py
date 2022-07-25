import os

def err(code: int, dir):
    print('Error code ' + str(code))
    return dir

def lexer(command):
    tokens = []
    cur_tok = ''
    for char in command:
        if char == ' ' and cur_tok != '':
            tokens.append(cur_tok)
            cur_tok = ''
        else:
            cur_tok = cur_tok + char
    if cur_tok != '':
        tokens.append(cur_tok)

    return tokens


def do(tokens: list, cur_directory: str):
    if len(tokens) == 1:
        if tokens[0] == 'updir':
            return str(os.path.abspath(os.path.join(cur_directory, os.pardir)))
        else:
            return err(0, cur_directory)
    elif len(tokens) == 2:
        if tokens[0] == 'finddir':
            if os.path.exists(tokens[1]):
                return tokens[1]
            else:
                return err(2, cur_directory)
        else:
            return err(0, cur_directory)
    else:
        return err(0, cur_directory)

def run():
    cur_dir: str = os.path.expanduser('~')
    print('Tech Group\n')
    while True:
        com = input(cur_dir + '> ')
        cur_dir = do(lexer(com), cur_dir)
