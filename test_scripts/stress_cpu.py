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
    ['sensors | grep "Node [0-9] Max"'],shell=True).decode('utf8').split('\n')


def temperature():
    """Отслеживание температуры."""
    while True:
        sleep(1)
        print(subprocess.check_output(
            ['sensors | grep "Node [0-9] Max"'],
            shell=True).decode('utf8'))

        os.write(fd, (UP) * int(len(sensors_list)))
        sleep(2)


def testing():
    """Тестирование CPU."""
    cpu_threads = subprocess.check_output(
        ['lscpu | grep -i "^cpu(s):"'],
        shell=True, stderr=subprocess.DEVNULL).decode('utf8').rsplit(
            ' ', maxsplit=1)[-1].split('\n')[0]

    status_file('Stress_ng CPU', 'start', datetime_func())
    print(f"\n[{datetime_func()}] Тестирование CPU (stress_ng CPU)...")
    try:
        stress_ng = subprocess.check_output(
            [f'stress-ng --cpu {cpu_threads} --cpu-method all --verify -t 30m --metrics-brief'],
            stderr=subprocess.STDOUT, shell=True)

        write_log(path_to_file='stress_ng.txt', test=stress_ng)

    except subprocess.CalledProcessError as error:
        write_log(path_to_file='errors/stress_ng_errors.txt', test=error.output)
        error_continue = True
        return error_continue


def stress_cpu_func():
    """Открытие потоков."""
    thr1 = Thread(target=testing)
    thr2 = Thread(target=temperature, daemon=True)
    thr1.start()
    thr2.start()
    thr1.join()
    error_continue = False

    if error_continue is True:
        print(f'{" " * int(len(sensors_list[0]))}\n' * int(len(sensors_list)))
        os.write(fd, (UP) * (int(len(sensors_list) - 1)))
        status_file('Stress_ng CPU', 'ERROR', datetime_func())
        input_err(name='CPU (stress_ng CPU)')

    else:
        print(f'{" " * 100}\n' * int(len(sensors_list)))
        os.write(fd, (UP) * (int(len(sensors_list) - 1)))
        status_file('Stress_ng CPU', 'complete', datetime_func())
        print(f"[{datetime_func()}] Успешно!\n\n")
    