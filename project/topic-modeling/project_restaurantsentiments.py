import pickle
import numpy as np
import matplotlib.pyplot as plt


def getPolarity(x):
    if x < -0.25:
        return -1
    elif x > 0.25:
        return 1
    else:
        return 0


df = pickle.load(open("review_dump.p", "rb"))
df['score'] = df.sentiment.apply(lambda object: object.score)
df['magnitude'] = df.sentiment.apply(lambda object: object.magnitude)

df['polarity'] = df.score.apply(lambda x: getPolarity(x))

df_new = df[['id','polarity']]
df_count = df_new.groupby(['id','polarity']).size().reset_index(name='count')

all = list(df_count['count'])

A = np.array([])
B = np.array([])
C = np.array([])

for i in range(0,len(all),3):
    a,b,c = all[i:i+3]
    A = np.append(A,a*1.0/(a+b+c))
    B = np.append(B,b*1.0/(a+b+c))
    C = np.append(C,c*1.0/(a+b+c))

X = np.arange(len(df_count)/3)

# print(A)
# print(B)
# print(C)

# plt.bar(X, A, width=0.8,color='r')
# plt.bar(X, B, width=0.8,color='b', bottom=A)
# plt.bar(X, C, width=0.8,color='g', bottom=A+B)
# plt.show()
# print()

f, ax1 = plt.subplots(1, figsize=(10,5))
bar_width = 0.75
ax1.bar(X,A,bar_width,label='Negative',alpha=0.5,color='r')
ax1.bar(X,B,bar_width,label='Neutral',alpha=0.5,color='b',bottom=A)
ax1.bar(X,C,bar_width,label='Positive',alpha=0.5,color='g',bottom=A+B)

ax1.set_xlabel('Restaurants')
ax1.set_ylabel('% of Reviews')


plt.legend(loc='upper left')
plt.savefig("review_analysis.png",bbox_inches='tight')
print()