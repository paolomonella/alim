#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This module edits Ctibor's logs
# 
# What are the script system requirements?
# It's written in Python 3.6, but it should work in
# Python 2.7 too, thanks to the __future__ module:
#   from __future__ import print_function
# It should work in Linux. I did not test it in OSX or
# in other, less functional OSs starting with W.


import re
import glob
from lxml import etree
import csv
import os


###############################
# Set input files and folders #
###############################

myInputXmlFilesFolder = '/home/ilbuonme/travaglio/alim/15/jan_ctibor/2019-12-12/ctibor/'
if not os.path.exists('xml-out'):   # Subfolder created in the same folder where the script runs
    os.makedirs('xml-out')
myLogFileFolder = '/home/ilbuonme/travaglio/alim/15/jan_ctibor/2019-12-12/ctibor/logs/Post-revisione linguistica/'
myLogFileList = [
    'log_00175-00203.txt',
    'log_00204-00220.txt',
    'log_00221-00270.txt',
    'log_00271-00300.txt',
    'log_00301-00320.txt',
    'log_00321-00370.txt',
    'log_00371-00390.txt',
    'log_00391-00410.txt',
    'log_00411-00430.txt',
    'log_00431-00470.txt',
    'log_00471-00510.txt',
    'log_00511-00530.txt',
    'log_00531-00560.txt',
    'log_00561-00580.txt',
    'log_00581-00600.txt',
    'log_00601-00616.txt',
    'log_03454-03483.txt',
    'log_04422-06511.txt'
    ]



# Per le seguenti note di log, meglio non creare <list> e <item>, perché contengono molte righe di codice TEI XML
logNumsNoList = ['181', '204', '217', '219', '253', '285', '360', '367', '398', '421', '448', '524', '3481']
 

#####################
# Set the namespace #
#####################

n = '{http://www.tei-c.org/ns/1.0}'              # for XML/TEI

xml = '{http://www.w3.org/XML/1998/namespace}'   # for attributes like xml:id
ns = {'t': 'http://www.tei-c.org/ns/1.0',               # for TEI XML
        'xml': 'http://www.w3.org/XML/1998/namespace',  # for attributes like xml:id
        'h': 'http://www.w3.org/1999/xhtml'}            # for (X)HTML output  



########################
# Define the functions #
########################

def jcNormalizedLogNum (fcLogNum):
    ''' Aggiungi uno o due zeri all'inizio se servono'''
    normLogNumFN = fcLogNum.zfill(5)
    '''
    if len(fcLogNum) == 5:
        normLogNumFN = fcLogNum
    elif len(fcLogNum) == 4:
        normLogNumFN = fcLogNum
        normLogNumFN = ''.join(['0', fcLogNum])
    elif len(fcLogNum) == 4:
    else:
        normLogNumFN = ''.join(['0', fcLogNum])
        '''
    return normLogNumFN

def jcGetLogNoteMatrix():
    myMatrix = {}
    myNoteLines = []
    myOldNoteNumber = ''
    for myLogFileName in myLogFileList:
        log = ''.join([myLogFileFolder, myLogFileName])
        with open(log, 'r') as f:
           lines = f.readlines()
        for line in lines:
            if line.strip() == '\ufeff':
                pass
            elif re.compile('\d\d\d').match(line) or re.compile('\d\d\d\d').match(line):
                myNewNoteNumber = line.strip()
                myMatrix[myNewNoteNumber] = None
                #print(myNoteNumber)
                #print(myNoteLines)
                if myOldNoteNumber != '':
                    myMatrix[myOldNoteNumber] = myNoteLines
                myNoteLines = []
                myOldNoteNumber = myNewNoteNumber
            else:
                myNoteLines.append(line)
    myMatrix[myNewNoteNumber] = myNoteLines  # Ultima riga dell'ultimo file (nota 6511)
    return myMatrix


