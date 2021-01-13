import os
import csv
import json
import re

from collections import OrderedDict

csv_src = "data/ocr/bbox_info.csv"
json_dist = "data/ocr/annotation.json"

csv_src = "data/ocr/bbox_info.csv"
json_dist = "data/ocr/annotation.json"

CLASS = {"1": 1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "0":10, "city":11, "sub":12}
city_list = ['서울','경기','대구','경북','경남','전북','전남','대전',
             '충북','충남','부산','강원','울산','인천','광주','제주','제주']

hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')


file_info = dict()
with open(csv_src, 'r', encoding='utf-8') as f:
    csf = csv.reader(f, delimiter=',')

    dir_basename = os.path.basename(os.path.split(csv_src)[0])

    # ['path', 'filename', 'image_width', 'image_height', 'x1', 'y1', 'x2', 'y2', 'target']
    for i, row in enumerate(csf):
        if i == 0:
            continue

        target = row[8]

        if target in city_list:
            target = "city"
        elif len(target) == 1:
            try:
                int(target)
            except:
                target = "sub"
        else:
            print(filename, target)
            exit()

        # target = hangul.sub('', target)

        path = row[0]
        filename = row[1]
        filename = os.path.join(path, filename)
        width = int(row[2])
        height = int(row[3])
        x1 = int(row[4])
        y1 = int(row[5])
        x2 = int(row[6])
        y2 = int(row[7])

        if filename not in file_info:
            info = file_info[filename] = dict()
            info['width'] = width
            info['height'] = height
            info['labels'] = [CLASS[target]]
            info['bboxes'] = [[x1, y1, x2, y2]]
        else:
            info = file_info[filename]
            info['labels'].append(CLASS[target])
            info['bboxes'].append([x1,y1,x2,y2])

ann_info_list = list()
for filename, info in file_info.items():
    temp_info = OrderedDict()
    temp_info['filename'] = filename
    temp_info['width'] = info['width']
    temp_info['height'] = info['height']
    ann_info = temp_info['ann'] = OrderedDict()

    ann_info['bboxes'] = info['bboxes']
    ann_info['labels'] = info['labels']
    ann_info['bboxes_ignore'] = []
    ann_info['labels_ignore'] = []

    ann_info_list.append(temp_info)

# json format
with open(json_dist, 'w', encoding='utf-8') as json_file:
    json.dump(ann_info_list, json_file, ensure_ascii=False, indent='\t')
