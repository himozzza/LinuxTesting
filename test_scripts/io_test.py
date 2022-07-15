"""Вызов интерпретатора."""
#!/usr/bin/python3

import subprocess
import re

from error_loging import datetime_func, input_err, status_file, write_log


def stress_io_func():
    """Обработка дисков и тестирование flexible I/O."""
    status_file('Fio I/O', 'start', datetime_func())
    jobs = []
    settings = []
    lsblk = subprocess.check_output(
        ['lsblk -dnpo KNAME --list'], shell=True, stderr=subprocess.STDOUT).decode('utf8')
    for name in lsblk:
        if str('1') not in subprocess.check_output(
            ['lsblk {name} -no RM'], shell=True, stderr=subprocess.STDOUT).decode('utf8'):
            jobs.append(name)

    with open('test_scripts/config/fio_config_original', 'r', encoding='utf-8') as fio_config:
        work_config = fio_config.read().split(' ')
    settings.append(work_config[0])
    work_config.pop(0)

    for work, job in zip(work_config, jobs):
        re.sub(r'^filename=$',
               f'filename={job}/testfile', work, flags=re.MULTILINE)
        if '/' in re.findall(r'/$', subprocess.check_output(
            [f'lsblk {job} -npno NAME,MOUNTPOINTS --list'], shell=True).decode(
                'utf8'), flags=re.MULTILINE):
            work = f'{work}rw=read\n'
        settings.append(work)

    with open('test_scripts/config/fio_config', 'w', encoding='utf-8') as write_line:
        write_line.writelines(settings)

    print(f"\n[{datetime_func()}] Тестирование Input/Output (flexible I/O)...")
    try:
        stress_io = subprocess.check_output(
            ['fio test_scripts/config/fio_config'], stderr=subprocess.STDOUT, shell=True)
        write_log(path_to_file='fio.txt', test=stress_io)
        status_file('Fio I/O', 'complete', datetime_func())
        print(f"[{datetime_func()}] Успешно!\n\n")
    except subprocess.CalledProcessError as error:
        write_log(path_to_file='errors/fio_errors.txt', test=error.output)
        status_file('Fio I/O', 'ERROR', datetime_func())
        input_err(name='накопителей (flexible I/O)')
