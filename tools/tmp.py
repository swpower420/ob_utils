import os
import csv


root_path = "data/hospital"

# csv_f = open(os.path.join(root_path, "val.csv"), 'w', encoding='utf-8')
# writer = csv.writer(csv_f, delimiter=' ', quotechar="'", quoting=csv.QUOTE_MINIMAL)
# writer.writerow(['original_vido_id', 'video_id', 'frame_id', 'path', 'labels'])
#
# video_id = 0
# for dirName, subdirList, fileList in os.walk(os.path.join(root_path, "frames")):
#     file_len = len(fileList)
#     for i, filename in enumerate(sorted(fileList)):
#         _, ext = os.path.splitext(filename)
#         if ext.lower() in [".jpg", ".png", "jpeg"]:
#             video_name = os.path.basename(dirName)
#
#             writer.writerow([video_name, video_id, i, os.path.join(video_name, filename), '""'])
#
#         if i+1 == file_len:
#             video_id += 1


test = "ava/ava_annotations/person_box_67091280_iou90/ava_detection_val_boxes_and_labels.csv"
# test = "/home/bong20/data/convalescent_hospital/val.csv"
csv_f = open(test, 'r', encoding='utf-8')
# csv_f.readline()
# for ttt in csv_f:
#     print(ttt)
#     row = ttt.split()
#     print(row)
#     exit()
#     # The format of each row should follow:
#     # original_vido_id video_id frame_id path labels.
#     assert len(row) == 5
#     # print(line)
#
r = csv.reader(csv_f)
for i, line in enumerate(r):
    if i > 10:
        break
    print(line)
