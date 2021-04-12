""" Домашняя работа Зивенко Константина.
Группа Python #2, GoIT, тема 4
формат вызова: hw4.py [path], где path - строковое представление пути к
директории для анализа файлов в директории в соотвествии с правилами используемой ОС.
По умолчанию проводится анализ в текущей директории"""

import sys
from pathlib import Path


def sort_file(path, file_type_dict):
    """функция сортирует файлы в директории path по расширениям после точки.
    path - директория для сортировки файлов, объект типа Path (в понимании модуля pathlib)
    file_type_dict словарь, ключи которого - это кортежи строк, которые соотвествуют
    сортируемым расширениям файлов. Добавляя/убирая ключи в словарь - Вы влияете на
    сотрировку - добавляете/убираете новые группы сортируемых файлов,
    изменяя состав кортежей - добавляя/убирая в кортежи новые строки с расширениями файлов
    - Вы добавляете/убираете новые типы файлов в группы
    Получать функция должна словарь с определенными для сортировки ключами, которым соотвествуют
    в виде значений пустые списки.
    Возвращает функция єтот же словарь со списками файлов. Расширения файлов соответствуют
    элементам ключей-кортежей"""

    all_file_set = set()
    for element in path.iterdir():
        if element.is_file():
            # накапливаем имена всех файлов
            all_file_set.add(element.name)
            for key in file_type_dict:
                # проверяем соотвествие расширени файла ключу
                if element.name.rsplit('.', 2)[-1] in set(key):
                    file_type_dict[key].append(element.name)
                file_type_dict[('unknown', )].extend(
                    all_file_set - set(file_type_dict[key]))        # из множества всех файлов вычитаем множества тех файлов, которые мы классифицировали. Получаем неклассифицированные файлы
        else:
            sort_file(element, file_type_dict)
    return file_type_dict


def output_result_sort(file_type_dict):
    """выводит в консоль в human friendly виде результаты сортировки"""
    for key, value in file_type_dict.items():
        title_string = str(key).center(78, '-')
        print(title_string)
        for file in value:
            print(file)
    unknown_type_files = []
    for unknown_file in file_type_dict[('unknown', )]:
        unknown_type_files.append(unknown_file.rsplit('.', 2)[-1])

    print(' unknown type '.center(78, '-'))
    print(set(unknown_type_files))


def main():
    """основной цикл программы
    изменяя словарь file_type_dict - задаем параметры сортировки
    вид сортируемых файлов (видео, документы и т.д.) соотвествует
    ключу-кортежу, включаемые в данный вид файлов типы файлов - определяются
    элементами кортежа - строками возможных расширений
    не попавшие ни в один из видов файлы в директории будут собраны
    в список с ключем 'unknown'"""
    file_type_dict = {
        ('jpeg', 'png', 'jpg', 'svg'): [],
        ('avi', 'mp4', 'mov', 'mkv'): [],
        ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'): [],
        ('mp3', 'ogg', 'wav', 'amr'): [],
        ('zip', 'gz', 'tar'): [],
        ('unknown', ): []
    }
    if len(sys.argv) <= 1:
        path = Path('')
    else:
        path = Path(sys.argv[1])
    if path.exists():
        if path.is_dir:
            file_type_dict = sort_file(path, file_type_dict)
            output_result_sort(file_type_dict)
        else:
            print(f'{path.absolute} is file')

    else:
        print(f'path {path.absolute()} not exist')


if __name__ == '__main__':
    main()
