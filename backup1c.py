# -*- coding: cp1251 -*-

import subprocess
import os
import shutil
import sys
import time
import logging

def create_html():
	''' Функция создания html из лога формата logging

	    Создаёт файл формата html из лога формата logging и копирует
	    его в \\NAS\copy1c\logs\log1c.html
	'''
	with open('D:\\backup\\logs\\backup1c.log', 'r', encoding='cp1251') as log:
		l = log.readlines()
		l1 = l[-60:]
		del l
	with open('D:\\backup\\logs\\log.html', 'w', encoding='utf-8') as loghtml:
		loghtml.write(u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n')
		loghtml.write(u'<html>\n')
		loghtml.write(u'<head>\n')
		loghtml.write(u'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n')
		loghtml.write(u'<title>log</title>\n')
		loghtml.write(u'</head>\n')
		loghtml.write(u'<body>\n')
		loghtml.write(u'Created: <b>'+time.strftime('%d.%m.%Y %H:%M') + '</b><br>\n')
		loghtml.write(u'<code>\n')
		for s in l1:
			if '=======' in s:
				loghtml.write(u'<b>'+s+'</b><br>\n')
			elif s.startswith('ERROR'):
				loghtml.write(u'<font color="red">'+ s + u'</font><br>\n')
			elif s.startswith('CRITICAL'):
				loghtml.write(u'<font color="red"><b>'+ s + u'</b></font><br>\n')
			else:
				loghtml.write(u'<font color="green">'+ s + u'</font><br>\n')
		loghtml.write(u'</code>\n')
		loghtml.write(u'</body>\n')
		loghtml.write(u'</head>\n')
	shutil.copy('D:\\backup\\logs\\log.html','\\\\NAS\\copy1c\\logs\\log1c.html') 


logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'D:\\backup\\logs\\backup1c.log')

# Пишем в лог приветствие запуска архивирования
logging.info(u'======= Archiving started on platform {} ======='.format(sys.platform))

# В этот список заносятся списки путей до файлов и имя архива
# Структура:
# lines[n][0] - номер строки в конф. файле (с учетом комментов, т.е. номер физической строки)
# lines[n][1] - путь до источника архива (что архивируем)
# lines[n][2] - путь до папки, где будет создан файл архива
# lines[n][3] - имя архива. к нему будет прибавлена строка _ГГГГММДДЧЧММСС


lines=[['1','D:\\1C_Base\\v8.2\\Бухгалтерия государственного учереждения', 'D:\\backup\\1C', '1cv82buh'],
       ['2','D:\\1C_Base\\V7.7\\Base1c_77', 'D:\\backup\1C', '1cv77buh'],
       ['3','D:\\1C_Base\\v8.2\\ZiK 2015', 'D:\\backup\\1C', '1cv82zik'],
       ['4','D:\\1C_Base\\v8.2\\Omega', 'D:\\backup\\1C', '1cv82ahd']
      ]

'''
lines = [['1','D:\\Тест папка', 'D:\\backup\\testbackup','pysource'],
         ['2','D:\\1C_Base\\v7.7\\Base1c_77_', 'D:\\backup\\testbackup', '1cBase77']
        ]
'''

# Проверяем содержимое lines[] 
i = 0
while i < len(lines):
	if len(lines[i]) != 4:             # количество параметров
		sys.stderr.write('Error: - invalid number of parameters in string {}...'.format(lines[i][0]))
		logging.error(u'- invalid number of parameters in string {}...'.format(lines[i][0]))
		del lines[i]
		continue
	if len(lines[i][3]) == 0:          # наличие имени архива
		sys.stderr.write('Error: - archive name missing in string {}...'.format(lines[i][0]))
		logging.error(u'- archive name missing in string {}...'.format(lines[i][0]))
		del lines[i]
		continue
	if not os.path.isdir(lines[i][1]): # правильность пути до источника
		sys.stderr.write('Error: in string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
		logging.error(u' - string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
		del lines[i]
		continue
	if not os.path.isdir(lines[i][2]): # правильность пути до приемника
		sys.stderr.write('Error: in string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
		logging.error(u' - string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
		del lines[i]
	i += 1

# Проверяем наличие строк в lines после проверки на правильность
if len(lines) == 0:
	sys.stderr.write('Error: file {} is empty...'.format(name))
	logging.critical(u'file {} is empty after testing. Aborting without archieving...'.format(name))
	create_html()
	raise SystemExit(3)

# собственно архивирование
archivator = 'C:\\Program Files\\7-Zip\\7z.exe'
copyto = '\\\\NAS\\copy1c\\py_backup'
total_size = 0
total_numberoffiles = 0
for s in lines:
    archive_file_name = s[3] + '_' + time.strftime('%Y%m%d%H%M%S') + '.zip'
    archive_file = s[2] + os.sep + archive_file_name 
    source_files = s[1] 
    zip_command = '"' + archivator + archive_file + source_files + '"'
    logging.info(u'+++ Start creating archive {}'.format(source_files))
    print('Start archive {}'.format(source_files))
    exit_code = subprocess.call([archivator, 'a', '-tzip', archive_file, '-mx5', source_files, '-ssw'])
    if exit_code == 0:
        logging.info(u'  Archive {} creating success...'.format(archive_file))
        listofarch = [ i for i in os.listdir(s[2]) if i[:8] == archive_file_name[:8]]
        size = 0
        for name in listofarch:
            size += os.path.getsize(s[2] + os.sep + name)
        total_size += size
        total_numberoffiles += len(listofarch)
        logging.info(u'Size of archives named {} is {} MB in {} files'.format(archive_file_name[:8], size // 1024 //1024, len(listofarch)))
        print('Start copy {}'.format(archive_file_name))
        try:
            shutil.copy(archive_file, copyto + os.sep + archive_file_name)
        except Exception as ex:
            logging.error(u'  Error copy {} to {} with exception {}'.format(archive_file, copyto, ex))
        else:
            logging.info(u'  Copy {} to {} success...'.format(archive_file, copyto))
    else:
        logging.critical(u'  Error on creating archive {} with exit code {} ...'.format(archive_file,exit_code))

logging.info(u'Total size of archives after this session is {} MB in {} files'.format(total_size // 1024 // 1024, total_numberoffiles))

create_html()
