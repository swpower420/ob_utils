import os
import json
import cv2
import numpy as np

from lxml import etree as ET
from collections import OrderedDict


CATEGORIES = [
        "__background", "1", "2", "3", "4", "5"
    ]


if __name__ == '__main__':
    root_path = "data/drone"

    src_dir = "test-11"
    dist_dir = "add_drone"
    xml_path = os.path.join(root_path, f"{src_dir}.xml")
    json_path = os.path.join(root_path, f"{src_dir}.json")

    src_path = os.path.join(root_path, src_dir)
    dist_path = os.path.join(root_path, dist_dir)
    if not os.path.isdir(dist_path):
        os.mkdir(dist_path)

    tree = ET.parse(xml_path)

    # get root
    root = tree.getroot()

    json_list = list()
    for elem in root:
        if elem.tag != 'image':
            continue  # read only image

        img_name = elem.get("name")
        img = cv2.imread(os.path.join(src_path, img_name))

        tmp_dict = OrderedDict()
        tmp_dict['filename'] = os.path.join(dist_dir, img_name)
        tmp_dict['width'] = elem.get('width')
        tmp_dict['height'] = elem.get('height')
        ann_info = tmp_dict['ann'] = OrderedDict()

        tmp_bboxes = list()
        tmp_labels = list()
        for sub_elem in elem:
            if sub_elem.tag == "box":
                label_index = CATEGORIES.index(sub_elem.get("label"))

                # xtl="0.00" ytl="112.00" xbr="1917.00" ybr=
                x1 = int(float(sub_elem.get("xtl")))
                y1 = int(float(sub_elem.get("ytl")))
                x2 = int(float(sub_elem.get("xbr")))
                y2 = int(float(sub_elem.get("ybr")))

                tmp_bboxes.append([x1,y1,x2,y2])
                tmp_labels.append(label_index)
            elif sub_elem.tag == "polygon":
                points = sub_elem.get("points").split(";")

                tmp_points = list()
                for point in points:
                    x, y = point.split(",")
                    tmp_points.append([float(x), float(y)])

                pts = np.array([tmp_points], dtype=np.int32)
                cv2.fillPoly(img, pts, 0)

        ann_info['bboxes'] = tmp_bboxes
        ann_info['labels'] = tmp_labels
        ann_info['bboxes_ignore'] = []
        ann_info['labels_ignore'] = []

        json_list.append(tmp_dict)

        cv2.imwrite(os.path.join(dist_path, img_name), img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_list, json_file, ensure_ascii=False, indent='\t')