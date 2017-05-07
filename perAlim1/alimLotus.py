#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Questo script 'avvolge' (wrapping) i tag HTML con le parentesi quadre,
# cambiando ad esempio "<B>verbum</B>" in "[<B>] verbum [</B>]"
# (vd. Norme_ALIM_1.1.pdf, paragrafo 4.2). Prende come input un file html
# e scrive l'output in un altro file html con "_3.0" alla fine del nome file.
#
# Una versione precedente di questo script toglieva i <BR>. Questo perché
#   prima normalmente salvavo i file LibreOffice in .html, e LibreOffice
#   metteva dei <BR> alla fine di ogni rigo. Ora però salvo i file di LibreOffice
#   in .txt e aggiungo io a mano tutti i tag, quindi ho commentato qui sotto
#   la parte dello script che faceva questo, cioè la riga
#   line = re.sub(r'\s*<BR>','',line)


import os
import re
import sys
import alimGestisciFile

os.system('clear')

###########################
# FILE DI INPUT ED OUTPUT #
###########################

# Se non è stato specificato come argomento dello script,
# chiede qual è il file di input
if len(sys.argv) > 1:
        oldFile = sys.argv[1]
else:
        oldFile = alimGestisciFile.scegli('html')
        if oldFile == '':
                exit('Esco perché non ho niente da fare')

#########################################
# EFFETTUA SOSTITUZIONI E SCRIVE OUTPUT #
#########################################

a=open(oldFile,'r')
b=open(alimGestisciFile.nuovaVersione(oldFile),'w')

for line in a.readlines():
	# Toglie <BR> inclusi eventuali spazi subito prima
	# line = re.sub(r'\s*<BR>','',line)
	# "?" rende "*" non-greedy
	# Tag d'apertura (ci mette uno spazio dopo):
	line = re.sub(r'(<\w.*?>)( *)',r'[\1] ',line)
##	# Toglie lo spazio che, col comando precedente, ha inserito dopo <BR>, e lo mette prima
##	line = re.sub(r'(.)(\s*)(\[<BR>\])( *)',r'\1\4\3',line)
	# Tag di chiusura (ci mette uno spazio prima):
	line = re.sub(r'(.)(\s*)(<\/.*?>)',r'\1 [\3]',line)
	# Commenti a fine riga (quando ha portato sopra)
	line = re.sub(r'(.)(\s*)(<!--.*?-->)',r'\1 [\3]',line)
	# Commenti a inizio riga (quando ha portato sotto)
	line = re.sub(r'^(<!--.*?-->)',r'[\1] ',line)
        # I <BR /> che io ho inserito a mano a fine riga per codificare le righe vuote significative
        #   (tra l'altro, la riga qui sopra sui tag d'apertura dovrebbe averci messo inopportunamente
        #    uno spazio dopo, che qui sto togliendo))
	line = re.sub(r'(\[<BR \/>\]) ',r' \1',line)
	print(line, file=b, end='')

a.close()
b.close()