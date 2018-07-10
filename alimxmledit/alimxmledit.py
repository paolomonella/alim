#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module defines a number of methods to parse
# and edit the XML tree of XML TEI files of the ALIM
# Archive.
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


##################
# Import modules #
##################

from __future__ import print_function
import os
import re
#import xml.etree.ElementTree as ET
from lxml import etree as ET      # I built most methods below with etree. I'll have to check whether they still work with lxml

#####################
# Set the namespace #
#####################

n = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI
#ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')   # This used to work when I used ElementTree

xml = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
ns = {'tei': 'http://www.tei-c.org/ns/1.0',             # for TEI XML
                'xml': 'http://www.w3.org/XML/1998/namespace'}  # for attributes like xml:id



########################
# Define the functions #
########################

def splitLargeXmlFile (myInputFile):
    """ It takes myInputFile, including a sequence of
        <div type="chapter" n="Cap. 1" xml:id="vol1-cap1">
        and splits the large file to smaller XML files (not valid against TEI XML)
        whose root element is one of those <div type="chapter">
        and whose filename is the value of @xml:id. Those files are saved into
        a folder "split_files" that should already exist.
        """

    tree = ET.parse(myInputFile)
    with open(myInputFile) as f:
        for x in tree.findall('.//' + n + 'div[@type="chapter"]'):

            cap = x.find(n + 'head[@rend="small-caps"]')
            if cap is not None:
                cap.text = cap.text + '. ' 
            rubr = x.find(n + 'head[@type="rubric"]')
            if rubr is not None:
                rubr.text = rubr.text + '. '

            a = x.xpath('normalize-space()').encode('utf8')
            outfn = x.get(xml + 'id')   # Output base filename
            if not os.path.exists('split_files'):   # Create output folder
                os.mkdir('split_files')
            myPath = 'split_files/' + outfn + '.txt'    # Output path
            #new_tree = ET.ElementTree(x)                # Create new tree
            #new_tree.write(myPath, encoding="UTF-8", method="xml")  # Output new tree to file
            with open (myPath, 'w') as o:
                o.write(a)


def outputTree (myTree, myInputFileName):
    # Create folder for edited files (if it does not exist)
    if not os.path.exists('edited_files'):
        os.mkdir('edited_files')
    # Save the edited file
    myOutputFileName = 'edited_files/' + myInputFileName
    myTree.write(myOutputFileName, encoding="UTF-8", method="xml")

def setAttInElem (myInputFile, myElem, myAtt, myValue):
    """ This function sets attribute myAtt to value myValue in all
        elements myElem in file myInputFile.
        If the attribute already existed, its value is changed to myValue.
        If the attribute did not exist, it is created.
        WARNING: It seems not to work properly if myElem is "TEI".
        """
    with open(myInputFile) as myI:
        print('Working on file: ' + myInputFile)
        tree = ET.parse(myInputFile)
        for e in tree.iter('*'):    # Iterate all elements in file 
            if e.tag == n + myElem:
                if myAtt in e.attrib:
                    print('\nAttribute @'+myAtt+' exists, with value "'+e.get(myAtt)+'". The value will be changed to "'+myValue+'"')
                    del e.attrib[myAtt]      # This deletes the old attribute altogether
                e.set(myAtt, myValue)
                #print('Setting \t@' + myAtt + '="' + myValue + '"\tin element\t@' + myElem)
    outputTree(tree, myInputFile)

def substituteAttInElem (myInputFile, myElem, myoa, myna):
    """ This function uses module ElementTree to edit the DOM
        and substitutes all attributes myoa (My Old Attribute)
        with attribute myna (My New Attribute) of element
        myElem (my element) in file myInputFile.
        """
    with open(myInputFile) as myI:
        print('Working on file: ' + myInputFile)
        tree = ET.parse(myInputFile)
        for e in tree.iter('*'):    # Iterate all elements in file 
            if e.tag == n + myElem and myoa in e.attrib:
                myValue = e.get(myoa)   # This is the value: I'm saving it for later
                del e.attrib[myoa]      # This deletes the old attribute
                print('Substituting\t@' + myoa + '="' + myValue + '"\twith\t@' + myna + '="' + myValue + '"')
                e.set(myna, myValue)
    outputTree(tree, myInputFile)

def lineNumberStartWithNewPage (myInputFile):
    """ This function inserts @n attributes in <lb> starting over
        the numbering at each new <pb> """
    with open(myInputFile) as myI:
        print('Working on file: ' + myInputFile)
        tree = ET.parse(myInputFile)
        c = 0
        for e in tree.findall('.//*'): # Iterate all children and grand-children of root. I've got to do this,
            # as opposed to tree.findall('//lb'), because I want to find both <lb> and <pb>
        #for e in tree.findall('//*'):  # This is what's suggested in http://www.diveintopython3.net/xml.html, but my
            # interpreter says: "FureWarning: This search is broken in 1.3 and earlier, and will be fixed in a future
            # version.  If you rely on the current behaviour, change it to './/*'
        #for e in tree.iter('*'): # That's another way to do this
            if e.tag == n+'lb':
                c = c + 1
                e.set('n', str(c))
                #print(e.tag + ' ' + 'n="' + str(c) + '"')
            if e.tag == n+'pb':
                c = 0
    outputTree(tree, myInputFile)

