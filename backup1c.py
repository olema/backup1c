# backup1c.py
# -*- coding: cp1251 -*-
# Скрипт архивирует базы и приложения 1С, копирует их на NAS и
# удаляет, при привышении порогового кол-ва, файлы архивов на локальном ресурсе
# сервера ServerHP

import subprocess
import os
import shutil
import sys
import time
import logging

# Путь до log-файла
logfile = u'D:\\backup\\logs\\backup1c.log'

# Формат логирования
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG,
                    filename=logfile)

# Путь до архиватора
archivator = 'C:\\Program Files\\7-Zip\\7z.exe'

# Путь до архивов на NAS
copyto = '\\\\NAS\\copy1c\\py_backup'

# Количество файлов каждого архива, который храним на ServerHP.
# Если больше, то удаляем 5 старых архивов
threshold = 9

# В этот список заносятся списки путей до файлов которые архивируем,
# , путь до файла-архива и имя архива
# В этот список заносятся списки путей до файлов и имя архива
# Структура:
# lines[n][0] - номер строки в конф. файле (с учетом комментов, т.е.
# номер физической строки)
# lines[n][1] - путь до источника архива (что архивируем)
# lines[n][2] - путь до папки, где будет создан файл архива
# lines[n][3] - имя архива. к нему будет прибавлена строка _ГГГГММДДЧЧММСС
# '''
lines = [
    ['1', 'D:\\1C_Base\\v8.2\\Бухгалтерия государственного учереждения',
     'D:\\backup\\1C', '1cv82buh'],
    ['2', 'D:\\1C_Base\\V7.7\\Base1c_77', 'D:\\backup\\1C', '1cv77buh'],
    ['3', 'D:\\1C_Base\\v8.2\\ZiK 2015', 'D:\\backup\\1C', '1cv82zik'],
    ['4', 'D:\\1C_Base\\v8.2\\Omega', 'D:\\backup\\1C', '1cv82ahd']
]
# '''

# lines = [['1','D:\\Тест папка', 'D:\\backup\\testbackup','pysource'],
#        ['2','D:\\Backup\\logs', 'D:\\backup\\testbackup', 'logs']
#        ]

