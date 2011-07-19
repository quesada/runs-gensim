'''
Created on 19.07.2011

@author: dedan
'''
import glob
import shutil

flist = glob.glob('/Users/dedan/projects/mpi/data/corpora/fridolin/marketing_glossar/*.txt')
assert flist
for file in flist:
    with open(file) as f:
        with open(file + '.tmp', 'w') as fwrite:
            for line in f.readlines():
                fwrite.write(unicode(line, 'latin-1').encode('utf8'))

    shutil.move(file + '.tmp', file)
