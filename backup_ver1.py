#!/usr/bin/env python3

import os
import time

# Что архивируем
source = '/media/base1c77onNAS/Base1c_77/'

# Куда архивируем
target_dir = '/media/maxtor/backup/1c'

target = target_dir + os.sep + 'base1c77_'+time.strftime('%Y%m%d%H%M%S') + '.zip'

zip_command = "zip -qr {0} {1}".format(target, source)

#print(zip_command)
if os.system(zip_command) == 0:
	print('Резервная копия успешно создана в', target)
else:
	print('Создание резервной копии не удалось!')
