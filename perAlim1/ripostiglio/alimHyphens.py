#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Questo script prende come input un html, unisce le parole separate
# da trattini andando a capo, e scrive l'output in un altro file html. 

import os
import re
import alimConferma
import alimGestisciFile
from string import whitespace
os.system('clear')

oldFile = alimGestisciFile.scegli('html')
if oldFile == '':
        exit('Esco perché non ho niente da fare')

# D'ora in poi effettua effettivamente le sostituzioni e scrive l'output
# in un file, al cui nome file viene aggiunto '_2.0', dunque file_1.0
# (o file_1.1.html etc.) diventa file_2.0.html

a=open(oldFile,'r')
b=open(alimGestisciFile.nuovaVersione(oldFile),'w')

rigaVecchia = ''       # La riga cui attaccare la parola alla fine
contaTutti = 0
contaPortaSopra = 0
contaPortaSotto = 0

for rigaNuova in a.readlines():
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
                                
                print(rigaVecchia, file=b, end='')      # Stampa la riga solo se non è la prima riga
        rigaVecchia = rigaNuova         # La riga nuova diventa vecchia, sia che siamo alla prima
                                        # riga sia che siamo alle successive
                                        
print(rigaVecchia, file=b, end='')      # Questo serve per stampare l'ultima riga del file.
print('\nHo trovato\t'+str(contaTutti)+' trattini.\n'
        '\t\t'+str(contaPortaSopra)+' spezzoni di parola sono stati portati sopra e\n'
        '\t\t'+str(contaPortaSotto)+' sotto.')
	
a.close()
b.close()
