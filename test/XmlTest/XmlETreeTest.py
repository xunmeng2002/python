#!python2
#!coding:utf-8

import xml.etree.ElementTree as ET

def PrintXml(root):
    print root.tag, root.attrib, root.text
    for elem in root:
        PrintXml(elem)

def ReadAndIterXml(root):
    print root.tag, root.attrib
    for child in root:
        print child.tag, child.attrib
    for neighbor in root.iter('neighbor'):
        print neighbor.attrib
    for country in root.findall('country'):
        rank = country.find('rank').text
        name = country.get('name')
        print name, rank

def ModifyXml(tree, root, filename):
    for rank in root.iter('rank'):
        new_rank = int(rank.text) + 1
        rank.text = str(new_rank)
        rank.set('updated', 'yes')
    for country in root.findall('country'):
        rank = int(country.find('rank').text)
        if rank > 50:
            root.remove(country)
    tree.write(filename)

def CreateXml(filename):
    root = ET.Element('data')
    tree = ET.ElementTree(root)
    country = ET.Element('country')
    country.set("name", "Liechtenstein")
    rank = ET.Element('rank')
    rank.text = "1"
    year = ET.Element('year')
    year.text = "2008"
    gdppc = ET.Element('gdppc')
    gdppc.text = "141100"
    neighbor1  = ET.Element('neighbor')
    neighbor1.set("name", "Austria")
    neighbor1.set("direction", "E")
    neighbor2  = ET.Element('neighbor')
    neighbor2.set("name", "Switzerland")
    neighbor2.set("direction", "W")
    country.append(rank)
    country.append(year)
    country.append(gdppc)
    country.append(neighbor1)
    country.append(neighbor2)

    country2 = ET.Element('country')
    country2.set("name", "Singapore")
    rank = ET.Element('rank')
    rank.text = "4"
    year = ET.Element('year')
    year.text = "2011"
    gdppc = ET.Element('gdppc')
    gdppc.text = "59900"
    neighbor1  = ET.Element('neighbor')
    neighbor1.set("name", "Malaysia")
    neighbor1.set("direction", "N")
    country2.append(rank)
    country2.append(year)
    country2.append(gdppc)
    country2.append(neighbor1)

    country3 = ET.Element('country')
    country3.set("name", "Singapore")
    rank = ET.Element('rank')
    rank.text = "68"
    year = ET.Element('year')
    year.text = "2011"
    gdppc = ET.Element('gdppc')
    gdppc.text = "13600"
    neighbor1  = ET.Element('neighbor')
    neighbor1.set("name", "Costa Rica")
    neighbor1.set("direction", "W")
    neighbor2  = ET.Element('neighbor')
    neighbor2.set("name", "Colombia")
    neighbor2.set("direction", "E")
    country3.append(rank)
    country3.append(year)
    country3.append(gdppc)
    country3.append(neighbor1)
    country3.append(neighbor2)

    root.append(country)
    root.append(country2)
    root.append(country3)
    Indent(root)
    #PrintXml(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

def Indent(elem, level=0, isLast=True):
    textIndent = "\n" + (level + 1)*"\t"
    tailIndent = "\n" + level*"\t"
    if isLast:
        tailIndent = "\n" + (level - 1)*"\t"

    if len(elem) > 0 and elem.text is None:
        elem.text = textIndent
    elem.tail = tailIndent
    i = 0
    length = len(elem)
    for child in elem:
        i += 1
        Indent(child, level + 1, (i == length))


def main():
    tree = ET.parse('ETreeRead.xml')
    root = tree.getroot()
    ReadAndIterXml(root)
    ModifyXml(tree, root, "ETreeModify.xml")
    CreateXml("ETreeCreate.xml")

if __name__ == '__main__':
    main()
        