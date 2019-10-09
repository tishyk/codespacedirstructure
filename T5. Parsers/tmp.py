import os
import xml.etree.ElementTree as ET

root = ET.Element(os.environ['USERNAME'])
os_items = ET.SubElement(root, 'system')

for key in os.environ.keys():
    system_item = ET.SubElement(os_items, 'system_attribute')
    system_item.set('name', key)
    system_item.text = os.environ[key]

mydata = ET.tostringlist(root, encoding="unicode", method='xml')
with open("computer.xml", "w") as xml_file:
    xml_file.writelines(mydata)
print(mydata)