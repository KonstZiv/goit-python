from datetime import datetime, date, timedelta
from pathlib import Path
import pickle
import sys


def congratulate(users):
    # итоговый список
    result_list = [['Monday'],
                   ['Tuesday'],
                   ['Wednesday'],
                   ['Thursday'],
                   ['Friday']]
    day_today = date.today()
    analyzed_day = day_today

    while True:
        if (analyzed_day.isoweekday() in {6, 7}) or (analyzed_day.isoweekday() == 1 and analyzed_day.isocalendar().week == (day_today + timedelta(days=7)).isocalendar().week):
            for elem in users:
                if (elem['bithday'].day == analyzed_day.day) and (elem['bithday'].month == analyzed_day.month):
                    result_list[0].append(elem['name'])
        elif analyzed_day.isoweekday() == 2 and analyzed_day.isocalendar().week == (day_today + timedelta(days=7)).isocalendar().week:
            for elem in users:
                if (elem['bithday'].day == analyzed_day.day) and (elem['bithday'].month == analyzed_day.month):
                    result_list[1].append(elem['name'])
        elif analyzed_day.isoweekday() == 3 and analyzed_day.isocalendar().week == (day_today + timedelta(days=7)).isocalendar().week:
            for elem in users:
                if (elem['bithday'].day == analyzed_day.day) and (elem['bithday'].month == analyzed_day.month):
                    result_list[2].append(elem['name'])
        elif analyzed_day.isoweekday() == 4 and analyzed_day.isocalendar().week == (day_today + timedelta(days=7)).isocalendar().week:
            for elem in users:
                if (elem['bithday'].day == analyzed_day.day) and (elem['bithday'].month == analyzed_day.month):
                    result_list[3].append(elem['name'])
        elif analyzed_day.isoweekday() == 5 and analyzed_day.isocalendar().week == (day_today + timedelta(days=7)).isocalendar().week:
            for elem in users:
                if (elem['bithday'].day == analyzed_day.day) and (elem['bithday'].month == analyzed_day.month):
                    result_list[4].append(elem['name'])

        analyzed_day = analyzed_day + timedelta(days=1)
        if analyzed_day.isocalendar().week == (day_today + timedelta(days=14)).isocalendar().week:
            break

    # печать результата в требуемой форме
    for elem in result_list:
        string = elem[0] + ':   '
        for el in elem[1:]:
            string = string + el + ', '
        print(string)


def users_list_make(users_in):
    """принимает на вход список словарей с именами и датами рождения (имя - str, ключ словаря,
     значение дата рождения - объект datatime), позволяет ввести новые имена и даты рождения.
     Возвращает расширенный список словарей введенными именами с датами рожденияв том же формате.
     При вводе контролирует уникальность имен."""

    users_out = users_in
    count = 0
    name_scoup = set()
    #print('рабочий файл: ', users_out)
    for elem in users_out:
        name_scoup.add(elem['name'])
        print('name_scoup: ', name_scoup)

    print('ввод пустой строки вместо имени или даты рождения- останавливает ввод данных')
    while True:
        name = input('Введите имя:  ')
        if name in name_scoup:
            print('Tакое имя уже есть в Вашем списке.')
            continue
        if name:
            bithday_str = input(
                'Введите дату рождения в формате: ДД-ММ-ГГГГ:  ')
            try:
                if bithday_str:
                    bithday_date = datetime.strptime(
                        bithday_str, '%d-%m-%Y').date()
                    users_out.append({'name': name, 'bithday': bithday_date})
                    name_scoup.add(name)
                    count += 1

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

    #print('файл прочитан')
    return users


def serialize_users(users, path):
    """Список словарей users сохраняет на диск по пути path (объект pathlib.Path)"""

    with open(path, "wb") as fh:
        pickle.dump(users, fh)

    #print(f'данные сохранены в файл {path}')


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

    #users = users_list_make(users_in)
    # print(users)
    #serialize_users(users, path=path_file)
    congratulate(users_in)


if __name__ == '__main__':
    main()
