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

def parse_xml(file_path,tag):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for ecuc in root.findall(tag,ns):
        short_name = ecuc.find('.//autosar:SHORT-NAME',ns).text
        if "_EcuSwComposition" in short_name:
            logging.info(f"Found short name satisfying criteria : {short_name}")
            if "_core" in short_name.lower():
                index = short_name.lower().find("_core") + 5
                core_no = short_name[index : index + 1]
                data.append({'swc-name':short_name,'core-no':core_no})
                logging.info(f'Extracted core number: {core_no}')
            elif "Par" in short_name:
                core_no = "Not mentioned"
                data.append({'swc-name':short_name,'core-no':core_no})
                logging.info(f'Extracted core number: {core_no}')
            else:
                for value_ref in ecuc.findall(".//autosar:VALUE-REF",ns):
                    dest = value_ref.get('DEST')
                    if dest == "ECUC-CONTAINER-VALUE":
                        core_details = value_ref.text
                        if "Core" in core_details:
                            index = core_details.find("Core") + 4
                            core_no = core_details[index : index + 1]
                            data.append({'swc-name':short_name,'core-no':core_no})
                            logging.info(f'Extracted core number: {core_no}')
                            break

folder_path = Path("/home/kpit/python/Port_Task")

for file_path in folder_path.iterdir():
    if file_path.name == 'CCU_Rte_ecuc.arxml':
        logging.info(f"Started parsing {file_path.name}")
        parse_xml(file_path,".//autosar:ECUC-CONTAINER-VALUE")
        logging.info(f"Parsing done {file_path.name}")

df = pd.DataFrame(data)
# print(df)
df.to_excel("5.xlsx",index = False)
