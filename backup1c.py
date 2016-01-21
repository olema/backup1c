# backup1c.py
# -*- coding: cp1251 -*-
# ������ ���������� ���� � ���������� 1�, �������� �� �� NAS �
# �������, ��� ���������� ���������� ���-��, ����� ������� �� ��������� �������
# ������� ServerHP

import subprocess
import os
import shutil
import sys
import time
import logging
import logging.handlers

# ���� �� log-�����
logfile = u'D:\\backup\\logs\\backup1c.log'

# html-log
loghtmlf = 'D:\\backup\\logs\\log.html'

# ������ �����������
# logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
#                    level=logging.DEBUG,
#                    filename=logfile)

dateformat = '%Y-%m-%d %H:%M:%S'
fileformat = '%(levelname)-8s [%(asctime)s] %(message)s'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024*1024, backupCount=10)
handler.setFormatter(logging.Formatter(fileformat, dateformat))
logger.addHandler(handler)

# ���� �� ����������
archivator = 'C:\\Program Files\\7-Zip\\7z.exe'

# ���� �� ������� �� NAS
copyto = '\\\\NAS\\copy1c\\py_backup'

# ���������� ������ ������� ������, ������� ������ �� ServerHP.
# ���� ������, �� ������� 5 ������ �������
threshold = 9

# � ���� ������ ��������� ������ ����� �� ������ � ��� ������
# ���������:
# lines[n][0] - ����� ������ � ����. ����� (� ������ ���������, �.�.
# ����� ���������� ������)
# lines[n][1] - ���� �� ��������� ������ (��� ����������)
# lines[n][2] - ���� �� �����, ��� ����� ������ ���� ������
# lines[n][3] - ��� ������. � ���� ����� ���������� ������ _��������������
# '''
lines = [
    ['1', 'D:\\1C_Base\\v8.2\\����������� ���������������� �����������',
     'D:\\backup\\1C', '1cv82buh'],
    ['2', 'D:\\1C_Base\\V7.7\\Base1c_77', 'D:\\backup\\1C', '1cv77buh'],
    ['3', 'D:\\1C_Base\\v8.2\\ZiK 2015', 'D:\\backup\\1C', '1cv82zik'],
    ['4', 'D:\\1C_Base\\v8.2\\Omega', 'D:\\backup\\1C', '1cv82ahd']
]
# '''

# lines = [['1','D:\\���� �����', 'D:\\backup\\testbackup','pysource'],
#        ['2','D:\\Backup\\logs', 'D:\\backup\\testbackup', 'logs']
#        ]


# ������� �������� ���� � ������� html
# ������� �������� html �� ���� ������� logging
# ������ ���� ������� html �� ���� ������� logging � ��������
#    ��� � \\NAS\copy1c\logs\log1c.html
def create_html(logfile, loghtmlf):
    with open(logfile, 'r', encoding='cp1251') as log:
        l = log.readlines()[-60:]
    with open(loghtmlf, 'w', encoding='utf-8') as loghtml:
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
        shutil.copy(loghtmlf, r'\\NAS\copy1c\logs\log1c.html')
    except OSError as ex:
        logger.error(u'Copy log1c.html error with exception: {}'.format(ex))
    else:
        logger.info(u'Copy log1c.html success...')

# ����� � ��� ����������� ������� �������������
logger.info(u'======= Archiving started on platform {}\
             ======='.format(sys.platform))

