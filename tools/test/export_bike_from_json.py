import json
import os
from collections import OrderedDict

dir_src = "data/train"
json_src = "data/annotation_merge_vis_coco_nexys_filtered.json"
json_dist = "data/only_bike_person.json"

json_f = open(json_src, 'r', encoding='utf-8')
ann_info = json.load(json_f, object_pairs_hook=OrderedDict)
json_f.close()

tmp_ann_info = list()
for info in ann_info:
    filename = info["filename"]
    dirname = os.path.dirname(filename)

    if dirname == "crawl":
        # "__background", "승용차", "SUV", "승합차", "트럭", "특수차", "번호판", "사람"
        ann = info["ann"]
        bboxes = ann['bboxes']
        labels = ann['labels']

        is_diff_obj = False
        tmp_bboxes = list()
        tmp_labels = list()
        for bbox, label in zip(bboxes, labels):
            if label == 6:
                tmp_labels.append(8)
                tmp_bboxes.append(bbox)
            elif label == 1:
                tmp_labels.append(7)
                tmp_bboxes.append(bbox)
            else:
                is_diff_obj = True
                break

        if is_diff_obj:
            continue

        ann['bboxes'] = tmp_bboxes
        ann['labels'] = tmp_labels

        tmp_ann_info.append(info)

with open(json_dist, 'w', encoding='utf-8') as json_file:
    json.dump(tmp_ann_info, json_file, ensure_ascii=False, indent='\t')
