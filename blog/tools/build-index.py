#!/usr/bin/env python

# Created by Justin DeSimpliciis
# Copyright (c) April 2023
# 

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import os

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape()
)

index_template = env.get_template('index.jinja.html')
rss_template = env.get_template('rss.jinja.xml')

file_metadata = []

files = Path('posts').rglob('*.md') # There should be a single markdown file per dir
for file in files:
    file_vars = {}

    canonical = file.stem
    folder = '/'.join(file.parts[:-1])
    os.rename('{}/{}.html'.format(folder, canonical), '{}/index.html'.format(folder))
    file_vars['url'] =  folder
    

    with open(file) as file:
        contents = file.read()

    # Start at 4 to account for the starting `---`
    header = contents[4:contents.find('---', 4)]
    lines = header.split('\n')

    for line in lines:
        if not line.startswith('-'):
            try:
                key, val = line.split(':')
            except ValueError:
                pass

            val = val.strip() # key-val is often formatted like 'key: value' and space may need to be removed

            file_vars[key] = val

    file_metadata.append(file_vars)



index_content = index_template.render(entries=file_metadata)
rss_content = rss_template.render(entires=file_metadata)

with open('index.html', mode='w') as f:
    f.write(index_content)

with open('feed.rss', mode='w') as f:
    f.write(rss_content)


