#!/usr/bin/env python
#coding=utf-8

import argparse
import django
from django.template import Template, Context
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', '--input', help='input csv file')
    parser.add_argument('-tmpl', '--template', help='latex template')
    parser.add_argument('-cap', '--caption', help='table caption')
    parser.add_argument('-lbl', '--label', help='table label')

    args = parser.parse_args()

    if not args.input:
        print "Please specify the input file"
        exit(-1)

    if not args.template:
        print "LaTex template was not specified, default is used"
        args.template = "table_template.tex"

    if not args.caption:
        print "Please specify the caption"
        exit(-1)

    if not args.label:
        print "Please specify the label"
        exit(-1)

    # This line is required for Django configuration
    django.conf.settings.configure()

    # Open and read CSV file
    fid = open(args.input)
    reader = csv.reader(fid)

    # Open and read template
    with open(args.template) as f:
        t = Template(f.read())

    # Define context with the table data
    head = reader.next()
    c = Context({"head": head, "table": reader, "caption": args.caption, "label": args.label})

    # Render template
    output = t.render(c)

    fid.close()

    # Write the output to a file
    with open(args.input.replace('.csv', '.tex'), 'w') as out_f:
        out_f.write(output)
