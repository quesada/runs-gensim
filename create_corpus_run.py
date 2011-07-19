'''
Created on 27.06.2011

@author: dedan
'''
from gensim.gensim.corpora.jsoncorpus import JsonCorpus
from gensim.corpora.textfilescorpus import TextFilesCorpus
from gensim.gensim.corpora.mmcorpus import MmCorpus
from os import path
import Stemmer
import os
import sys
import tools

def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    logger = tools.get_logger('gensim', os.path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    preprocess = []

    if 'stoplist' in p.as_dict():
        stoplist = open(path.join(base_path, p['stoplist'])).readlines()
        stoplist = [unicode(s.strip(), encoding='utf-8').lower() for s in stoplist]
        def remove_stopwords(sentence):
            return [word for word in sentence if not word in stoplist]
        preprocess.append(remove_stopwords)

    if 'stemmer' in p.as_dict():
        stemmer = Stemmer.Stemmer(p['stemmer'])
        preprocess.append(stemmer.stemWords)

    if p['input'].endswith('.json'):
        cor = JsonCorpus(path.join(base_path, p['input']),
                         no_below=p['no_below'],
                         no_above=p['no_above'],
                         preprocess=preprocess)
    else:
        cor = TextFilesCorpus(path.join(base_path, p['input']),
                      no_below=p['no_below'],
                      no_above=p['no_above'],
                      preprocess=preprocess)

    MmCorpus.serialize(path.join(output_dir, p['corpus_name']), cor, progress_cnt=10000)
    cor.dictionary.save(path.join(output_dir, p['dict_name']))



if __name__ == '__main__':
    main()