def syllDash (myInputFile):
    """ This function eliminates the syllabation dashes at the end of
        lines, thus:
            Input:
                <lb/>omnia vani-
                <lb/>tas, dixit Qohelet
            Output:
                <lb/>omnia vani<!-- Trattino di sillabazione a fine riga -->tas,
                <lb/>dixit Qohelet

        If the second line does not start with '<lb/>', the function does nothing
        but adding an XML comment '<!-- Trattino da togliere a mano -->' after
        the dash in the first line. Output:
                <lb/>omnia vani-<!-- Trattino da togliere a mano -->
                <cb/>

        If the only textual content of the second line is the final part of the
        previously split word, function does nothing but adding an XML comment
        '<!-- Trattino da togliere a mano (riunire parola nella seconda riga) -->'
        after the dash in the first line. Output:
            <lb/>Fuit non lon<!-- Trattino da togliere a mano (riunire parola nella seconda riga) -->
            <lb/>ge...! <!-- Random comment previously included in the input file-->

        The function adds a trailing whitespace (' ') at the end of each line, and
        writes the output in a folder 'edited_files/'. Example:
            Input file:
                foo.xml
            Output file:
                edited_files/foo.xml
                        
        Finally, the function prints to screen a list of the lines with the latter
        comment added to it.
        """
    myOutputFile = 'edited_files/' + myInputFile
    of = open(myOutputFile, 'w')
    tam_a = []    # List of lines to edit manually because the second line does not start with <lb/>
    tam_b = []    # List of lines to edit manually because the word must be reunited in the second line
    with open(myInputFile, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip() # This removes trailing whitespace, including the final '\n'
            if i < len(lines)-1:

                first = lines[i]    # The first line
                second = lines[i+1] # The second line

                if len(first) > 1 and first[-1] == '-':
                #if len(first) > 1 and first[-1] == '-' and not second.startswith('<lb/>'):
                    if second.startswith('<lb/>'):
                    # elif len(first) > 1 and first[-1] == '-' and second.startswith('<lb/>'):
                    # If the first line ends with '-' and the second line starts with <lb/>

                        # Get the final part of the word (e.g: in "ta- / men", this is "men")
                        second_part, sep, rest_of_second_line = second.partition(' ') 
                        if '<!--' in second_part:       # If the string looks like '<lb/>men<!--'
                            second_part, sep, rest_of_second_line = second.partition('<!--')   # The result will be '<lb/>men'
                        second_part = second_part[5:]   # Strip the first 4 characters the line ('<lb/>') the result is now 'men'

                        # Remove the final '-' from the first line
                        first = first[:-1]  


                        # Check if the rest of the second line is empty (i.e. if the final part of the word originally
                        # was its only content. If so, write an XML comment and do nothing
                        rest_check = rest_of_second_line
                        rest_check = re.sub('<!--.*?>', '', rest_check) # Remove XML comments
                        rest_check = rest_check.strip()                 # Remove start- and end-whitespace
                        if rest_check == '':
                        #if rest_of_second_line.strip() == '':
                            first = first + '<!-- Trattino da togliere a mano (riunire parola nella seconda riga) -->'
                            tam_b.append('  ' + first + '\n  ' + second)
                        else:   # If the rest of the second line is not empty
                            first = first + '<!-- Trattino di sillabazione a fine riga -->' + second_part # Join 2 parts of word
                            second = '<lb/>' + rest_of_second_line   # Add <lb/> back to the 2nd line

                    else:
                        # If the first line ends with '-' but the second line dows not start with <lb/>,
                        # write an XML comment at the end of the first line and do nothing
                        first = first + '<!-- Trattino da togliere a mano -->'
                        tam_a.append('  ' + first + '\n  ' + second)


                    lines[i] = first
                    lines[i+1] = second
            print(lines[i], file=of, end=' \n')  # The final '\n' is added here

    of.close()
                    
    print('\n\n\n\n\n\n\nLines to edit manually (marked with an XML comment):\n')
    print('\nA) The second line does not start with <lb/>:\n')
    for t in tam_a:
        print(t + '  ---')
    print('\nB) The word must be reunited in the second line, not in the first:\n')
    for t in tam_b:
        print(t + '  ---')



def lbizeElement (e):
    ''' Replace each line break with an element <lb/> in the text
        and the tail of element myel '''
    mytype = 'automaticallAddedByScript'
    if e.text is not None:
        lines = e.text.split('\n')  # Create a string for each line, those strings are now in list 'lines'
        e.text = ''
        for x in reversed(lines):            # For each line (in reverse order)
            if len(x.strip()) > 0:
                newlb = ET.Element(n + 'lb')
                newlb.set('type', mytype)
                newlb.tail = x.strip()  # Strip whitespace before and after
                if e.tag is not ET.Comment and not (e.get('type') == mytype) and lines.index(x) > 0:
                    e.insert(0, newlb)
                else:
                    e.text = x.strip()
    if e.tail is not None:
        lines = e.tail.split('\n')  # Create a string for each line, those strings are now in list 'lines'
        e.tail = ''
        for x in reversed(lines):            # For each line (in reverse order)
            if len(x.strip()) > 0:
                newlb = ET.Element(n + 'lb')
                newlb.set('type', mytype)
                newlb.tail = x.strip()  # Strip whitespace before and after
                if e.tag is not ET.Comment and not (e.get('type') == mytype) and lines.index(x) > 0:
                    e.addnext(newlb)
                else:
                    e.tail = x.strip()
        
def lbizeFile (inputfile):
    ''' Take all elements in myfile, and for each text and tail of those elements
        replace each \n with <lb/> '''

    mytype = 'automaticallAddedByScript'
    tree = ET.parse(inputfile)
    els = tree.iter()

    for myelem in els:
        lbizeElement(myelem)

    for newlb in tree.findall('.//tei:lb[@type="%s"]' % (mytype), ns):
        ''' Remove the @type="automaticallAddedByScript" that the 'lbize'
            function has added to avoid repeated <lb> insertions '''
        try:
            if newlb.get('type') == mytype:
                del newlb.attrib['type']
        except KeyError:
            pass

    tree.write('edited-%s' % (inputfile), encoding='UTF-8', method='xml', pretty_print=True, xml_declaration=True)
