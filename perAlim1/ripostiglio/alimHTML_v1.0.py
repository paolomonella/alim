#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# questo script prende come input un html esportato da openoffice/libreoffice in
# html (con file/esporta), fa alcune sostituzioni e scrive
# l'output in un altro file html. 
# la lista delle sostituzioni da compiere è in un csv.
#
# inoltre controlla che non ci siano caratteri non-ascii

import os
import re
import sys,codecs   # servono per cercare i caratteri non-ascii
import alimconferma
import alimgestiscifile
os.system('clear')


###########################
# file di input ed output #
###########################

# se non è stato specificato come argomento dello script,
# chiede qual è il file di input
if len(sys.argv) > 1:
        oldfile = sys.argv[1]
else:
        oldfile = alimgestiscifile.scegli('html')
        if oldfile == '':
                exit('esco perché non ho niente da fare')

# chiede qual è il file di output
newfile = alimgestiscifile.nuovaversione(oldfile)


#############
# non-ascii #
#############

def checkfile(filename):
    # questa funzione sarà usata più sotto in questo stesso script
    f = codecs.open(filename,encoding='ascii')
    contaerrascii = 0

    lines = open(filename).readlines()
    print('cerco caratteri non-ascii\n\tnumero totale di righe: %d' % len(lines))
    for i in range(0,len(lines)):
        try:
            l = f.readline()
        except:
            contaerrascii += 1        
            num = i+1
            print('\tcodifica non-ascii alla riga: %d' % num)

    f.close()
    if contaerrascii == 0:
            print('\tnessun carattere non-ascii trovato\n')
    else:
            print('\ttrovati in tutto '+str(contaerrascii)+' caratteri non-ascii.')
            exit('prima di processare ulteriormente il file, sostituisci i caratteri non-ascii.')

# utilizza la funzione sul file
# checkfile(oldfile)


################
# sostituzioni #
################

# importa la lista delle correzioni dal file csv 'correzione.csv', ee le trasforma in
# due dizionari. il dizionario 'correzione' dice con cosa sostituire, il dizionario
# 'procedura' dice se farlo interattivamente o automaticamente.
correzioni = {}
procedura = {}
with open('correzioni.csv','r') as c:
    for cl in c.readlines():
        if not cl.startswith('#'):
            autointer, sbagliato, giusto = cl[:-1].split('\t')
            correzioni[sbagliato] = giusto
            procedura[sbagliato]  = autointer
            # nel file 'correzioni.csv', se bisogna cancellare una stringa,
            # dopo il tab ho messo la stringa 'cancella'
            if correzioni[sbagliato] == 'cancella':
                correzioni[sbagliato] = ''

# effettua le sostituzioni indicate nel file 'correzioni.csv'

a=open(oldfile,'r')
with open(oldfile) as f:
    testoorig = f.readlines()
c=open('tag_strani_trovati.txt','w')
contatagstrani = 0
testopulito = []

for line in testoorig:
    for indesiderato in correzioni:
        if re.search(indesiderato,line):
            if procedura[indesiderato] == "auto":
                line = re.sub(indesiderato,correzioni[indesiderato],line)
                if correzioni[indesiderato] == '':
                    print('cancello '+indesiderato)
                else:
                    print('sostituisco '+indesiderato+' con '+correzioni[indesiderato])
            elif procedura[indesiderato] == "inter":
                if alimconferma.confermasostituz(indesiderato,correzioni[indesiderato],line):
                    line = re.sub(indesiderato,correzioni[indesiderato],line)
                    print('fatto. il risultato è\n\t' + line)
                else:
                    print('ok, non sostituisco niente. la riga resta\n\t' + line)
            else:
                print('non so se la procedura per '+indesiderato+' sia "auto" o "inter"')
                while true:
                    testo_risposta = input('OK?').lower()
                    if testo_risposta is not '':
                        break
    testoPulito.append(line)    # Ogni riga dovrebbe già finire con \n qui

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
        print('\n---\n\nSono stati trovati %d %s\n' % (contaTagStrani, abbrevTag))
        print('\nL\'elenco di tali tag è nel file "tag_strani_trovati.txt"\n')

########
# <BR> #
########

# Fa in modo che le uniche interruzioni di riga siano quelle dopo <BR> e che
# tra i <BR> e i \n non ci siano spazi
testoBR = ' '.join(line.strip('\n') for line in testoPulito).replace('<BR> ','<BR>\n<fineriga>').split('<fineriga>')    # è una lista

############
# TRATTINI #
############

# a=open(oldFile,'r')
# b=open(alimGestisciFile.nuovaVersione(oldFile),'w')

