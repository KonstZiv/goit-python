from collections import UserDict
from datetime import datetime, date, timedelta


class Phone:

    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    def __eq__(self, ob) -> bool:
        return self.phone == ob.phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        num = phone.translate(str.maketrans('', '', '+() -_'))
        if num.isdigit() and (3 <= len(num) <= 20):
            self.__phone = num
        else:
            raise ValueError(
                'phone number can contain from 3 to 20 digits and symbols: space +-()xX.[]_')

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
        self.name = name
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
                st += f"|                                         |             | {elem.__repr__(): <20} |\n"
        return st

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def search_birthday(self, data_start, data_stop=False, year: bool = False):
        # если дата рождения находится в интервале от data до data_stop\
        # возвращает экзкмпляр записи, иначе возвращает False. Если \
        # date_stop=False, то сравнение проходит не по интервалу дат, а по\
        # одной дате date. Если year=False - то при сравнении год не \
        # учитывается, иначе год участвует в сравнении
        if not self.birthday.birthday:
            # если дата рождения не записана - возвращаем None
            return None

        data_start_local = datetime.strptime(data_start, "%d-%m-%Y")
        data_stop_local = datetime.strptime(
            data_stop, "%d-%m-%Y") if data_stop else datetime.strptime(data_start, "%d-%m-%Y") + timedelta(days=1)
        data_record_local = self.birthday.birthday

        if not year:
            # если year=False то все даты приводятся к текущему году (сравниваются только\
            # по числу и месяцу )
            current_year = date.today().year
            data_start_local = data_start_local.replace(year=current_year)
            data_stop_local = data_stop_local.replace(year=current_year)
            data_record_local = data_record_local.replace(year=current_year)

        if data_start_local <= data_record_local < data_stop_local:
            return self
        # если дата рождения попадает в интервал - возвращаем экземпляр записи, иначе False
        return False

    def search(self, pattern):
        # просматривает текстовые поля записи (name, phone). Если встречает \
        # сответствие паттерну - возвращает экземпляр записи. Иначе возвращает\
        # False
        if pattern.casefold() in self.name.casefold():
            return self
        for phone in self.phones:
            if pattern.casefold() in phone.casefold():
                return self
        return False


class AdressBook(UserDict):
    def add_record(self, record: Record):
        if record.name in self:
            raise KeyError(
                'Запись с таким именем уже существует в адресной книге')
        self[record.name] = record

    def del_record(self, name: str):
        if name in self:
            self.pop(name)
        raise KeyError('записи с таким именем нет в адресной книге')

    def search(self, pattern):
        pass


if __name__ == '__main__':
    name = input('input name: ')
    record = Record(name)
    record.add_birthday(input('input birthday: '))
    counter = 1
    phone = input(f'input phone {counter}: ')
    while phone:
        record.add_phone(phone)
        counter += 1
        phone = input(f'input phone {counter}: ')
    print(record)

    record.del_phone(input('input del phone: '))
    print(record)
