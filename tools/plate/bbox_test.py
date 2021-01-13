import os
import json
import cv2
import colorsys
import random
import numpy as np

import matplotlib
matplotlib.use('agg')

from matplotlib import patches
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from collections import OrderedDict

root = "data/crawl/"
json_file = "data/crawl/08.json"

root = "data/testworks/train"
json_file = "data/testworks/train/train_total.json"

json_f = open(json_file, 'r', encoding='utf-8')
ann_info = json.load(json_f, object_pairs_hook=OrderedDict)
json_f.close()


def random_colors(N, bright=True):
    """
    Generate random colors.
    To get visually distinct colors, generate them in HSV space then
    convert to RGB.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors


for img_info in ann_info:
    img_path = os.path.join(root, img_info["filename"])
    print(img_path)

    # if "re" not in img_path:
    #     continue
    image = cv2.imread(img_path)

    ann_info = img_info['ann']
    boxes = ann_info['bboxes']
    labels = ann_info['labels']

    image_shape = image.shape

    figsize = ((image_shape[1]) / 100.0, image_shape[0] / 100.0)

    fig, ax = plt.subplots(1, figsize=figsize, frameon=False)
    ax = fig.add_axes([0., 0., 1., 1.])

    font_path = '../../demo/NanumGothic.ttf'
    font_path = os.path.expanduser(font_path)
    font_name = fm.FontProperties(fname=font_path, size=50).get_name()
    plt.rc('font', family=font_name)

    linewidth = 1
    N = len(boxes)

    colors = random_colors(N)

    # Draw Prediction

    for i, box, label_name in zip(range(len(boxes)), boxes, labels):
        color = colors[i]

        [x1, y1, x2, y2] = box

        # Bounding box
        p = patches.Rectangle((x1, y1), (x2 - x1)+1, (y2 - y1)+1, linewidth=linewidth,
                              alpha=0.5, linestyle="dashed",
                              # edgecolor=color, facecolor=color)
                              edgecolor="yellow", facecolor='none')
        ax.add_patch(p)

        # Label
        # label_name = unicodedata.normalize('NFC', label_name)
        caption = "{}".format(label_name)

        ax.text(x1, y1 + 8, caption,
                color='b', size=20, backgroundcolor="none")

    ax.imshow(image.astype(np.uint8))
    fig.canvas.draw()  # draw the canvas, cache the renderer

    result_image = np.array(fig.canvas.renderer._renderer)
    # result_image = cv2.cvtColor(result_image[:, :, :3], cv2.COLOR_BGR2RGB)

    plt.close(fig)  # close figure memory

    # cv2.imwrite(result_path, result_image)

    cv2.imshow("test", result_image)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
