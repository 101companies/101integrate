#!/usr/bin/env python
#coding=utf-8

import argparse
from jinja2 import Environment, FileSystemLoader
import csv
import logging #needed for nunning the whole project in debug/info-mode

if __name__ == "__main__":
    env = Environment(line_statement_prefix='#', loader=FileSystemLoader('templates'), trim_blocks=True)

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
        print "LaTex template was not specified, default (tabular_template.tex) is used"
        args.template = "tabular_template.tex"

    #if not args.caption:
    #    print "Please specify the caption"
    #    exit(-1)

    #if not args.label:
    #    print "Please specify the label"
    #    exit(-1)

    # Open and read CSV file
    fid = open(args.input, 'rU')
    reader = csv.reader(fid)

    # Open and read template
    t = env.get_template(args.template)

    # Define context with the table data
    head = reader.next()
    #c = Context({"head": head, "table": reader, "caption": args.caption, "label": args.label})

    # Render template
    #output = t.render(c)
    output = t.render(head=head, table=reader, caption=args.caption, label=args.label)

    fid.close()

    # Write the output to a file
    with open(args.input.replace('.csv', '.tex'), 'w') as out_f:
        out_f.write(output)
