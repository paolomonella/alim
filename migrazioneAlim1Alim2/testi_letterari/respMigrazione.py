#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Questo script aggiunge il responsabile della migrazione 
# da ALIM1 ad ALIM2 livello 0
#
# È scritto in Python 3.4, ma funziona anche in Python 2.7
# per via del modulo __future__
# from __future__ import print_function
#
# Dovrebbe funzionare in Linux. Non l'ho testato in OSX o
# in altri sistemi operativi meno funzionali.
#

from __future__ import print_function
import os
import sys
import re
import glob
import subprocess

# Clear screen
#os.system('clear')
subprocess.call(['clear'])


globList = glob.glob('*.xml')
for f in globList:
    print('File: '+f)
    myO=open('ripostiglio/temp.xml','w')   # File Handler for the output file 
    with open(f) as myI:
        for line in myI:
            if re.match('.*<resp>compilato da</resp>.*', line):
                line=line.replace('<resp>compilato da</resp>', '<resp>esportazione in formato TEI XML livello 0 effettuata da</resp>')
            elif re.match('.*<name>ALIM</name>.*', line):
                line=line.replace('<name>ALIM</name>', '<name>Paolo Monella</name>')
            print(line, file=myO, end='')
    myO.close()
    subprocess.call([ 'xmllint', '--noout', '--dtdvalid', '/home/ilbuonme/alim/12/orso/DTD/tei_all.dtd', f])
    os.rename(f, 'ripostiglio/'+f)
    os.rename('ripostiglio/temp.xml', f)

# Quando l'utente dà invio, apre il file per il controllo finale
#choice = raw_input('Inserisci invio per vedere il file in VIM e fare il controllo finale')
#subprocess.call([ 'vim', newFN])



## Dà al file di output il nome definitivo
#newFN = prefix+' '+author+' - '+title+'.xml'
#os.rename('temp.xml', newFN)
#
## Feedback sui file di input e di output
#print('File di  input:\t'+myInputFile)
#print('File di output: '+newFN+'\n')
#
## Controlla se il file è valido
#subprocess.call([ 'xmllint', '--noout', '--dtdvalid', '/home/ilbuonme/alim/12/orso/DTD/tei_all.dtd', newFN])
#print('Il file è valido\n')
#
## Archivia il file di input originario (esportato dallo "strumentino" di ALIM1
## senza nessuna modifica nella cartella "ripostiglio"
#os.rename(myInputFile, 'ripostiglio/'+prefix+' '+author+' - '+title+'_v1.0.xml')

