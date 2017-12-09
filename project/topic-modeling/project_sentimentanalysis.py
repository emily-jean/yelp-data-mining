"""
    sudo pip3 install google-cloud
    Don't share NearBy-48c3bde69f93.json...It is the API_Key
"""

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import pymysql
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from datetime import datetime
import pickle


def process_review(review):
    tokens = tokenizer.tokenize(str(review).lower())
    stopped_tokens = [i for i in tokens if not i in stopWords]
    stopped_tokens = [word for word in stopped_tokens if word.isalpha()]
    tokens = [i for i in stopped_tokens]
    return tokens


def analyze_entities(review):
    document = language.types.Document(content=review, type='PLAIN_TEXT')
    response = client.analyze_entities(document=document, encoding_type='UTF32')
    return [object.name for object in response.entities]


def sentiment_analysis(review):
    document = language.types.Document(content=review, type='PLAIN_TEXT')
    response = client.analyze_sentiment(document=document, encoding_type='UTF32')
    sentiment = response.document_sentiment
    return sentiment


def print_time():
    print("Current Time: " + str(datetime.now()))
    print("Time elapsed until now: " + str(datetime.now() - start_time))
    print("\n")


start_time = datetime.now()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'NearBy-48c3bde69f93.json'
client = language.LanguageServiceClient()
text = 'Hello, world!'
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)
stopWords = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')
sentiment = client.analyze_sentiment(document=document).document_sentiment
print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

connection = pymysql.connect(host='localhost', user='root', password='root', db='yelp_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
sql = """select top_biz.stars,top_biz.id,review.text FROM \
  (select * \
   from business \
   where business.review_count > 200 and business.city = 'Pittsburgh'\
   ORDER BY review_count DESC \
   ) top_biz \
INNER join review on top_biz.id = review.business_id \
INNER join category on category.business_id = top_biz.id and category.category = 'Restaurants' \
ORDER BY top_biz.review_count DESC;"""

df2 = pd.read_sql(sql, connection)
df = df2.head(df2.shape[0])
print_time()
df['review_processed_tokens'] = df.text.apply(process_review)
# df['google_tokens'] = df.text.apply(analyze_entities)
print_time()
df['sentiment'] = df.text.apply(sentiment_analysis)
# df['score'] = df.sentiment.apply(lambda object: object.score)
# df['magnitude'] = df.sentiment.apply(lambda object: object.magnitude)
pickle.dump(df, open("reviews_dump.p", "wb"))
print_time()