from lxml import etree as ET
import os
import cv2


CATEGORIES = [
        "__background", "승용차", "SUV", "승합차", "트럭", "특수차", "번호판", "사람", "오토바이"
    ]
COLORS = [(128,128,128), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (0, 0, 0), (255, 255, 255)]


if __name__ == '__main__':
    img_dir = "cctv/etri-03"
    xml_path = "cctv/etri-03.xml"
    tree = ET.parse(xml_path)

    # get root
    root = tree.getroot()

    for elem in root:
        if elem.tag != 'image':
            continue  # read only image

        img_name = elem.get("name")
        img_path = os.path.join(img_dir, img_name)

        img = cv2.imread(img_path)

        for sub_elem in elem:
            label_index = CATEGORIES.index(sub_elem.get("label"))

            # xtl="0.00" ytl="112.00" xbr="1917.00" ybr=
            x1 = int(float(sub_elem.get("xtl")))
            y1 = int(float(sub_elem.get("ytl")))
            x2 = int(float(sub_elem.get("xbr")))
            y2 = int(float(sub_elem.get("ybr")))

            cv2.rectangle(img, (x1,y1), (x2,y2), COLORS[label_index], 3)

        cv2.imshow("test", img)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

