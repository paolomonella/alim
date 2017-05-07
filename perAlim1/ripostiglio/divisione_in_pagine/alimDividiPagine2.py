#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Questo script divide le pagine in singoli file di testo, il cui filename
# è il numero di pagina, su 4 cifre (ad es. 0024 per pagina 24).

import os
os.system('clear')

a=open('00','r')
for line in a.readlines():
	if line.startswith("pag."):
		foo, p = line[:-1].split(" ")
		if p is not "1":
			b.close()
		for i in range(4-len(p)):
			p='0'+p
		b = open(p,'w')
	elif line == "\n":
		continue
	else:
		print(line, file=b)
a.close()
b.close()
