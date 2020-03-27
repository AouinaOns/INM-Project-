# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:59:07 2020

@author: JessicaPINAIRE
"""

import json
import pandas as pd
import re
import string
import os
#nltk.download()  # Download text data sets, including stop words
from nltk.corpus import stopwords # Import the stop word list
#from nltk import pos_tag
#from nltk.stem import WordNetLemmatizer

# print (stopwords.words("english") )

# 1. Init Lemmatizer
#lemmatizer = WordNetLemmatizer()

# Work directory
os.chdir("C:/Users/JessicaPINAIRE/OneDrive - KALYA/textmining")
from Tools.ProcessTime import tic, tac

#corpus_json_file = 'Data/Sample.json'
#corpus_final_file = 'Data/Sample_final.csv'
corpus_json_file = 'C:/Users/JessicaPINAIRE/KALYA/Commun - Documents/08-Data Analysis/Data/CANCER_STUDIES_180320.json'
corpus_final_csv = 'Data/KC_TextCleaned_180320.csv'
corpus_final_json = 'Data/KC_TextCleaned_180320.json'

def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)

def remove_html(text):
    html = re.compile(r'<.*?>')
    return html.sub(r'',text)

def remove_punct(text):
    table = str.maketrans('','',string.punctuation)
    return text.translate(table)

def remove_copyright(text):
    start0 = text.find("Copyright")
    start1 = text.find("©")
    if start0!=-1 & start1!=-1:
      start = min(start0, start1)
    elif start0!=-1 & start1==-1:
      start = start0
    elif start0==-1 & start1!=-1:
      start = start1
    else:
        start = -1
    if start!=-1: 
      text = text[0:start]
    
    return text
  
def remove_trialregistration(text):
    # The format for the ClinicalTrials.gov registry number is “NCT” followed by an 8-digit number
    text = re.sub('[N][C][T][[\d]{8}', '', text)
    text = re.sub('ClinicalTrials.gov', '', text)
    text = re.sub('Trial registration', '', text)
    text = re.sub('Trial register', '', text)
    text = re.sub('Identifier', '', text)
    
    return text  

# Time
tic()

# Load data
with open(corpus_json_file, 'r') as f:
   my_publi = json.load(f)

# Dictionnary initialisation
TEXT = {}
j = 0 # compteur    

# Initialisation du dataframe
df_output = pd.DataFrame()

# Text processing: concatenate title, abstract, keywords, mesh words and substances
#for key in ["30418475"]:
for key in my_publi.keys():
   #print(key)
#if my_publi[key]['title'] is not None:
   journal = my_publi[key]['journalname']
   text = my_publi[key]['title'] + ' ' + my_publi[key]['fullabstract']

   if my_publi[key]['keywords'] is not None:
         for keyword in my_publi[key]['keywords']:
              if keyword is not None:
                  text = text + ' ' + keyword

   if my_publi[key]['meshkeywords'] is not None:
         for mkeyword in my_publi[key]['meshkeywords']:
              if mkeyword is not None:
                  if type(mkeyword) is str:
                       text = text + ' ' + mkeyword
                  else:
                       text = text + ' ' + mkeyword['Text']

   if my_publi[key]['substances'] is not None:
         for substance in my_publi[key]['substances']:
              if substance is not None:
                  if type(substance) is str:
                       text = text + ' ' + substance
                  else:
                       text = text + ' ' + substance['NameOfSubstance']
                       
   # Remove url and html characters
   text = remove_URL(text)
   #print(text)
   text = remove_html(text)
   #print(text)
   
   # Remove copyrights and Trial registration
   text = remove_copyright(text) 
   #print(text)
   text = remove_trialregistration(text)
   #print(text)
                       
   # Remove punctuation, numbers, special characters and symbols 
   # and
   # Convert to lower case                       
   text_clean = text.translate(str.maketrans('', '', '/"()%-$@{}>=<[].;,:!?+&/#°®0123456789')).lower()
   #print(text_clean)
                                        
   # Remove whitespaces
   text_interm = text_clean.strip()
   
#    # replace contractions
#    text_contract = contractions.fix(text_interm)
   
   # Lemmatize
   #text_lem = " ".join([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(text_interm)])
   
   # Split into individuals words
   words = text_interm.split()
   
   # Remove stop words
   # Remove the 100 most frequent words in the corpus
   # and
   # remove non alphanumeric words
   stops = set(stopwords.words("english"))
   mylist = pd.read_csv("C:/Users/JessicaPINAIRE/OneDrive - KALYA/TextVisualAnalytics/Data/FrequentWords_sorted_v160320.csv")
#   stops2 = mylist['x'].tolist()[0:122] # we take only the 123 first words
   stops2 = mylist['x'].tolist()
   myUNITS = pd.read_csv("C:/Users/JessicaPINAIRE/OneDrive - KALYA/TextVisualAnalytics/Data/units.csv", header=None)
   stops3 = myUNITS[0].tolist()
   #print(stops3)
   meaningful_words = [w for w in words if ((w.isalpha()==1) & (w not in stops) & (w not in stops2) & (w not in stops3))] 
   
   # Join the words back into one string separated by space, 
   # and return the result.
   text_final =  " ".join( meaningful_words )
   #print(text_final)
   df_output = df_output.append({'pmid': key, 'journalname': journal, 'text': text_final}, ignore_index = True)
   TEXT[j]={}
   TEXT[j]['pmid']=key
   TEXT[j]['journalname']=journal
   TEXT[j]['text']=text_final
   j +=1
   
#print(df_output)
   
# Save as dataframe in csv file
df_output.to_csv(corpus_final_csv)

# Save as a dictionnary
#mydict = df_output.to_dict('index')
with open(corpus_final_json, 'w') as f:
   json.dump(TEXT, f) 
   
   
   ## Record data
#   TEXT[key][journal] = text_final
#   
## Record in a json file
#with open(corpus_final_file, 'w') as f:
#   json.dump(TEXT, f) 


tac()
# 9min:59sec