# ��������� ���������� lines[]
# � ������ ���� ������ �� ������ ��������, ��� ��������� �� ������
i = 0
while i < len(lines):
    if len(lines[i]) != 4:  # ���������� ����������
        sys.stderr.write('Error: - invalid number of parameters in string {}...'.format(lines[i][0]))
        logger.error(u'- invalid number of parameters in string {}...'.format(lines[i][0]))
        del lines[i]
        continue
    if len(lines[i][3]) == 0:  # ������� ����� ������
        sys.stderr.write('Error: - archive name missing in string {}...'.format(lines[i][0]))
        logger.error(u'- archive name missing in string {}...'.format(lines[i][0]))
        del lines[i]
        continue
    if not os.path.isdir(lines[i][1]):  # ������������ ���� �� ���������
        sys.stderr.write('Error: in string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        logger.error(u' - string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        del lines[i]
        continue
    if not os.path.isdir(lines[i][2]):  # ������������ ���� �� ���������
        sys.stderr.write('Error: in string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        logger.error(u' - string {}: {} not a path...'.format(lines[i][0], lines[i][1]))
        del lines[i]
    i += 1

# ��������� ������� ����� � lines ����� �������� �� ������������
if len(lines) == 0:
    logger.critical(u'List is empty after testing. Aborting without archieving...')
    create_html()
    raise SystemExit(3)

# ���������� �������������
total_size = 0
total_numberoffiles = 0
for s in lines:
    archive_file_name = s[3] + '_' + time.strftime('%Y%m%d%H%M%S') + '.zip'
    archive_file = s[2] + os.sep + archive_file_name
    source_files = s[1]
    zip_command = '"' + archivator + archive_file + source_files + '"'
    logger.info(u'+++ Start creating archive {} to folder {}'.format(source_files, s[2]))
    print('Start archive {}'.format(source_files))
    exit_code = subprocess.call([archivator, 'a', '-tzip', archive_file, '-mx5', source_files, '-ssw'])
    if exit_code == 0:
        logger.info(u'Archive {} creating success...'.format(archive_file))
        listofarch = [i for i in os.listdir(s[2]) if i[:8] == archive_file_name[:8]]
        size = 0
        for name in listofarch:
            size += os.path.getsize(s[2] + os.sep + name)
        total_size += size
        total_numberoffiles += len(listofarch)
        logger.info(u'Size of archives named {} is {} MB in {} files'.format(archive_file_name[:8], size // 1024 // 1024, len(listofarch)))
        print('Start copy {}'.format(archive_file_name))
        try:
            shutil.copy(archive_file, copyto + os.sep + archive_file_name)
        except OSError as ex:
            logger.error(u'  Error copy {} to {} with exception {}'.format(archive_file, copyto, ex))
        else:
            logger.info(u'  Copy {} to {} success...'.format(archive_file, copyto))
    else:
        logger.critical(u'  Error on creating archive {} with exit code {} ...'.format(archive_file, exit_code))

logger.info(u'Total size of archives after this session is {} MB in {} files'.format(total_size // 1024 // 1024, total_numberoffiles))

# �������� ������ ������� � ����� � �������� �� ����� �������
# - pathtofiles - ���� �� �����, ��� ����� ������ �� ServerHP
# - pathtonas - ���� �� ����� � �������� �� NAS
# - namearc - ������ 8 �������� ����� ������, ������� ���� �������
# - threshold - ����� �������, ����� ���������� �������� ���� ������� 5 ������
# def delfiles(pathtofiles, pathtonas, namearc, threshold):
for i in lines:
    pathtofiles = i[2]
    pathtonas = copyto
    namearc = i[3]
    # �������� ������ ������
    d = os.listdir(pathtofiles)
    d.sort()
    # ��������� ����� �������, ������� ����� �������
    dn = [i for i in d if i.startswith(namearc)]
    # ���� ���-�� ������ � �������� ������ ���������� � threshold, ������� 5
    # ������ ������, �������������� �������� �� �� ������� �� NAS
    if len(dn) > threshold:
        filesfordel = dn[:5]
        for i in filesfordel:
            # ��������� ������� ����� �� NAS
            if os.path.isfile(pathtonas + os.sep + i):
                # ������� ���� � ���������� � �������� �� ��������� �������
                # ServerHP
                try:
                    os.remove(pathtofiles + os.sep + i)
                except OSError:
                    logger.error(u'Error deleting {}'.format(pathtofiles + os.sep + i))
                else:
                    logger.info(u'{} deleting success'.format(pathtofiles + os.sep + i))
            else:
                logger.error(u'Not find on NAS: {}'.format(pathtonas + os.sep + i))

create_html(logfile, loghtmlf)
