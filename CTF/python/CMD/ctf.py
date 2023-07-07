
FLAG_FILE = 'flag.txt'

def __read_flag():
    with open(FLAG_FILE, 'r') as flag_file:
        return flag_file.read()

def __remove_prefix(data):
    return data[2:] if data[:2] == '50' else data[3:]

def get_flag_by_user_input(data):
    data = __remove_prefix(data)
    if data and data[0] == ';' and data[-1] == ';':
        return __read_flag()
    return None

