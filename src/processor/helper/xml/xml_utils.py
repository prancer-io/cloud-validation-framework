import xml.etree.ElementTree as ET

def xml_to_json(xml_content):
    root = ET.fromstring(xml_content)
    json_dict = {
        root.tag: {}
    }
    for child in root:
        json_dict[root.tag][child.tag] = {
            "text" : child.text,
            "attributes" : {}
        }
        for attr_key, attr_value in child.attrib.items():
            json_dict[root.tag][child.tag]["attributes"][attr_key] = attr_value
    return json_dict