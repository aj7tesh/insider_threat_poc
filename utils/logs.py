# author:ajitesh
# Created on Sun Oct 31 2021
# Copyright (c) 2021 Your Company

'''
Customised logger
'''
import logging

def init_logger(log_file=None, log_file_level=logging.NOTSET, rotate=False):
    log_format = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]

    return logger