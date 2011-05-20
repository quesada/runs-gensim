#!/usr/bin/env python
# encoding: utf-8
"""

correlate wikipedia article similarity with human perceived similarity of terms

Created by Stephan Gabler on 2011-05-12.
"""

import sys
import os
from os import path
import logging

import string
import pickle

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pylab as plt
import scipy.stats
from sumatra.parameters import build_parameters
from gensim import models, matutils
from gensim.corpora import Dictionary


def order(l, indices):
    """reorder a list according to the indices"""
    return [l[i] for i in indices]


# read the parameters and create output folder
parameter_file = sys.argv[1]
p = build_parameters(parameter_file)
result_path = path.join(p['base_path'], p['result_path'])
output_dir = path.join(result_path, p['sumatra_label'])
if not path.exists(output_dir):
    os.mkdir(output_dir)

# set up the logger to print to a file and stdout
logger = logging.getLogger('gensim')
file_handler = logging.FileHandler(path.join(output_dir, "run.log"), 'w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)
logger.info("running %s" % ' '.join(sys.argv))


logger.info('load the id to word mapping')
id_word = {}
with open(os.path.join(p['base_path'], p['sparql_path'], 'id_word.txt')) as f:
    for line in f.readlines():
        idx, word = line.strip().split('\t')
        id_word[idx] = word

logger.info('loading models and dictionary')
dictionary = Dictionary.loadFromText(path.join(p['base_path'], p['dict_path']))
model_path = os.path.join(result_path, p['model_label'])
lsi = pickle.load(open(os.path.join(model_path, 'lsi.model')))
pre = pickle.load(open(os.path.join(model_path, 'pre.model')))

# and get all the wikipedia articles
article_path = os.path.join(result_path, p['article_label'])
wiki = pickle.load(open(os.path.join(article_path, 'articles.pickle')))
info = pickle.load(open(os.path.join(article_path, 'info.pickle')))

not_found = []

#add human rating to the wikipedia data
with open(path.join(p['base_path'], p['sparql_path'], p['human_file'])) as f:
    for line in f.readlines():
        arr = line.split()
        word = id_word[arr[0]]
        term = arr[3]
        try:
            wiki[word][term]['rating'] = int(arr[4])
        except KeyError:
            not_found.append(term)
logger.info("%d words from the reference queries not found" % len(not_found))

for query_key, query in wiki.iteritems():
    logger.info("working on: %s" % query_key)
    n = len(query)
    human = [val['rating'] for val in query.itervalues()]
    sim_res = np.zeros((n,n))

    for i, val1 in enumerate(query.itervalues()):
        for j, val2 in enumerate(query.itervalues()):
            bow1 = dictionary.doc2bow(val1['text'])
            bow2 = dictionary.doc2bow(val2['text'])
            sim_res[i,j] = matutils.cossim(lsi[pre[bow1]], lsi[pre[bow2]])
    avg = np.mean(sim_res, axis=0)
    idx = np.argsort(avg)

    # compute correlation with human rating
    res = np.zeros((n,2))
    for i in range(n):
        human_r = [human[j] for j in sorted(idx[i:])]
        avg_r = [avg[j] for j in sorted(idx[i:])]
        r, p = scipy.stats.pearsonr(human_r, avg_r)
        res[i,0] = r
        res[i,1] = p

    fig = plt.figure()

    # plot correlation
    ax = fig.add_subplot(2,1,1)
    ax.plot(res)
    ax.legend(['r', 'p'])

    # plot similarity distribution
    ax = fig.add_subplot(2,1,2)
    ax.bar(range(n), avg[idx])

    # Set the x tick labels to the group_labels defined above and rotate labels
    ax.set_xticks(range(n))
    k = [key + ' ' + str(query[key]['rating']) for key in query.keys()]
    ax.set_xticklabels(order(k, idx))
    fig.autofmt_xdate()

    plt.savefig(os.path.join(output_dir, query_key + '.pdf'))
    plt.close()
