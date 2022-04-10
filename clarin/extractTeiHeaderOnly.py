#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
''' Empty <body> and keep <teiHeader> for each file '''

import glob
import os
from sys import stdout
from lxml import etree
from validator import Validator
# import re
# import csv


#########################
# Set input/out folders #
#########################

# baseFolder = '/home/ilbuonme/voluminosi/0.foo/2020-03-10_alim'
baseFolder = ('/home/ilbuonme/travaglio/alim/alim_clarin_2020/'
              '2020-03-17_alim_clarin')
logFolder = '%s' % baseFolder
inLett = '%s/in/letterarie' % baseFolder
inDoc = '%s/in/documentarie' % baseFolder
outLett = '%s/out/letterarie' % baseFolder
outDoc = '%s/out/documentarie' % baseFolder
# dtdPath = '%s/tei_alim.dtd' % baseFolder
# dtdPath = '%s/tei_all.dtd' % baseFolder
dtdPath = '%s/tei_alim.dtd' % baseFolder
for p in [inLett, inDoc, outLett, outDoc]:
    if not os.path.exists(p):
        os.makedirs(p)

##################
# Set namespaces #
##################

n = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI

xml = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
ns = {'t': 'http://www.tei-c.org/ns/1.0',               # for TEI XML
      'xml': 'http://www.w3.org/XML/1998/namespace',  # for attrs like xml:id
      'h': 'http://www.w3.org/1999/xhtml'}            # for (X)HTML output


##############
# Letterarie #
##############
#


def emptyFileLett(fileLett):
    # Parse input tree and find body:
    tree = etree.parse(fileLett)
    body = tree.find('.//t:body', ns)
    # Empty body
    for child in body:
        body.remove(child)

    # Create <ab> child of <body> (to make it valid TEI)
    etree.SubElement(body, 'ab')
    # Write output file
    bareFileNameLett = fileLett.rpartition('/')[2]
    outFileLett = '%s/%s' % (outLett, bareFileNameLett)
    tree.write(outFileLett, encoding="UTF-8", method="xml")


def emptyTree(my_file):
    ''' Files 'letterarie' only have one <body>;
        files 'documentarie' have many <body>es.
        This function finds he <body>(es)
        and empties it/them. It returns the tree '''
    # Parse input tree and find all <body> elements:
    tree = etree.parse(my_file)
    bodyList = tree.findall('.//t:body', ns)
    # Empty body
    for body in bodyList:
        for child in body:
            body.remove(child)
        # Create <ab> child of <body> (to make it valid TEI)
        etree.SubElement(body, 'ab')
    return tree


def emptyAllFilesInFolder(my_input_folder, my_output_folder):
    ''' This function inputs (with glob) all *.xml files
    in my_input_folder, passes them to function emptyFile
    to empty their <body>(es), then writes them to my_out_folder '''

    # Input files with glob:
    my_files = glob.glob('%s/*xml' % my_input_folder)

    # For each XML input file:
    for f in my_files:
        # Empty its <body>(es)
        my_tree = emptyTree(f)

        # Write it to the output folder
        my_filename = f.rpartition('/')[2]
        output_file = '%s/%s' % (my_output_folder, my_filename)
        my_tree.write(output_file, encoding="UTF-8", method="xml")


def validateShowErrors(f_input_folder, f_dtd, log_on_file=False):
    ''' Validate all files in f_input_folder
        and show validation errors '''
    # Instantiate validator:
    validator = Validator(f_dtd)
    # Input and parse files
    input_files = glob.glob('%s/*xml' % f_input_folder)
    count_valid = 0
    count_not_valid = 0
    log_file = '%s/log.txt' % logFolder
    if log_on_file:
        log = open(log_file, 'w')
    else:
        log = stdout
    for f in input_files:
        if validator.validate(f) is True:
            count_valid += 1
        else:
            count_not_valid += 1
            print(('\n\tFile {} not valid. Errors:\n{}').format(
                f, validator.errors(f)), file=log)
    if log_on_file:
        log.close()
    print(('\n\nSummary for folder {}'
           '\n\tValid: {}'
           '\n\tNot valid: {}').format(
               f_input_folder,
               count_valid,
               count_not_valid,
           ))


emptyAllFilesInFolder(inLett, outLett)
emptyAllFilesInFolder(inDoc, outDoc)

print('Files: {}\nDTD:\n{}'.format(inLett, dtdPath))
validateShowErrors(inLett, dtdPath)
validateShowErrors(inDoc, dtdPath)

validateShowErrors(outLett, dtdPath)
validateShowErrors(outDoc, dtdPath)
