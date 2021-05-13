from pathlib import Path
import pickle
import sys

FILE_NAME = 'bot_asisstant_data.dat'    # data file name
DATA_DIRECTORY = ''                     # data file direcory


def deserialize_data(path):
    """By path reads a dictionary that stores data with names (keys) and phone numbers (values)"""

    with open(path, "rb") as fh:
        data = pickle.load(fh)

    return data


def serialize_data(data, path):
    """saves data (data) to a file at path (path)"""

    with open(path, "wb") as fh:
        pickle.dump(data, fh)


def parse_word(word, value=None):
    l = len(word)

    def result(src):
        if src.casefold().startswith(word.casefold()):  # опять if! вот живучая тварь!
            return value, src[l:].lstrip()

    return result


def hello_func():
    pass


def inp_out_data_func(path, func):

    def wrapper(*args, **kwargs):
        data = deserialize_data(path)
        result = func(data, *args, **kwargs)
        serialize_data(result, path)
        return result
    return wrapper


@inp_out_data_func
def add_func(data, name, phone):

    if name in set(data):
        raise ValueError('trying to add an existing name')
    data[name] = phone
    return data


def change_func():
    pass


def phone_func():
    pass


def show_all_func():
    pass


def exit_func():
    pass


def input_error():
    pass


def get_handler():
    pass


def main():
    pass

    # while True:
    #    input_string = input()
    #    res_pars = parce(input_string)
    #    get_handler(res_pars[word])(res_pars[args])
    if len(sys.argv) < 2:
        path = DATA_DIRECTORY
        name = FILE_NAME
        path_file = Path(path) / name
        data = deserialize_data(
            path_file) if Path.exists(path_file) else []

    else:
        path = sys.argv[1]
        name = FILE_NAME
        path_file = Path(path) / name
        data = deserialize_data(path_file)


if __name__ == '_main__':
    main()
