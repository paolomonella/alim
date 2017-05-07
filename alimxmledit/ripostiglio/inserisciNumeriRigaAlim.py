#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# What does this script do?
# This script adds @n attributes to <lb/>s to create line
# numbering. This version starts the numbering over for
# each new page (i.e.: its starts over when it meets
# <pb/>). A new version might cope with different
# line numbering conventions.
# 
# Which file(s) should the script work on?
# This is defined in the last lines of this script.
#
# Where do the edited files go?
# The edited files are saved in the 'edited_files' sub-folder.
# Warning: files in the 'edited_files' folder will be overwritten.
# 
# What are the script system requirements?
# It's written in Python 3.4, but it should work in
# Python 2.7 too, thanks to the __future__ module:
#   from __future__ import print_function
# It should work in Linux. I did not test it in OSX or
# in other, less functional OSs starting with W.


####################################
# Import modules and set variables #
####################################

from __future__ import print_function
import os
import sys
import xml.etree.ElementTree as ET
# import glob # Use this if you want to edit more than one file
# import subprocess # Use this is you want to clear the screen

# Clear screen
# subprocess.call(['clear'])

# Create folder for edited files (if it does not exist)
if not os.path.exists('edited_files'):
    os.mkdir('edited_files')

##########################
# Function editing files #
##########################


def lineNumberStartWithNewPage (myInputFile):
    """ This function uses module ElementTree to edit the DOM """

    with open(myInputFile) as myI:

        print('Working on file: ' + myInputFile)

        # Set the namespace
        n = '{http://www.tei-c.org/ns/1.0}' 
        ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')

        # Root element (TEI)
        tree = ET.parse(myInputFile)
        root = tree.getroot()

        # Iterate all children and grand-children of root
        c = 0
        for e in root.iter('*'):
            if e.tag == n+'lb':
                c = c + 1
                e.set('n', str(c))
                #print(e.tag + ' ' + 'n="' + str(c) + '"')
            if e.tag == n+'pb':
                c = 0


    # Save the edited file
    myOutputFile = 'edited_files/' + myInputFile
    tree.write(myOutputFile, encoding="UTF-8", method="xml")
    



################
# Do the stuff #
################

# Un-comment this if you want to edit all *xml files in the working folder
# for f in glob.glob('*xml'):
#     inserisciNumeriRigaAlim.lineNumberPerPage(f)

# This line runs the function on the first argument given through command line
lineNumberStartWithNewPage(sys.argv[1])
