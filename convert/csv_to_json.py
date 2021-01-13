import json
import csv


src = "t1_gt.json"
dist = "temp_t1_gt.csv"

fw = open(dist, 'w', encoding='utf-8', newline='')
csv_wr = csv.writer(fw)
with open(src, 'r') as f:
    # json_f = json.dump(f)
    json_f = json.load(f)

    track1_GT = json_f["track1_GT"]

    for gt_info in track1_GT:
        p, ext, hydrant, car, bicycle, bike = gt_info['objects']

        csv_wr.writerow(["", p, "", ext, "", hydrant, "", car, "", bicycle, "", bike])

fw.close()