def jcCheckLogNoteInXML (ckLogNum, ckTeiFile, ckMatrix):
    ''' Controlla se c'è o no già una nota di Ctibor'''

    tree = etree.parse(fnTeiFile)
    jcChanges = tree.findall('.//t:change[@who="JC"]', ns)
    allChanges = tree.findall('.//t:change', ns)

    if len(jcChanges) == 0:
        lenAll = len(allChanges)

        print('\n------------\n\nFile:\n', ckTeiFile.split('/')[-1])

        print('\nNota:')
        print(ckMatrix[ckLogNum])

        if lenAll == 0:
            print('Nessun <change>')
        else:
            print('\nElementi <change>:')
            for c in allChanges:
                print(c.get('who'), c.text)




def jcInsertLogNote1 (fnLogNum, fnTeiFile, fnMatrix):
    '''fnLogNum = il numero della nota di log, fnTeiFile = il path completo del file'''

    changeText = 'Nota di Jan Ctibor relativa alla sua revisione del file di luglio 2018:\n' + ''.join(fnMatrix[fnLogNum])

    tree = etree.parse(fnTeiFile)
    revisionDesc = tree.find('.//t:revisionDesc', ns)
    if revisionDesc is None:
        print(fnLogNum, revisionDesc)

    newChange = etree.Element(n + 'change')
    newChange.set('when', '2018-07')
    newChange.set('who', 'JC')
    newChange.set('type', 'notaJC')
    newChange.text = changeText
    
    if revisionDesc is not None:
        revisionDesc.append(newChange)

    newTeiFN = fnTeiFile.split('/')[-1].strip()
    newTeiPath = 'xml-out/' + newTeiFN

    tree.write(newTeiPath, encoding="UTF-8", method="xml")


def jcAppendList (fnParentElement, fnList):
    '''Takes a parent element and returns the same element with a <list> child.
        The <list> includes a series of <item>s, one for each element of fnList.
        Argument fnList is a [list]'''
    newList = etree.Element(n + 'list')
    newList.set('type', 'listaNoteJC')
    for i in fnList:
        if i.strip() != '':
            newItem = etree.Element(n + 'item')
            newItem.set('type', 'itemNotaJC')
            newItem.text = i.strip()
            newList.append(newItem)
        #else:   # debug
            #print('Riga vuota: «' + i.strip() + '»')    # debug
    #print('Item inseriti in <change> nuovi: ', len(newList))    # debug
    if len(newList) > 0:
        fnParentElement.append(newList)
    else:
        print('Tutte le righe del log di JC sono vuote')

def jcInsertLogNote2 (fnLogNum, fnTeiFile, fnMatrix):
    '''fnLogNum = il numero della nota di log, fnTeiFile = il path completo del file'''

    tree = etree.parse(fnTeiFile)
    revisionDesc = tree.find('.//t:revisionDesc', ns)
    jcChanges = tree.findall('.//t:change[@who="JC"]', ns)

    if revisionDesc is None:
        print('Nota di log numero:', fnLogNum, ':\t<revisionDesc> è ', revisionDesc)
    else:
        if len(jcChanges) == 0: # Se non c'erano <change> precedenti di JC, creane uno nuovo
            newChange = etree.Element(n + 'change')
            newChange.set('when', '2018-07')
            newChange.set('who', 'JC')
            newChange.set('type', 'noteJCtratteDaiLogTxt')
            newChange.text = ''.join(['Note relative alla revisione del file di luglio 2018 ',
                        '(adeguamento al livello di codifica ALIM2_1):\n'])
            if fnLogNum in logNumsNoList:
                newChange.text = newChange.text + ''.join(fnMatrix[fnLogNum]) # Aggiungo la nota in formato testo
            else:
                jcAppendList( newChange, fnMatrix[fnLogNum] ) # Aggiungo una <list> di <item>s
            revisionDesc.append(newChange)

        elif len(jcChanges) > 1: # Se c'era più di un <change> precedente di JC
            print('Nota di log numero %d: esistevano più d\'uno, e precisamente %d, elementi <change> di JC' \
                    % (fnLogNum, len(jcChanges))  )
        elif len(jcChanges) == 1: # Se c'era un <change> precedente di JC
            jcChange = jcChanges[0]
            #oldChangeText = jcChange.text
            #print('Testo <change> preesistente di JC: %s' % (oldChangeText)  )   # debug
            #newChangeText = oldChangeText + '. Note: \n' + ''.join(fnMatrix[fnLogNum]) # old
            jcChange.text = jcChange.text + '. Note: \n'

            if fnLogNum in logNumsNoList:
                jcChange.text = jcChange.text + ''.join(fnMatrix[fnLogNum]) # Aggiungo la nota in formato testo
            else:
                jcAppendList( jcChange, fnMatrix[fnLogNum] ) # Aggiungo una <list> di <item>s

    newTeiFN = fnTeiFile.split('/')[-1].strip()
    newTeiPath = 'xml-out/' + newTeiFN

    #print('newTeiPath:',newTeiPath)#debug

    tree.write(newTeiPath, encoding="UTF-8", method="xml")

