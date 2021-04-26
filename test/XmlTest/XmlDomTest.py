#!python2
#!coding:utf-8

import xml.dom.minidom

def CreateXml(filename):
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'root', None)
    root = dom.documentElement

    country = dom.createElement('country')
    country.setAttribute("name", "Liechtenstein")
    rank = dom.createElement('rank')
    rankText = dom.createTextNode('1')
    rank.appendChild(rankText)
    year = dom.createElement('year')
    yearText = dom.createTextNode('2008')
    year.appendChild(yearText)
    gdppc = dom.createElement('gdppc')
    gdppcText = dom.createTextNode('141100')
    gdppc.appendChild(gdppcText)
    neighbor1  = dom.createElement('neighbor')
    neighbor1.setAttribute("name", "Austria")
    neighbor1.setAttribute("direction", "E")
    neighbor2  = dom.createElement('neighbor')
    neighbor2.setAttribute("name", "Switzerland")
    neighbor2.setAttribute("direction", "W")

    country.appendChild(rank)
    country.appendChild(year)
    country.appendChild(gdppc)
    country.appendChild(neighbor1)
    country.appendChild(neighbor2)

    country2 = dom.createElement('country')
    country2.setAttribute("name", "Singapore")
    rank = dom.createElement('rank')
    rankText = dom.createTextNode('4')
    rank.appendChild(rankText)
    year = dom.createElement('year')
    yearText = dom.createTextNode('2011')
    year.appendChild(yearText)
    gdppc = dom.createElement('gdppc')
    gdppcText = dom.createTextNode('59900')
    gdppc.appendChild(gdppcText)
    neighbor1  = dom.createElement('neighbor')
    neighbor1.setAttribute("name", "Malaysia")
    neighbor1.setAttribute("direction", "N")
    
    country2.appendChild(rank)
    country2.appendChild(year)
    country2.appendChild(gdppc)
    country2.appendChild(neighbor1)

    country3 = dom.createElement('country')
    country3.setAttribute("name", "Panama")
    rank = dom.createElement('rank')
    rankText = dom.createTextNode('68')
    rank.appendChild(rankText)
    year = dom.createElement('year')
    yearText = dom.createTextNode('2008')
    year.appendChild(yearText)
    gdppc = dom.createElement('gdppc')
    gdppcText = dom.createTextNode('13600')
    gdppc.appendChild(gdppcText)
    neighbor1  = dom.createElement('neighbor')
    neighbor1.setAttribute("name", "Costa Rica")
    neighbor1.setAttribute("direction", "W")
    neighbor2  = dom.createElement('neighbor')
    neighbor2.setAttribute("name", "Colombia")
    neighbor2.setAttribute("direction", "E")

    country3.appendChild(rank)
    country3.appendChild(year)
    country3.appendChild(gdppc)
    country3.appendChild(neighbor1)
    country3.appendChild(neighbor2)

    root.appendChild(country)
    root.appendChild(country2)
    root.appendChild(country3)

    f= open(filename, 'w')
    dom.writexml(f, indent="", addindent='\t', newl='\n', encoding="utf8")
    f.close()

def main():
    CreateXml("DomCreate.xml")

if __name__ == "__main__":
    main()