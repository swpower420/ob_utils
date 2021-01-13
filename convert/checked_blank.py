import os
import json
from collections import OrderedDict

json_path = "data/0310/train.json"
result_json_path = "data/etri/0310/train_new.json"

f = open(json_path, 'r', encoding='utf-8')
ann_list = json.load(f, object_pairs_hook=OrderedDict)
f.close()

tmp_list = list()
for ann_info in ann_list:
    filename = ann_info["filename"]
    ann = ann_info["ann"]
    bboxes = ann["bboxes"]

    if len(bboxes) == 0:
        print(filename, bboxes)
        continue

    tmp_list.append(ann_info)

with open(result_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(tmp_list, json_file, ensure_ascii=False, indent='\t')