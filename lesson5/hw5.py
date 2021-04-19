"""Домашняя работа Зивенко Константина группа Python 2, тема 5
функция транслитерации украинских слов в латиницу отличается от формально задания - транслитерация 
соотвествует постановлению КМУ №55 от 27.01.2010
(транслитерация ряда букв зависит от положения буквы в слове и особым образом определена для ряда сочетаний 
букв)
формат вызова: normalize(text) --> str
text - строка кирилицей (транслитерирует ТОЛЬКО букві украинского алфавита)"""

import re


def delete_apostrof_soft_sign(text):
    "очищает строку от апострофов и мягких знаков"

    return text.replace('ь', '').replace("'", "")


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

    ukr_sumbol_string = 'абвгдежзийклмнопрстуфхцчшщюяєіїґ'
    latin_transliter_list = ("a", "b", "v", "h", "d", "e", "zh", "z", "y", "i", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                             "f", "kh", "ts", "ch", "sh", "shch", "iu", "ia", "ie", "i", "i", "g")
    TRANS = {}
    for c, l in zip(ukr_sumbol_string, latin_transliter_list):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.title()
    return text.translate(TRANS)


def normalize(text):
    "принимает строку, кирилических символов украинского алфавита и транслитерированную латиницей"
    "строку в соттвествии с постановлением КМУ №55 от 27.01.2010"

    return replaces_last_step(replaces_start_sumbol(replaces_comb_zgh(delete_apostrof_soft_sign(text))))


if __name__ == '__main__':
    text = input('введіть строку українською для транслітерації: ')
    # print(text)
    #print("прибираємо апострофи і м'який знак")
    #text1 = delete_apostrof_soft_sign(text)
    # print(text1)
    #print("замінюємо Зг, зг, зГ на Zgh, zgh, zgh")
    # print(replaces_comb_zgh(text1))
    #print('на початках слів')
    #text2 = replaces_start_sumbol(text1)
    # print(text2)
    #print('останній крок')
    #text3 = replaces_last_step(text2)
    # print(text3)
    print(normalize(text))
