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
contatore = 0

for rigaNuova in a.readlines():
        if rigaVecchia is not '':   # Se non siamo alla prima riga, quindi c'è una riga precedente
                if rigaVecchia.endswith('-<BR>\n'):    # Se la riga precedente finiva col trattino.
                        contatore += 1
                        print('Trattino n. '+str(contatore))
                        # Non c'è bisogno di mettere un 'else', perché se la rigaVecchia non
                        # finisce con un trattino, va stampata così com'è.
                        # sgn print('\n---\n\nDivido la riga:\n\t'+rigaNuova+'in:',end='')
                        primaParola, _, rigaNuova = rigaNuova.partition(' ') # Rispetto a split(), pare
                                # che partition() funzioni anche se c'è una parola sola nel rigo.
                        # sgn print('\nPrima parola:\t'+primaParola+'\ne\nResto:\t'+rigaNuova+'\n')

                        if rigaNuova in whitespace:   # Se la seconda riga ha una parola sola.
                        #if rigaNuova == '':   # Se la seconda riga ha una parola sola.
                                rigaVecchia, _, ultParola = rigaVecchia.rpartition(' ')
                                rigaVecchia += '<BR>\n'
                                rigaNuova = ''.join([ultParola, primaParola]).replace('-<BR>\n','')
                        else:   # Se la seconda riga ha più di una parola.
                                rigaVecchia = ''.join([rigaVecchia, primaParola]).replace('-<BR>\n','')+'<BR>\n'
                                # sgn print('La riga "fusa" è: '+rigaVecchia)
                print(rigaVecchia, file=b, end='')      # Stampa la riga solo se non è la prima riga
        rigaVecchia = rigaNuova         # La riga nuova diventa vecchia, sia che siamo alla prima
                                        # riga sia che siamo alle successive
                                        
print(rigaVecchia, file=b, end='')      # Questo serve per stampare l'ultima riga del file.
print('Ho trovato '+str(contatore)+' trattini.')

	
a.close()
b.close()
