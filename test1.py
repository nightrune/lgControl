import xml.dom.minidom
"""
dom1 = parse('c:\\temp\\mydata.xml') # parse an XML file by name

datasource = open('c:\\temp\\mydata.xml')
dom2 = parse(datasource)   # parse an open file

"""

def printChildNodes(parentNode, indent):
    if(len(parentNode.childNodes) > 0):
        for node in parentNode.childNodes:
            print ' '* indent, "Node: ", node
            print ' '* indent, 'Text Node: ', node.nodeType == node.TEXT_NODE
            printChildNodes(node, indent + 1)
    else:
        return
print '*'*79 
dom = xml.dom.minidom.parse('test2.xml') # parse an XML file by name

printChildNodes(dom, 0)

for node in dom.getElementsByTagName("input"):
    print "Node: ", node," Node Name: ", node.getAttribute('name')
    for childNode in node.childNodes:
        print childNode.data
    
print '*'*79   
print dom.getElementsByTagName("tv")[0].getAttribute('name')

