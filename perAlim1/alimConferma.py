#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Questo modulo contiene funzioni che facilitano
    le sostituzioni di testo in un file.
    """

import re

# Dizionario che traduce le risposte in valori booleani
valid = {"yes":True,   "y":True,  "ye":True,
        "sì":True,   "si":True,  "s":True,
        "no":False,     "n":False}

def conferma(richiesta,default='sì'):
        """ Valuta la risposta. Se non c'è stata risposta, restituisce la risposta standard, che può
        essere "sì" o "no" (vd. riga "def" della funzione). Setta 'risposta' a True o False"""

        while True:
                testo_risposta = input(richiesta).lower()
                if default is not None and testo_risposta == '':
                        return valid[default]
                elif testo_risposta in valid:
                        return valid[testo_risposta]
                else:
                        print('Per favore rispondi con "s" o "n" ("sì"/"si"/"yes"/"y" o "no")\n')

def confermaSostituz(sostituendo,sostituito,stringa,default='sì'):
        """Questa funzione chiede se sostituire, all'interno della 'stringa',
        'sostituendo' con 'sostituito'. Esempio:
                conferma('onmia','omnia',line)
        """
        # Costruisce la richiesta sulla base delle stringhe da sostituire
        richiesta = '\n---\n\nNella riga\n\t'+stringa+'Sto '
        if sostituito == '':
                richiesta += 'cancellando\n\t'+sostituendo+'\n'
        else:
                richiesta += 'sostituendo\n\t"'+sostituendo+'"\ncon\n\t"'+sostituito+'"\n'
        richiesta += 'Il risultato sarà\n\t'+ re.sub(sostituendo,sostituito,stringa)
        richiesta += 'Procedo? (s/n)\n'
        return conferma(richiesta)