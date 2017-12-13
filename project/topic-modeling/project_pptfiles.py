import pickle
from collections import defaultdict
from gensim import corpora,models
import pyLDAvis.gensim
from datetime import datetime
import warnings
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def print_time():
    print("Current Time: " + str(datetime.now()))
    print("Time elapsed until now: " + str(datetime.now() - start_time))
    print("\n")


def generate_ldavis(lda, corpus, dictionary, filename):
    print("Latent Dirichlet Allocation......")
    print_time()
    lda_vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(lda_vis, "pyldavis_"+filename+".html")


def topic_modeling(docs, filename, freq):
    frequency = defaultdict(int)

    for text in docs:
        for token in text:
            frequency[token] += 1

    processed_corpus = [[token for token in text if frequency[token] > freq] for text in docs]

    dictionary = corpora.Dictionary(processed_corpus)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in processed_corpus]
    lda = models.LdaModel(doc_term_matrix, id2word=dictionary, num_topics=18, passes=20, iterations=50)
    generate_ldavis(lda, doc_term_matrix, dictionary,filename)
    #generate_wordclouds(lda,12)
    #lmlist, c_v = evaluate_graph(filename, dictionary,doc_term_matrix,processed_corpus,limit=50)


def generate_wordclouds(lda, topic_count):
    print("Latent Dirichlet Allocation......")
    print_time()
    for i in range(topic_count):
        wordcloud.fit_words(dict(lda.show_topics(i+1,200,formatted=False)[0][1])).to_file('wordcloud_negative_'+str(i+1)+'.png')


def evaluate_graph(filename, dictionary, corpus, texts, limit):
    coherence_values = {}
    lda_models = {}
    for num_topics in range(1, limit):
        lm = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
        lda_models[num_topics] = lm
        cm = models.CoherenceModel(model=lm, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values[num_topics] = cm.get_coherence()

    x = list(coherence_values.keys())
    y = list(coherence_values.values())
    plt.plot(x,y)
    plt.xlabel("num_topics")
    plt.ylabel("Coherence score")
    plt.legend(("c_v"), loc='best')
    plt.show()
    plt.savefig(filename+"_coherence-topic.pdf",bbox_inches='tight')
    return lda_models,coherence_values


wordcloud = WordCloud()
start_time = datetime.now()
print("Started the program....")
print_time()
warnings.filterwarnings("ignore", category=DeprecationWarning)
df = pickle.load(open("review_dump.p", "rb"))
df['score'] = df.sentiment.apply(lambda object: object.score)
df['magnitude'] = df.sentiment.apply(lambda object: object.magnitude)

df_positive = df[(df.score > 0)&(df.magnitude > 3)]
df_negative = df[(df.score < 0)&(df.magnitude > 3)]

#topic_modeling(df_negative.review_processed_tokens, "negative", 10)
topic_modeling(df_positive.review_processed_tokens, "positive", 50)
print_time()