'''
Created on 15.06.2011

@author: dedan
'''
from gensim.gensim.corpora.dictionary import Dictionary
from gensim.gensim.corpora.mmcorpus import MmCorpus
from nose.tools import assert_equal, assert_true, assert_not_equal
from os import path
import create_corpus_run
import wp2txt2json_run

out_dir = path.join(path.dirname(__file__),
                    'data',
                    'results',
                    'test')
create_corpus_param_file = path.join(path.dirname(__file__),
                                     'param_files',
                                     'create_corpus_test.param')


def test_corpus_exists():
    """test whether all output files were created"""
    global out_dir
    create_corpus_run.main(create_corpus_param_file)
    assert_true(path.exists(path.join(out_dir, 'corpus.mm')))
    assert_true(path.exists(path.join(out_dir, 'dic1.dict')))

def test_corpus_correct():
    """is the corpus in the right format?"""
    global out_dir
    correct = [[(0, 1.0), (6, 2.0), (7, 1.0)],
               [(0, 2.0), (1, 2.0), (2, 2.0), (3, 1.0), (4, 2.0), (5, 1.0),
                (6, 1.0), (7, 1.0)]]

    cor = MmCorpus(path.join(out_dir, 'corpus.mm'))
    assert_equal(list(cor), correct)

def test_dict_correct():
    """did it create the correct dictionary?"""
    correct = {u'chap': 2,
               u'desc': 7,
               u'first': 6,
               u'of': 1,
               u'one': 3,
               u'second': 4,
               u'sentence': 0,
               u'two': 5}

    d = Dictionary.load(path.join(out_dir, 'dic1.dict'))
    assert_equal(d.token2id, correct)

