import os


def delfiles(pathtofiles, pathtonas, namearc, threshold):
    # получаем список файлов
    d = os.listdir(pathtofiles)
    d.sort()
    # фильтруем имена архивов, которые хотим удалить
    dn = [i for i in d if i.startswith(namearc)]
    # если кол-во файлов в каталоге больше барьера, удаляем 5 старых файлов
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
                    print(r'Ошибка удаления {}'.format(i))
                else:
                    print(r'Файл {} успешно удален.'.format(i))
            else:
                print('Не найден на NAS: {}'.format(pathtonas + os.sep + i))

delfiles('/media/hpserver_d/Backup/test1c', '/media/windowsshare/copy1c/py_backup', '1cv77buh', 10)
# delfiles('/media/hpserver_d/Backup/test1c', '1cv82ahd', 10)
