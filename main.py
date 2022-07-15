"""Вызов интерпретатора."""
#!/usr/bin/python3

import os
from time import sleep
import subprocess
import sys
from test_scripts.io_test import stress_io_func
from test_scripts.iperf_test import iperf_func
from test_scripts.p7zip_test import stress_p7zip_func
from test_scripts.stress_cpu import stress_cpu_func
from test_scripts.stress_mem import stress_mem_func
from test_scripts.usb_test import usb_testing
sys.path.append('./test_scripts/')


def main():
    """Подготовка зависимостей."""
    deps = ['memtester', 'stress-ng', 'fio', 'sysbench', 'beep', 'iperf3']
    no_deps = []

    for dep in deps:
        try:
            subprocess.check_output(
                [f'which {dep}'], shell=True, stderr=subprocess.STDOUT).decode('utf8')

        except subprocess.CalledProcessError:
            if dep == 'beep':
                dep = 'beep-speaker'
                no_deps.append(dep)
            else:
                no_deps.append(dep)

    if 'root' not in subprocess.check_output(
        ['whoami'], shell=True, stderr=subprocess.STDOUT).decode('utf8'):
        print("\nТребуется режим администратора.\nИспользуйте команду 'su -'.")
        input("\nНажмите Enter для выхода.\n")
        sys.exit()

    else:
        while len(no_deps) != 0:
            aptget = subprocess.call(
                ['apt-get update'], shell=True, stderr=subprocess.STDOUT)
            if 'E: Tried to dequeue a fetching object' in str(aptget):
                subprocess.call(['apt-get update'], shell=True,
                                stderr=subprocess.STDOUT)
            else:
                subprocess.call(
                    [f'apt-get install {" ".join(no_deps)}'], shell=True, stderr=subprocess.STDOUT)
                no_deps = []

    os.system('clear')
    sleep(0.5)

def start_test():
    """Начало тестирования."""
    print("\nВарианты Тестирования: \n\n\
            1. Тест всех устройств.\n\
            2. Тест USB портов.\n\
            3. Тест сетевых устройств.\n\
            4. Тест накопителей.\n\
            5. Тест оперативной памяти.\n\
            6. Тест ЦПУ.\n\
            7. Тест ЦПУ p7zip.\n")
    input_number = 0
    while input_number == 0:
        try:
            select = int(input("\nВыберите тест: "))
            assert len(str(select)) == 1
            if select > 8:
                print("\nНекорректный ввод.\n")
            elif select < 8:
                input_number = 1
        except (ValueError, TypeError):
            print("\nНекорректный ввод.\n")

    os.system(
        'cd /home/user/LinuxTesting/; mkdir logs &> /dev/null; mkdir logs/errors &> /dev/null')
    os.system(
        '\\cp test_scripts/config/status_config_original.json ./status.json &> /dev/null')
    if select == 1:
        usb_testing()
        iperf_func()
        stress_io_func()
        stress_mem_func()
        stress_cpu_func()
        stress_p7zip_func()

    elif select == 2:
        usb_testing()

    elif select == 3:
        iperf_func()

    elif select == 4:
        stress_io_func()

    elif select == 5:
        stress_mem_func()

    elif select == 6:
        stress_cpu_func()

    elif select == 7:
        stress_p7zip_func()


if __name__ == '__main__':
    try:
        main()
        start_test()
    except KeyboardInterrupt:
        print("\n\n\n\n\nВыходим...\n\n")
        sleep(1)
        quit()
