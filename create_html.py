#!/usr/bin/env python3

import shutil

#with open('D:\\backup\\logs\\backup1c.log', 'r', encoding='cp1251') as log:
with open('/media/hpserver_d/Backup/logs/backup1c.log', 'r', encoding='cp1251') as log:
    l = log.readlines()
l1 = l[-40:]
del l

#with open('D:\\backup\\logs\\log.html', 'w', encoding='cp1251') as loghtml:
with open('/media/hpserver_d/Backup/logs/log.html', 'w') as loghtml:
    loghtml.write(u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n')
    loghtml.write(u'<html>\n')
    loghtml.write(u'<head>\n')
    loghtml.write(u'<meta http-equiv="content-type" content="text/html; charset=utf-8">\n')
    loghtml.write(u'<title>log</title>\n')
    loghtml.write(u'</head>\n')
    loghtml.write(u'<body>\n')
    loghtml.write(u'<code>\n')
    for s in l1:
        if s.startswith('ERROR'):
            loghtml.write(u'<font color="red">'+ s + u'</font><br>\n')
        elif s.startswith('CRITICAL'):
            loghtml.write(u'<font color="red"><b>'+ s + u'</b></font><br>\n')
        else:
            loghtml.write(u'<font color="green">'+ s + u'</font><br>\n')
    loghtml.write(u'</code>\n')
    loghtml.write(u'</body>\n')
    loghtml.write(u'</head>\n')


