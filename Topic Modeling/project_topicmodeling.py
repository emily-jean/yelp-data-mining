import pickle
from collections import defaultdict
from gensim import corpora,models
import pyLDAvis.gensim
from datetime import datetime
import warnings


def print_time():
    print("Current Time: " + str(datetime.now()))
    print("Time elapsed until now: " + str(datetime.now() - start_time))
    print("\n")


def generate_ldavis(lda, doc_term_matrix, dictionary, filename):
    print("Latent Dirichlet Allocation......")
    print_time()
    lda_vis = pyLDAvis.gensim.prepare(lda, doc_term_matrix, dictionary)
    pyLDAvis.save_html(lda_vis,filename)


def topic_modeling(docs, filename, freq):
    frequency = defaultdict(int)

    for text in docs:
        for token in text:
            frequency[token] += 1

    processed_corpus = [[token for token in text if frequency[token] > freq] for text in docs]

    dictionary = corpora.Dictionary(processed_corpus)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_corpus]
    lda = models.LdaModel(doc_term_matrix, id2word=dictionary, num_topics=50, passes=20, iterations=50)
    generate_ldavis(lda, doc_term_matrix, dictionary,filename)


start_time = datetime.now()
warnings.filterwarnings("ignore", category=DeprecationWarning)
df = pickle.load(open("review_dump.p", "rb"))
df['score'] = df.sentiment.apply(lambda object: object.score)
df['magnitude'] = df.sentiment.apply(lambda object: object.magnitude)

df_positive = df[(df.score > 0)&(df.magnitude > 3)]
df_negative = df[(df.score < 0)&(df.magnitude > 3)]

topic_modeling(df_negative.review_processed_tokens, "pyldavis_negative.html", 10)
topic_modeling(df_positive.review_processed_tokens, "pyldavis_positive.html", 50)
print_time()