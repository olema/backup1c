import os


def delfiles(pathtofiles, pathtonas, namearc, threshold):
    # �������� ������ ������
    d = os.listdir(pathtofiles)
    d.sort()
    # ��������� ����� �������, ������� ����� �������
    dn = [i for i in d if i.startswith(namearc)]
    # ���� ���-�� ������ � �������� ������ �������, ������� 5 ������ ������
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
                    print(r'������ �������� {}'.format(i))
                else:
                    print(r'���� {} ������� ������.'.format(i))
            else:
                print('�� ������ �� NAS: {}'.format(pathtonas + os.sep + i))

delfiles('/media/hpserver_d/Backup/test1c', '/media/windowsshare/copy1c/py_backup', '1cv77buh', 10)
# delfiles('/media/hpserver_d/Backup/test1c', '1cv82ahd', 10)
