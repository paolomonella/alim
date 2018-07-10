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
#fileSuCuiLavorare               = "[PA-PM-0] Anonimo - Epistolae latinae anonymorum auctorum.xml"
fileSuCuiLavorare               = "[PI-CDM-1] Anonimo - Chronicon Salernitanum_v1.0.xml"
elementoSuCuiLavorare           = "date"
attributoIndesiderato           = "when"
attributoDaMettereAlSuoPosto    = "when-iso"

################
# Do the stuff #
################

#alimxmledit.substituteAttInElem(fileSuCuiLavorare, elementoSuCuiLavorare, attributoIndesiderato, attributoDaMettereAlSuoPosto)
#alimxmledit.setAttInElem(fileSuCuiLavorare, "TEI", "xmlns", "0")
#alimxmledit.setAttInElem(fileSuCuiLavorare, "pb", "n", "0")
#alimxmledit.lineNumberStartWithNewPage(fileSuCuiLavorare)
#alimxmledit.syllDash(fileSuCuiLavorare)
#alimxmledit.splitLargeXmlFile ('MP_v2.2.xml')
alimxmledit.lbizeFile (fileSuCuiLavorare)
