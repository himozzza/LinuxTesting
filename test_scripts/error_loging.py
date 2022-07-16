"""Вызов интерпретатора."""
#!/usr/bin/python3

import json
import datetime
import sys


def input_err(name):
    """Сообщение о продолжении при ошибке."""
    test_continued = False
    while test_continued is False:
        input_error = input(f'\nОшибка тестирования {name}.\nПродолжить? y/N\n# ')

        if input_error.lower() == 'y':
            print('\nПродолжаем...\n')
            test_continued = True
        elif input_error.lower() == 'n':
            print('\n\nВыход...\n\n')
            sys.exit()
        else:
            print("\nОшибка ввода. ВВедите 'y' или 'n'.\n")


def write_log(path_to_file, test):
    """Запись логов."""
    with open(f'logs/{path_to_file}', 'wb') as txtfile:
        txtfile.write(test)


def status_file(test, value, time):
    """Запись статуса тестирования."""
    with open('status.json', 'r', encoding='utf-8') as json_file:
        status = json.load(json_file)
        status[test]['status'] = value
        status[test]['time'] = time
    with open('status.json', 'w', encoding='utf-8') as js_file:
        json.dump(status, js_file, indent=4)


def datetime_func():
    """Получение актуального времени."""
    date = datetime.datetime.today().strftime("%H:%M:%S")
    return date
