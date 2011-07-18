# coding=utf-8

'''
Created on 15.07.2011

this file will contain some research on the dictionary. The reason ist that I
once created a dictionary from the german wikipedia and I set the no_above
in filter_extremes to 0.5. The rationale was to avoid a stoplist.

But then during the training of a LSI model with this dictionary I saw that
there was a topic containing:
0.211*"von" + 0.180*"f�r" + 0.176*"im" + 0.174*"er" + 0.172*"den" + 0.167*"de
s" + 0.164*"das" + 0.153*"mit" + 0.142*"dem" + 0.141*"wurde"

This was suprising for me, I thought that at least the article "das" should
appear in at least 50% of the documents and therefore be filtered out. I guess
the problem is that there are many very very short articles that don't contain
even the articles.

So in this file I'll do some experiments on the no_obove value to filter
out stopwords without a explicit list.

@author: dedan
'''

from __future__ import division
from gensim.corpora.dictionary import Dictionary
import pylab as plt
import numpy as np

min_freq = 1000
n_words  = 200

stoplist = open('/Users/dedan/projects/mpi/data/stoplists/german_stoplist.txt').readlines()
stoplist = [unicode(s.strip(), encoding='utf-8').lower() for s in stoplist]
dic = Dictionary.load('/Users/dedan/projects/mpi/data/results/20110628-170809/dic.dict')


# word frequncy distibution of the dictionary
freqs = np.array(dic.dfs.values())
freqs = freqs[freqs > min_freq]
plt.figure()
plt.subplot(3,1,1)
plt.hist(freqs, bins=100)
plt.title('distribution of word frequencies with frequency > %s' % min_freq)

# most frequent words in the dictionary
freqs   = np.array([dic.dfs[dic.token2id[key]] for key in dic.token2id.keys()])
words   = dic.token2id.keys()
idx     = np.argsort(freqs)
freqs   = freqs[idx[-n_words:]]
words   = [words[i] for i in idx[-n_words:]]

plt.subplot(3,1,2)
plt.bar(range(len(freqs)), freqs)
plt.title('word frequencies of the %d most frequent words' % n_words)

print 'word frequencies of the %d most frequent words' % n_words
for i in reversed(range(len(words))):
    print "%s%d" % (words[i].ljust(20), freqs[i])


# fraction of the most frequent words which are also in the stoplist?
frac = len(set(words) & set(stoplist)) / len(words)
print '\nfraction of most freq words which are also in stoplist: %f \n' % frac


# which words are already stopped by the no_above 0.5? wordnames and fraction
stopped = [stopword for stopword in stoplist if not dic.doc2bow([stopword])]
print 'the following words got stopped by the no_obove=0.5 filtering:'
for word in stopped:
    print '\t%s' % word


# document frequencies for the stopwords
doc_freqs = [dic.dfs[dic.token2id[stopword]] for stopword in stoplist if dic.token2id.has_key(stopword)]
plt.subplot(3,1,3)
plt.bar(range(len(doc_freqs)), sorted(doc_freqs))
plt.title('document frequencies of the stopwords')



stoplist_fraction = float(len(dic.doc2bow(stoplist))) / float(len(stoplist))
print '\nfraction of stoplist words in dict: %f\n' % stoplist_fraction

idx = np.argsort(doc_freqs)
stop2 = [stopword for stopword in stoplist if dic.token2id.has_key(stopword)]
doc_freqs = [doc_freqs[i] for i in idx]
stop2 = [stop2[i] for i in idx]
doc_freqs.reverse()
stop2.reverse()
s = np.cumsum(doc_freqs)
s = s / np.max(s)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
valid = s < 0.8
x = np.array(doc_freqs)[valid]
ax.set_xticks(range(len(valid)))

plt.bar(range(len(x)), x)
labels = [stop2[i] for i, val in enumerate(valid) if val]
ax.set_xticklabels(labels)
fig.autofmt_xdate()
plt.title('stopword frequencies')


plt.show()


print " "
print """ remaining open questions

    unsre
    unsrem
    unsren
    unsrer
    unsres

    were stopped by the no_obove=0.5 criterion. Is it possible that they
    are more frequent than the article 'das'?

    can the filter_extremes be used instead of a stoplist? if not, why not?
    To a certain degree: yes. The most frequent words are stopwords. The problem
    would be to find a criterion where to cut off? Because later in the list of
    the 200 most frequent there are words like 'politician' and 'american' which
    definitively carry meaning.

"""