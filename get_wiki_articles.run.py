#!/usr/bin/env python
# encoding: utf-8
"""


Created by Stephan Gabler on 2011-05-12.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import mwclient
import glob
import codecs
import pickle
import unicodedata as ud
import logging
import re
import tools

from sumatra.parameters import build_parameters
from gensim.corpora import wikicorpus
from gensim.parsing.preprocessing import preprocess_string

# setup
p = build_parameters(sys.argv[1])
output_dir = os.path.join(p['base_path'], p['result_path'], p['sumatra_label'])
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
logger.info("running %s" % ' '.join(sys.argv))

# initializations
articles = {}
all_missing = []
redir_on = {}
collisions = {}
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
        
        # follow the redirect and check for collisions
        if page.redirect:
            res = re.search('\[\[(.+)\]\]', page.edit())
            redir_word = res.groups()[0]
            if redir_on.has_key(redir_word):
                logger.warning("[%s AND %s] both redirect on --> %s" % 
                                    (word, redir_on[redir_word], redir_word))
                collisions[redir_word] = redir_on[redir_word]
            else:
                logger.info("[%s] redir from [%s]" % (redir_word, word))
                redir_on[redir_word] = word
            text = site.Pages[redir_word].edit()
            data['redirected'] = redir_word

        else:
            text = page.edit()

        # check for missing wikipedia articles
        if  text == "":
            all_missing.append(word)
            break

        # preprocess the received article
        data['text'] = wikicorpus.filterWiki(text)
        in_ascii = ud.normalize('NFKD',
                                data['text']).encode('ascii', 'ignore')
        data['text'] = preprocess_string(in_ascii)
        articles[k_word][word] = data

f = open(os.path.join(output_dir, "articles.pickle"), 'wb')
pickle.dump(articles, f)
f.close

info = {}
info['missing'] = all_missing
info['redirs'] = redir_on
info['collisions'] = collisions
f = open(os.path.join(output_dir, "info.pickle"), 'wb')
pickle.dump(info, f)
f.close

logger.info("%d redirecting collisions (see info.pickle)" % len(collisions))