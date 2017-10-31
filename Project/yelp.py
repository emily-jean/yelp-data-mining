from collections import Counter

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


def findFrequentWords(fwdf,sentiment,plotname):
    fwdf = fwdf[(fwdf.sentiment == sentiment)]
    all = fwdf['keywords'].tolist()
    r = []
    for wordlist in all:
        parseList = [x for x in wordlist if not '.' in x]
        parseList = [x for x in parseList if not "'" in x]
        r.extend(parseList)
    words = Counter(" ".join(r).split(" ")).most_common(50)
    df = pd.DataFrame(words, columns=['Word', 'Count'])
    df.plot.bar(x='Word', y='Count')
    plt.savefig(plotname)


def plotRatings(pdf,plotname):
    ratingsdf = pdf.groupby('id')['sentiment', 'stars'].mean().head(pdf.shape[0])
    ratingsdf.columns = ['Ratings from Sentiment Analysis', 'Ratings from Dataset']
    # print(ratingsdf)
    ratingsdf.plot.hist(alpha=0.5)
    plt.savefig(plotname)


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
INNER join category on category.business_id = top_biz.id and category.category = 'Restaurants' \
ORDER BY top_biz.review_count DESC;"""

df = pd.read_sql(sql, connection)
# blob = TextBlob("some random text where you!! extract intelligent key word with an, new boy and an rein deer dear")
df['keywords'] = df.apply(lambda row: TextBlob(row.text).noun_phrases, axis=1)
df['polarity'] = df.apply(lambda row: TextBlob(row.text).polarity,axis=1)
df['sentiment'] = df.apply(lambda row: -5 if row.polarity < 0 else 5,axis=1)

findFrequentWords(df,-5,'top50_negativereviews')
findFrequentWords(df,5,'top50_positivereviews')
#plotRatings(df,'sentimentanalysis.png')



