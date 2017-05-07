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
import sys,codecs   # Servono per cercare i caratteri non-ASCII
import alimConferma
import alimGestisciFile
os.system('clear')


###########################
# FILE DI INPUT ED OUTPUT #
###########################

# Chiede qual è il file di input
oldFile = alimGestisciFile.scegli('html')
if oldFile == '':
        exit('Esco perché non ho niente da fare')

# Chiede qual è il file di output
newFile = alimGestisciFile.nuovaVersione(oldFile)


#############
# NON-ASCII #
#############

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

# Utilizza la funzione sul file
checkfile(oldFile)


################
# SOSTITUZIONI #
################

# Importa la lista delle correzioni dal file csv 'correzione.csv', ee le trasforma in
# due dizionari. Il dizionario 'correzione' dice con cosa sostituire, il dizionario
# 'procedura' dice se farlo interattivamente o automaticamente.
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

# Effettua le sostituzioni indicate nel file 'correzioni.csv'

a=open(oldFile,'r')
with open(oldFile) as f:
    testoOrig = f.readlines()
#sgn b=open(newFile,'w')
c=open('tag_strani_trovati.txt','w')
contaTagStrani = 0
testoPulito = []

for line in testoOrig:
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
        print('\n---\n\nSono stati trovati %d %s\n' % contaTagStrani, abbrevTag)
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
contaPortaSopra = 0
contaPortaSotto = 0

testoTrattini = []  # è una lista

for rigaNuova in testoBR:
        rigaNuova = rigaNuova.lstrip()   # Gli spazi iniziali in questo caso vanno tolti sempre
        if rigaVecchia is not '':   # Se non siamo alla prima riga, quindi c'è una riga precedente
                m = re.search('-(<.*?>\s*)*<BR>\n', rigaVecchia)
                if m:
                # if rigaVecchia.endswith('-<BR>\n'):    # Se la riga precedente finiva col trattino.
                        spezz = m.group(0)
                        if m.group(1):
                                tag  = m.group(1)
                        else:
                                tag = ''
                        contaTutti += 1

                        if re.match(r'\W*\w+\W*<BR>',rigaNuova): # Se la seconda riga ha una parola sola e poi <BR> (porta sotto).
                                # Attenzione: lo script non gestisce bene il caso in cui la nuova riga fosse
                                #       tionis<BR>et omnia...
                                # Ma, per come esporta LibreOffice in HTML, questo caso non dovrebbe darsi mai.
                                # Comunque, per sicurezza bisogna poi controllare tutti gli "ad lineam posteriorem"
                                # (vd. stringa "avvPortaSotto") uno per uno, se ce ne sono.
                                contaPortaSotto += 1
                                rigaVecchia, _, ultParola = rigaVecchia.rpartition(' ')
                                rigaVecchia += '<BR>\n'
                                if m.group(1):  # Se ci sono tag tra "-" e "<BR>", fammeli vedere
                                        print('Spezz: "'+spezz[:-1]+'"')
                                        print('Tag:   "'+tag+'"')
                                avvPortaSotto = ('<!--Litteras "'+ultParola.replace('-<BR>\n','')+'" lineae prioris '
                                        'ad lineam posteriorem transposuit Paulus Monella-->\n') # Avviso
                                rigaNuova = ''.join([ultParola, rigaNuova, avvPortaSotto]).replace(spezz,tag)

                        else:   # Se la seconda riga ha più di una parola (porta sopra).
                                contaPortaSopra += 1
                                primaParola, _, rigaNuova = rigaNuova.partition(' ') # Rispetto a split(),
                                # pare che partition() funzioni anche se c'è una parola sola nel rigo.
                                avvPortaSopra = ('<!--Litteras "'+primaParola[:-1]+'" '
                                                 'ad lineam priorem transposuit Paulus Monella-->\n') # Avviso
                                rigaVecchia = ''.join([rigaVecchia, primaParola, avvPortaSopra, '<BR>\n']).replace(spezz,tag)
                                
                testoTrattini.append(rigaVecchia)   # Licenzia riga solo se non è la prima riga
                #print(rigaVecchia, file=b, end='')      
        rigaVecchia = rigaNuova         # La riga nuova diventa vecchia, sia che siamo alla prima
                                        # riga sia che siamo alle successive
                                        
testoTrattini.append(rigaVecchia)   # Questo serve per licenziare anche l'ultima riga del file.
print('\nHo trovato\t'+str(contaTutti)+' trattini.\n'
        '\t\t'+str(contaPortaSopra)+' spezzoni di parola sono stati portati sopra e\n'
        '\t\t'+str(contaPortaSotto)+' sotto.')



#########################
# SCRIVE OUTPUT SU FILE #
#########################

# Scrive l'output nel file
with open(newFile,'w') as f:
    for line in testoTrattini:
        print(line, end='\n', file=f)
