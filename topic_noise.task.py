#!/usr/bin/env python
# encoding: utf-8
"""
topic_noise.py

Created by Stephan Gabler on 2011-05-12.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

import string
import pickle
from gensim import models
from gensim import matutils
from gensim.corpora import Dictionary
import numpy as np
import pylab as plt

def order(l, indices):
    """reorder a list according to the indices"""
    return [l[i] for i in indices]



# the format is  queryID- Global ID - Local ID  title  rating confidence

id_word = {}
with open('/Users/dedan/projects/mpi/data/corpora/sparql/id_word.txt') as f:
    for line in f.readlines():
        arr = line.split()
        idx = arr[0]
        word = " ".join(arr[1:])
        id_word[idx] = word


dictionary = Dictionary.loadFromText("/Users/dedan/projects/mpi/data/corpora/wiki/wiki-mar2008/head500.noblanks.cor_wordids.txt")
lsi = pickle.load(open("/Users/dedan/projects/mpi/data/results/20110429-143751/lsi.model"))
pre = pickle.load(open("/Users/dedan/projects/mpi/data/results/20110429-143751/pre.model"))

wiki = pickle.load(open("/Users/dedan/projects/mpi/data/results/sparql_wiki.pickle"))
print wiki['kangaroos'].keys()
with open('/Users/dedan/projects/mpi/data/corpora/sparql/reference_queries.txt') as f:
    for line in f.readlines():
        arr = line.split()
        word = id_word[arr[0]]
        term = string.replace(arr[3], "_", " ")
        wiki[word][term]['rating'] = int(arr[4])


print wiki.keys()
print wiki['hamster']['Adolescent Radioactive Black Belt Hamsters']['rating']
crash

hamster = wiki['hamster']
keys = []
n = len(hamster)
res = np.zeros((n,n))

for i, val1 in enumerate(hamster.itervalues()):
    for j, val2 in enumerate(hamster.itervalues()):
        
        bow1 = dictionary.doc2bow(val1['text'])
        bow2 = dictionary.doc2bow(val2['text'])
        res[i,j] = matutils.cossim(lsi[pre[bow1]], lsi[pre[bow2]])
    
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

avg = np.mean(res, axis=0)
idx = np.argsort(avg)
ax.bar(np.arange(n), avg[idx])

# Set the x tick labels to the group_labels defined above and rotate labels
ax.set_xticks(x)
ax.set_xticklabels(order(hamster.keys(), idx)) 
fig.autofmt_xdate()

plt.show()