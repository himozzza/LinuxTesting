#!/usr/bin/python3

import subprocess
import os
import curses
import sys
from threading import Thread
from time import sleep

from test_scripts.error_loging import datetime_func, input_err, status_file, write_log

curses.setupterm()
UP = curses.tigetstr('cuu1')
fd = sys.stdout.fileno()


memory_lines = subprocess.check_output(
    ['free -h --giga | cut -c 1-50'], stderr=subprocess.STDOUT, shell=True).decode('utf8').replace(
        'total    ', '    Всего').replace(
            'used      ', 'Использовано').replace(
                'free', 'Свободно').replace(
                    'Mem:', 'Память: ').replace(
                        'Swap:', 'Подкачка:').split('\n')


def free_mem():
    """Мониторинг памяти."""
    while True:
        sleep(1)
        print(subprocess.check_output(
            ['free -h --giga | cut -c 1-50'],
            stderr=subprocess.STDOUT, shell=True).decode('utf8').replace(
                'total    ', '    Всего').replace(
                    'used      ', 'Использовано').replace(
                        'free', 'Свободно').replace(
                            'Mem:', 'Память: ').replace(
                                'Swap:', 'Подкачка:'))

        os.write(fd, (UP) * int(len(memory_lines)))
        sleep(2)


def testing_mem():
    """Подсчет памяти для тестирования и тестирование."""
    status_file('Memory', 'start', datetime_func())
    print(f"\n[{datetime_func()}] Тестирование памяти (Stress-ng)...")
    # call_memory = subprocess.check_output(
    #     ['cat /proc/meminfo | grep "MemFree"'], stderr=subprocess.STDOUT, shell=True).decode(
    #         'utf8').split(" ")[-2]
    # free_memory = int(call_memory) // 1300

    try:
        memtester = subprocess.check_output(
            ['stress-ng --vm 4 --vm-bytes 75% --vm-method all --verify -t 300m -v'],
            shell=True, stderr=subprocess.STDOUT)

        # memtester = subprocess.check_output(
        #     [f'memtester {free_memory} 1'],
        # stderr=subprocess.STDOUT, shell=True)        #Закомментиррован memtester тест.

        write_log(path_to_file='memory.txt', test=memtester)

    except subprocess.CalledProcessError as error:
        write_log(path_to_file='errors/memory_errors.txt', test=error.output)
        error_continue = True
        return error_continue


def stress_mem_func():
    """Открываем потоки."""
    thr1 = Thread(target=testing_mem)
    thr2 = Thread(target=free_mem, daemon=True)
    thr1.start()
    thr2.start()
    error_continue = False
    thr1.join()

    if error_continue is True:
        print(f'{" " * int(len(memory_lines[0]))}\n' * int(len(memory_lines)))
        os.write(fd, (UP) * (int(len(memory_lines) - 1)))
        status_file('Memory', 'ERROR', datetime_func())
        input_err(name='памяти (Stress-ng)')

    else:
        print(f'{" " * 100}\n' * int(len(memory_lines)))
        os.write(fd, (UP) * 3)
        status_file('Memory', 'complete', datetime_func())
        print(f"[{datetime_func()}] Успешно!\n\n")
