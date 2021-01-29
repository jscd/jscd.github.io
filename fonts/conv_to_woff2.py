import os
import sys
from fontTools.ttLib import TTFont


dir = './'
if len(sys.argv) > 1:
    dir = sys.argv[1]

if dir[-1] != '/':
    dir += '/'

for file in os.listdir(dir):
    if file.endswith('.ttf'):
        f = TTFont(dir + file)
        f.flavor = 'woff2'
        f.save(dir + file[:-4] + '.woff2')
