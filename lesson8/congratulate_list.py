from datetime import datetime
from pathlib import Path
import pickle
import sys


def congratulate(users):
    pass


def users_list_make(users_in):
    """принимает на вход список словарей с именами и датами рождения (имя - str, ключ словаря,
     значение дата рождения - объект datatime), позволяет ввести новые имена и даты рождения. 
     Возвращает расширенный список словарей введенными именами с датами рожденияв том же формате. 
     При вводе контролирует уникальность имен."""

    users_out = users_in
    count = 0
    name_scoup = set()
    print('рабочий файл: ', users_out)
    for elem in users_out:
        for el in elem.keys():
            name_scoup.add(el)
        print('name_scoup: ', name_scoup)

    print('ввод пустой строки вместо имени или даты рождения- останавливает ввод данных')
    while True:
        key = input('Введите имя:  ')
        if key in name_scoup:
            print('Tакое имя уже есть в Вашем списке.')
            continue
        if key:
            bithday_str = input(
                'Введите дату рождения в формате: ДД-ММ-ГГГГ:  ')
            try:
                if bithday_str:
                    bithday_date = datetime.strptime(
                        bithday_str, '%d-%m-%Y').date()
                    users_out.append({key: bithday_date})
                    name_scoup.add(key)

                else:
                    break

            except ValueError:
                print(
                    'Неверный формат ввода даты. Попробуйте сначала. /nВвод пустой строки прекращает ввод данных.')
                continue
        else:
            break

    print(f'в течении этого сеанса Вы ввели {count} имен с датами рождения')
    print(f'всего в Вашем списке {len(users_out)} имен с датами рождения')
    return users_out


def deserialize_users(path):
    """По пути path читает файл, который хранит данные с именами и датами рождения.
    Возвращает список словарей, ключи словаря это имена (str), значения это даты рождения
    (datetime)."""

    with open(path, "rb") as fh:
        users = pickle.load(fh)

    print('файл прочитан')
    return users


def serialize_users(users, path):
    """Список словарей users сохраняет на диск по пути path (объект pathlib.Path)"""

    with open(path, "wb") as fh:
        pickle.dump(users, fh)

    print(f'данные сохранены в файл {path}')


def main():
    if len(sys.argv) < 2:
        path = ''
        name = 'users_data.dat'
        path_file = Path(path) / name
        users_in = deserialize_users(
            path_file) if Path.exists(path_file) else []

    else:
        path = sys.argv[1]
        name = 'users_data.dat'
        path_file = Path(path) / name
        users_in = deserialize_users(path_file)

    users = users_list_make(users_in)
    print(users)
    serialize_users(users, path=path_file)


if __name__ == '__main__':
    main()
