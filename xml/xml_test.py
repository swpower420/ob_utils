from lxml import etree as ET



def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


if __name__ == '__main__':
    xml_path = "cctv/etri-02.xml"
    tree = ET.parse(xml_path)

    # get root
    root = tree.getroot()

    image = ET.SubElement(root, 'image')
    image.set("id", "0")
    image.set("name", "1-20190927-085240-092240.mp4_snapshot_00.03_[2020.03.05_12.55.15].png")
    image.set("width", "1920")
    image.set("height","1080")

    box = ET.SubElement(image, 'box')
    box.set("label", "트럭")
    box.set("occluded", "0")
    box.set("xtl", "0.38")
    box.set("ytl", "567.94")
    box.set("xbr", "534.53")
    box.set("ybr", "1077.46")


    """
    <image id="0" name="1-20190927-085240-092240.mp4_snapshot_00.03_[2020.03.05_12.55.15].png" width="1920" height="1080">
    <box label="트럭" occluded="0" xtl="0.38" ytl="567.94" xbr="534.53" ybr="1077.46">
    </box>
    <box label="승용차" occluded="0" xtl="1191.84" ytl="124.61" xbr="1662.88" ybr="326.26">
    </box>
    <box label="번호판" occluded="0" xtl="720.64" ytl="726.54" xbr="855.34" ybr="770.16">
    </box>
    <box label="번호판" occluded="0" xtl="1403.34" ytl="963.40" xbr="1555.74" ybr="1020.35">
    </box>
    <box label="승용차" occluded="0" xtl="606.88" ytl="517.14" xbr="1553.60" ybr="972.80">
    </box>
    <box label="승용차" occluded="0" xtl="1296.51" ytl="641.83" xbr="1918.41" ybr="1079.00">
    </box>
    </image>
    """
    indent(root)
    print(ET.dump(root))
    tree.write("cctv/etri-02_test.xml", xml_declaration=True, encoding='utf-8', method="xml")

