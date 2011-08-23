

import oshea2json_run
from os import path
import codecs

def setup_test():
    """create the jsoncorpus"""
    global out_dir, cor_dir
    out_dir = path.join(path.dirname(__file__),
                        'data',
                        'results',
                        'test')
    cor_dir = path.join(path.dirname(__file__),
                        'data',
                        'corpora',
                        'oshea')
    oshea2json_run.main(path.join(path.dirname(__file__),
                               'param_files',
                               'oshea2json_test.param'))
    

def test_output_exists():
    """ test whether the output file exists """
    global out_dir, cor_dir
    assert(path.exists(path.join(out_dir, 'oshea_similarity.json')))

def test_output_correct():
    """test whether output file is correct"""
    global out_dir, cor_dir
    out = codecs.open(path.join(out_dir, 'oshea_similarity.json'),
                      mode='r', encoding='utf-8')
    inp = codecs.open(path.join(cor_dir, 'oshea_similarity.json'),
                    mode='r', encoding='utf-8')
    assert(out.read() == inp.read())
