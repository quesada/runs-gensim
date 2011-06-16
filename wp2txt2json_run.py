#!/usr/bin/env python
# encoding: utf-8
"""
wp2txt2json.py

Created by Stephan Gabler on 2011-06-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import codecs
import glob
import json
import os
import re
import time

path = '/Users/dedan/projects/mpi/data/corpora/wiki/wiki_de_2011/'

files = glob.glob(path + '*.txt')

out = codecs.open(os.path.join(path, 'wiki.json'), mode='w', encoding='utf-8')

headline = re.compile('\[\[(.*)\]\]')
level2 = re.compile('== (.*) ==')

t0 = time.time()
c = 0
res = {}

for file in files:
    print 'work on: %s' % file
    with codecs.open(file, encoding='utf-8') as f:
        for line in f:

            # ignore linebreaks
            if line == '\n':
                continue

            # if we found a headline
            if headline.search(line):
                if len(res) > 0:
                    out.write(json.dumps(res, encoding='utf-8', ensure_ascii=False) + '\n')
                topic = headline.search(line).groups()[0]
                res = {topic: {}}
                sub = None

            elif level2.search(line):
                sub = level2.search(line).groups()[0]
            else:
                if not sub:
                    res[topic].setdefault('desc', []).append(line.strip())
                else:
                    res[topic].setdefault(sub, []).append(line.strip())
    c += 1
    print 'average execution time: %f' % ((time.time() - t0) / c)
out.write(json.dumps(res, encoding='utf-8', ensure_ascii=False) + '\n')

print time.time() - t0
