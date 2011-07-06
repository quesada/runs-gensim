#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This run produces an LSI model with Tfidf or log_entropy preprocessing.
"""

from datetime import datetime
from gensim import utils, similarities, matutils, models
from gensim.corpora import Dictionary, MmCorpus
from gensim.models.logentropy_model import LogEntropyModel
from gensim.models.tfidfmodel import TfidfModel
from gensim.parsing import preprocessing
from os import path
import numpy as np
import os
import sys
import tools


def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    working_corpus = path.join(base_path, p['corpus_path'], p['corpus_name'])
    human_data_file = path.join(base_path, p['human_data_file'])
    lee_corpus = path.join(base_path, p['lee_corpus'])
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    # remember starting time for runtime evaluation
    start = datetime.now()

    logger.info('loading word mapping')
    dictionary = Dictionary.load(path.join(base_path,
                                           p['corpus_path'],
                                           p['dict_name']))
    Dictionary.save(dictionary, path.join(output_dir, p['dict_name']))
    logger.info(dictionary)

    logger.info('loading corpus')
    corpus_bow = MmCorpus(working_corpus)

    logger.info("create preprocessing model and save it to disk")
    if p['pre_model'] == 'tfidf':
        pre_model = TfidfModel(corpus_bow, id2word=dictionary, normalize=True)
    elif p['pre_model'] == 'log_ent':
        pre_model = LogEntropyModel(corpus_bow,
                                    id2word=dictionary, normalize=True)
    else:
        raise ValueError('model parameter %s not known' % p['pre_model'])
    pre_model.save(os.path.join(output_dir, p['pre_model_extension']))

    logger.info('initialize LSI model')
    lsi = models.LsiModel(pre_model[corpus_bow],
                          id2word=dictionary, num_topics=p['num_topics'])
    lsi.save(os.path.join(output_dir, p['lsi_extension']))
    logger.info('finished --> lsi model saved to: %s' %
                os.path.join(output_dir, p['lsi_extension']))

    # check for correlation with lee human data
    logger.info('load smal lee corpus and preprocess')
    with open(lee_corpus, 'r') as f:
        preproc_lee_texts = preprocessing.preprocess_documents(f.readlines())
    bow_lee_texts = [dictionary.doc2bow(text,
                                        allow_update=False,
                                        return_missing=False)
                    for text in preproc_lee_texts]

    logger.info('transforming small lee corpus (LSI)')
    corpus_lsi = lsi[pre_model[bow_lee_texts]]

    # # compute pairwise similarity matrix of transformed corpus
    sim_matrix = np.zeros((len(corpus_lsi), len(corpus_lsi)))
    for i, par1 in enumerate(corpus_lsi):
        for j, par2 in enumerate(corpus_lsi):
            sim_matrix[i, j] = matutils.cossim(par1, par2)
    sim_vector = sim_matrix[np.triu_indices(len(corpus_lsi), 1)]

    # read the human similarity data and flatten upper triangular
    human_sim_matrix = np.loadtxt(human_data_file)
    sim_m_size = np.shape(human_sim_matrix)[0]
    human_sim_vector = human_sim_matrix[np.triu_indices(sim_m_size, 1)]

    # compute correlations
    cor = np.corrcoef(sim_vector, human_sim_vector)
    logger.info("correlation with lee human data: %f" % cor[0, 1])

    dif = start - datetime.now()
    logger.info("finished after %d days and %d secs" % (dif.days, dif.seconds))


if __name__ == '__main__':
    main()
