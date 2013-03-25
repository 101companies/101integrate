#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

books = []
for bookDir in get_immediate_subdirectories('../data/perbook'):
  if os.path.exists('../data/perbook/' + bookDir + '/contents'):
    books.append(bookDir)

print books 	
with open ('Makefile.vars', 'w') as f: f.write ('BOOKS = ' + ' '.join(books))