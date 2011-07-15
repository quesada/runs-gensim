'''
Created on 15.07.2011

@author: dedan
'''

from gensim import utils
from gensim.corpora.dictionary import Dictionary
from gensim.gensim.utils import SaveLoad
from gensim.models.lsimodel import LsiModel
from gensim.similarities.docsim import MatrixSimilarity
from os import path
import glob
import numpy as np
import re
import string
import sys
import tools

def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    model_path = path.join(base_path,
                           p['result_path'],
                           p['model_label'])
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    dictionary = Dictionary.load(path.join(model_path, p['dict_name']))
    pre = SaveLoad.load(path.join(model_path, 'pre.model'))
    lsi = LsiModel.load(path.join(model_path, 'lsi.model'))

    corpus_path = '/Users/dedan/projects/mpi/data/corpora/fridolin/'
    test_answers, gold_answers, ratings = [], [], []

    flist = glob.glob(path.join(corpus_path, 'corpus_3', '*.txt'))
    for file in flist:
        match = re.search('data3_(\d)_\d+.txt', file)
        ratings.append(int(match.group(1)))
        with open(file) as f:
            doc = string.join(map(string.strip, f.readlines()))
            doc = utils.tokenize(doc)
            corpus = lsi[pre[dictionary.doc2bow(doc)]]
            test_answers.append(corpus)
    flist = glob.glob(path.join(corpus_path, 'corpus_3_golden', '*.txt'))
    for file in flist:
        with open(file) as f:
            doc = string.join(map(string.strip, f.readlines()))
            doc = utils.tokenize(doc)
            corpus = lsi[pre[dictionary.doc2bow(doc)]]
            gold_answers.append(corpus)


    print ratings

    sim = MatrixSimilarity(test_answers)[gold_answers]
    mean_sim = np.mean(sim, axis=0)
    print mean_sim
    print np.corrcoef(ratings, mean_sim)


if __name__ == '__main__':
    main()