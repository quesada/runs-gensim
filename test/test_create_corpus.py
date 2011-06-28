'''
Created on 15.06.2011

@author: dedan
'''
from nose.tools import assert_equal, assert_true, assert_not_equal
from os import path
import create_corpus_run

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
    assert_true(path.exists(path.join(out_dir, 'dic.dict')))
