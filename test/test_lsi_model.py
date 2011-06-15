'''
Created on 15.06.2011

@author: dedan
'''
from os import path
import lsi_model_run
import shutil
from nose.tools import assert_true
import model_dim_task

def setUp(self):
    global out_dir
    lsi_param_file = path.join('test',
                               'param_files',
                               'lsi_model_test.param')
    dim_param_file = path.join('test',
                               'param_files',
                               'model_dim_test.param')
    out_dir = path.join('test',
                        'data',
                        'results',
                        'test')
    lsi_model_run.main(lsi_param_file)
    model_dim_task.main(dim_param_file)


def tearDown(self):
    global out_dir
#    shutil.rmtree(out_dir)


def test_output_exists():
    """test whether all output files were created"""
    global out_dir
    assert_true(path.exists(path.join(out_dir, 'run.log')))
    assert_true(path.exists(path.join(out_dir, 'lsi.model')))
    assert_true(path.exists(path.join(out_dir, 'pre.model')))
    assert_true(path.exists(path.join(out_dir, 'dic.dict')))
    assert_true(path.exists(path.join(out_dir, 's.npy')))
    assert_true(path.exists(path.join(out_dir, 'u.npy')))

def test_cor_plot_exits():
    """check whether output of model_dim_task exists"""
    global out_dir
    assert_true(path.exists(path.join(out_dir, 'cor_plot.png')))



