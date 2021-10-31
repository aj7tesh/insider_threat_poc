# author:ajitesh
# Created on Sun Oct 31 2021
# Copyright (c) 2021 Your Company

'''
Contains Regex patterns used across project
'''
import enum

class Patterns:  
    P1 = { "regex":r'(\w*)(\w)\2(\w*)', "description":"regex pattern to capture repeatition of characters in a word" }
    P2 = { "regex":r'\1\2\3', "description":"regex pattern to execute removal of repeated characters in a word" }