# Inizializza una serie di variabili
rigaVecchia = ''       # La riga cui attaccare la parola alla fine
contaTutti = 0
contaPortaSopra = 0     # Conta quante volte ha portato lettere sopra
contaPortaSotto = 0     # Conta quante volte ha portato lettere sotto
contaAFinePag = 0       # Conta quante volte ha trovato trattini a fine pagina

testoTrattini = []  # è una lista

fp=open('righe_con_trattini_a_fine_pagina.txt','w')    # Scrive qui le righe con trattini a fine pag.

for rigaNuova in testoBR:
        rigaNuova = rigaNuova.lstrip()   # Gli spazi iniziali in questo caso vanno tolti sempre
        if rigaVecchia is not '':   # Se non siamo alla prima riga, quindi c'è una riga precedente
                m = re.search('-(<.*?>\s*)*<BR>\n', rigaVecchia)
                if m:
                        spezz = m.group(0)
                        if m.group(1):
                                tag  = m.group(1)
                        else:
                                tag = ''
                        contaTutti += 1
                        if re.match(r'(<\w+?>)*\w+?[\.\?\!\:\;\s]*(</\w+?>)*[\.\?\!\:\;\s]*<BR>',rigaNuova): # Se la seconda riga ha una parola sola e poi <BR> (porta sotto).
                                # Questa regex non funziona perfettamente. Porta sotto anche nel caso
                                # che la riga di sotto abbia tante parole, purché inizi con un tag
                                # Comunque, per sicurezza bisogna poi controllare tutti gli "ad lineam posteriorem"
                                # (vd. stringa "avvPortaSotto") uno per uno, se ce ne sono.
                                contaPortaSotto += 1
                                rigaVecchia, _, ultParola = rigaVecchia.rpartition(' ')
                                rigaVecchia += '<BR>\n'
                                if m.group(1):  # Se ci sono tag tra "-" e "<BR>", fammeli vedere
                                        print('Spezz: "'+spezz[:-1]+'"')
                                        print('Tag:   "'+tag+'"')
                                avvPortaSotto = ('<!-- Litteras "'+ultParola.replace('-<BR>\n','')+'" lineae prioris '
                                        'ad lineam posteriorem transposuit Paulus Monella -->') # Avviso
                                rigaNuova = ''.join([avvPortaSotto, ultParola, rigaNuova]).replace(spezz,tag)
                        elif re.match(r'<BR>',rigaNuova): # Se la seconda riga ha solo <BR> (trattino a fine pagina).
                                contaAFinePag += 1
                                print(rigaVecchia, file=fp, end='')     # Poi processerò queste righe manualmente
                                rigaVecchia = re.sub('<BR>','<!-- Trattino a fine pagina n. '+str(contaAFinePag)+' --><BR>',rigaVecchia)
                        else:   # Se la seconda riga ha più di una parola (porta sopra).
                                contaPortaSopra += 1
                                primaParola, _, rigaNuova = rigaNuova.partition(' ') # Rispetto a split(),
                                # pare che partition() funzioni anche se c'è una parola sola nel rigo.
                                avvPortaSopra = ('<!-- Litteras "'+primaParola+'" '
                                                 'ad lineam priorem transposuit Paulus Monella -->') # Avviso
                                rigaVecchia = ''.join([rigaVecchia, primaParola, avvPortaSopra, '<BR>\n']).replace(spezz,tag)
                                
                testoTrattini.append(rigaVecchia)   # Licenzia riga solo se non è la prima riga
                #print(rigaVecchia, file=b, end='')      
        rigaVecchia = rigaNuova         # La riga nuova diventa vecchia, sia che siamo alla prima
                                        # riga sia che siamo alle successive
                                        
testoTrattini.append(rigaVecchia)   # Questo serve per licenziare anche l'ultima riga del file.

fp.close()

# Comunica i trattini che ha trovato
print('\n---\n\nHo trovato\t'+str(contaTutti)+' trattini.\n'
        '\t\t'+str(contaPortaSopra)+' spezzoni di parola sono stati portati sopra e\n'
        '\t\t'+str(contaPortaSotto)+' sotto.\n'
        '\t\t'+str(contaAFinePag)+' trattini sono a fine pagina. Le righe relative sono state scritte\n'
        '\t\t\tsul file "righe_con_trattini_a_fine_pagina.txt"\n')


#########################
# SCRIVE OUTPUT SU FILE #
#########################

# Scrive l'output nel file
with open(newFile,'w') as f:
    for line in testoTrattini:
        print(line, end='', file=f)
