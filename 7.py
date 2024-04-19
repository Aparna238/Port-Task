import pandas as pd
import logging

data7 = [] 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='task7.log'
                    )    
   
intercore = pd.read_excel('6.xlsx')
df1 = pd.read_excel('1.xlsx')
df2 = pd.read_excel('2.xlsx')
df3 = pd.read_excel('3.xlsx')
df1.drop_duplicates()
df2.drop_duplicates()
df3.drop_duplicates(subset=['Application_Ref', 'Implementation_Ref','Category'])
for i1,row1 in df1.iterrows():
    i_name = row1['Interface_name']
    for i2,row2 in df2.iterrows():
        if i_name == row2['interface_name']:
            i_ref = row2['interface_type_ref']
            logging.info(f" found  I_NAME {i_name}")
            for i3,row3 in df3.iterrows():
                if i_ref == row3['Implementation_Ref'] or i_ref == row3['Application_Ref']:
                    i_category = row3['Category']
                    logging.info(f" got  I_REF {i_ref}")
                    data7.append({'SWC':row1['Swc_component'], 'Port name':row1['Swc_port'],'Interface name':i_name, 'Interface type':row2['interface_type'], 'Category':i_category})
                    logging.info(f" yippee found CATEGORY {i_category}")
                    break

df7 = pd.DataFrame(data7)
df7.to_excel('7.xlsx',index=False)



   
