# -*- coding: cp1251 -*-

import subprocess
import os, os.path
import shutil
import sys
import time
import logging

def create_html():
	''' ������� �������� html �� ���� ������� logging

	    ������ ���� ������� html �� ���� ������� logging � ��������
	    ��� � \\NAS\copy1c\logs\log1c.html
	'''
	with open('D:\\backup\\logs\\backup1c.log', 'r', encoding='cp1251') as log:
		l = log.readlines()
		l1 = l[-40:]
		del l
	with open('D:\\backup\\logs\\log.html', 'w', encoding='utf-8') as loghtml:
		loghtml.write(u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n')
		loghtml.write(u'<html>\n')
		loghtml.write(u'<head>\n')
		loghtml.write(u'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n')
		loghtml.write(u'<title>log</title>\n')
		loghtml.write(u'</head>\n')
		loghtml.write(u'<body>\n')
		loghtml.write(u'Created: <b>'+time.strftime('%d.%m.%Y %H:%M') + '</b><br>')
		loghtml.write(u'<code>\n')
		for s in l1:
			if '=======' in s:
				loghtml.write(u'<b>'+s+'</b><br>')
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

# ����� � ��� ����������� ������� �������������
logging.info(u'======= Archiving started in platform {} ======='.format(sys.platform))

# ��������� ���������� ���������� � ��������� ������
if len(sys.argv) != 2:
	sys.stderr.write('Usage: python {} cfgfile\n'.format(sys.argv[0]))
	logging.critical(u'Usage: python {} cfgfile\n'.format(sys.argv[0]))
	create_html()
	raise SystemExit(1)

# ��� ����. �����
name = sys.argv[1].strip()

# ��������� ������� ����������������� ����� 
if not os.path.isfile(name):
	sys.stderr.write('Error: {} not a file...'.format(name))
	logging.critical(u'{} not a file...'.format(name))
	create_html()
	raise SystemExit(2)

# � ���� ������ ��������� ������ ����� �� ������ � ��� ������
# ���������:
# lines[n][0] - ����� ������ � ����. ����� (� ������ ���������, �.�. ����� ���������� ������)
# lines[n][1] - ���� �� ��������� ������ (��� ����������)
# lines[n][2] - ���� �� �����, ��� ����� ������ ���� ������
# lines[n][3] - ��� ������. � ���� ����� ���������� ������ _��������������

lines=[]

# ������ ���������������� ����
with open(name, 'r') as cfg:
	strnum = 0
	for s in cfg:
		strnum += 1
		if '#' not in s:
			lines += [[str(strnum)] + s.strip().split(';')] 

# ��������� ������� ����� � lines 
if len(lines) == 0:
	sys.stderr.write('Error: file {} is empty...'.format(name))
	logging.critical(u'file {} is empty. Aborting without archieving...'.format(name))
	create_html()
	raise SystemExit(3)

# ��������� ���������� ����. �����
i = 0
while i < len(lines):
	if len(lines[i]) != 4:             # ���������� ����������
		sys.stderr.write('Error: {} - invalid number of parameters in string {}...'.format(name, lines[i][0]))
		logging.error(u'{} - invalid number of parameters in string {}...'.format(name, lines[i][0]))
		del lines[i]
		continue
	if len(lines[i][3]) == 0:          # ������� ����� ������
		sys.stderr.write('Error: {} - archive name missing in string {}...'.format(name, lines[i][0]))
		logging.error(u'{} - archive name missing in string {}...'.format(name, lines[i][0]))
		del lines[i]
		continue
	if not os.path.isdir(lines[i][1]): # ������������ ���� �� ���������
		sys.stderr.write('Error: in {} string {}: {} not a path...'.format(name, lines[i][0], lines[i][1]))
		logging.error(u'in {} string {}: {} not a path...'.format(name, lines[i][0], lines[i][1]))
		del lines[i]
		continue
	if not os.path.isdir(lines[i][2]): # ������������ ���� �� ���������
		sys.stderr.write('Error: in {} string {}: {} not a path...'.format(name, lines[i][0], lines[i][1]))
		logging.error(u'in {} string {}: {} not a path...'.format(name, lines[i][0], lines[i][1]))
		del lines[i]
	i += 1

# ��������� ������� ����� � lines ����� �������� �� ������������
if len(lines) == 0:
	sys.stderr.write('Error: file {} is empty...'.format(name))
	logging.critical(u'file {} is empty after testing. Aborting without archieving...'.format(name))
	create_html()
	raise SystemExit(3)

# ���������� �������������
archivator = 'C:\\Program Files\\7-Zip\\7z.exe'
copyto = '\\\\NAS\\copy1c\\py_backup'
for s in lines:
    archive_file_name = s[3] + '_' + time.strftime('%Y%m%d%H%M%S') + '.zip'
    archive_file = s[2] + os.sep + archive_file_name 
    source_files = s[1] 
    zip_command = '"' + archivator + archive_file + source_files + '"'
    logging.info(u'+++ Start creating archive {}'.format(source_files))
    exit_code = subprocess.call([archivator, 'a', '-tzip', archive_file, '-mx5', source_files, '-ssw'])
    if exit_code == 0:
        logging.info(u'  Archive {} creating success...'.format(archive_file))
        logging.info(u'  Starting copy {} to {}'.format(archive_file_name, copyto))
        try:
            shutil.copy(archive_file, copyto + os.sep + archive_file_name)
        except Exception as ex:
            logging.error(u'  Error copy {} to {} with exeption {}'.format(archive_file, copyto, ex))
        else:
            logging.info(u'  Copy {} to {} success...'.format(archive_file, copyto))
    else:
        logging.critical(u'  Error on creating archive {} with exit code {} ...'.format(archive_file,exit_code))

create_html()
