from os import name
import sys
import pickle
from pathlib import Path


CONTACTS_FILE = 'contacts.dat'
CONTACTS_DIR = ''


def deserialize_users(path):
    """using the path "path" reads the file with contacts"""

    with open(path, "rb") as fh:
        users = pickle.load(fh)

    return users


def serialize_users(contacts, path):
    """saves a file with contacts on the path (object pathlib.Path) to disk"""

    with open(path, "wb") as fh:
        pickle.dump(contacts, fh)


def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result

        except Exception as message:

            x = message.args
            if x[0] == 'this name is already in the contact list':
                return 'this name is already in the contact list'
            elif x[0] == 'this name is not in the contact list':
                return 'this name is not in the contact list'

        except KeyError:
            return "No user with given name"

        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name or command"
    return inner


def parse(input_string):  # --> ('key word', parameter)
    # extracts a command and parameters from a string, returns as a list with one \
    # element - a tuple of two elements: commands and parameters

    def parse_phone(src):
        # the function takes a string as an argument and looks for a phone number in it\
        # (on the right). Returns a tuple of two arguments - everything up to the phone \
        # number (no spaces on the left and right) and the phone number. If the phone \
        # number is not found, it returns an empty string instead.

        import re
        phone_regex = re.compile(r'[+]?[\d\-\(\)]{5,18}\s?$')
        match = phone_regex.search(src)
        if match is None:
            result = (src.strip(), '')
        else:
            result = (src[:match.start()].strip(), match.group())
        return result

    def parse_word(word):
        # factory function. Produces parser functions for individual commands. \
        # Returns  a tuple from a command, the line after the command and \
        # the phone number. If there is no phone number, an empty string \
        # is returned instead.

        l = len(word)

        def result(src):
            if src.casefold().startswith(word.casefold()):
                return word, parse_phone(src[l:].lstrip())[0], parse_phone(src[l:].lstrip())[1]

        return result

    parse_scoup = [
        parse_word('hello'),
        parse_word('add'),
        parse_word('change'),
        parse_word('phone'),
        parse_word('show all'),
        parse_word('exit'),
        parse_word('close'),
        parse_word('good bye'),
        parse_word('.'),
        parse_word('help')
    ]

    res_pars = [i(input_string) for i in parse_scoup if i(input_string)][0] if [
        i(input_string) for i in parse_scoup if i(input_string)] else ('unrecognize', '')

    return res_pars


@error_handler
def get_handler(res_pars, contacts):

    def help_f(*args):
        return '''format: command parameters
        command:
        - add - format: add name phone_number - add new contact
        - change - format: change name phone_number - change phone number for old contact
        - show all - format: show all - show all contact
        - exit/./close/goog bye - format: exit - stops the program
        - phone - format: phone name - 
        - hello -'''

    def add_f(name, phone, contacts):

        if contacts.get(name):
            raise Exception('this name is already in the contact list')

        contacts[name] = phone

        return f'Contact {name} added with phone number {phone}'

    def hello_f(*args):
        return 'How can I help you?'

    def change_f(name, phone, contacts):
        if not contacts.get(name):
            raise Exception('this name is not in the contact list')
        old_phone = contacts[name]
        contacts[name] = phone

        return f'''for contact {name} number replaced
                old number: {old_phone}
                new number: {phone}'''

    def phone_f(name, phone, contacts):
        if not contacts.get(name):
            raise Exception('this name is not in the contact list')

        return f'for contact {name} number is {contacts[name]}'

    def show_all_f(name, phone, contacts):
        result = ""
        for name, phone in contacts.items():
            result += f"{name}:   {phone}\n"
        return result

    def exit_f(name, phone, contacts):
        return None

    def unrecognize_f(*args):
        return 'incorrect input to get help enter "help"'

    HANDLING = {
        'hello': hello_f,
        'exit': exit_f,
        '.': exit_f,
        'good bye': exit_f,
        'close': exit_f,
        'add': add_f,
        'show all': show_all_f,
        'phone': phone_f,
        'change': change_f,
        'unrecognize': unrecognize_f,
        'help': help_f
    }

    return HANDLING[res_pars[0]](res_pars[1], res_pars[2], contacts)


def main():
    if len(sys.argv) < 2:
        path = CONTACTS_DIR
        name = CONTACTS_FILE
        path_file = Path(path) / name
        contacts = deserialize_users(
            path_file) if Path.exists(path_file) else {}

    else:
        path = sys.argv[1]
        name = CONTACTS_FILE
        path_file = Path(path) / name
        contacts = deserialize_users(path_file)

    while True:
        input_string = input('>>>  ')
        # получить строку выделить комaнду и параметр. Если результат неопределенный\
        #  - вернуть сообщение об ошибке в параметре
        res_pars = parse(input_string)
        print(res_pars)
        # вызывает обработчик, выполняет команду. Возвращает сообщение (или об ошибке, или требуемое)
        result = get_handler(res_pars, contacts)
        if not result:
            serialize_users(contacts, path_file)
            print('Good bye!')
            break
        print(result)


if __name__ == '__main__':
    main()
