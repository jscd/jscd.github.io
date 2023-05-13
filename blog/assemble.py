#!/usr/bin/env python

# Created by Justin DeSimpliciis
# Copyright (c) April 2023
# 

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import os

ABSOLUTE_URL_BASE = 'https://jscd.pw/blog'

def parse_file(filepath):
    file_vars = {}

    # Pull canonical name from the file stem
    canonical = filepath.stem
    folder = '/'.join(filepath.parts[:-1]) 
    print('Parsing {}...'.format(filepath))

    # Rename the html files so that we can have prettier page URLs
    os.rename(
        '{}/{}.html'.format(folder, canonical),
        '{}/index.html'.format(folder)
    )
    file_vars['url'] = folder
    file_vars['absolute_url'] = '{}/{}'.format(ABSOLUTE_URL_BASE, folder)


    # Parse the entire file
    with open(filepath) as file:
        contents = file.read()

    header = contents.split('---')[1].strip() # Toss extra newlines
    lines = header.split('\n')

    for line in lines:
        if not line.startswith('-'):
            try:
                key, val = line.split(':', maxsplit=1) # Split at the first ':'
            except ValueError:
                print('Invalid header line: `{}`. Skipping...'.format(line))
                continue

            val = val.strip() 
            file_vars[key] = val

    return file_vars



def run():
    # Create the Jinja env
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape()
    )

    # Load the index & rss feed Jinja templates
    index_template = env.get_template('index.html.jinja')
    rss_template = env.get_template('rss.xml.jinja')

    # Global list of file metadata
    file_metadata = []

    # Glob every markdown file to get metadata
    files = Path('posts').rglob('*.md') # (Should be a single markdown file per dir)

    for file in files:
        headers = parse_file(file)
        file_metadata.append(headers)

    print('All files parsed! Generating index and feed...')

    # Generate blog index and RSS, and write out
    index_content = index_template.render(entries=file_metadata)
    rss_content = rss_template.render(entries=file_metadata)

    with open('index.html', mode='w') as f:
        f.write(index_content)

    with open('rss.xml', mode='w') as f:
        f.write(rss_content)

    print('Done!')



if __name__ == '__main__':
    run()
