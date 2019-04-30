#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This scripts imports the alimxmledit module
    and actually edits the files.
    """

##################
# Import modules #
##################
from __future__ import print_function
import alimxmledit 
# import sys  # Only needed if I use arguments, such as in lineNumberStartWithNewPage(sys.argv[1])
# import glob       # Use this if you want to edit more than one file


##############################
# Set customizable variables #
##############################
myInputFile               = "input.xml"
myElement           = "date"
attributeYouDontLike           = "when"
attributeYouLikeInstead    = "when-iso"

################
# Do the stuff #
################

#alimxmledit.substituteAttInElem(myInputFile, myElement, attributeYouDontLike, attributeYouLikeInstead)
#alimxmledit.setAttInElem(myInputFile, "TEI", "xmlns", "0")
#alimxmledit.setAttInElem(myInputFile, "pb", "n", "0")
#alimxmledit.lineNumberStartWithNewPage(myInputFile)
#alimxmledit.syllDash(myInputFile)
#alimxmledit.splitLargeXmlFile ('MP_v2.2.xml')
#alimxmledit.lbizeFile (myInputFile)
print('Elements in <body>:',  alimxmledit.getListOfAllElementsInBody ('input.xml') )
#alimxmledit.checkIfAllPsHaveCorrectNAttribute ('input.xml')
alimxmledit.wordCount('input.xml')
