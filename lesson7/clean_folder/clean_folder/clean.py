'''скрипт принимает на вход первым параметром имя папки с файлами\папками для разбора
(по умолчанию принимается текущая папка) и сортирует имеющиеся в ней файлы в соотвествии
с раширениями файлов (структура сортировки задается словарем sort_dict). При этом из
названий файлов удаляются все символы кроме букв, цифр и символа _ (` и ь удаляются,
остальные заменяются на _), кирилица заменяется на латиницу в соотвествии с правилами
транслитерации украинского языка. Сортировка файлоа производится путем записи в создаваемые
субпапки (названия - беруться из словаря sort_dict), все пустые папки уничтожаются, файлы с
неизвестными расширениями перемещаются в папку для неополнанных. Архивы, с которыми умеет
работать скрипт, паспаковываются в папке с архивными файлами, при этом для каждого архива
создается своя папка, название которой совпадает с исходным архивным файлом'''

import sys
import re
import shutil
import os
from pathlib import Path


def normalize(text):  # --> str
    """функция принимает строку и убирает символы "ь" и "'", кирилицу заменяет на латиницу
    в соотвествии с правилами транслитерации украинского языка (пост 55 КМУ 2010 год),
    цифры и латиницу - не трогает, остальные символы заменяет нижним подчерком"""

    def delete_apostrof_soft_sign(text):
        "очищает строку от апострофов, мягких знаков и твердых знаков"

        return text.replace('ь', '').replace("'", "").replace("ъ", "")

    def replaces_comb_zgh(text):
        "заменяет сочетание букв 'зг' на 'zgh' "
        return text.replace('зг', 'zgh').replace('Зг', 'Zgh').replace('зГ', 'zgh')

    def replaces_start_sumbol(text):
        "для букв, транслитерация которых отличается в зависимости от"
        "нахождения буквы в начале/не в начале слова, производит замены для начала слова"
        text = re.sub(r"\b[Є]", 'Ye', text)
        text = re.sub(r"\b[є]", 'ye', text)
        text = re.sub(r"\b[Ї]", 'Yi', text)
        text = re.sub(r"\b[ї]", 'yi', text)
        text = re.sub(r"\b[Й]", 'Y', text)
        text = re.sub(r"\b[й]", 'y', text)
        text = re.sub(r"\b[Ю]", 'Yu', text)
        text = re.sub(r"\b[ю]", 'yu', text)
        text = re.sub(r"\b[Я]", 'Ya', text)
        text = re.sub(r"\b[я]", 'ya', text)
        return text

    def replaces_last_step(text):
        "последняя ступень замен украинских символов на их транслитерацию"
        "!!!!Должна использоваться последней в цепочке преобразований"

        ukr_sumbol_string = 'абвгдежзийклмнопрстуфхцчшщюяєіїґыэ'
        latin_transliter_list = ("a", "b", "v", "h", "d", "e", "zh", "z", "y", "i", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                                 "f", "kh", "ts", "ch", "sh", "shch", "iu", "ia", "ie", "i", "i", "g", "y", "e")
        TRANS = {}
        for c, l in zip(ukr_sumbol_string, latin_transliter_list):
            TRANS[ord(c)] = l
            TRANS[ord(c.upper())] = l.title()
        return text.translate(TRANS)
    text1 = re.sub(r"\W", '_', text)
    return replaces_last_step(replaces_start_sumbol(replaces_comb_zgh(delete_apostrof_soft_sign(text1))))


def get_sort_dist_strukture():
    "функция создает словарь для сортировки файлов"
    sort_dict = {
        'archives': (['zip', 'gz', 'tar'], []),
        'music': (['mp3', 'ogg', 'wav', 'amr'], []),
        'pictures': (['jpeg', 'png', 'jpg', 'svg'], []),
        'video': (['avi', 'mp4', 'mov', 'mkv'], []),
        'doc': (['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'], []),
        'unknown': ([], [])
    }
    return sort_dict


def creating_sort_list_in_dict(path, sort_dict):
    """функция просматривает файлы в исходной директории и наполняет списки в соотвествии с
    категриями в sort_dict"""

    unknown_file_set = set()
    for element in path.iterdir():
        if element.is_file():
            # накапливаем имена всех файлов
            unknown_file_set.add(element)
            for key, value in sort_dict.items():
                # проверяем соотвествие расширени файла ключу
                if element.name.rsplit('.', 2)[-1] in set(value[0]):
                    sort_dict[key][1].append(element)
                    unknown_file_set.discard(element)
                    continue

        else:
            creating_sort_list_in_dict(element, sort_dict)
    sort_dict['unknown'][1].extend(list(unknown_file_set))
    return sort_dict


def moves_files(sort_dict_full, path):
    """создает субпапки в указанной директории path, перемещает туда файлы в соотвествии с sort_dict"""
    for key in sort_dict_full:
        if not (path / key).exists():
            (path / key).mkdir()
        for elem in sort_dict_full[key][1]:
            new_name = normalize(elem.stem) + elem.suffix if not(
                elem in sort_dict_full['unknown'][1]) else elem.name
            elem.replace(path / key / new_name)


def delete_empty_folder(sort_dict_full, path):
    """вытирает вложенные в path пустые папки, если это не папки c именами ключей словаря sort_dict_full"""
    for elem in path.iterdir():
        if elem.is_dir() and not (elem.name in set(sort_dict_full)):
            # print(f'папка {elem.name}, надо уничтожать')
            if (not bool(sorted(elem.rglob('*')))):
               # print(f'папка {elem.name} пустая')
                elem.rmdir()
                # print(f'папка {elem.name} уничтожена')
            else:
                # print(f"папка {elem.name} не пустая, в ней {elem.rglob('*')}")
                delete_empty_folder(sort_dict_full, elem)
                # print('вернулись из рекурсивного вызова')
                elem.rmdir()
                # print(f'папка {elem.name} уничтожена')


def unzip_archives(path):
    """функция просматривает архивные файлы в папке 'archives' и если встречает архивы обрабатываемых форматов
    то разархивирует их в субпапки с названием файла архива внутри директории 'archives'"""
    available_arch_type = set()
    for elem in shutil.get_archive_formats():
        available_arch_type.add(elem[0])
    # print('доступные форматы: ', available_arch_type)

    for elem in (path / 'archives').iterdir():
        # print(f'просматриваю файл - {elem.name}')
        # print(elem.suffix)
        if elem.suffix[1:] in available_arch_type:
            print(
                f'найден архив доступного для обработки формата: {elem.name}')
            shutil.unpack_archive(elem, path / 'archives' / elem.stem)
            print('архив разархивирован')


def main():

    if len(sys.argv) < 2:
        path_str = os.getcwd()
    else:
        path_str = sys.argv[1]

    print(f'будет обработана папка {path_str}')
    print('в ходе обработки файлы будут отсортированы по новым папкам, кирилические символы в названиях')
    print('будут заменены на латиницу, старая структура папок внутри указанной Вами будет уничтожена')
    if input('для продолжения работы скрипта подтвердите действие (y/n): ') == 'y':
        path = Path(path_str)
        if path.exists():
            if path.is_dir:
                sort_dict = get_sort_dist_strukture()
                file_type_dict = creating_sort_list_in_dict(path, sort_dict)
                print(file_type_dict)
                moves_files(file_type_dict, path)
                delete_empty_folder(file_type_dict, path)
                unzip_archives(path)
            else:
                print(f'{path.absolute} is file')

        else:
            print(f'path {path.absolute()} not exist')
    print('работа скрипта завершена')


if __name__ == '__main__':
    main()
