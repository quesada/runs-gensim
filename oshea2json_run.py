#!/usr/bin/env python
# encoding: utf-8
"""
  annotate the oshea corpus and store it in a better to access json format


  Created by Stephan Gabler on 2011-06-09.
  Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import codecs
import json
import os
import re
import string
import tools
from os import path
import sys

def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    inp = codecs.open(os.path.join(p['base_path'],
                                   p['corpora_path'],
                                   p['corpus_name']),
                      mode='r', encoding='utf-8')
    out = codecs.open(os.path.join(output_dir,
                                   p['result_name']),
                      mode='w', encoding='utf-8')
    pair = re.compile('\d\.(\w+):(\w+)')
    exclude = set(string.punctuation)

    line_count = 0
    res = []

    for line in inp:
        
        # skip empty lines
        if line == "\n":
            continue
        
        # finished one entry
        if line_count % 5 == 0:
            print pair.search(line).groups()
            res.append({'terms': pair.search(line).groups(),
                        'sentences': [],
                        'sentences_tagged': [],
                        'values': []})

        # annotate sentence and add it to result
        if line_count % 5 == 1 or line_count % 5 == 2:
            res[-1]['sentences'].append(line.strip())
            cleaned = "".join(ch for ch in line.strip() if ch not in exclude)
            tagged = tools.tag(cleaned, p['senna_path'])
            res[-1]['sentences_tagged'].append(tagged)

        # add the ratings
        if line_count % 5 == 3 or line_count % 5 == 4:
            res[-1]['values'].append(float(line))

        line_count = line_count+1
    
    # store the output
    json.dump(res, out, indent=2)



if __name__ == '__main__':
    main()
