import os
import json
import numpy as np

from collections import OrderedDict


json_src = "1_video_1024\\annotation.json"
json_dist = "1_video_1024\\annotation_1920.json"

json_f = open(json_src, 'r', encoding='utf-8')
ann_info = json.load(json_f, object_pairs_hook=OrderedDict)
json_f.close()

for annotation in ann_info:
    filename = annotation["filename"]
    width = annotation["width"]
    height = annotation["height"]

    if "DSC" in filename:
        continue

    if width == 1024:
        annotation["width"] = 1920
        annotation["height"] = 1080
        ann = annotation["ann"]

        bboxes = list()
        for bbox in ann["bboxes"]:
            _bbox = np.array(bbox)
            _bbox = (1920 * _bbox) / width
            _bbox = _bbox.astype(np.int32)
            bboxes.append(_bbox.tolist())
        ann["bboxes"] = bboxes

with open(json_dist, 'w', encoding='utf-8') as json_file:
    json.dump(ann_info, json_file, ensure_ascii=False, indent='\t')