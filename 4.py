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

    for connector in root.findall(tag,ns):
        logging.info('Found assembly-sw-connector')
        for p_port in connector.findall('.//autosar:TARGET-P-PORT-REF',ns):
            p_port_type = p_port.get('DEST')
            pport_name = p_port.text
            p_port_name = pport_name.split('/')[-1]
            p_port_swc = pport_name.split('/')[-2]
            logging.info(f'Found {p_port_swc} provided port')
        for r_port in connector.findall('.//autosar:TARGET-R-PORT-REF',ns):
            r_port_type = r_port.get('DEST')
            rport_name = r_port.text
            r_port_name = rport_name.split('/')[-1]
            r_port_swc = rport_name.split('/')[-2]
            logging.info(f'Found {r_port_swc} recieved port')
        data.append({'P-port-type': p_port_type,'P-port-name':p_port_name,'P-port-swc': p_port_swc,'R-port-type': r_port_type,'R-port-name':r_port_name,'R-port-swc': r_port_swc})


folder_path = Path("/home/kpit/python/Port_Task")

for file_path in folder_path.iterdir():
    if file_path.name == 'FlatExtract.arxml':
        logging.info(f"Started parsing {file_path.name}")
        parse_xml(file_path,".//autosar:ASSEMBLY-SW-CONNECTOR")
        logging.info(f"Parsing done {file_path.name}")

df = pd.DataFrame(data)
# print(df)
df.to_excel("4.xlsx",index = False)
