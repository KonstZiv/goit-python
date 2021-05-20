from collections import UserDict


class Field:
    pass


class Name(Field):
    def add_name(self, name):
        self.value = name


class Phone(Field):
    pass


class Record:
    name = Name()
    phone = []

    def add_phone(self, phone):
        # добавить проверку существования такого телефона в списке
        self.phone.append(phone)

    def del_phone(self, phone):
        # добавить обработку исключения ValueError если нет такого телефона в списке
        self.phone.remove(phone)

    def change_phone(self, phone_old, phone_new):
        self.del_phone(phone_old)
        self.add_phone(phone_new)


class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
