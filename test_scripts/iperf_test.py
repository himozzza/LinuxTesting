#!/usr/bin/python3

import subprocess
from time import sleep

from test_scripts.error_loging import datetime_func, input_err, status_file, write_log


def iperf_func():
    """Обработка Ethernet портов и тестирование сети."""
    status_file('Ethernet', 'start', datetime_func())
    ethernet_list = []
    iperf_enable = False
    while iperf_enable is False:
        try:
            eth_ports = int(input("\nКоличество дополнительных Ethernet раъёмов: "))
            if int(eth_ports) < 3:
                iperf_enable = True
            elif int(eth_ports) >= 3:
                print("\nОшибка! Неверный ввод.")
                continue

        except (ValueError, AssertionError):
            print("\nОшибка! Неверный ввод.")
            continue

    hw_addr = subprocess.check_output(
        ["ifconfig | grep HWaddr"],
        shell=True, stderr=subprocess.STDOUT).decode('utf8')


    for list_hw_addr in str(hw_addr).split('\n'):
        ethernet_list.append(''.join(str(list_hw_addr).split(" ", maxsplit=1)[0]))

    ethernet_list.remove('')

    if eth_ports == 0:
        eth_ports = 2
    elif eth_ports == 2:
        eth_ports = 0

    while len(ethernet_list) != eth_ports:
        for eth_list in ethernet_list:
            ip_addr = subprocess.check_output(
                [f'ifconfig {eth_list}'],
                shell=True, stderr=subprocess.STDOUT).decode('utf8')

            if 'inet addr' in ip_addr:
                print(f"\n[{datetime_func()}] Тестирование Ethernet порта {eth_list} (iperf3)...")
                sleep(5)
                try:
                    iperf = subprocess.check_output(
                        ['iperf3 -i 5 -t 60 -c 192.168.1.109'],
                        shell=True,stderr=subprocess.STDOUT)

                    write_log(path_to_file=f'iperf-{eth_list}.txt', test=iperf)
                    status_file('Ethernet', 'complete', datetime_func())
                    print(f"[{datetime_func()}] Успешно!\n\n")

                except subprocess.CalledProcessError as error:
                    write_log(path_to_file=f'errors/iperf_errors-{eth_list}.txt', test=error.output)
                    status_file('Ethernet', 'ERROR', datetime_func())
                    input_err(name='сети (iperf3)')
                ethernet_list.remove(eth_list)
