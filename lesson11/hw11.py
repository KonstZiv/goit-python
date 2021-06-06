from collections import UserDict
from datetime import date, datetime


class Field(str):
    pass


class Name(Field):

    def __init__(self, name):
        self.value = name

    def __repr__(self):
        return self.value

    def add_name(self, name):
        self.value = name


class Phone(Field):

    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        print('стартовал сеттер phone')
        num = phone.translate(str.maketrans('', '', '+() -'))
        if num.isdigit() and (3 <= len(num) <= 16):
            self.__phone = num
        else:
            raise ValueError(
                'phone number can contain from 3 to 16 digits and symbols: space + - ( )')
        print('self.__phone:  ', self.__phone)
        print('self.phone:  ', self.phone)

    def __repr__(self):
        return self.phone


class Birthday(Field):

    def __init__(self, date) -> None:
        from datetime import datetime
        self._birthday = datetime.strptime(date, "%d-%m-%Y")

    def __repr__(self) -> str:
        return f'{self.birthday:%d-%m-%Y}'

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthdey(self, new_value):
        from datetime import date
        # проверка типа передаваемых данных
        if isinstance(new_value, date):
            # проверка корректности передаваемых данных
            if new_value > date.today():
                raise ValueError(
                    'the field value cannot be a date from the future')
            self._birthday = new_value
        raise TypeError('the <bitrhday> field should be of type datetime')


class Record:
    def __init__(self, name, phone=[], birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def __repr__(self):
        st = f"| {self.name:.<20}| {self.birthday: <11} | {self.phone[0] if self.phone else '': <16} |\n"
        if len(self.phone) > 1:
            for elem in self.phone[1:]:
                st += f"|                     |             | {elem: <16} |\n"
        return st

    def add_phone(self, phone):
        z = Phone(phone)
        # добавить проверку существования такого телефона в списке
        self.phone.append(z)

    def del_phone(self, phone):
        # добавить обработку исключения ValueError если нет такого телефона в списке
        self.phone.remove(phone)

    def change_phone(self, phone_old, phone_new):
        self.del_phone(phone_old)
        self.add_phone(phone_new)

    def days_to_birthday(self):
        from datetime import date, timedelta
        if self.birthday:
            if date.today() > self.birthday.replace(year=date.today().year):
                return (self.birthday.replace(year=date.today().year + 1) - date.today()).days
            return (self.birthday.replace(year=date.today().year) - date.today()).days
        return f'date of birth has not been entered for {self.name.value}'


class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n):
        print(n)
        res = ''
        k = 0
        while k < n:
            res += next(self).value.__repr__()
            k += 1
            print(res)
        yield res


def main():

    adress_book = AdressBook()

    def convert_to_datetime(date):
        date_datetime = datetime.strptime(date, "%Y %m %d")
        return date(date_datetime.year, date_datetime.month, date_datetime.day)
    k = 0
    while k < 2:

        name = Name(input('name: '))
        birthday = Birthday(input('birthday, format: dd-mm-YYYY   : '))
        record = Record(name=name, birthday=birthday)
        count = 1
        phone_str = input(
            'input phones (3-16 numers, (+-() - valid symbols)): ')
        while phone_str:
            record.add_phone(phone_str)
            print(f'it was phone {count}. Empty string breack input')
            phone_str = input(
                'input phones (3-16 numers, (+-() - valid symbols)): ')
            count += 1

        print(record)
        adress_book.add_record(record)
        k += 1

    while True:
        print(adress_book.iterator(int(input("N= "))))


if __name__ == '__main__':
    main()
