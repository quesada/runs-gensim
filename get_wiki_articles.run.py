#!/usr/bin/env python
# encoding: utf-8
"""


Created by Stephan Gabler on 2011-05-12.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import mwclient
import simplejson
import glob
import codecs
import pickle
import unicodedata as ud
import logging
from datetime import datetime

from sumatra.parameters import build_parameters
from gensim.corpora import wikicorpus
from gensim.parsing.preprocessing import preprocess_string
from urllib import FancyURLopener
from BeautifulSoup import BeautifulStoneSoup as BSS

# setup
parameter_file = sys.argv[1]
p = build_parameters(parameter_file)

output_dir = os.path.join(p['base_path'], p['result_path'], p['sumatra_label'])
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# set up the logger to print to a file and stdout
logger = logging.getLogger('gensim')
file_handler = logging.FileHandler(os.path.join(output_dir, "run.log"), 'w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)
logger.info("running %s" % ' '.join(sys.argv))


articles = {}
all_missing = []
site = mwclient.Site('en.wikipedia.org', '/w/api.php/')

# get all txt files in a folder and iterate over them
filelist = glob.glob(os.path.join(p['base_path'],
                                  p['folder_path'],
                                  "*.txt"))
for f in filelist:

    # get the word we are working on
    f_name = os.path.basename(f)
    k_word = os.path.splitext(f_name)[0]
    logger.info("working on file: %s" % f_name)

    # try to convert the word into ascii for the http query
    file_obj = codecs.open(f, "r", "utf-16")
    counter = 0
    words = []
    for w in file_obj.readlines():
        try:
            s = w.strip().decode('ascii')
            words.append(s)
        except Exception:
            counter += 1
    logger.info("\t%d words with non ascii characters are ommited" % counter)

    articles[k_word] = {}
    logger.info("\tfound %d words in file" % len(words))

    for word in words:
        data = {}
        page = site.Pages[word]
        if page.redirect:
            data['redirected'] = True

        text = page.edit()
        if  text == "":
            all_missing.append(word)
            break

        data['text'] = wikicorpus.filterWiki(text)
        in_ascii = ud.normalize('NFKD',
                                data['text']).encode('ascii', 'ignore')
        data['text'] = preprocess_string(in_ascii)
        articles[k_word][word] = data

f = open(os.path.join(output_dir, "articles.pickle"), 'wb')
pickle.dump(articles, f)
f.close

f = open(os.path.join(output_dir, "missing.pickle"), 'wb')
pickle.dump(all_missing, f)
f.close
