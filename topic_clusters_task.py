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

from gensim.corpora import Dictionary
from os import path
import numpy as np
import os
import pickle
import sys
import tools


def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    result_path = path.join(base_path, p['result_path'])
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    logger.info('load the articles..')
    article_path = path.join(result_path, p['article_label'])
    wiki = pickle.load(open(path.join(article_path, 'articles.pickle')))

    logger.info('load dictionary and models')
    dictionary = Dictionary.load(path.join(result_path,
                                           p['dict_label'],
                                           p['dict_extension']))
    model_path = path.join(result_path, p['model_label'])
    lsi = pickle.load(open(path.join(model_path, 'lsi.model')))
    pre = pickle.load(open(path.join(model_path, 'pre.model')))
    if int(p['num_topics']) > lsi.num_topics:
        logger.error('model to small')
    lsi.num_topics = int(p['num_topics'])

    data = {}
    for topic, entries in wiki.iteritems():
        logger.info('working on: %s' % topic)

        data[topic] = {}
        data[topic]['keys'] = []
        vecs = []
        data[topic]['ratings'] = []
        for key, val in entries.iteritems():
            data[topic]['keys'].append(key)
            vecs.append(lsi[pre[dictionary.doc2bow(val['text'])]])
            data[topic]['ratings'].append(val['rating'])
        data[topic]['vecs'] = np.squeeze(np.array(vecs)[:, :, 1:2]).T

        U, d, _ = np.linalg.svd(data[topic]['vecs'], full_matrices=False)
        data[topic]['U'] = U
        data[topic]['d'] = d

    f = open(os.path.join(output_dir, "data.pickle"), 'wb')
    pickle.dump(data, f)

if __name__ == '__main__':
    main()