def jcCheckLogs ():


    # Check existing text numbers

    myFileNumList = []
    with open('/home/ilbuonme/travaglio/alim/15/jan_ctibor/2019-07-04/lab/textlist.txt', 'r') as tl:
        lines = tl.readlines()
    for line in lines:
        myNum = line.split('_')[0]
        if myNum[0] == '0':
            myNum = myNum[1:4]
        myFileNumList.append(myNum)
    

    # Check headers in log files

    myLogNumList = []
    c = 175
    for myLogFileName in myLogFileList:
        log = ''.join([myLogFileFolder, myLogFileName])
        #print(log) # debug

        with open(log, 'r') as f:
           lines = f.readlines()
        for line in lines:
            line = line.strip()
            if re.compile('\d\d\d').match(line) or re.compile('\d\d\d\d').match(line):

                myLogNumList.append(line)

                #print(line, end=' ')   # debug
                if int(line) != c:
                    mydiff = int(line) - c
                    for r in range(mydiff):
                        #print(c, end=' ')
                        c = c + 1
                    #print()
                else:
                    #print('%s%10s%10s%20s%10s' % ('SÌ', 'Nota:', line, 'Contatore:', c))
                    pass
                c = c + 1
            elif re.compile('\d\d\d.*').match(line) and re.compile('.*,.*').search(line):
                print('Virgola:\n\t%s\n\t%s\n' % (log, line))
            elif re.compile('\d\d\d-\d\d\d.*').match(line) or re.compile('\d\d\d\d.-\d\d\d\d.*').match(line):
                print('Una sola nota per più file:\n\t%s\n\t%s' % (log, line))
            elif re.compile('\d\d\d-\d*').match(line) or re.compile('\d\d\d\d.-\d*').match(line):
                print('Una sola nota per più file:\n\t%s\n\t%s' % (log, line))



def jcCreateLogCsv(itemDict):
    
    listWriter = csv.DictWriter(
    open('logs.csv', 'wb'),
    fieldnames=itemDict[itemDict.keys()[0]].keys(),
    delimiter=',',
    quotechar='|',
    quoting=csv.QUOTE_MINIMAL
    )

    for a in itemDict:
        print(a)
        listWriter.writerow(a)
        pass


def jcInsertAllNotes():

    myMatrix = jcGetLogNoteMatrix()

    for myLogNum in myMatrix:

        # Aggiungi lo 0 all'inizio se serve
        logNumFN = jcNormalizedLogNum(myLogNum)

        #mySpecifGlob = glob.glob('/home/ilbuonme/travaglio/alim/15/jan_ctibor/2019-07-04/xml-orig/%s_*' % (logNumFN))
        #print('%s%s_*' % (myInputXmlFilesFolder, logNumFN))    # debug
        mySpecifGlob = glob.glob('%s%s_*' % (myInputXmlFilesFolder, logNumFN))
        if len(mySpecifGlob) == 0:
            print('Al log', myLogNum, 'non corrisponde nessun file')
            if myLogNum == '296':
                print('...ma Jan Ctibor ci ha scritto il 16.07.2019 che non trova neanche lui il file 296')
        else:
            myTeiFile = mySpecifGlob[0]
            if myTeiFile.endswith('xml'):
                jcInsertLogNote2(myLogNum, myTeiFile, myMatrix)

jcInsertAllNotes()
