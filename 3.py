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
    implementation = ""
    application = " "

    for data_type in root.findall(tag,ns):
        swc_name = data_type.find('.//autosar:SHORT-NAME',ns).text
        for data_ in data_type.findall('.//autosar:DATA-TYPE-MAP',ns):
            logging.info("DATA-TYPE-MAP found")
            application = data_.find('.//autosar:APPLICATION-DATA-TYPE-REF', ns).text
            application = application.split('/')[-1]
            logging.info(f"Application-data-type:{application} ")
            implementation = data_.find('.//autosar:IMPLEMENTATION-DATA-TYPE-REF', ns).text
            implementation = implementation.split('/')[-1]
            data.append({'Application_Ref':application, 'Implementation_Ref':implementation,'SWC':swc_name})
            logging.info(f"Implementation-data-type:{implementation} ")

    for implement in root.findall('.//autosar:IMPLEMENTATION-DATA-TYPE',ns):
        short_name = implement.find('.//autosar:SHORT-NAME',ns).text
        for row in data:
            if short_name == row['Implementation_Ref']:
                category = implement.find('.//autosar:CATEGORY',ns).text
                row['Category'] = category
                logging.info(f"Category found: {category}")

folder_path = Path("/home/kpit/python/Port_Task")

for file_path in folder_path.iterdir():
    if file_path.name == 'DataTypes.arxml':
        logging.info(f"Started parsing {file_path.name}")
        parse_xml(file_path,".//autosar:DATA-TYPE-MAPPING-SET")
        logging.info(f"Parsing done {file_path.name}")

df = pd.DataFrame(data)
# print(df)
df.to_excel("3.xlsx",index = False)

df = df.drop_duplicates(subset=['Application_Ref', 'Implementation_Ref','Category'])
df.to_excel("333.xlsx",index = False)



