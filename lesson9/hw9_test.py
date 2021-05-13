

def parse(input_string):

    def parse_word(word):
        l = len(word)

        def result(src):
            if src.casefold().startswith(word.casefold()):
                return word, src[l:].lstrip()

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

    res_pars = [i(input_string) for i in parse_scoup if i(input_string)] if [
        i(input_string) for i in parse_scoup if i(input_string)] else [('unrecognize', '')]

    return res_pars


def get_handler(res_pars):

    def help_f(*args):
        return '''format: command parameters
        command:
        - add - 
        - change - 
        - show all - 
        - exit/./close/goog bye - 
        - phone - 
        - hello -'''

    def add_f():
        pass

    def hello_f(*args):
        return 'How can I help you?'

    def change_f(*args):
        pass

    def phone_f(*args):
        pass

    def show_all_f(*args):
        pass

    def exit_f(*args):
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

    return HANDLING[res_pars[0][0]](res_pars[0][1])


def main():
    while True:
        input_string = input()                           # получить строку
        # выделить комaнду и параметр. Если результат неопределенный - вернуть сообщение об ошибке в параметре
        res_pars = parse(input_string)
        # print(res_pars)
        # вызывает обработчик, выполняет команду. Возвращает сообщение (или об ошибке, или требуемое)
        if not get_handler(res_pars):
            print('Good bye!')
            break
        print(get_handler(res_pars))


if __name__ == '__main__':
    main()
