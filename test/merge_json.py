import json
import os

from collections import OrderedDict

target_dir = "0310_car"
out_path = "0310_car/car_train_last.json"
#
# target_dir = "data/drone"
# out_path = "data/drone/merge_add_drone.json"


def load_json(file_path, ann_info):
    f = open(file_path, 'r', encoding='utf-8')
    anns = json.load(f, object_pairs_hook=OrderedDict)
    print(len(anns))
    if "crawl_ann.json" in file_path:
        anns = anns*2
        print(len(anns))

    ann_info.extend(anns)
    f.close()


json_list = ["car_train.json", "merge_add_drone.json"]
# json_list = os.listdir(target_dir)

ann_info = list()
for filename in json_list:
    if ".json" in filename:
        file_path = os.path.join(target_dir, filename)
        load_json(file_path, ann_info)


with open(out_path, 'w', encoding='utf-8') as json_file:
    json.dump(ann_info, json_file, ensure_ascii=False, indent='\t')

print("total:", len(ann_info))
