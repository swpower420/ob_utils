import json
import os



src_dir = "data/ocr/final_test/song2"
dest_path = "ocr/final_test/song2_carinfo.csv"

car_info_list = []

for dirName, subdirList, fileList in os.walk(src_dir):
    subdirList.sort()
    fileList.sort()
    for filename in fileList:
        if '.txt' in filename:
            json_path = os.path.join(dirName, filename)
            with open(json_path)  as f:
                json_data = json.load(f)

            if json_data['event'] != "car_info":
                continue

            car_type = json_data['car_type']
            plate_number = json_data['plate_number']
            time = json_data['time']

            print(time, car_type, plate_number)
            car_info_list.append([time, car_type, plate_number])


import csv
f = open(dest_path, 'w', encoding='utf-8')
wr = csv.writer(f)

for car_info in car_info_list:
    wr.writerow(car_info)

f.close()