# author:ajitesh
# Created on Sun Oct 31 2021
# Copyright (c) 2021 Your Company

'''
Implements Data Preparation steps
'''
import pandas as pd
import email
import sys
from joblib import Parallel, delayed
from joblib import Memory
from utils import sentence_tokenize, word_tokenize,remove_contractions,identify_stopwords,remove_punctuation,word_detokenize,get_stem_word,\
                  repeated_char_removal


sys.setrecursionlimit(10000)


class Normalizer:
    '''
    Implements email normalization steps mentioned in paper
    1. Email -> Email body
    2. Lowercasing
    3. Tokenization
    4. Contraction Removal
    5. Punctuation Removal
    6. Repeated Characters Replacement
    7. Stopwords removal
    8. Stemming 
    9. Spellcheck  
    10. Final csv file with normalized data
    '''
    def __init__(self, input_file,out_norm_file):
        '''
        Read poc csv file and extract email body and store them in a list
        '''
        self.csv_file = input_file
        self.normalized_file = out_norm_file
        self.email_body_df = self.extract_email_body(self.csv_file)
        self.email_body_list = list(map(self.text_cleaning, self.email_body_df['email_body']))
        self.lowercased_email_list = self.lowercasing(self.email_body_list)
        # self.sent_tokenized_emails = self.paragraph_tokenizer(self.email_body_list)
        self.fully_tokenized_emails_list = [word_tokenize(i) for i in self.lowercased_email_list]
        self.expanded_email_list = [self.contraction_removal(email) for email in self.fully_tokenized_emails_list]
        self.depunctuated_email_list = [self.punctuation_removal(email) for email in self.expanded_email_list]
        self.replaced_email_list = [self.repeated_char_replacement(email) for email in self.depunctuated_email_list]
        self.sw_removed_email_list = [self.stopwords_removal(email) for email in self.replaced_email_list]
        self.stemmed_email_list = [self.apply_stemming(email) for email in self.sw_removed_email_list]
        self.final_processed_email_list = [word_detokenize(email) for email in self.stemmed_email_list]
        print(self.final_processed_email_list[:2])
        
        ''' Saving normalised output to csv file'''
        df = pd.DataFrame({'final_normalized_email_body': self.final_processed_email_list}) 
        df.to_csv(self.normalized_file)
        
    
    def paragraph_tokenizer(self,email_list):
        '''
        Split emails into sentences,i.e creating list of list of sentences
        '''
        tokenized_emails = list()
        for email in email_list:
            tokenized_emails.append(sentence_tokenize(email)) 

        return tokenized_emails    
    
    def word_tokenizer(self,sent_list):
        '''
        tokenize sentences in a list to list of words, relevant after paragraph tokenization
        '''        
        tokenized_sent = [word_tokenize(sent) for sent in sent_list]
        return tokenized_sent    
            
    
    def contraction_removal(self,email):
        '''
        works at tokenized email level
        '''
        expaned_email_token = [remove_contractions(token) for token in email]
        return expaned_email_token
    
    def lowercasing(self,email_list):
        '''
        works at email body level
        '''
        lower_cased_emails = [email.lower() for email in email_list]
        return lower_cased_emails
    
    def punctuation_removal(self,email):
        '''
        Remove punctuation at tokenized email level
        '''
        updated_email = [remove_punctuation(token) for token in email if len(remove_punctuation(token))>0]
        return updated_email
    
    def stopwords_removal(self,email):
        '''
        Removes stopwords at tokenized email level
        '''
        updated_email = [token for token in email if identify_stopwords(token)==False ]
        # updated_email = Parallel(n_jobs=-1, backend="multiprocessing")(
            #               delayed(identify_stopwords)(token) for token in email if identify_stopwords(token)==False)
        return updated_email
    
    def apply_stemming(self,email):
        '''
        Convert tokenized email into list of stemming words
        '''
        stemmed_email = [get_stem_word(token) for token in email]  
        return stemmed_email  
    
    def repeated_char_replacement(self,email):
        '''
        Convert words(in a tokenized email(list)) with repeated characters to original form using wordnet,
        This method also performs spell checking using nltk edit distance on words dictionary which will
        save lot of computational time as it no longer will require to spell check all words but only those 
        which fails the test of wordnet and repeated char regex
        '''
        # location = '/data'
        # memory = Memory()
        # costly_compute_cached = memory.cache(repeated_char_removal)
        # reformed_email  = Parallel(n_jobs=3)(
        #                     delayed(costly_compute_cached)(token)
        #                     for token in email)
        reformed_email  = [repeated_char_removal(token) for token in email]
        
        return reformed_email
    
    def spell_check(self):
        pass
    
    def extract_email_body(self, csv_file):
        '''
        This funtions read every email in parts and stores the body of each email into a list
        '''
        body_list = list()
        df_input = pd.read_csv(csv_file)
        messages = list(map(email.message_from_string, df_input['message']))
        df_input.drop(['message','file'], axis=1, inplace=True)

        for message in messages:
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    body_list.append(part.get_payload()) 
   
        df_input['email_body'] = body_list
        return df_input
    
    def text_cleaning(self,text):
        '''
        new line character -> space
        '''
        text = text.replace("\n", " ")
        return text
        
    
    
    
    
  