import os

filename = '1cv82buh_2015'
base = 'D:\\Backup\\testbackup'
l = [ i for i in os.listdir(base) if i[:8] == filename[:8]]
size = 0
for name in l:
    size += os.path.getsize(base + os.sep + name)
print('Size of archives in {} named {} : {} MB'.format(base, filename[:8], size // 1024 //1024))
