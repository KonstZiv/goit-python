from hw12_classes import AdressBook, Record, Phone, Birthday
from os import name
import sys
import pickle
from pathlib import Path
from faker import Faker

# директория может быть выбрана при запуске программы, имя файла - константа.
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
    # сюда вынесена обработка всех возникающих ошибок в ходе работы программы - как типов и
    # форматов, так и логические (дата рождения в будущем, попытка удалить несуществующий параметр и т.д.)
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
        # parse_word('change'),
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
    # получив результаты работы парсера функция управляет передачей параметров
    # и вызовм соотвествующего обработчика команды

    def help_f(*args):
        return '''формат команд:
        - add - формат: add name phone_number - добавляет новый контакт
        - other phone - формат: other phone name phone_number - добавляет дополнительный телефон в существующую запись
        - show all - формат: show all [N] - показывает всю адресную книгу. N - необязательный параметр - количество одновременно выводимых записей
        - exit/./close/goog bye - формат: exit - остановка работы с программой. Важно! чтобы сохранить все изменения и введенные данные - используйте эту команду
        - phone - формат: phone name - поиск телефона по имени. Можно ввести неполной имя либо его часть - программа выведет все совпадения
        - hello - формат: hello - просто Ваше привествие программе. Доброе слово - оно и для кода приятно)
        - bd add - формат: bd add name dd-mm-YYYY - ввод либо перезапись ранее введенной даты рождения. Соблюдайте формат ввода даты.
        - search - формат: search pattern - поиск совпадений по полям имени и телефонов. Будут выведены все записи в которых есть совпадения'''

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

    # def change_f(name, phone, contacts):
    # закоментирована, так как по сути своей совершенно бессмысленная функция
    #    if not contacts.get(name):
    #        raise Exception('this name is not in the contact list')
    #    old_phone = contacts[name]
    #    contacts[name] = phone#
    #
    #    return f'''for contact {name} number replaced
    #            old number: {old_phone}
    #            new number: {phone}'''

    def phone_f(pattern, phone, adressbook):
        # осуществляет поиск по паттерну во всех текстовых полях адресной книги
        result = adressbook.search(pattern)

        if not result:
            raise Exception('По данному запросу ничего не найдено')

        return result

    def show_all_f(N, phone, adressbook):
        # выводит на экран всю адресную книгу блоками по N записей. Основная обработка
        # реализована как метод класса AdressBook, что позволяет использовать аналогичный
        # вывод для результатов поиска по запросам, так как функции поиска возвращают
        # объект типа AdressBook с результатами
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
        # позволяет добавить в запись дополнительный телефон
        if name in adressbook:
            adressbook[name].add_phone(phone)
        else:
            return f'имени {name} нет в адресной книге'
        return f'в запись добавлен новый телефон: \n {adressbook[name]}'

    def bd_add_f(name, birthday_str, adressbook):
        # позволяет добавить (перезаписать, если ранее было введена) дату рождения в запись
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
        # 'change': change_f,
        'unrecognize': unrecognize_f,
        'help': help_f,
        'other phone': add_phone,
        'bd add': bd_add_f
    }
    return HANDLING[res_pars[0]](res_pars[1], res_pars[2], adressbook)


def main():
    # главный цикл работы программы
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
        # adressbook.add_fake_records(40)
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
