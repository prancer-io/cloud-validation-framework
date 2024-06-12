import xml.etree.ElementTree as ET

def parse_element(element):
    parsed = {
        "name": element.tag,
        "text": element.text.strip() if element.text and element.text.strip() else None,
        "attributes": element.attrib,
        "children": []
    }

    for child in element:
        parsed["children"].append(parse_element(child))

    return parsed

def xml_to_json(xml_content):
    root = ET.fromstring(xml_content)
    parsed_xml = parse_element(root)
    return parsed_xml
