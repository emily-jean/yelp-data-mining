from sqlalchemy import (create_engine, Table, Column, Integer, String, MetaData, inspect)
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import pymysql
from textblob import TextBlob
import matplotlib.pyplot as plt

'''
    db_uri should be "dialect+driver://username:password@host:port/database"    
    pip install -U textblob
    python -m textblob.download_corpora
'''

db_uri = "mysql+pymysql://root:root@localhost:3306/yelp_db"

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='yelp_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

sql = """select top_biz.stars,top_biz.id,review.text FROM \
  (select * \
   from business \
   where business.review_count > 200 and business.city = 'Pittsburgh'\
   ORDER BY review_count DESC \
   ) top_biz \
INNER join review on top_biz.id = review.business_id \
ORDER BY top_biz.review_count DESC;"""

df = pd.read_sql(sql,connection)

df['polarity'] = df.apply(lambda row: TextBlob(row.text).polarity,axis=1)
df['sentiment'] = df.apply(lambda row: -5 if row.polarity < 0 else 5,axis=1)
ratingsdf = df.groupby('id')['sentiment', 'stars'].mean().head(df.shape[0])
ratingsdf.columns = ['Ratings from Sentiment Analysis', 'Ratings from Dataset']
#print(ratingsdf)

ratingsdf.plot.hist(alpha=0.5)
plt.savefig('sentimentanalysis.png')






