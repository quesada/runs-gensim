#!/usr/bin/env python
# encoding: utf-8
"""
model_dim.py

do lower dim analysis on a higher dim model

"""
import matplotlib
matplotlib.use("Agg")
import sys
from os import path
import os

import numpy as np
import pylab as plt
import logging
from datetime import datetime
import tools

from sumatra.parameters import build_parameters
from gensim.models.lsimodel import LsiModel
from gensim.utils import SaveLoad
from gensim.parsing import preprocessing
from gensim.corpora import Dictionary
from gensim import utils, similarities, matutils, models


# read the parameters and create output folder
p = build_parameters(sys.argv[1])
result_path = path.join(p['base_path'], p['result_path'])
output_dir = path.join(result_path, p['sumatra_label'])
lee_corpus = p['base_path'] + p['lee_corpus']
if not path.exists(output_dir):
    os.mkdir(output_dir)
logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
logger.info("running %s" % ' '.join(sys.argv))

# remember starting time for runtime evaluation
start = datetime.now()

# load model and corpus
logger.info('loading word mapping')
dictionary = Dictionary.load(path.join(result_path, p['run'], p['dict_extension']))

model_path = path.join(result_path, p['run'], p['lsi_ext'])
logger.info('load model from: %s' % model_path)
lsi = LsiModel(id2word=dictionary)
if os.path.exists(path.join(result_path, p['run'], 'u.npy')):
    lsi.projection.u = np.load(path.join(result_path, p['run'], 'u.npy'))
    lsi.projection.s = np.load(path.join(result_path, p['run'], 's.npy'))
    lsi.numTerms = len(dictionary)
    lsi.numTopics = np.shape(lsi.projection.s)[0]
else:
    lsi = LsiModel.load(model_path)
pre = SaveLoad.load(path.join(result_path, p['run'], p['pre_model_ext']))


logging.info('load smal lee corpus and preprocess')
with open(lee_corpus, 'r') as f:
    preproc_lee_texts = preprocessing.preprocess_documents(f.readlines())
bow_lee_texts = [dictionary.doc2bow(text,
                                    allowUpdate=False,
                                    return_missing=False)
                for text in preproc_lee_texts]

logger.info('transforming small lee corpus (only pre model)')
corpus_pre = pre[bow_lee_texts]

# read the human similarity data and flatten upper triangular
human_sim_matrix = np.loadtxt(p['base_path'] + p['human_data_file'])
sim_m_size = np.shape(human_sim_matrix)[0]
human_sim_vector = human_sim_matrix[np.triu_indices(sim_m_size, 1)]

max_topics = lsi.numTopics

logger.info("iterate from %d to %d dimensions (stepsize: %d)" %
            (p['min_dim'], max_topics, p['dim_step']))

iter_range = range(p['min_dim'], max_topics, p['dim_step'])
res = np.zeros(len(iter_range))
for k, l in enumerate(iter_range):

    # do the lower dimensionality transformation
    lsi.numTopics = l
    corpus_lsi = lsi[corpus_pre]

    # compute pairwise similarity matrix of transformed corpus
    sim_matrix = np.zeros((len(corpus_lsi), len(corpus_lsi)))
    for i, par1 in enumerate(corpus_lsi):
        for j, par2 in enumerate(corpus_lsi):
            sim_matrix[i, j] = matutils.cossim(par1, par2)
    sim_vector = sim_matrix[np.triu_indices(len(corpus_lsi), 1)]

    # compute correlations
    cor = np.corrcoef(sim_vector, human_sim_vector)
    logger.info("step %d: correlation with lee data: %f" % (k, cor[0, 1]))
    res[k] = cor[0, 1]

plt.figure()
plt.plot(iter_range, res)
plt.savefig(os.path.join(output_dir, 'cor_plot.pdf'))
plt.close()

dif = datetime.now() - start
logger.info("finished after %d days and %d secs" % (dif.days, dif.seconds))