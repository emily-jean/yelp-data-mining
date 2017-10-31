from sqlalchemy import (create_engine, Table, Column, Integer, String, MetaData, inspect)
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import pymysql
from textblob import TextBlob

'''
    db_uri should be "dialect+driver://username:password@host:port/database"    
'''
db_uri = "mysql+pymysql://root:root@localhost:3306/yelp_db"

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='yelp_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

sql = "SELECT review.id,review.text FROM review,business where review.business_id = business.id and business.city = 'Pittsburgh' limit 3;"
reviews = pd.read_sql(sql,connection).values
'''
    pip install -U textblob
    python -m textblob.download_corpora
'''
reviewsDict = {}
for review in reviews:
    reviewId,reviewText = review
    blob = TextBlob(reviewText)
    reviewsDict[reviewId] = blob


for k,v in reviewsDict.items():
    print(k)
    print(set(v.words)-set(stopwords.words('english')))
    print(v.noun_phrases)





# engine = create_engine(db_uri)
# connection = engine.connect()

# reviews = pd.read_sql("SELECT id,text FROM review limit 10", connection).values

# porterStemmer = PorterStemmer()
# wordLemmatizer = WordNetLemmatizer()
# tokenizer = RegexpTokenizer(r'\w+')
# reviews_dict = {}
# for review in reviews:
#     reviewId,reviewText = review
#     reviewTokens = []
#     ''' import nltk
#         nltk.download('punkt')
#         nltk.download('wordnet')
#         nltk.download('stopwords')
#     '''
#     for token in tokenizer.tokenize(reviewText.lower()):
#         if token not in stopwords.words('english'):
#             reviewTokens.append(wordLemmatizer.lemmatize(porterStemmer.stem(token)))
#     reviews_dict[reviewId] = reviewTokens
#
# print(reviews_dict)