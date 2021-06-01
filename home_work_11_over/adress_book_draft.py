from collections import UserDict
from time import strftime
from faker import Faker
from datetime import datetime, date, timedelta


class Field(str):
    # для меня совершенно непонятно для чего необходимый\
    # класс. Наследовал от str для поддержки производными \
    # классами методов форматирования строк

    def __init__(self):
        self.value = None


class Name(Field):
    def __init__(self, name):
        self.value = name


class Phone:
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        # поверяет введенное значение телефона (цифр 3-20, допустимы\
        # символы +() -хХ[] ) и приводит к виду - только цифры. Иначе\
        # генерирует ValueError
        num = phone.translate(str.maketrans('', '', '+() -xX.[]'))
        if num.isdigit() and (3 <= len(num) <= 20):
            self.__phone = num
        else:
            raise ValueError(
                'phone number can contain from 3 to 20 digits and symbols: space +-()xX.[]')
        #print('self.phone:   ', self.phone)
        #print('self.__phone: ', self.__phone)

    def __repr__(self):
        return self.phone


class Birthday:
    def __init__(self, date_str):
        self.__birthday = None
        self.birthday = datetime.strptime(date_str, "%d-%m-%Y")

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, new_value):
        if isinstance(new_value.date(), date):
            if new_value.date() > date.today():
                raise ValueError('введенная дата роджения в будущем')
            self.__birthday = new_value
        else:
            raise TypeError('поле Birthday.birthday должно быть типа datetime')

    def __repr__(self):
        return self.birthday.strftime('%d-%m-%Y')


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        if Phone(phone) in self.phones:
            raise ValueError(
                'добавление телефона: такой номер уже есть в списке')
        else:
            self.phones.append(Phone(phone))
        return self

    def del_phone(self, phone):
        if Phone(phone) in self.phones:
            self.phones.remove(Phone(phone))
        else:
            raise ValueError(
                'операция удаления: такого телефона нет в данной записи')

    def change_phone(self, old_phone, nev_phone):
        self.del_phone(old_phone)
        self.add_phone(nev_phone)

    def days_tobirthday(self):
        if self.birthday:
            if date.today() > self.birthday.replace(year=date.today().year):
                return (self.birthday.replace(year=date.today().year + 1) - date.today()).days
            return (self.birthday.replace(year=date.today().year) - date.today()).days
        return f'Не введена дата родения для {self.name.value}'

    def __repr__(self):
        st = f"| {self.name:.<40}| {self.birthday.__repr__(): <11} | {self.phones[0].__repr__() if self.phones else '': <20} |\n"
        if len(self.phones) > 1:
            for elem in self.phones[1:]:
                st += f"|                     |             | {elem: <20} |\n"
        return st


class AdressBook(UserDict):

    def add_record(self, record):
        if record.name.value in self.data:
            raise ValueError('добавление записи: такое имя уже существует')
        else:
            self.data[record.name.value] = record

    def iterator(self, n):
        counter = 0
        res_string = ''
        for key, value in self.data.items():
            if counter == n:
                yield res_string
            res_string += value.__repr__() + '\n'

    def add_fake_records(self, n):
        fake = Faker(['uk_UA', 'en_US', 'ru_RU'])
        for i in range(n):
            name = fake.name()
            phone = fake.phone_number()
            date_of_birth = fake.date_of_birth(
                minimum_age=10, maximum_age=115).strftime('%d-%m-%Y')
            record = Record(name, date_of_birth).add_phone(phone)
            self.add_record(record)
            print(f'Добавлена запись: {name}  {date_of_birth}  {phone}')
            print(
                f'вид в record: {record.name.value}  {record.birthday.birthday:%d-%m-%Y}  {record.phones[0].phone}')


'''
phone_1 = Phone('1-1-(2233)')
record_1 = Record('mary')
print('record_1.__dict__: ', record_1.__dict__)
record_1.add_phone('+38-445-566')
print('после добавки телефона +38-445-566')
print('record_1.__dict__: ', record_1.__dict__)
print('что записано в списке телефонов записи: ')
print(record_1.phones[0].phone)
'''


adress_book = AdressBook()

adress_book.add_fake_records(20)


print(adress_book.iterator(8))
