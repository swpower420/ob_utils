import os
import cv2
import numpy as np


def apply_clahe(image, clip_limit=2.0):

    image_shape =image.shape
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))

    if len(image_shape)<3 or image_shape[2]==1:
        image = image.astype(np.uint8)
        image = clahe.apply(image)
    elif image_shape[2]==3:
        for i in range(3):
            temp = image[:,:,i].astype(np.uint8)
            image[:,:,i] = clahe.apply(temp)
    return image


dir_path = "t1_video_1024\\t1_video_1024\\t1_video_10000_only_train"
res_path = "t1_video_1024\\t1_video_1024\\t1_video_10000_only_train\\test"
target = "t1_video_10000_00%d.jpg"

for i in range(233,335):
    img = cv2.imread(os.path.join(dir_path, target%(i)))

    img = apply_clahe(img)

    cv2.imwrite(os.path.join(res_path, target%(i)), img)


# CLAHE => 1.0 ~ 1.5 사이로 맞추고 // 적용 확률은 0.3

# 테스트 할떄는 1.5 유지