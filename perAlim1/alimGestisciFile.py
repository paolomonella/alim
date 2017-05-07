#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Funzioni per gestire i file di input e di output """


import os
import re
import alimConferma
os.system('clear')

def scegli(estensione):
    """ Lista i file con una data estensione e chiede all'utente di sceglierne
    uno. Attenzione: se non è stato scelto nessun file, ritorna ''   """
    
    oldFile = ''
    print('I file .'+estensione+' presenti nella cartella sono:')
    for f in os.listdir('.'):
            if re.match('.*\.'+estensione+'$', f):
                    print('\t'+f)

    for f in os.listdir('.'):
            if re.match('.*\.'+estensione+'$', f):
                    if alimConferma.conferma('\nDevo lavorare sul file "'+f+'"?\n'):
                        oldFile = f
                        print('OK, lavoro sul file "'+f+'"\n')
                        break
		    
    if oldFile == '':
            print('Non è stato selezionato nessun file')
            # In questo caso ritorna ''

    return oldFile

def nuovaVersione(oldFile):
    """ Se numeroVersione è 4, prende un nome file del tipo file_1.1.html o
    file_3.0.html e lo trasforma in file 4.0.html (con lo zero dopo il punto),
    a prescindere da quale fosse il numero di versione del primo file.
    """

    numeroVersione = input("""Il file di input è """+oldFile+""".
    Che numero di versione vuoi dare al file di output?
    (Se inserisci 12, il nuovo file avrà versione 12.0)\n""")
    newFile = re.sub('\d+\.\d+\.html$', numeroVersione+'.0.html',oldFile)
    print('Il nuovo file si chiamerà '+newFile)
    return newFile