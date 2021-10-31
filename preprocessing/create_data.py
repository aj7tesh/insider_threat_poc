# author:ajitesh
# Created on Sun Oct 31 2021
# Copyright (c) 2021 Your Company

'''
Create data for implementing this research from the original csv
'''
import pandas as pd
from utils import init_logger

logger = init_logger()

class CreateData:
    def __init__(self):
        pass
    
    def create_data(self,input_file,output_file,test_size):
        '''
        Read orignial csv data, shuffle it and create new csv file with 10k rows for the poc
        '''
        try:
            read_csv = pd.read_csv(input_file)
            df_shuffled = read_csv.sample(frac=1).reset_index(drop=True)
            df_truncated = df_shuffled[:test_size]
            df_truncated.to_csv(output_file,index=False)
            return output_file
        
        except Exception as e:
            logger.exception("Exception caught | Method:create_data | value:{}".format(e))

                    