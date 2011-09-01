#!/usr/bin/env python
# encoding: utf-8
"""

correlate wikipedia article similarity with human perceived similarity of terms

Created by Stephan Gabler on 2011-05-12.
"""

from gensim import models, matutils
from gensim.corpora import Dictionary
from gensim.gensim.models.lsimodel import LsiModel
from gensim.similarities.docsim import MatrixSimilarity
from os import path, mkdir
from sumatra.parameters import build_parameters
import matplotlib
import numpy as np
import pickle
import pylab as plt
import sys
import time
import tools
matplotlib.use("Agg")


def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    result_path = path.join(base_path, p['result_path'])
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    logger.info('loading models and dictionary')
    dictionary = Dictionary.load(path.join(result_path,
                                           p['model_label'],
                                           'dic.dict'))
    model_path = path.join(result_path, p['model_label'])
    lsi = LsiModel.load(path.join(model_path, 'lsi.model'))
    pre = pickle.load(open(path.join(model_path, 'pre.model')))
    lsi.num_topics = p['num_topics']

    logger.info('load wikipedia articles')
    article_path = path.join(result_path, p['article_label'])
    wiki = pickle.load(open(path.join(article_path, 'articles.pickle')))

    times = np.zeros((1, len(wiki)))
    count = 0
    for query_key, query in wiki.iteritems():
        logger.info("working on: %s" % query_key)
        n = len(query)
        human = [val['rating'] for val in query.itervalues()]

        t0 = time.time()
        corpus = [lsi[pre[dictionary.doc2bow(val['text'])]]
                    for val in query.itervalues()]
        sim_res = MatrixSimilarity(corpus)[corpus]
        sim_res.save(path.join(output_dir, 'sim_' + query_key))
        avg = np.mean(sim_res, axis=0)
        idx = np.argsort(avg)
        times[count] = time.time() - t0

        # compute correlation with human rating
        res = np.zeros((n, 1))
        for i in range(n):
            human_r = [human[j] for j in idx[i:]]
            res[i, 0] = np.mean(human_r)

        # plot correlation
        fig = plt.figure()
        ax = fig.add_subplot(3, 1, 1)
        ax.plot(res)

        ax = fig.add_subplot(3, 1, 2)
        ratings = [val['rating'] for val in query.itervalues()]
        ax.scatter(avg[idx], [ratings[i] for i in idx])

        # plot similarity distribution
        ax = fig.add_subplot(3, 1, 3)
        ax.bar(range(n), avg[idx])

        # Set the x tick labels to the group_labels defined above and rotate
        ax.set_xticks(range(n))
        k = [key + ' ' + str(query[key]['rating']) for key in query.keys()]
        ax.set_xticklabels([k[i] for i in idx])
        fig.autofmt_xdate()
        plt.savefig(path.join(output_dir, query_key + '.' + p['format']))
        plt.close()
    logger.info('average similarity calculation time: %f' % np.mean(times))

if __name__ == '__main__':
    main()
