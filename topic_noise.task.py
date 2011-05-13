#!/usr/bin/env python
# encoding: utf-8
"""

correlate wikipedia article similarity with human perceived similarity of terms

Created by Stephan Gabler on 2011-05-12.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import matplotlib
matplotlib.use("Agg")

import sys
import os

import string
import pickle
from gensim import models
from gensim import matutils
from gensim.corpora import Dictionary
import numpy as np
import pylab as plt
import scipy.stats


def order(l, indices):
    """reorder a list according to the indices"""
    return [l[i] for i in indices]

base = '/Users/dedan/projects/mpi/data/'

# read in the id to word mapping
id_word = {}
with open(base + 'corpora/sparql/id_word.txt') as f:
    for line in f.readlines():
        arr = line.split()
        idx = arr[0]
        word = " ".join(arr[1:])
        id_word[idx] = word

# read in model and dictionary
dictionary = Dictionary.loadFromText(base + "corpora/wiki/wiki-mar2008/head500.noblanks.cor_wordids.txt")
lsi = pickle.load(open(base + "results/20110429-143751/lsi.model"))
pre = pickle.load(open(base + "results/20110429-143751/pre.model"))

# and get all the wikipedia articles
wiki = pickle.load(open(base + "results/test/articles.pickle"))
info = pickle.load(open(base + "results/test/info.pickle"))

not_found = []

#add human rating to the wikipedia data
with open('/Users/dedan/projects/mpi/data/corpora/sparql/reference_queries.txt') as f:
    for line in f.readlines():
        arr = line.split()
        word = id_word[arr[0]]
        term = arr[3]
        try:
            wiki[word][term]['rating'] = int(arr[4])
        except KeyError:
            not_found.append(term)

print len(not_found)
print wiki['hamster']['Adolescent_Radioactive_Black_Belt_Hamsters']['rating']


hamster = wiki['hamster']
n = len(hamster)
res = np.zeros((n,n))

for i, val1 in enumerate(hamster.itervalues()):
    for j, val2 in enumerate(hamster.itervalues()):
        
        bow1 = dictionary.doc2bow(val1['text'])
        bow2 = dictionary.doc2bow(val2['text'])
        res[i,j] = matutils.cossim(lsi[pre[bow1]], lsi[pre[bow2]])
avg = np.mean(res, axis=0)
idx = np.argsort(avg)


human = [hamster[key]['rating'] for key in hamster.keys()]

cor = scipy.stats.pearsonr(human, avg)
print(cor)
cor = scipy.stats.pearsonr(sorted(human), sorted(avg))
print(cor)

res = np.zeros((n,2))
for i in range(n):
    human_r = [human[j] for j in sorted(idx[i:])]
    avg_r = [avg[j] for j in sorted(idx[i:])]
    r, p = scipy.stats.pearsonr(human_r, avg_r)
    res[i,0] = r
    res[i,1] = p

fig = plt.figure()
ax = fig.add_subplot(2,1,1)
ax.plot(res)

ax = fig.add_subplot(2,1,2)
ax.bar(range(n), avg[idx])

# Set the x tick labels to the group_labels defined above and rotate labels
ax.set_xticks(range(n))
k = [key + str(hamster[key]['rating']) for key in hamster.keys()]
ax.set_xticklabels(order(k, idx)) 
fig.autofmt_xdate()

plt.savefig(os.path.join(base, 'results/test/hamster.pdf'))
plt.close()
