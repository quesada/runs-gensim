'''
Created on 15.06.2011

@author: dedan
'''
from nose.tools import assert_true, assert_equal, assert_almost_equals
from os import path
import model_dim_task
import numpy as np

out_dir = path.join(path.dirname(__file__),
                    'data',
                    'results',
                    'test')


def test_output_exists():
    """test whether all output files were created"""
    global out_dir
    assert_true(path.exists(path.join(out_dir, 'run.log')))
    assert_true(path.exists(path.join(out_dir, 'lsi.model')))
    assert_true(path.exists(path.join(out_dir, 'pre.model')))
    assert_true(path.exists(path.join(out_dir, 'dic.dict')))
    assert_true(path.exists(path.join(out_dir, 'lsi.model.npy')))


def test_cor_plot_exits():
    """check whether output of model_dim_task exists"""
    global out_dir
    dim_param_file = path.join(path.dirname(__file__),
                               'param_files',
                               'model_dim_test.param')
    model_dim_task.main(dim_param_file)
    assert_true(path.exists(path.join(out_dir, 'cor_plot.png')))

def test_model_dim_cor_correct():
    """are the right values for model dim correlation computed?"""
    global out_dir
    correct = np.array([ 0.12538605,  0.29167289,  0.32614645])
    res = np.load(path.join(out_dir, 'model_dim_res.npy'))
    assert_almost_equals(res[0], correct[0], 1)
    assert_almost_equals(res[1], correct[1], 1)
    assert_almost_equals(res[2], correct[2], 1)

