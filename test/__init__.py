"""
This folder contains the unittests for runs-gensim
"""
from os import path
import get_wiki_articles_run
import lsi_model_run
import model_dim_task
import shutil


def setup_package(self):
    """
    setup runs the RUNs, which are the files that have a quite long
    execution time. The results of these files are needed in all
    the tests and should not be computed all the time
    """
    global out_dir
    lsi_param_file = path.join(path.dirname(__file__),
                               'param_files',
                               'lsi_model_test.param')
    wiki_param_file = path.join(path.dirname(__file__),
                                'param_files',
                                'get_wiki_articles_test.param')
    out_dir = path.join(path.dirname(__file__),
                        'data',
                        'results',
                        'test')
    lsi_model_run.main(lsi_param_file)
    get_wiki_articles_run.main(wiki_param_file)


def teardown_package():
    """remove all the data created in the runs"""
    global out_dir
    shutil.rmtree(out_dir)

