import os
import cv2
import random
import json
import unicodedata
import numpy as np

from collections import OrderedDict
from tqdm import tqdm

import imgaug
from imgaug import augmenters as iaa


BOX_AUGMENTERS = ["Sequential", "SomeOf", "OneOf", "Sometimes",
                               "Fliplr", "Flipud", "CropAndPad",
                               "Affine", "PiecewiseAffine"]


def hook(keypoints, augmenter, parents, default):
    return augmenter.__class__.__name__ in BOX_AUGMENTERS

def random_affine(img, bboxes, coordinate):
    x1, y1, x2, y2 = coordinate

    w = x2-x1
    h = y2-y1

    srcTri = np.array([[x1, y1], [x2-1, y1],
                       [x1, y2-1], [x2-1, y2-1]]).astype(np.float32)

    trans_x1 = random.randint(x1, x1+int(w * 0.2))
    trans_y1 = random.randint(y1, y1+int(h * 0.2))

    trans_x2 = random.randint(x1+int(w*0.8), x2-1)
    trans_y2 = random.randint(y1, y1+int(h * 0.2))

    # trans_x3 = random.randint(start_x, start_x+int(w * 0.2))
    trans_x3 = random.randint(trans_x1 - int(trans_x1 * 0.05), trans_x1 + int(trans_x1 * 0.05))
    trans_y3 = random.randint(y1+int(h*0.8), y2-1)

    # trans_x4 = random.randint(start_x+int(w*0.8), end_x-1)
    trans_x4 = random.randint(trans_x2-int(trans_x2*0.05), trans_x2+int(trans_x2*0.05))
    trans_y4 = random.randint(y1+int(h*0.8), y2-1)

    dstTri = np.array([[trans_x1, trans_y1], [trans_x2, trans_y2],
                       [trans_x3, trans_y3], [trans_x4, trans_y4]]).astype(np.float32)

    warp_mat = cv2.getPerspectiveTransform(srcTri, dstTri)
    warp_dst = cv2.warpPerspective(img, warp_mat, (img.shape[1], img.shape[0]), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255))

    warp_bboxes = list()
    for bbox in bboxes:
        b_x1, b_y1, b_x2, b_y2 = bbox
        bbox_src = np.float32([[b_x1, b_y1], [b_x2, b_y1], [b_x1, b_y2], [b_x2, b_y2]]).reshape(-1, 1, 2)
        cnt = cv2.perspectiveTransform(bbox_src, warp_mat).reshape((4,2))
        x, y, w, h = cv2.boundingRect(cnt)

        warp_bboxes.append([x,y,x+w,y+h])
        # cv2.rectangle(warp_dst, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # center = (warp_dst.shape[1]//2, warp_dst.shape[0]//2)
    # angle = random.randint(-10,10)
    # scale = random.randint(8,10)/10
    # rot_mat = cv2.getRotationMatrix2D(center, angle, scale)
    # warp_rotate_dst = cv2.warpAffine(warp_dst, rot_mat, (warp_dst.shape[1], warp_dst.shape[0]))

    # cv2.imshow('Source image', img)
    # cv2.imshow('Warp', warp_dst)
    # cv2.imshow('Warp + Rotate', warp_rotate_dst)
    # cv2.waitKey()

    return warp_dst, warp_bboxes


custom_aug = iaa.Sequential([
            # iaa.CropAndPad(percent=(0.1)),
            # iaa.Affine(
            #     scale={"x": (0.9, 1.0), "y": (0.9, 1.0)},
            #     # translate_percent={"x": (-0.05, 0.05), "y": (-0.05, 0.05)},
            #     rotate=(-5, 5),
            #     # shear=(-25, 25)
            #     # cval=255
            # ),
            # iaa.ElasticTransformation(sigma=6, alpha=(0, 5)),

            # iaa.Sometimes(0.2, iaa.MotionBlur(k=7, angle=(-60, 120))),
            # iaa.GaussianBlur((0, 2.0)),

            # iaa.PiecewiseAffine(scale=(0.0, 0.01)),
            iaa.SomeOf((0, None), [
                iaa.AddToHueAndSaturation((-5, 5)),
                iaa.Multiply((0.7, 1.0)),
                # iaa.GaussianBlur((0.0, 1.0)),
                # iaa.AdditiveGaussianNoise(scale=(0.0, 0.03*255)),
                # iaa.CoarseDropout((0.0, 0.1), size_percent=0.3)
            ]),
            iaa.Grayscale(1.0),
            iaa.Invert(0.3)
    ])

custom_aug = iaa.Sequential([
    # iaa.CropAndPad(percent=(0.1)),
    iaa.Affine(
        scale={"x": (1.0, 1.4), "y": (1.0, 1.4)},
        # translate_percent={"x": (-0.05, 0.05), "y": (-0.05, 0.05)},
        rotate=(-15, 15),
        # shear=(-25, 25)
        # cval=255
    ),
    iaa.ElasticTransformation(sigma=6, alpha=(0, 5)),

    iaa.Sometimes(0.2, iaa.MotionBlur(k=7, angle=(-60, 120))),
    iaa.GaussianBlur((0, 2.0)),

    # iaa.PiecewiseAffine(scale=(0.0, 0.01)),
    iaa.SomeOf((0, None), [
        iaa.AddToHueAndSaturation((-10, 5)),
        iaa.Multiply((0.3, 1.0)),
        # iaa.GaussianBlur((0.0, 1.0)),
        iaa.AdditiveGaussianNoise(scale=(0.0, 0.03 * 255)),
        # iaa.CoarseDropout((0.0, 0.1), size_percent=0.3)
    ]),
    iaa.Grayscale(1.0),
    iaa.Invert(0.5)
])


