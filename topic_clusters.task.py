#!/usr/bin/env python
# encoding: utf-8
"""
clusters.py

with get_wiki_articles I download the wikipedia articles for all results of a
sparql query. These articles are then transformed to an lsi space and
projected on the first 2 principal components of this space in order to look
for clusters. This script only saves the cluster data to a file which can
then be visualized with the corresponding viewer.
"""

import sys
import os
from os import path
import pickle

import numpy as np
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

data = {}
for topic, entries in wiki.iteritems():
    logger.info('working on: %s' % topic)

    data[topic] = {}
    data[topic]['keys'] = []
    data[topic]['vecs'] = []
    data[topic]['ratings'] = []
    for key, val in entries.iteritems():
        data[topic]['keys'].append(key)
        data[topic]['vecs'].append(lsi[pre[dictionary.doc2bow(val['text'])]])
        data[topic]['ratings'].append(val['rating'])
    data[topic]['vecs'] = np.squeeze(np.array(data[topic]['vecs'])[:,:, 1:2]).T

    U, d, V = np.linalg.svd(data[topic]['vecs'], full_matrices=False)
    data[topic]['U'] = U
    data[topic]['d'] = d

f = open(os.path.join(output_dir, "data.pickle"), 'wb')
pickle.dump(data, f)
