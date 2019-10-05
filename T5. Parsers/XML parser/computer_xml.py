import os
import xml.etree.ElementTree as ET

env = os.environ

# create the file structure
data = ET.Element(env['COMPUTERNAME'])
os_items = ET.SubElement(data, 'system')
for key in env.keys():
    if 'OS' in key or 'PROCESSOR' in key:
        system_item = ET.SubElement(os_items, 'system_item')
        system_item.set('item', key)
        system_item.text = env[key]

# create a new XML file with the results

with open("computer.xml", "w") as xml_file:
    mydata = ET.tostringlist(data, encoding="unicode", method='xml')
    xml_file.writelines(mydata)


tree = ET.parse('computer.xml')
root = tree.getroot()


# Read all attributes
print('\nAll attributes:')
for elem in root:
    for subelem in elem:
        print(subelem.attrib)

print('\nAll item data:')
for elem in root:
    for subelem in elem:
        print(subelem.text)


# Modify existed xml file

# changing a field text
for elem in root.iter('system_item'):
    print('Change text value')
    elem.text = 'default value'

# modifying an attribute
for elem in root.iter('system_item'):
    elem.set('sys_item', 'default')

# adding an attribute
for elem in root.iter('system_item'):
    elem.set('remote', 'true')

tree.write('computer2.xml')
