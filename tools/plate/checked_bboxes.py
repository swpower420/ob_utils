import cv2
import os
import json
import unicodedata

import numpy as np

img_src = "C:\\Users\\Desktop\\google크롤링"
json_src = "C:\\Users\\Desktop\\google크롤링\\num_annotation.json"
# except_data = ["t1_video_00030", "t1_video_00031", "t1_video_00032", "t1_video_00033", "t1_video_00034"]
except_data = ["t1_video_00051_baek"]

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        return None

with open(json_src, 'r') as json_file:
    json_data = json.load(json_file)

    for file_info in json_data:
        filename = file_info['filename']
        filename = filename.split("/")[-1]
        ann = file_info['ann']

        # dir_name = filename[:-10]
        #
        # if dir_name not in except_data:
        #     continue
        #
        # img_dir_path = os.path.join(img_src, dir_name)
        #
        # img = cv2.imread(os.path.join(img_dir_path, filename))

        if "t1_video" in filename:
            continue

        # img = cv2.imread(os.path.join(img_src, "t1_video_00051_baek_1024", filename))
        img_path = unicodedata.normalize('NFC', os.path.join(img_src, filename))
        img = imread(img_path)
        print(img.shape)

        bboxes = ann["bboxes"]
        labels = ann["labels"]

        for i, bbox in enumerate(bboxes):
            x1, y1, x2, y2 = bbox
            img = cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,0), 1)
            cv2.putText(img, str(labels[i]), (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)

        cv2.imshow('image', img)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
