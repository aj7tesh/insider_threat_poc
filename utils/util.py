# author:ajitesh
# Created on Sun Oct 31 2021
# Copyright (c) 2021 Your Company

'''
This files contains independent third party utility functions which can be used across modules
'''

from nltk.tokenize import sent_tokenize,word_tokenize,TreebankWordTokenizer
from nltk.stem import PorterStemmer
from sacremoses import MosesTokenizer, MosesDetokenizer
from nltk.corpus import stopwords, words, wordnet
from nltk.metrics.distance  import edit_distance
import contractions
import string
from config import Patterns
import re
from utils.logs import init_logger

logger = init_logger()


def sentence_tokenize(para):
    '''
    paragraph to list of sentences
    '''
    return sent_tokenize(para)

def word_tokenize(sent):
    '''
    tokenize sentence into list of words
    '''
    try:
        mt = MosesTokenizer(lang='en')
        tokenized_text = mt.tokenize(sent)
        return tokenized_text
        
    except Exception as e:
        logger.exception("Exception caught | Method:word_tokenize | value:{}".format(e))
        
    
def word_detokenize(word_list):
    '''
    detokenize a sentence using sacremoses
    '''    
    md = MosesDetokenizer(lang='en')
    detokenized_text = md.detokenize(word_list)
    return detokenized_text

def remove_contractions(token):
    '''
    Expand the contracted word to original form
    '''   
    return contractions.fix(token)

def identify_stopwords(token):
    '''
    Identify stopword if it qualifies as nltk stopword
    '''
    nltk_sw = stopwords.words('english')
    
    if token.lower() in nltk_sw:
        return True
    else:
        return False

def remove_punctuation(token):
    '''
    Remove punctuation from a token using string lib
    '''  
    updated_token = "".join([char for char in token if char not in string.punctuation])
    return updated_token

def get_stem_word(token):
    '''
    Apply porter stemming to a word
    '''
    ps = PorterStemmer()
    stem_word = ps.stem(token)
    return stem_word

def repeated_char_removal(token):
    '''
    Removes illegitimate repeated char from a word using nltk wordnet
    '''
    re_p1 = Patterns.P1['regex']
    re_p2 = Patterns.P2['regex']

    complile_regex = re.compile(re_p1)
    if wordnet.synsets(token):
        ''' Checking if the word exist in wordnet dictionary; processing is time consuming'''
        return token
    new_token = complile_regex.sub(re_p2, token)
    if new_token !=token:
        return repeated_char_removal(new_token)
    else:
        return new_token

def spell_corrector(token):
    '''
    Correct spelling of a word using nltk edit distance,
    Calculating ED for words starting with same alphabet;
    time consuming step
    '''
    nltk_ref_words = words.words()
    try:   
        if type(token)== str and token.isalpha():            
            temp = [(edit_distance(token, w),w) for w in nltk_ref_words if w[0]==token[0]]
            return sorted(temp, key = lambda val:val[0])[0][1]
        else:
            print("token ins not alpha")
            return token
    except Exception as e:
        logger.exception("Exception caught | Method:word_tokenize | value:{}".format(e))