# Функция создания лога в формате html
# Функция создания html из лога формата logging
# Создаёт файл формата html из лога формата logging и копирует
#    его в \\NAS\copy1c\logs\log1c.html
def create_html():
    with open('D:\\backup\\logs\\backup1c.log', 'r', encoding='cp1251') as log:
        l = log.readlines()[-60:]
    with open('D:\\backup\\logs\\log.html', 'w', encoding='utf-8') as loghtml:
        loghtml.write(
            u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n')
        loghtml.write(u'<html>\n')
        loghtml.write(u'<head>\n')
        loghtml.write(u'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n')
        loghtml.write(u'<title>log</title>\n')
        loghtml.write(u'</head>\n')
        loghtml.write(u'<body>\n')
        loghtml.write(u'Created: <b>'+time.strftime('%d.%m.%Y %H:%M') + '</b><br>\n')
        loghtml.write(u'<code>\n')
        for st in l:
            if '=======' in st:
                loghtml.write(u'<b>' + st + '</b><br>\n')
            elif st.startswith('ERROR'):
                loghtml.write(u'<font color="red">' + st + u'</font><br>\n')
            elif st.startswith('CRITICAL'):
                loghtml.write(u'<font color="red"><b>' + st +
                              u'</b></font><br>\n')
            else:
                if '+++' in st:
                    st = '<b>' + st + '</b>'
                loghtml.write(u'<font color="green">' + st + u'</font><br>\n')
        loghtml.write(u'</code>\n')
        loghtml.write(u'</body>\n')
        loghtml.write(u'</head>\n')
    try:
        shutil.copy(r'D:\backup\logs\log.html', r'\\NAS\copy1c\logs\log1c.html')
    except OSError as ex:
        logging.error(u'Copy log1c.html error with exception: {}'.format(ex))
    else:
        logging.info(u'Copy log1c.html success...')

# Пишем в лог приветствие запуска архивирования
logging.info(u'======= Archiving started on platform {}\
             ======='.format(sys.platform))

# Проверяем содержимое lines[]
# в случае если строка не прошла проверку, она удаляется из списка
i = 0
while i < len(lines):
    if len(lines[i]) != 4:  # количество параметров
        sys.stderr.write('Error: - invalid number of parameters in string {}...'.format(lines[i][0]))
        logging.error(u'- invalid number of parameters in string {}...'.format(lines[i][0]))
        del lines[i]
        continue
    if len(lines[i][3]) == 0:  # наличие имени архива
        sys.stderr.write('Error: - archive name missing in string {}...'.format(lines[i][0]))
        logging.error(u'- archive name missing in string {}...'.format(lines[i][0]))
        del lines[i]
        continue
    if not os.path.isdir(lines[i][1]):  # правильность пути до источника
        sys.stderr.write('Error: in string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        logging.error(u' - string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        del lines[i]
        continue
    if not os.path.isdir(lines[i][2]):  # правильность пути до приемника
        sys.stderr.write('Error: in string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        logging.error(u' - string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        del lines[i]
    i += 1

# Проверяем наличие строк в lines после проверки на правильность
if len(lines) == 0:
    logging.critical(u'List is empty after testing. Aborting without archieving...')
    create_html()
    raise SystemExit(3)

# собственно архивирование
total_size = 0
total_numberoffiles = 0
for s in lines:
    archive_file_name = s[3] + '_' + time.strftime('%Y%m%d%H%M%S') + '.zip'
    archive_file = s[2] + os.sep + archive_file_name
    source_files = s[1]
    zip_command = '"' + archivator + archive_file + source_files + '"'
    logging.info(u'+++ Start creating archive {} to folder {}'.format(source_files, s[2]))
    print('Start archive {}'.format(source_files))
    exit_code = subprocess.call([archivator, 'a', '-tzip', archive_file, '-mx5', source_files, '-ssw'])
    if exit_code == 0:
        logging.info(u'Archive {} creating success...'.format(archive_file))
        listofarch = [i for i in os.listdir(s[2]) if i[:8] == archive_file_name[:8]]
        size = 0
        for name in listofarch:
            size += os.path.getsize(s[2] + os.sep + name)
        total_size += size
        total_numberoffiles += len(listofarch)
        logging.info(u'Size of archives named {} is {} MB in {} files'.format(archive_file_name[:8], size // 1024 // 1024, len(listofarch)))
        print('Start copy {}'.format(archive_file_name))
        try:
            shutil.copy(archive_file, copyto + os.sep + archive_file_name)
        except Exception as ex:
            logging.error(u'  Error copy {} to {} with exception {}'.format(archive_file, copyto, ex))
        else:
            logging.info(u'  Copy {} to {} success...'.format(archive_file, copyto))
    else:
        logging.critical(u'  Error on creating archive {} with exit code {} ...'.format(archive_file, exit_code))

logging.info(u'Total size of archives after this session is {} MB in {} files'.format(total_size // 1024 // 1024, total_numberoffiles))

# Удаление старых архивов в папке с архивами на диске сервера
# - pathtofiles - путь до папки, где лежат архивы на ServerHP
# - pathtonas - путь до папок с архивами на NAS
# - namearc - первые 8 символов имени архива, который надо удалить
# - threshold - число архивов, после превышения которого надо удалить 5 старых
# def delfiles(pathtofiles, pathtonas, namearc, threshold):
for i in lines:
    pathtofiles = i[2]
    pathtonas = copyto
    namearc = i[3]
    # получаем список файлов
    d = os.listdir(pathtofiles)
    d.sort()
    # фильтруем имена архивов, которые хотим удалить
    dn = [i for i in d if i.startswith(namearc)]
    # если кол-во файлов в каталоге больше указанного в threshold, удаляем 5
    # старых файлов, предварительно проверив их на наличие на NAS
    if len(dn) > threshold:
        filesfordel = dn[:5]
        for i in filesfordel:
            # проверяем наличие файла на NAS
            if os.path.isfile(pathtonas + os.sep + i):
                # удаляем файл в директории с бэкапами на локальном ресурсе
                # ServerHP
                try:
                    os.remove(pathtofiles + os.sep + i)
                except OSError:
                    logging.error(u'Error deleting {}'.format(pathtofiles + os.sep + i))
                else:
                    logging.info(u'{} deleting success'.format(pathtofiles + os.sep + i))
            else:
                logging.error(u'Not find on NAS: {}'.format(pathtonas + os.sep + i))

create_html()
