import pandas as pd
import logging 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='task6.log'
                    ) 

data6 = []
df4 = pd.read_excel('4.xlsx')
df5 = pd.read_excel('5.xlsx')      
    
    