'''
Created on 15.06.2011

@author: dedan
'''
from nose.tools import assert_true
from os import path
import model_dim_task

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
