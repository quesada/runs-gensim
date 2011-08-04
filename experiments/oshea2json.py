#!/usr/bin/env python
# encoding: utf-8
"""
wp2txt2json.py

Created by Stephan Gabler on 2011-06-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import codecs
import json
import os
import re
import string
import tools


corpora_path = "/Users/dedan/projects/mpi/data/corpora/oshea/"

inp = codecs.open(os.path.join(corpora_path, 'oshea_similarity.txt'), mode='r', encoding='utf-8')
out = codecs.open(os.path.join(corpora_path, 'oshea_similarity.json'), mode='w', encoding='utf-8')
pair = re.compile('\d\.(\w+):(\w+)')
exclude = set(string.punctuation)

c = 0
res = []

for line in inp:
    if line == "\n":
        continue
    if c % 5 == 0:
        print pair.search(line).groups()
        res.append({'terms': pair.search(line).groups(),
                    'sentences': [],
                    'sentences_tagged': [],
                    'values': []})
    
    if c % 5 == 1 or c % 5 == 2:
        res[-1]['sentences'].append(line.strip())
        cleaned = "".join(ch for ch in line.strip() if ch not in exclude)        
        res[-1]['sentences_tagged'].append(tools.tag(cleaned, '/Users/dedan/Downloads/senna-v2.0/'))

    if c % 5 == 3 or c % 5 == 4:
        res[-1]['values'].append(float(line))
    
    
    c = c+1


json.dump(res, out, indent=2)