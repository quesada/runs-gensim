#!/usr/bin/env python
# encoding: utf-8
"""

correlate wikipedia article similarity with human perceived similarity of terms

Created by Stephan Gabler on 2011-05-12.
"""

import sys
from os import path, mkdir

import string
import pickle
import time

import tools
import matplotlib
matplotlib.use("Agg")
import numpy as np
import pylab as plt
import scipy.stats
from sumatra.parameters import build_parameters
from gensim import models, matutils
from gensim.corpora import Dictionary
from gensim.similarities.docsim import MatrixSimilarity

# read the parameters, create output folder and logger
p = build_parameters(sys.argv[1])
result_path = path.join(p['base_path'], p['result_path'])
output_dir = path.join(result_path, p['sumatra_label'])
if not path.exists(output_dir):
    mkdir(output_dir)
logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
logger.info("running %s" % ' '.join(sys.argv))

logger.info('loading models and dictionary')
dictionary = Dictionary.loadFromText(path.join(p['base_path'], p['dict_path']))
model_path = path.join(result_path, p['model_label'])
lsi = pickle.load(open(path.join(model_path, 'lsi.model')))
pre = pickle.load(open(path.join(model_path, 'pre.model')))
lsi.numTopics = p['num_topics']

logger.info('load wikipedia articles')
article_path = path.join(result_path, p['article_label'])
wiki = pickle.load(open(path.join(article_path, 'articles.pickle')))
info = pickle.load(open(path.join(article_path, 'info.pickle')))

times = np.zeros((1,len(wiki)))
count = 0
for query_key, query in wiki.iteritems():
    logger.info("working on: %s" % query_key)
    n = len(query)
    human = [val['rating'] for val in query.itervalues()]
    sim_res = np.zeros((n,n))

    t0 = time.time()
    corpus = [lsi[pre[dictionary.doc2bow(val['text'])]] for val in query.itervalues()]
    sim_res = MatrixSimilarity(corpus)[corpus]
    avg = np.mean(sim_res, axis=0)
    idx = np.argsort(avg)
    times[count] = time.time() - t0

    # compute correlation with human rating
    res = np.zeros((n,2))
    for i in range(n):
        human_r = [human[j] for j in sorted(idx[i:])]
        avg_r = [avg[j] for j in sorted(idx[i:])]
        r, p_v = scipy.stats.pearsonr(human_r, avg_r)
        res[i,0] = r
        res[i,1] = p_v

    # plot correlation
    fig = plt.figure()
    ax = fig.add_subplot(3,1,1)
    ax.plot(res)
    ax.legend(['r', 'p'])

    ax = fig.add_subplot(3,1,2)
    ratings = [val['rating'] for val in query.itervalues()]
    ax.scatter(avg[idx], [ratings[i] for i in idx])

    # plot similarity distribution
    ax = fig.add_subplot(3,1,3)
    ax.bar(range(n), avg[idx])

    # Set the x tick labels to the group_labels defined above and rotate labels
    ax.set_xticks(range(n))
    k = [key + ' ' + str(query[key]['rating']) for key in query.keys()]
    ax.set_xticklabels([k[i] for i in idx])
    fig.autofmt_xdate()
    plt.savefig(path.join(output_dir, query_key + '.' + p['format']))
    plt.close()
logger.info('average similarity calculation time: %f' % np.mean(times))
