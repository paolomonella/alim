#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Questo script rinomina il file e opera i cambiamenti di base per
# esportare un file XML/TEI con un testo letterario
# da ALIM1 ad ALIM2 livello 0
#
# È scritto in Python 3.4, ma funziona anche in Python 2.7
# per via del modulo __future__
# from __future__ import print_function
#
# Dovrebbe funzionare in Linux. Non l'ho testato in OSX o
# in altri sistemi operativi meno funzionali.
#
# Ora non ha bisogno di argomenti. Ci dev'essere però nella
# cartella un solo file che inizi con TEI (del tipo TEI20151211160351.xml)
#
# Nella variabile 'prefix' ho messo il prefisso con unità,
# responsabile e livello di codifica: il suo valore va cambiato
# se un'altra unità usa lo script.

from __future__ import print_function
import os
import sys
import re
import glob
import subprocess

# Sigla per unità, responsabile e livello di codifica nel nome del file
prefix = '[PA-PM-0]'

# File di input/versione A. Se si vuole dare un argomento allo script
# myInputFile = sys.argv[1]


# File di input/versione B. Se c'è un solo file TEI* nella cartella
    # Adesso il file di input non è più l'argomento
    # dello script, ma l'unico file nella cartella che
    # inizia con TEI, dato che i nomi dei file esportati
    # dallo "strumentino" sono del tipo TEI20151211160351.xml
globList = glob.glob('TEI*')
if len(globList) > 1:
    print('Nella cartella ci sono più file che iniziano con TEI*, e precisamente')
    for x in globList:
        print('\t'+x)
    print('Ce ne dovrebbe essere uno solo.')
    print('Io sto lavorando sul file\n\t'+globList[0])
myInputFile = globList[0]

# Clear screen
#os.system('clear')
subprocess.call(['clear'])

# Regex per cercare autore e titolo
myAu = '(<author>)(.*)(</author>)'

myO=open('temp.xml','w')   # File Handler for the output file 

with open(myInputFile) as myI:
    print('<?xml version="1.0" encoding="UTF-8"?>', file=myO)
    print('Righe scritte:\n\n<?xml version="1.0" encoding="UTF-8"?>\n') # Feedback
    for line in myI:
        line = line.replace('when-iso="', 'when="')
        if line.startswith('<note>Tipo'):
            #print('Cambio la riga\n\t'+line[:-1])
            line='<note>Tipo: Fonti Letterarie</note>\n'
            print(line) # Feedback
        elif line.startswith('</notesStmt>'):
            line = '<note>Livello di codifica: 0</note>\n'+line
            print(line) # Feedback
        elif line.startswith('<body>'):
            line = line+'<ab>\n'
            print(line) # Feedback
        elif line.startswith('</body>'):
            line = '</ab>\n'+line
            print(line) # Feedback
        elif re.match('(<author>)(.*)(</author>)', line):   #Cerca l'autore
            auM = re.match('(<author>)(.*)(</author>)', line)
            author = auM.group(2) 
        elif re.match('(<title>)(.*)(</title>)', line):   #Cerca l'autore
            tiM = re.match('(<title>)(.*)(</title>)', line)
            title = tiM.group(2) 
        print(line, end='', file=myO)

myO.close()


# Dà al file di output il nome definitivo
newFN = prefix+' '+author+' - '+title+'.xml'
os.rename('temp.xml', newFN)

# Feedback sui file di input e di output
print('File di  input:\t'+myInputFile)
print('File di output: '+newFN+'\n')

# Controlla se il file è valido
subprocess.call([ 'xmllint', '--noout', '--dtdvalid', '/home/ilbuonme/alim/12/orso/DTD/tei_all.dtd', newFN])
print('Il file è valido\n')

# Archivia il file di input originario (esportato dallo "strumentino" di ALIM1
# senza nessuna modifica nella cartella "ripostiglio"
os.rename(myInputFile, 'ripostiglio/'+prefix+' '+author+' - '+title+'_v1.0.xml')

# Quando l'utente dà invio, apre il file per il controllo finale
choice = raw_input('Inserisci invio per vedere il file in VIM e fare il controllo finale')
subprocess.call([ 'vim', newFN])