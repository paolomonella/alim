#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Questo script prende come input un html, fa alcune sostituzioni e scrive
# l'output in un altro file html. 
# La lista delle sostituzioni da compiere è in un csv.
#
# Inoltre controlla che non ci siano caratteri non-ASCII

import os
import re
import sys,codecs	# Servono per cercare i caratteri non-ASCII
import alimConferma
import alimGestisciFile
os.system('clear')

def checkfile(filename):
    # Questa funzione sarà usata più sotto in questo stesso script
    f = codecs.open(filename,encoding='ascii')
    contaErrASCII = 0

    lines = open(filename).readlines()
    print('Cerco caratteri non-ASCII\n\tNumero totale di righe: %d' % len(lines))
    for i in range(0,len(lines)):
        try:
            l = f.readline()
        except:
            contaErrASCII += 1        
            num = i+1
            print('\tCodifica non-ASCII alla riga: %d' % num)

    f.close()
    if contaErrASCII == 0:
            print('\tNessun carattere non-ASCII trovato\n')
    else:
            exit('\tPrima di processare ulteriormente il file, sostituisci i caratteri non-ASCII.')

# Chiede qual è il file di input
oldFile = alimGestisciFile.scegli('html')
if oldFile == '':
        exit('Esco perché non ho niente da fare')

# Chiede qual è il file di output
newFile = alimGestisciFile.nuovaVersione(oldFile)

# Importa la lista delle correzioni dal file csv 'correzione.csv', il cui carattere
# separatore è la tabulazione, e le trasforma in due dizionari. Il dizionario
# 'correzione' dice con cosa sostituire, il dizionario 'procedura' dice se farlo
# interattivamente o automaticamente.
correzioni = {}
procedura = {}
with open('correzioni.csv','r') as c:
	for cl in c.readlines():
		if not cl.startswith('#'):
			autoInter, sbagliato, giusto = cl[:-1].split('\t')
			correzioni[sbagliato] = giusto
			procedura[sbagliato]  = autoInter
			# Nel file 'correzioni.csv', se bisogna cancellare una stringa,
			# dopo il tab ho messo la stringa 'cancella'
			if correzioni[sbagliato] == 'cancella':
				correzioni[sbagliato] = ''

# Innanzitutto controlla se ci sono caratteri non-ASCII
checkfile(oldFile)

# Fa in modo che le uniche interruzioni di riga siano quelle dopo <BR> e che
# tra i <BR> e i \n non ci siano spazi
b=open(newFile,'w')
with open(oldFile) as f:
    print(' '.join(line.strip() for line in f).replace('<BR> ','<BR>\n'),file=b)
b.close()

# D'ora in poi effettua effettivamente le sostituzioni e scrive l'output
# nel file col nome file che indica la nuova versione

a=open(oldFile,'r')
#sgn
b=open(newFile,'w')
c=open('tag_strani_trovati.txt','w')
contaTagStrani = 0

for line in a.readlines():
	for indesiderato in correzioni:
		if re.search(indesiderato,line):
			if procedura[indesiderato] == "auto":
				line = re.sub(indesiderato,correzioni[indesiderato],line)
				if correzioni[indesiderato] == '':
					print('Cancello '+indesiderato)
				else:
					print('Sostituisco '+indesiderato+' con '+correzioni[indesiderato])
			elif procedura[indesiderato] == "inter":
				if alimConferma.confermaSostituz(indesiderato,correzioni[indesiderato],line):
					line = re.sub(indesiderato,correzioni[indesiderato],line)
					print('Fatto. Il risultato è\n\t' + line)
				else:
					print('OK, non sostituisco niente. La riga resta\n\t' + line)
			else:
				print('Non so se la procedura per '+indesiderato+' sia "auto" o "inter"')
				while True:
					testo_risposta = input('OK?').lower()
					if testo_risposta is not '':
						break
	print(line, end='')
	print(line, file=b, end='')

	# Se la riga contiene un altro tag che non sia <B>, <BR>, <I> o <P>, lo scrive
	# nel file "tag_strani_trovati.txt"
	tagStrani = re.search('<[a-zAC-HJ-OQ-Z].*?>',line)
	if tagStrani:
                contaTagStrani += 1
                print(tagStrani.group(0),file=c)

# Comunica se sono stati trovati o no tag 'strani'
abbrevTag = 'tag \'strani\' (cioè diversi da <B>, <BR>, <I> o <P>)'
if contaTagStrani == 0:
        print('\n---\n\nNon sono stati trovati %s' % abbrevTag)
else:
        print('\n---\n\nSono stati trovati %d %s\n' % contaTagStrani, abbrevTag)
        print('\nL\'elenco di tali tag è nel file "tag_strani_trovati.txt"\n')

a.close()
b.close()
c.close()
