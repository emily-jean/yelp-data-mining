"""
    Run the file using 'python topicmodels.py sentiment num_of_topics num_of_words'
    - sentiment is positive/negative
    - num_of_topics is integer
    - num_of_words is integer
"""

import pymysql
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import gensim
from gensim import corpora,models
from collections import defaultdict
import sys
from datetime import datetime
import pyLDAvis.gensim
import warnings


def process_review(review):
    tokens = tokenizer.tokenize(str(review).lower())
    stopped_tokens = [i for i in tokens if not i in stopWords]
    stopped_tokens = [word for word in stopped_tokens if word.isalpha()]
    stopped_tokens = bigram[stopped_tokens]
    tokens = [i for i in stopped_tokens]
    return tokens


def print_time():
    print("Current Time: " + str(datetime.now()))
    print("Time elapsed until now: " + str(datetime.now() - start_time))
    print("\n")


def train_models(topics, words):

    print("Latent Dirichlet Allocation......")
    lda = models.LdaModel(doc_term_matrix, id2word=dictionary, alpha='auto', num_topics=topics, passes=20, iterations=50)
    print_time()

    print_topics(lda,topics,words)
    print_time()


def print_topics(lda,topics,words):
    print(lda.print_topics(-1, words))

    lda_vis = pyLDAvis.gensim.prepare(lda, doc_term_matrix, dictionary)
    # pyLDAvis.display(lda_vis)
    pyLDAvis.save_html(lda_vis, 'visualization_'+sentiment+'_'+str(topics)+'.html')


start_time = datetime.now()
warnings.filterwarnings("ignore", category=DeprecationWarning)
print("Start time of program: " + str(start_time))
sentiment = sys.argv[1]
isPositiveReview = ">3" if sentiment == "positive" else "<3"
number_of_topics = sys.argv[2]
number_of_words = sys.argv[3]
tokenizer = RegexpTokenizer(r'\w+')
stopWords = set(stopwords.words('english'))
db_uri = "mysql+pymysql://root:root@localhost:3306/yelp_db"
Lda = gensim.models.ldamodel.LdaModel
connection = pymysql.connect(host='localhost', user='root', password='root', db='yelp_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

sql = """select top_biz.stars,top_biz.id,review.text FROM \
  (select * \
   from business \
   where business.review_count > 200 and business.city = 'Pittsburgh'\
   ORDER BY review_count DESC \
   ) top_biz \
INNER join review on top_biz.id = review.business_id and review.stars """ + isPositiveReview + """ \
INNER join category on category.business_id = top_biz.id and category.category = 'Restaurants' \
ORDER BY top_biz.review_count DESC;"""

df = pd.read_sql(sql, connection)
bigram = gensim.models.phrases.Phrases(df.text)
df['review_tokens'] = df.text.apply(process_review)

print(df.head(len(df)))
doc_clean = df.review_tokens
frequency = defaultdict(int)

for text in doc_clean:
    for token in text:
        frequency[token] += 1


processed_corpus = [[token for token in text if frequency[token] > 10] for text in doc_clean]

dictionary = corpora.Dictionary(processed_corpus)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_corpus]

train_models(100, 3)