#!/usr/bin/env python
# encoding: utf-8
"""
clusters.py

with get_wiki_articles I download the wikipedia articles for all results of a
sparql query. These articles are then transformed to an lsi space and
projected on the first 2 principal components of this space in order to look
for clusters. The points in the plots are colored (grayscaled) by the value
a human gave as rating of how good this term fits the sparqle query termn.
"""

import sys
import os
from os import path
import pickle

import matplotlib
matplotlib.use("Agg")
import numpy as np
import pylab as plt
from gensim.corpora import Dictionary
from sumatra.parameters import build_parameters
import tools

# setup
p = build_parameters(sys.argv[1])
result_path = path.join(p['base_path'], p['result_path'])
output_dir = path.join(result_path, p['sumatra_label'])
if not path.exists(output_dir):
    os.mkdir(output_dir)
logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
logger.info("running %s" % ' '.join(sys.argv))

logger.info('load the articles..')
article_path = path.join(result_path, p['article_label'])
wiki = pickle.load(open(path.join(article_path, 'articles.pickle')))

logger.info('load dictionary and models')
dictionary = Dictionary.loadFromText(path.join(p['base_path'], p['dict_path']))
model_path = path.join(result_path, p['model_label'])
lsi = pickle.load(open(path.join(model_path, 'lsi.model')))
pre = pickle.load(open(path.join(model_path, 'pre.model')))
if int(p['num_topics']) > lsi.numTopics:
    logger.error('model to small')
lsi.numTopics = int(p['num_topics'])

for topic, data in wiki.iteritems():
    logger.info('working on: %s' % topic)

    keys = []
    vecs = []
    ratings = []
    for key, val in data.iteritems():
        keys.append(key)
        vecs.append(lsi[pre[dictionary.doc2bow(val['text'])]])
        ratings.append(val['rating'])
    vecs = np.squeeze(np.array(vecs)[:,:, 1:2]).T

    U, d, V = np.linalg.svd(vecs, full_matrices=False)
    proj = np.dot(U[:,0:2].T, vecs)

    plt.figure()
    plt.subplot(2,1,1)
    for i in range(proj.shape[1]):
        col = (1- (ratings[i] / 100.0)) * 0.7
        plt.plot(proj[0, i], proj[1, i], '.', color=('%f' % col))
    plt.subplot(2,1,2)
    plt.plot(d)
    plt.savefig(path.join(output_dir, topic + '.' + p['format']))
    plt.close()
