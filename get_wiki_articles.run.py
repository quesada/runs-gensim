#!/usr/bin/env python
# encoding: utf-8
"""


Created by Stephan Gabler on 2011-05-12.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import os
import glob
import sys

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

# query url to the wikipedia api
query_base = "http://en.wikipedia.org/w/api.php?action=query&titles=%s" \
                + "&format=xml"\
                + "&redirects"


parameter_file = sys.argv[1]
p = build_parameters(parameter_file)

output_dir = os.path.join(p['base_path'], p['result_path'], 'test') #p['sumatra_label'])
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

# remember starting time for runtime evaluation
start = datetime.now()



# init and config
articles = {}
all_missing = []

# create a new URL opener class because websites like google or wikipedia
# reject queries from unknown user agents
# solution from here: http://wolfprojects.altervista.org/changeua.php
class MyOpener(FancyURLopener):
    version = 'AppleWebKit/531.21.10'
myopener = MyOpener()


# get all txt files in a folder and iterate over them
filelist = glob.glob(os.path.join(p['base_path'],
                                  p['folder_path'], 
                                  "coffee.txt"));
print os.path.join(p['base_path'], p['folder_path'], "coffee.txt")
print filelist
for f in filelist:
    

    # get the word we are working on
    f_name = os.path.basename(f)
    k_word = os.path.splitext(f_name)[0]
    logger.info("working on file: %s" % f_name)


    # try to convert the word into ascii for the http query
    file_obj = codecs.open(f, "r", "utf-16" )
    counter = 0
    words = []
    for w in file_obj.readlines():
        try:
            s = w.strip().decode('ascii')
            words.append(s)
        except Exception:
            counter += 1
    logger.info("\t%d words with non ascii characters are ommited" % counter)


    # the wikipedia api restricts queries to a length of 50
    logger.info("\tfound %d words in file" % len(words))
    for i in range((len(words) / 50)+1):
                
        # create the query and parse it
        query   = query_base % "|".join(words[(i*50):(i*50)+50])
        
        text    = myopener.open(query).read()
        soup    = BSS(text, convertEntities=BSS.ALL_ENTITIES)
        cont    = soup.api.query
    
        # collect all missing words
        missing = cont.pages.findAll(missing=True)
        all_missing.append([m['title'] for m in missing])
    
        # create dict containing all data from the available articles
        for page in cont.pages.findAll(missing=None):
            logger.info('title: ' + page['title'])
            title = page['title']
            data = {}
        
            # check whether article was found through redirect
            if cont.redirects:
                redir = cont.redirects.findAll(to=title)
                if redir:
                    logger.info('\tredirect from: ' + redir[0]['from'])
                    data['from'] = data.get('from', []) + [redir[0]['from']]
            
            # download the content of the article
            
            # some redirects introduce no ascii characters 
            # TODO introduce a proper conversion of this characters
            try:
                title = title.decode('ascii')
            except Exception:
                continue
                
            query = (query_base + "&export") % title
            text    = myopener.open(query).read()
            soup    = BSS(text, convertEntities=BSS.ALL_ENTITIES)
            print soup
            export  = BSS(soup.api.query.export.prettify())
            text    = BSS(export.mediawiki.page.revision.prettify())
            if text.revision.minor:
                data['text'] = wikicorpus.filterWiki(text.revision.minor.text)
            else:
                data['text'] = wikicorpus.filterWiki(text.revision.text)
            in_ascii = ud.normalize('NFKD',
                                    data['text']).encode('ascii', 'ignore')
            data['text'] = preprocess_string(in_ascii)
            articles[title] = data

f = open(os.path.join(output_dir, "articles.pickle"), 'wb')
pickle.dump(articles, f)
f.close

f = open(os.path.join(output_dir, "missing.pickle"), 'wb')
pickle.dump(all_missing, f)
f.close

