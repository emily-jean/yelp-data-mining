from sqlalchemy import (create_engine, Table, Column, Integer, String, MetaData, inspect)
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd

'''
    db_uri should be "dialect+driver://username:password@host:port/database"    
'''
db_uri = "mysql+pymysql://root:root@localhost:3306/yelp_db"
engine = create_engine(db_uri)
connection = engine.connect()

inspector = inspect(engine)
print("Tables in the database are " + str(inspector.get_table_names()))

reviews = pd.read_sql("SELECT id,text FROM review limit 10", connection).values

porterStemmer = PorterStemmer()
wordLemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')
reviews_dict = {}
for review in reviews:
    reviewId,reviewText = review
    reviewTokens = []
    ''' import nltk 
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')
    '''
    for token in tokenizer.tokenize(reviewText.lower()):
        if token not in stopwords.words('english'):
            reviewTokens.append(wordLemmatizer.lemmatize(porterStemmer.stem(token)))
    reviews_dict[reviewId] = reviewTokens

print(reviews_dict)