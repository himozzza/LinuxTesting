#!/usr/bin/python3

import subprocess
import curses
import os
import sys
from time import sleep
from threading import Thread

from test_scripts.error_loging import datetime_func, input_err, status_file, write_log


curses.setupterm()
UP = curses.tigetstr('cuu1')
fd = sys.stdout.fileno()


sensors_list = subprocess.check_output(
    ['sensors | grep "Node [0-9] Max"'],
    shell=True).decode('utf8').split('\n')


def temperature():
    """Отслеживание температуры."""
    while True:
        sleep(1)
        print(subprocess.check_output(['sensors | grep "Node [0-9] Max"'],shell=True).decode('utf8'))
        os.write(fd, (UP) * int(len(sensors_list)))
        sleep(2)


def testing():
    """Тестирование 7zip."""
    status_file('7zip', 'start', datetime_func())
    print(f"\n[{datetime_func()}] Тестирование CPU (7zip)...")
    try:
        p7zip = subprocess.check_output(
            ['7z b -md26'],
            stderr=subprocess.STDOUT, shell=True)

        write_log(path_to_file='p7zip.txt', test=p7zip)


    except subprocess.CalledProcessError as error:
        write_log(path_to_file='errors/p7zip_errors.txt', test=error.output)
        error_continue = True
        return error_continue


def stress_p7zip_func():
    """Открытие потоков."""
    thr1 = Thread(target=testing)
    thr2 = Thread(target=temperature, daemon=True)
    thr1.start()
    thr2.start()
    error_continue = False
    thr1.join()


    if error_continue is True:
        print(f'{" " * int(len(sensors_list[0]))}\n' * int(len(sensors_list)))
        os.write(fd, (UP) * (int(len(sensors_list) - 1)))
        status_file('7zip', 'ERROR', datetime_func())
        input_err(name='CPU (p7zip)')

    else:
        print(f'{" " * 100}\n' * int(len(sensors_list)))
        os.write(fd, (UP) * (int(len(sensors_list) - 1)))
        status_file('7zip', 'complete', datetime_func())
        print(f"[{datetime_func()}] Успешно!\n\n")
