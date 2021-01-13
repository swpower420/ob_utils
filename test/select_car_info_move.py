src_dir = "data/send_to_server_car_info"
dest_dir = "data/send_to_server_car_image"

import os
import json
from shutil import copyfile, move

if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

cnt = 0
for dirName, subdirList, fileList in os.walk(src_dir):
    subdirList.sort()
    fileList.sort()
    for filename in fileList:
        if '.jpg' in filename:
            cnt += 1
            src_path = os.path.join(src_dir, filename)
            dest_path = os.path.join(dest_dir, filename)
            move(src_path, dest_path)
            #
            # src_path = src_path.replace('.jpg', '.txt')
            # dest_path = dest_path.replace('.jpg', '.txt')
            # move(src_path, dest_path)

print(cnt)