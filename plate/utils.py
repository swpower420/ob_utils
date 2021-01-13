import os
import cv2
import math
import numpy as np


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        return None


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        return False


def ratio_resize(img, new_w=-1, new_h=-1):
    h, w = img.shape[:2]
    if new_w == -1:
        # 2005년 white 판때기만 일단은 처리한다 세로 220px 기준
        new_w = new_h*w//h
    elif new_h == -1:
        new_h = new_w*h//w

    resize_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    return resize_img


def merge_bounding_box(a, b):
    x1, y1, x2, y2 = a
    x3, y3, x4, y4 = b

    left = x1
    top = y1
    right = x2
    bottom = y3

    if x2 < left: left = x2
    if x3 < left: left = x3
    if x4 < left: left = x4

    if x1 > right: right = x1
    if x3 > right: right = x3
    if x4 > right: right = x4

    if y2 < top: top = y2
    if y3 < top: top = y3
    if y4 < top: top = y4

    if y1 > bottom: bottom = y1
    if y2 > bottom: bottom = y2
    if y4 > bottom: bottom = y4

    return [left, top, right, bottom]


def get_bbox(img, ori_bbox_list, plate_bg_name, font_type, one_label_index, is_merge=False, plus_pad=0, is_only_city_str=False):
    _, year, plate_size, plate_type = plate_bg_name.split("_")

    if isinstance(font_type, list):
        font_type, choice_num_type = font_type

    is_long = 0
    if year == "2003" or year == "2006":
        is_long = 1
    elif year == "2005":
        if "white" in plate_type:
            is_long = 0
        else:
            is_long = 1

        if plate_size == "520" and "yellow" in plate_type:
            is_merge = True
            is_long = 0

    elif year == "2004":
        is_long = 0

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(img, 100, 200)
    _, contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # {0:[[],[]], 1:[[][]]}
    check_two_bbox_dict = dict()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)  # cnt

        for index, bbox in enumerate(ori_bbox_list):
            if bbox[0] < x and bbox[1] < y and bbox[2] > x + w and bbox[3] > y + h:
                if index not in check_two_bbox_dict:
                    check_two_bbox_dict[index] = [[x, y, x + w, y + h]]
                else:
                    check_two_bbox_dict[index].append([x, y, x + w, y + h])

    # [(index, bbox)]
    piece_bbox = list()
    plus_index = 0
    for i, bbox_list in check_two_bbox_dict.items():
        if is_merge:
            if len(bbox_list) == 1:
                if i+is_long in one_label_index:
                    x1, y1, x2, y2 = bbox_list[0]
                    w = (x2-x1)+1
                    # h = y2-y1+1

                    if font_type == "old":
                        if year == "2006":
                            if choice_num_type == "bold":
                                x1 = x1 - int(w * 0.9)
                                x2 = x2 + int(w * 1.0)
                            else:
                                x1 = x1 - int(w * 0.25)
                                x2 = x2 + int(w * 0.5)
                        else:
                            x1 = x1 - int(w * 1.7)
                            x2 = x2 + int(w * 1.7)
                    else:
                        x1 = x1 - int(w*0.25)
                        x2 = x2 + int(w*0.5)

                    bbox_list[0] = [x1, y1, x2, y2]

                piece_bbox.append((i, bbox_list[0]))

                # x1, y1, x2, y2 = bbox_list[0]
                # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            else:
                merge_bbox = merge_bounding_box(bbox_list[0], bbox_list[1])
                for index in range(2, len(bbox_list)):
                    merge_bbox = merge_bounding_box(merge_bbox, bbox_list[index])
                piece_bbox.append((i, merge_bbox))

                # x1, y1, x2, y2 = merge_bbox
                # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
        else:
            if len(bbox_list) == 1:
                if i+is_long in one_label_index:
                    x1, y1, x2, y2 = bbox_list[0]
                    w = (x2-x1)+1
                    # h = y2-y1+1

                    if font_type == "old":
                        if year == "2006":
                            if choice_num_type == "bold":
                                x1 = x1 - int(w * 0.9)
                                x2 = x2 + int(w * 1.0)
                            else:
                                x1 = x1 - int(w * 0.25)
                                x2 = x2 + int(w * 0.5)
                        else:
                            x1 = x1 - int(w * 1.7)
                            x2 = x2 + int(w * 1.7)
                    else:
                        x1 = x1 - int(w*0.25)
                        x2 = x2 + int(w*0.5)

                    # if font_type == "old":
                    #     if year == "2006":
                    #         if choice_num_type == "bold":
                    #             x1 = x1 - int(w * 1)
                    #             x2 = x2 + int(w * 1.1)
                    #         else:
                    #             x1 = x1 - int(w * 1 / 3)
                    #             x2 = x2 + int(w * 0.6)
                    #     else:
                    #         x1 = x1 - int(w * 1.8)
                    #         x2 = x2 + int(w * 1.8)
                    # else:
                    #     x1 = x1 - int(w*1/3)
                    #     x2 = x2 + int(w*0.6)

                    bbox_list[0] = [x1, y1, x2, y2]

                piece_bbox.append((i+plus_index, bbox_list[0]))

                # x1, y1, x2, y2 = bbox_list[0]
                # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            else:
                if i == 0 or is_only_city_str:
                    merge_bbox = merge_bounding_box(bbox_list[0], bbox_list[1])
                    for index in range(2, len(bbox_list)):
                        merge_bbox = merge_bounding_box(merge_bbox, bbox_list[index])

                    x1, y1, x2, y2 = merge_bbox

                    if year == "2003":
                        new_x = (x2+x1)//2 - 1
                    else:
                        new_x = (x2+x1)//2

                    def _get_city_bbox(crop_img, is_first=True):
                        h, w = img.shape[:2]
                        bg = np.ones((h, w), dtype=np.uint8) * 255
                        if is_first:
                            bg[y1:y2, x1:new_x] = crop_img
                        else:
                            bg[y1:y2, new_x:x2] = crop_img

                        _, contours, _ = cv2.findContours(cv2.Canny(bg, 100, 200),
                                                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        bbox_list = list()
                        for cnt in contours:
                            x, y, w, h = cv2.boundingRect(cnt)
                            bbox_list.append([x, y, x + w, y + h])

                        if len(bbox_list) > 1:
                            merge_bbox = merge_bounding_box(bbox_list[0], bbox_list[1])
                            for index in range(2, len(bbox_list)):
                                merge_bbox = merge_bounding_box(merge_bbox, bbox_list[index])
                        else:
                            merge_bbox = bbox_list[0]

                        return merge_bbox

                    city_first_bbox = _get_city_bbox(img[y1:y2,x1:new_x])
                    city_second_bbox = _get_city_bbox(img[y1:y2,new_x:x2], False)

                    piece_bbox.append((i + plus_index, city_first_bbox))
                    plus_index += 1
                    piece_bbox.append((i + plus_index, city_second_bbox))

                    # x1, y1, x2, y2 = city_first_bbox
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    # x1, y1, x2, y2 = city_second_bbox
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

                else:
                    merge_bbox = merge_bounding_box(bbox_list[0], bbox_list[1])
                    for index in range(2, len(bbox_list)):
                        merge_bbox = merge_bounding_box(merge_bbox, bbox_list[index])
                    piece_bbox.append((i, merge_bbox))

                    # x1, y1, x2, y2 = merge_bbox
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

    # cv2.imshow("test", img)
    # cv2.waitKey()
    sorted_bbox = list()
    for box_info in  sorted(piece_bbox, key=lambda k:k[0]):
        sorted_bbox.append(box_info[1])

    # print(sorted_bbox)
    return sorted_bbox


def BGRA2BGR(img, is_convert=True):
    h, w = img.shape[:2]

    if is_convert:
        result = np.ones((h, w, 3)) * 255
        img[:, :, :3] = 255 - img[:, :, :3]
    else:
        result = np.zeros((h, w, 3))

    alpha = img[:, :, 3] / 255.0

    result[:, :, 0] = (1. - alpha) * result[:, :, 0] + alpha * img[:, :, 0]
    result[:, :, 1] = (1. - alpha) * result[:, :, 1] + alpha * img[:, :, 1]
    result[:, :, 2] = (1. - alpha) * result[:, :, 2] + alpha * img[:, :, 2]

    result = result.astype(np.uint8)

    return result


# 600 : 462
# 520 : 400
# 335 : 260
def ratio_resize_img_and_bbox(img, img_info, new_w=-1, new_h=-1):
    h, w = img.shape[:2]
    if new_w == -1:
        # 2005년 white 판때기만 일단은 처리한다 세로 220px 기준
        new_w = new_h*w//h
    elif new_h == -1:
        new_h = new_w*h//w

    # resize_img = cv2.resize(img, (w//2, h//2), interpolation=cv2.INTER_CUBIC)
    resize_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    img_info["width"] = new_w
    img_info["height"] = new_h
    ann = img_info["ann"]

    bboxes = list()
    for bbox in ann["bboxes"]:
        _bbox = np.array(bbox)
        _bbox = (new_w * _bbox) / w
        # size가 너무 큰 이미지를 아주 작게 resize 하면 pixel 이 2씩 밀린다.(이유 모름)
        _bbox =  np.round(_bbox) - 2
        _bbox = _bbox.astype(np.int32)
        bboxes.append(_bbox.tolist())
    ann["bboxes"] = bboxes

    return resize_img


def change_class_num(piece_name_list):
    labels = list()
    for label in piece_name_list:
        labels.append(CLASSES[label])

    return labels


def get_key_by_value(index):
    return list(CLASSES.keys())[list(CLASSES.values()).index(index)]