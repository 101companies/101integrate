#!/usr/bin/env python
#coding=utf-8
import json
import urllib2
import os

themes = json.load(urllib2.urlopen('http://data.101companies.org/resources/themes/members.json'))
languages = json.load(urllib2.urlopen('http://data.101companies.org/resources/languages/members.json'))
wikipages = json.load(urllib2.urlopen('http://data.101companies.org/dumps/wiki.json'))['wiki']['pages']

#books = [b for b in os.listdir("../../data/perbook/") if os.path.exists('../../data/perbook/' + b + '/contents')  ]
