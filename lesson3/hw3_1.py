""" 
домашняя работа 3 студента Зивенко Константина

курс GoIT, группа Python Omline 2
модуль 3: 'Функции'
задание: 'Ряд Фибоначчи'
"""


def fibonacci(n):
    """ 
    Функция возвращает n-й член ряда Фибоначчи, 
    считая первым элементом элемент с номером 0
    """
    if n <= 1:
        return 0 or n
    return fibonacci(n-1) + fibonacci(n-2)


def main():
    """
    Функция самопроверки модуля. Запускается при автономном запуске модуля.
    Валидирует вводимые данные (целое число больше 0) и выводит результат работы функции
    fibonacci() в консоль.
    ВАЖНО! При передаче аргумента более 45 - время расчетов может быть значительным.
    """
    n = None
    while n is None:
        try:
            n = int(input("введите целое число, 0 - допустимое значение: "))
            if n < 0:
                print(
                    f"Вы ввели {n}. Введенное число должнот быть положительным. Попробуйте еще раз.")
                n = None
                continue

        except ValueError:
            print("вводимые символы должны быть целым числом")

    print(fibonacci(n))


if __name__ == "__main__":
    main()
