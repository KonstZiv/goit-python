from hw12 import AdressBook, Record, Phone, Birthday
from os import name
import sys
import pickle
from pathlib import Path
from faker import Faker

CONTACTS_FILE = 'contacts.dat'
CONTACTS_DIR = ''


def deserialize_users(path):
    """using the path "path" reads the file with contacts"""

    with open(path, "rb") as fh:
        adressbook = pickle.load(fh)

    return adressbook


def serialize_users(adressbook, path):
    """saves a file with contacts on the path (object pathlib.Path) to disk"""

    with open(path, "wb") as fh:
        pickle.dump(adressbook, fh)


def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except Exception as message:
            return message.args[0]
        except KeyError:
            return "No user with given name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name or command"
    return inner


def parse(input_string):  # --> ('key word', parameter)
    # извлекает команду и параметры из строки, возвращает в виде списка с
    # одним элементом - кортеж из двух элементов: команды и параметры

    def parse_phone(src):
        # функция принимает строку в качестве аргумента и ищет в ней номер телефона (справа)
        # Возвращает кортеж из двух аргументов - все, вплоть до номера телефона (без
        # пробелов слева и справа) и номера телефона. Если номер телефона не найден,
        # вместо него возвращается пустая строка.

        import re
        phone_regex = re.compile(r'[+]?[\d\-\(\)]{5,18}\s?$')
        match = phone_regex.search(src)
        if match is None:
            result = (src.strip(), '')
        else:
            result = (src[:match.start()].strip(), match.group())
        return result

    def parse_word(word):
        # фабричная функция. Производит функции синтаксического анализатора для
        # отдельных команд. Возвращает кортеж из команды, строку после команды
        # и номер телефона. Если номер телефона отсутствует, вместо него
        # возвращается пустая строка.

        l = len(word)

        def result(src):
            if src.casefold().startswith(word.casefold()):
                return word, *parse_phone(src[l:].lstrip())

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
        parse_word('help'),
        parse_word('search'),
        parse_word('other phone'),
        parse_word('bd add')
    ]
    res_pars = [i(input_string) for i in parse_scoup if i(
        input_string)] or [('unrecognize', '', '')]

    return res_pars[0]


@error_handler
def get_handler(res_pars, adressbook):

    def help_f(*args):
        return '''format: command parameters
        command:
        - add - format: add name phone_number - add new contact
        - change - format: change name phone_number - change phone number for old contact
        - show all - format: show all - show all contact
        - exit/./close/goog bye - format: exit - stops the program
        - phone - format: phone name - 
        - hello -'''

    def add_f(name, phone, adressbook):

        record = Record(name)
        record.add_phone(phone)
        birthday_str = input(
            'введите день рождения в формате дд-мм-гггг ("ввод" - пропустить): ')
        if birthday_str:
            record.add_birthday(birthday_str)
        adressbook.add_record(record)

        return f'в адресную книгу внесена запись: \n{record}'

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

    def phone_f(pattern, phone, adressbook):

        result = adressbook.search(pattern)

        if not result:
            raise Exception('По данному запросу ничего не найдено')

        return result

    def show_all_f(N, phone, adressbook):
        n = int(N) if N else 10
        print(f'всего к выводу {len(adressbook)} записей: ')
        for block in adressbook.out_iterator(n):
            print(block)
            print('---------------------------------------------------------------------------------------------------')
            input('для продолжения вывода нажмите "ввод"')
        return 'вывод окончен'

    def exit_f(name, phone, contacts):
        return None

    def unrecognize_f(name, phone, contacts):
        return 'ввод не распознан. Для получения помощи введите "help"'

    def add_phone(name, phone, adressbook):
        if name in adressbook:
            adressbook[name].add_phone(phone)
        else:
            return f'имени {name} нет в адресной книге'
        return f'в запись добавлен новый телефон: \n {adressbook[name]}'

    def bd_add_f(name, birthday_str, adressbook):
        if name in adressbook:
            adressbook[name].add_birthday(birthday_str)
        else:
            return f'имени {name} нет в адресной книге'
        return f'в запись добавлена дата рождения: \n {adressbook[name]}'

    HANDLING = {
        'hello': hello_f,
        'exit': exit_f,
        '.': exit_f,
        'good bye': exit_f,
        'close': exit_f,
        'add': add_f,
        'show all': show_all_f,
        'phone': phone_f,
        'search': phone_f,
        'change': change_f,
        'unrecognize': unrecognize_f,
        'help': help_f,
        'other phone': add_phone,
        'bd add': bd_add_f
    }
    return HANDLING[res_pars[0]](res_pars[1], res_pars[2], adressbook)


def main():
    if len(sys.argv) < 2:
        path = CONTACTS_DIR
        name = CONTACTS_FILE
        path_file = Path(path) / name
        adressbook = deserialize_users(
            path_file) if Path.exists(path_file) else AdressBook()

    else:
        path = sys.argv[1]
        name = CONTACTS_FILE
        path_file = Path(path) / name
        adressbook = deserialize_users(path_file)

    while True:
        adressbook.add_fake_records(20)
        input_string = input('>>>  ')
        res_pars = parse(input_string)
        result = get_handler(res_pars, adressbook)
        if not result:
            serialize_users(adressbook, path_file)
            print('Good bye!')
            break
        print(result)


if __name__ == '__main__':
    main()
