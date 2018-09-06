import xml.etree.ElementTree as ET

# import this data by reading from a file
tree = ET.parse('country_data.xml')
root = tree.getroot()

# Or directly from a string
#root = ET.fromstring(country_data_as_string)


# As an Element, root has a tag and a dictionary of attributes:

root.tag  # ---> 'data'
root.attrib  # ---> {}

# It also has children nodes over which we can iterate

for child in root:
    print(child.tag, child.attrib)
    # country {'name': 'Liechtenstein'}
    # country {'name': 'Singapore'}
    # country {'name': 'Panama'}


# Children are nested, and we can access specific child nodes by index
root[0][1].text   # ---> '2008'


# Element has some useful methods that help iterate recursively
# over all the sub-tree below it (its children, their children, and so on).
for neighbor in root.iter('neighbor'):
    print(neighbor.attrib)


# Element.findall() finds only elements with a tag which are direct children of the current element.
# Element.find() finds the first child with a particular tag,
# Element.text accesses the element’s text content.
# Element.get() accesses the element’s attributes:

for country in root.findall('country'):
    rank = country.find('rank').text
    name = country.get('name')
    print(name, rank)


# Modifying(filtering) an XML File

for rank in root.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
    rank.set('updated', 'yes')

tree.write('country_output.xml')

# We can remove elements using Element.remove().
# Let’s say we want to remove all countries with a rank higher than 50

for country in root.findall('country'):
    rank = int(country.find('rank').text)
    if rank > 50:
        root.remove(country)

tree.write('country_output.xml')
