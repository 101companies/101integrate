#!/usr/bin/env python
#coding=utf-8
import json
import urllib2
import os

themes = json.load(urllib2.urlopen('http://data.101companies.org/resources/themes/members.json'))
languages = json.load(urllib2.urlopen('http://data.101companies.org/resources/languages/members.json'))

books = os.listdir("../../data/perbook")
