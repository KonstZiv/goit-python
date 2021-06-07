from collections import UserDict
from datetime import datetime, date, timedelta
from faker import Faker


class Phone:
    # класс для хранения и предварительно обработки номера телефона

    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    def __eq__(self, ob) -> bool:
        # два объекта равны если равны строковые значения сохраненных телефонов
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
                'телефон при вводе может содержать от 3 до 20 цифр и символы: пробел +-()xX.[]_')

    def __repr__(self):
        return self.phone


class Birthday:
    # класс для храниения и предварительной обработки даты рождения. Данные вводятся в строковом
    # виде и отображаются в строковом виде, хранятся в виде объекта datetime
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
    # класс для хранения данных об одном человеке. Тк же содержит методы обработки этой записи
    def __init__(self, name, birthday=None):
        # обязательное поле name
        self.name = name
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        # добавляет номер телефона в существующую запись. Если такой номер есть - генерирует исключение
        if Phone(phone) in self.phones:
            raise ValueError(
                'добавление телефона: такой номер уже есть в списке')
        else:
            self.phones.append(Phone(phone))
        return self

    def del_phone(self, phone):
        # удаляет телефон из записи. При попытке удалить несуществующий номер
        # телефона - генерирует исключение
        if Phone(phone) in self.phones:
            self.phones.remove(Phone(phone))
        else:
            raise ValueError(
                'операция удаления: такого телефона нет в данной записи')

    def change_phone(self, old_phone, nev_phone):
        # замена номера телефона - удаление старого и добавление нового
        self.del_phone(old_phone)
        self.add_phone(nev_phone)

    def days_tobirthday(self):
        if self.birthday:
            if date.today() > self.birthday.replace(year=date.today().year):
                return (self.birthday.replace(year=date.today().year + 1) - date.today()).days
            return (self.birthday.replace(year=date.today().year) - date.today()).days
        return f'Не введена дата родения для {self.name.value}'

    def __repr__(self):
        # форматирует и выводит одну запись в читаемом виде одной или нескольких строк
        # (если запись содержит несколько телефонов)
        st = f"| {self.name:.<40}| {self.birthday.__repr__(): <11} | {self.phones[0].__repr__() if self.phones else '': <20} |\n"
        if len(self.phones) > 1:
            for elem in self.phones[1:]:
                st += f" |                                         |             | {elem.__repr__(): <20} |\n"
        return st

    def add_birthday(self, birthday):
        # добавляет день рождения в существующую запись
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
            if pattern.casefold() in phone.phone.casefold():
                return self
        return False


class AdressBook(UserDict):

    def out_iterator(self, n):
        '''
        метод возвращает на каждой итерации объект класса AdressBook, 
        содержащий n записей из вызывающего метод объекта AdressBook,
        на последнем шаге (исчерпание записей вызывающего объекта) выводятся
        оставшиеся записи
        '''
        # количество элементов выводимых за один вызов метода
        self.n = n
        # счетчик общего количества выведенных записей
        self.k = 0
        # список из ключей вызывающего метод объекта AdressBook
        key_list = list(self)
        # общее кличество записей, которые должны быть выведены
        key_list_max = len(key_list)
        while self.k < key_list_max:
            result = AdressBook()
            # определяем сколько записей можно вывести на текущем шаге (пна последнем шаге
            # выводим меньше чем n)
            max_iter = key_list_max if len(
                key_list[self.k:]) < self.n else self.k + self.n
            for i in range(self.k, max_iter):
                result.add_record(self[key_list[i]])
                self.k += 1
            yield result

    def add_record(self, record: Record):
        # добавляет новую запись в существующую адрессную книгу.
        # Если запись с таким ключем (именем) уже существует - генерирует исключение
        if record.name in self:
            raise KeyError(
                'Запись с таким именем уже существует в адресной книге')
        self[record.name] = record

    def del_record(self, name: str):
        # удаляет запись с ключем name (строка)
        # из существующей адресной книги. Если такого имени нет - генерирует исключение
        if name in self:
            self.pop(name)
        else:
            raise KeyError('записи с таким именем нет в адресной книге')

    def search(self, pattern):
        # возвращает объект класса AdressBook, содержащий
        # все записи, которые при проверке методом Record.search вернут значение
        result = AdressBook()
        for record in self.values():
            res_rec = record.search(pattern)
            if res_rec:
                result.add_record(res_rec)
        return result

    def search_birthday(self, data_start, data_stop=False, year: bool = False):
        # возвращает объект класса AdressBook, содержащий записи, для которых \
        # день рождения попадает в интервал дат data_start и data_stop. \
        # Для всех аргументов действуют те же правила, что и для метода \
        # Birthday.search_bithday()
        result = AdressBook()
        for record in self.values():
            res_rec = record.search_birthday(data_start, data_stop, year)
            if res_rec:
                result.add_record(res_rec)
        return result

    def __repr__(self) -> str:
        res = ''
        for elem in self.values():
            res += elem.__repr__()
        return res

    def add_fake_records(self, n):
        fake = Faker(['uk_UA', 'ru_RU'])
        for i in range(n):
            name = fake.name()
            phone = fake.phone_number()
            date_of_birth = fake.date_of_birth(
                minimum_age=10, maximum_age=115).strftime('%d-%m-%Y')
            record = Record(name, date_of_birth).add_phone(phone)
            self.add_record(record)
            print(f'Добавлена запись: {name}  {date_of_birth}  {phone}')
            print(
                f'вид в record: {record.name}  {record.birthday.birthday:%d-%m-%Y}  {record.phones[0].phone}')


if __name__ == '__main__':
    pass
