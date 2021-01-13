import cv2
import os
import json
import numpy as np
from collections import OrderedDict

root_path = "data/crawl"
json_path = "data/crawl/merge_add_crawl.json"
result_json_path = "data/crawl/merge_add_crawl_re.json"

f = open(json_path, 'r', encoding='utf-8')
ann_list = json.load(f, object_pairs_hook=OrderedDict)
f.close()

for ann_info in ann_list:
    filename = ann_info["filename"]

    file_path = os.path.join(root_path, filename)

    img = cv2.imread(file_path)
    zeros = np.zeros(img.shape, dtype=np.uint8)

    h,w = img.shape[:2]

    r_h = h // 2
    r_w = w // 2

    re_img = cv2.resize(img, (r_w, r_h))

    start_y = r_h//2
    start_x = r_w//2
    zeros[start_y:start_y+r_h,start_x:start_x+r_w] = re_img

    ann = ann_info["ann"]
    bboxes = ann["bboxes"]

    tmp_bboxes = list()
    for bbox in bboxes:
        x1,y1,x2,y2 = bbox
        rx1 = x1//2+start_x
        ry1 = y1//2+start_y
        rx2 = x2//2+start_x
        ry2 = y2//2+start_y

        tmp_bboxes.append([rx1,ry1,rx2,ry2])

    ann["bboxes"] = tmp_bboxes
    rename = filename.split(".")[0] + "_re.jpg"

    ann_info["filename"] = rename

    result_path = os.path.join(root_path, rename)
    cv2.imwrite(result_path, zeros)

with open(result_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(ann_list, json_file, ensure_ascii=False, indent='\t')