def do_custom_augmentation(img, bboxes, count=1):
    if count == 3:
        # augmentation 이 3번 실패하면 원본을 return 한다.
        return img, bboxes

    image_shape = img.shape
    h, w = image_shape[:2]

    try:
        det = custom_aug.to_deterministic()
        img_aug = det.augment_image(img)

        ia_bboxes = list()
        for bounding_box in bboxes:
            x1, y1, x2, y2 = bounding_box
            ia_bboxes.append(imgaug.BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2))

        bbs = imgaug.BoundingBoxesOnImage(ia_bboxes, shape=image_shape)
        bbs_aug = det.augment_bounding_boxes([bbs], hooks=imgaug.HooksKeypoints(activator=hook))[0]
        # img = bbs_aug.draw_on_image(img)

        after_bboxes = list()
        for bounding_box in bbs_aug.bounding_boxes:
            bbox_list = [bounding_box.x1_int, bounding_box.y1_int, bounding_box.x2_int, bounding_box.y2_int]

            if bbox_list[0] >= w: bbox_list[0] = w - 1
            if bbox_list[1] >= h: bbox_list[1] = h - 1
            if bbox_list[2] >= w: bbox_list[2] = w - 1
            if bbox_list[3] >= h: bbox_list[3] = h - 1

            if bbox_list[0] == bbox_list[2] or bbox_list[1] == bbox_list[3]:
                return do_custom_augmentation(img, bboxes, count+1)

            bbox_list = [bounding_box.x1, bounding_box.y1, bounding_box.x2, bounding_box.y2]
            bbox_list = list(map(lambda x: max(x, 0), bbox_list))
            after_bboxes.append(bbox_list)

        # after_bboxes = np.array(after_bboxes).astype(np.float32)

        assert img_aug.shape == image_shape, "Augmentation shouldn't change image size"

        return img_aug, after_bboxes
    except:
        # 알 수 없는 버그 같은 경우 augment 를 적용하지 않고 리턴 한다.s
        return img, bboxes

src_path = "data/ocr/ocr_train/train"
json_path = "data/ocr/ocr_train/box_info.json"
dst_path = "data/ocr/affine_plate"
make_num = 100

if not os.path.isdir(dst_path):
    os.mkdir(dst_path)

json_f = open(json_path, 'r', encoding='utf-8')
ann_infos = json.load(json_f, object_pairs_hook=OrderedDict)
json_f.close()

new_ann_infos = list()
for annotation in tqdm(ann_infos, desc="file_process"):
    relative_path = annotation["filename"]
    width = annotation["width"]
    height = annotation["height"]
    ann = annotation["ann"]

    img_path = os.path.join(src_path, relative_path)
    img = cv2.imread(img_path)

    relative_path = unicodedata.normalize('NFC', relative_path)
    sub_dir, filename = os.path.split(relative_path)
    sub_dir_path = os.path.join(dst_path, "affine", sub_dir)
    if not os.path.isdir(sub_dir_path):
        os.makedirs(sub_dir_path)

    for i in tqdm(range(make_num), desc="img_process"):
        labels = ann['labels']
        border_index = labels.index(86)
        x1, y1, x2, y2 = ann['bboxes'][border_index]

        bboxes = ann["bboxes"]
        affine_img, bboxes = random_affine(img, bboxes, [x1,y1,x2,y2])
        affine_img, bboxes = do_custom_augmentation(affine_img, bboxes)

        # affine_img, bboxes = do_custom_augmentation(img, bboxes)

        img_name = os.path.splitext(filename)[0]
        img_name = img_name + "_%04d.jpg" % i

        new_relative_path = os.path.join("affine", sub_dir, img_name)

        cv2.imwrite(os.path.join(dst_path, new_relative_path), affine_img)

        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(affine_img, (int(x1), int(y1)), (int(x2), int(y2)), [0, 0, 255], 2)
        new_relative_path = os.path.join(dst_path, "affine_bbox", sub_dir)
        if not os.path.isdir(new_relative_path):
            os.makedirs(new_relative_path)
        re_path = os.path.join(new_relative_path, img_name)
        cv2.imwrite(re_path, affine_img)

        new_anno = OrderedDict()
        new_anno["filename"] = new_relative_path
        new_anno["width"] = width
        new_anno["height"] = height
        new_anno["ann"] = ann.copy()
        new_anno["ann"]["bboxes"] = bboxes
        new_ann_infos.append(new_anno)

# ann_infos.extend(new_ann_infos)
json_dist = os.path.join(dst_path, os.path.basename(json_path))
with open(json_dist, 'w', encoding='utf-8') as json_file:
    json.dump(new_ann_infos, json_file, ensure_ascii=False, indent='\t')