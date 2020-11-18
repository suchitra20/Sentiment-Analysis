# Topic : what are the words used in bad reviews.
# For this research, you could add more juicy explorations such as 
# "among the common bad words used in bad reviews, what are those worst words, and what are not that bad".
# To achieve this purpose, you could do a text classification to predict bad reviews using the 
# existence of the bad words and report the most informative features.

import pandas as pd
import os
from textblob import TextBlob
import nltk
import nltk.data
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string
from nltk.tokenize import word_tokenize
import re
import matplotlib.pyplot as plt

# 1. LOADING DATA CSV 

path = 'C:/Users/Suchitra/Desktop/MSBA Subjects/BAN 675 Text Mining/Group Project'
os.chdir(path)
reviews = pd.read_csv('reviews.csv')

# 2. DATA PRE-PROCESSING

stop_words=stopwords.words("english")

def clean_text(text):
    words=word_tokenize(text)
    # lower case text, remove stop words, punctuations, check if alphabet
    text = [word.lower() for word in words if word not in stop_words and word not in string.punctuation and word.isalpha()]    
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)

# 3. DATA EXPLORATION
 
# Extract only the negative reviews
def sentiment_analysis(text):    
    review = TextBlob(text)        
    analyzer=SentimentIntensityAnalyzer()  # Analyzing the intensity of the bad review
    sent=analyzer.polarity_scores(review)
    if sent['compound']<0:  # bad review
        return text
        
# Extract ajdectives from each bad review    
def tag_adjectives(text):
    words=nltk.word_tokenize(text)
    tagged=nltk.pos_tag(words)    
    adjectives=[x for x,y in tagged if re.search('JJ',y) or re.search('JJR', y) or re.search('JJS', y)]
    return(adjectives)       
    
# Perform sentiment analysis for the first 500 reviews
    
adj = []   
bad_words = []
all_bad_words = []
word_list = []

with open('negative-words.txt','r') as f:
        all_bad_words = f.read().splitlines()  # bad words reference
for i in range(0,100000): #10,000 rows
    review = clean_text(reviews['text'][i])  # returns processed data    
    neg = sentiment_analysis(review)         # returns the negative review words    
    if neg != None:     
        adj = tag_adjectives(neg)       # contains all adjectives used in a review
        bad_words = [bad for bad in adj if bad in all_bad_words]
        word_list.append(bad_words)  # This is a list of lists -->  [[], [], []]     
        
# Converting list of lists into a flat list containing all the bad words in the review csv
        
words_list = []
for sublist in word_list:
    for item in sublist:
        words_list.append(item)
        
a = set(words_list)  # extracting only the unique bad words
words_list = list(a)   # converting the set back to a list   
print(words_list)

# Assigning negativity score to each bad word based on the star rating

negativity_score = {}
for word in words_list:
    for i in range(0,100000):
        if word in reviews['text'][i]:
            a = []
            a.append(reviews['stars'][i])
    negativity_score[word] = (max(set(a), key = a.count)) # Storing the star rating (i.e negativity score) 
                                                          # corresponding to each bad word

# Printing the bad word and how bad/negative each word is
                                  
for word in negativity_score:
    print(word,negativity_score[word]) # {"bad_word":negativity score}


with open('Negativity_Score.txt','w') as f:
    for word in negativity_score:
        str_write = ''
        str_write = word + ' : '+ str(negativity_score[word])+'\n'
        f.write(str_write)

#####################################################################
        
r = clean_text(reviews['text'][223])
rr = TextBlob(r)        
analyzer=SentimentIntensityAnalyzer()  # Analyzing the intensity of the bad review
sent=analyzer.polarity_scores(rr)
print(tag_adjectives(r))
