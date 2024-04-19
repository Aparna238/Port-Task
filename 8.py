import pandas as pd
import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

df = pd.read_excel('4.xlsx')
integration_requirements = Element('IntegrationRequirements')
connections = SubElement(integration_requirements, 'Connections')
sender_receiver = SubElement(connections, 'SenderReceiver')

for row in df:
    connection = SubElement(sender_receiver, 'Connection')
    receiver = SubElement(connection, 'Receiver', Parent=row['R-port-swc'])
    receiver.text = row['R-port-name']
    sender = SubElement(connection, 'Sender', Parent=row['P-port-swc'])
    sender.text = row['P-port-name']

xml_str = tostring(integration_requirements, encoding='unicode', method='xml')

dom = xml.dom.minidom.parseString(xml_str)

pretty_xml_str = dom.toprettyxml()

with open('RemoveMapping.xml', 'w') as f:
    f.write(pretty_xml_str)

