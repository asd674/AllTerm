import os
import platform


def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def just_create_file(dir):
    f = open(dir, "x")
    f.close()


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
        com = str(tokens[0])
        if com == 'find':
            if os.path.isdir(cur_directory):
                dirs = []
                a = 1
                for f in os.listdir(cur_directory):
                    print('   ', str(a), ') ', f)
                    a += 1
                    dirs.append(cur_directory + '\\' + f)
                try:
                    a = int(input('>> '))
                    return dirs[a - 1]
                except:
                    return err(1, cur_directory)
            else:
                return err(3, cur_directory)
        elif com == 'up':
            return str(os.path.abspath(os.path.join(cur_directory, os.pardir)))
        elif com == 'start':
            print('   Starting...')
            if os.path.isfile(cur_directory):
                if platform.system() == 'Windows':
                    os.system('"' + cur_directory + '"')
                elif platform.system() == 'Darwin':
                    os.system('open "' + cur_directory + '"')
                return cur_directory
            else:
                return err(2, cur_directory)
        else:
            return err(0, cur_directory)
    elif len(tokens) == 2:
        com = str(tokens[0])
        if com == 'find_disk':
            if str(tokens[1]).find(':') > 0 and os.path.isdir(str(tokens[1])):
                return str(tokens[1])
            else:
                return err(1, cur_directory)
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
