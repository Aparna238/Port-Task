from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='task.log'
                    )    
   
data = []
ns = {'autosar': 'http://autosar.org/schema/r4.0'}

def parse_xml(file,tag):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for interface in root.findall(tag,ns):
            interface_name = interface.find('.//autosar:SHORT-NAME', ns).text
            logging.info(f"Found interface swc: {interface_name}")
            for type in interface.findall('.//autosar:TYPE-TREF',ns):
                interface_type = type.get('DEST')
                interface_type_ref = type.text
                interface_type_ref = interface_type_ref.split('/')[-1]
                logging.info(f"Found interface type reference: {interface_type_ref}")
                data.append({'interface_name':interface_name, 'interface_type':interface_type,'interface_type_ref':interface_type_ref})

folder_path = Path("/home/kpit/python/Port_Task")

for file_path in folder_path.iterdir():
    if file_path.name == 'PortInterfaces.arxml':
        logging.info(f"Started parsing {file_path.name}")
        parse_xml(file_path,".//autosar:SENDER-RECEIVER-INTERFACE")
        logging.info(f"Parsing done {file_path.name}")

df = pd.DataFrame(data)
# print(df)
df.to_excel("2.xlsx",index = False)
df = df.drop_duplicates()
df.to_excel("22.xlsx",index = False)


