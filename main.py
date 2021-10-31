# author:ajitesh
# Created on Sun Oct 31 2021
# Copyright (c) 2021 Your Company

'''
Starter script file which executes step 1,2,3 for the POC
'''
from preprocessing import Normalizer
from preprocessing import CreateData
import config
from utils import init_logger

logger = init_logger()

def data_preparation():
    '''
    This method executes end to end data creation as part 1 of Poc
    Approximate time to execute: 5-6 min on 4vCPUs
    '''
    try:    
        logger.info("Step 1.0: Data Preparation | process begins")
        poc_csv_file = CreateData().create_data(config.ORIGINAL_FILE,config.POC_FILE,config.TEST_SIZE)
        logger.info("Step 1.1: Data Preparation | poc data created")
        email_normalizer_init = Normalizer(poc_csv_file,config.NORMALIZED_FILE) 
        logger.info("Data Preparation | process finished")
        return True
    except Exception as e:
        logger.exception("Exception caught | Method:data_preparation | value:{}".format(e))  
        return False  


def data_discovery():
    pass

if __name__ == '__main__':
    data_preparation()
