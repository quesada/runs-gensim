'''
Created on 27.06.2011

@author: dedan
'''
from gensim.gensim.corpora.mmcorpus import MmCorpus
from gensim.gensim.corpora.jsoncorpus import JsonCorpus
from os import path
import os
import sys
import tools

def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    logger = tools.get_logger('gensim', os.path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    cor = JsonCorpus(path.join(base_path, p['wiki_json']),
                     no_below=p['no_below'],
                     no_above=p['no_above'])
    MmCorpus.serialize(path.join(output_dir, p['corpus_name']), cor, progress_cnt=10000)
    cor.dictionary.save(path.join(output_dir, p['dict_name']))



if __name__ == '__main__':
    main()

