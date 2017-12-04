"""
    Run the file using 'python topicmodels.py sentiment'
    - sentiment is positive/negative/all
    all - all reviews
    positive - positive reviews
    negative - negative reviews
"""
import pdb
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
from wordcloud import WordCloud
import matplotlib.pyplot as plt


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


def generate_wordclouds(lda, topic_count,word_count):
    print("Latent Dirichlet Allocation......")

    print_time()
    print(lda.print_topics(-1, word_count))
    print_time()
    for i in range(topic_count):
        wordcloud.fit_words(dict(lda.show_topics(i+1,200,formatted=False)[0][1])).to_file('lda_'+str(sentiment)+'_'+str(i+1)+'.png')


def generate_ldavis(lda, topic_count, word_count):
    print("Latent Dirichlet Allocation......")

    print(lda.print_topics(-1, word_count))
    print_time()
    lda_vis = pyLDAvis.gensim.prepare(lda, doc_term_matrix, dictionary)
    pyLDAvis.save_html(lda_vis, 'visualization_' + sentiment + '_' + str(topic_count) + '.html')


start_time = datetime.now()
warnings.filterwarnings("ignore", category=DeprecationWarning)
print("Start time of program: " + str(start_time))
sentiment = str(sys.argv[1])
review_rating_check = ""
# number_of_topics = sys.argv[2]
# number_of_words = sys.argv[3]
tokenizer = RegexpTokenizer(r'\w+')
stopWords = set(stopwords.words('english'))
wordcloud = WordCloud()
db_uri = "mysql+pymysql://root:root@localhost:3306/yelp_db"
Lda = gensim.models.ldamodel.LdaModel
connection = pymysql.connect(host='localhost', user='root', password='root', db='yelp_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

if sentiment == 'all' :
    review_rating_check = ">0"
elif sentiment == 'positive' :
    review_rating_check = ">3"
else:
    review_rating_check = "<3"

sql = """select top_biz.stars,top_biz.id,review.text FROM \
  (select * \
   from business \
   where business.review_count > 200 and business.city = 'Pittsburgh'\
   ORDER BY review_count DESC \
   limit 2) top_biz \
INNER join review on top_biz.id = review.business_id and review.stars """ + review_rating_check + """ \
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

pdb.set_trace()
processed_corpus = [[token for token in text if frequency[token] > 10] for text in doc_clean]

dictionary = corpora.Dictionary(processed_corpus)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_corpus]

lda = models.LdaModel(doc_term_matrix, id2word=dictionary, num_topics=50, passes=20, iterations=50)

#generate_wordclouds(lda, 50, 3)
generate_ldavis(lda, 50, 3)