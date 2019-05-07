import os
import shutil
import sys
import time

# 想备份的文件扩展名后四位
file_ext = ['.jpg']  

def time_to_str(time_strap):
    return time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(int(time_strap)))


folder_path = input("请输入需要查找的路径\n")

if not os.path.exists(folder_path):
    print("该目录不存在，请确认！")
    sys.exit()

target_folder_path = input('请输入保存的文件夹路径\n')
if not target_folder_path:
    print("请输入文件保存的路径")
    sys.exit()

befor_time = input('请输入备份文件开始时间\n')
befor_time_number = ''

if befor_time != '':
    timeArray = time.strptime(befor_time, "%Y-%m-%d %H:%M:%S")
    befor_time_number = int(time.mktime(timeArray))

dirs = os.walk(folder_path)

file_count = 1

for root, folder, files in dirs:

    for file in files:
        full_path = os.path.join(root, file)
        tmp_ext = full_path[-4:]

        if tmp_ext in file_ext:
            file_stat = os.stat(full_path)
            file_mktime =int(file_stat.st_mtime)
            if befor_time_number != '' and file_mktime < befor_time_number:
                continue
            else:

                mktime = time_to_str(file_stat.st_mtime)

                newfile_name = mktime + '-' + str(file_count)
                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)

                shutil.copy2(full_path, target_folder_path + '/' + newfile_name + tmp_ext)
                print("复制", file_count, "个成功,文件", os.path.basename(full_path),mktime)
                file_count += 1

                fo = open(os.path.join('log.txt'), 'a+')
                fo.write(full_path + '\n')

                fo.close()

if __name__ == "__main__":
    pass
 
