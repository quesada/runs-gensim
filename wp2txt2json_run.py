#!/usr/bin/env python
# encoding: utf-8
"""
wp2txt2json.py

Created by Stephan Gabler on 2011-06-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from os import path
import codecs
import glob
import json
import os
import re
import sys
import time
import tools


def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    # in test case
    if param_file:
        files = [path.join(base_path, p['wiki_txt'])]
    else:
        files = glob.glob(path.join(base_path, p['wiki_txt']) + '*.txt')

    out = codecs.open(os.path.join(output_dir, 'wiki.json'), mode='w', encoding='utf-8')

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

                # if headline found
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


if __name__ == '__main__':
    main()

