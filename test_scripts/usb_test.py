#!/usr/bin/python3

import subprocess
import re
import os

from test_scripts.error_loging import datetime_func, status_file


def usb_testing():
    """Тестирование USB."""
    lsblk_check = False
    usb_tester = 0
    usb_list = []
    dmesg_list = []
    status_file('USB', 'start', datetime_func())
    print(f"\n[{datetime_func()}] Тестирование USB...\nПоочерёдно подключайте USB-flash.\n")

    subprocess.call(['mkdir mountpoint'],
    shell=True, stderr=subprocess.DEVNULL)

    while usb_tester != 2:
        while lsblk_check is False:
            try:
                lsblk = subprocess.check_output(
                    ['lsblk /dev/sd[a-z][0-9] -npo KNAME,RM --list | grep " 1"'],
                    shell=True, stderr=subprocess.STDOUT).decode('utf8').split('\n')
                lsblk_check = True
            except subprocess.CalledProcessError:
                continue


        for name in lsblk:
            if str('1') in name.split(' ')[-1]:
                if name not in usb_list:
                    device_id = subprocess.check_output(
                        ['dmesg | grep "] usb-storage"'],
                        shell=True, stderr=subprocess.STDOUT).decode('utf8').split('\n')[-2]

                    port = re.findall(r'[0-9]-[0-9]\:[0-9].[0-9]', device_id)
                    if port not in dmesg_list:
                        name = name.split(' ')[0]

                        subprocess.call([f'umount {name}'],
                        shell=True, stderr=subprocess.DEVNULL)

                        subprocess.call(
                            [f'mount -r {name} /home/user/LinuxTesting/mountpoint'],
                            shell=True, stderr=subprocess.DEVNULL)

                        if 'linuxusbtestfile.txt' in os.listdir('mountpoint'):

                            usb_list.append(name)
                            dmesg_list.append(port)
                            print(f"[{datetime_func()}] Порт USB работает.")
                            usb_tester += 1


    if usb_tester == 2:
        os.system('while [[ $(findmnt mountpoint) != "" ]];\
             do umount mountpoint; done &> /dev/null')
        os.system('\\rm -r mountpoint &> /dev/null')
        status_file('USB', 'complete', datetime_func())
        print(f"\n[{datetime_func()}] Успешно!\n\n")
        