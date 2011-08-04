'''
Created on 04.08.2011

@author: dedan
'''

import tools

def setup_test():
    global senna_path
    senna_path = '/Users/dedan/Downloads/senna-v2.0/'

def test_short_sentence():
    """tag a simple and short sentence"""
    tagged = tools.tag('Alcohol is very good for you', senna_path)
    assert tagged[0]['term'] == 'Alcohol'
    assert not 'base' in tagged[0]
    assert [len(tag) for tag in tagged] == [3, 3, 3, 3, 3, 3]
    
def test_sentence_with_loc():
    """tag a sentence that contains a location"""
    tagged = tools.tag('To drink alcohol is very good for you in Berlin', senna_path)
    assert 'base' in tagged[1]
    assert tagged[1]['base'] == 'drink'
    assert tagged[-1]['ner'] == "S-LOC"


