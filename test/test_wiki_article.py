'''
Created on 15.06.2011

@author: dedan
'''
from nose.tools import assert_equal, assert_true, assert_not_equal
from os import path
import pickle
import topic_noise_task
import topic_clusters_task

out_dir = path.join(path.dirname(__file__),
                    'data',
                    'results',
                    'test')

def test_output_exists():
    """test whether all output files were created"""
    global out_dir
    assert_true(path.exists(path.join(out_dir, 'run.log')))
    assert_true(path.exists(path.join(out_dir, 'info.pickle')))
    assert_true(path.exists(path.join(out_dir, 'articles.pickle')))

def test_missing_words():
    """ test that missing words get recorded

        when an article for a word in the list cannot be found then record
        this in missing of the info struct
    """
    info = pickle.load(open(path.join(out_dir, 'info.pickle')))
    assert_equal(info['missing'], [u'not_a_hamster'])
    assert_equal(len(info['missing']), 1)

def test_non_ascii():
    """ ommit words that contain non ascii letters, but record them in info"""
    info = pickle.load(open(path.join(out_dir, 'info.pickle')))
    assert_equal(info['non_ascii'], [u'Ry\u016bky\u016b_Scops_Owl'])
    assert_equal(len(info['non_ascii']), 1)

def test_collisions():
    """ sometimes two words get redirected to the same article

        this has to be recorded because if it happens to often we have to
        deal with this
    """
    info = pickle.load(open(path.join(out_dir, 'info.pickle')))
    assert_equal(info['collisions'],
                 {u"Guardians_of_Ga'Hoole#Characters_from_the_books": u'Kludd'})
    assert_equal(len(info['collisions']), 1)

def test_redirs():
    """the program should follow redirections"""
    info = pickle.load(open(path.join(out_dir, 'info.pickle')))
    assert_equal(info['redirs'],
                 {u"Guardians_of_Ga'Hoole#Characters_from_the_books": u'Kludd',
                  u'Mayotte Scops-owl': u'Mayotte_Scops_Owl'})
    assert_equal(len(info['redirs']), 2)

def test_articles():
    """the text attribute for an article should always be non empty"""
    articles = pickle.load(open(path.join(out_dir, 'articles.pickle')))
    for topic in articles.itervalues():
        for entry in topic.itervalues():
            assert_not_equal(entry['text'], "")

def test_rating():
    """a human rating should be added to all articles"""
    articles = pickle.load(open(path.join(out_dir, 'articles.pickle')))
    for topic in articles.itervalues():
        for entry in topic.itervalues():
            assert_true('rating' in entry)

def test_topic_noise():
    """test creation ot topic noise plots"""
    noise_param_file = path.join(path.dirname(__file__),
                                 'param_files',
                                 'topic_noise_test.param')
    topic_noise_task.main(noise_param_file)
    articles = pickle.load(open(path.join(out_dir, 'articles.pickle')))
    for key in articles.keys():
        assert_true(path.exists(path.join(out_dir, key + '.png')))

def test_topic_cluster():
    """test creation of the pickle used in the cluster viewer"""
    cluster_param_file = path.join(path.dirname(__file__),
                                   'param_files',
                                   'topic_clusters_test.param')
    topic_clusters_task.main(cluster_param_file)
    global out_dir
    assert_true(path.exists(path.join(out_dir, 'data.pickle')))
    data = pickle.load(open(path.join(out_dir, 'data.pickle')))
    articles = pickle.load(open(path.join(out_dir, 'articles.pickle')))
    assert_equal(data.keys(), articles.keys())




