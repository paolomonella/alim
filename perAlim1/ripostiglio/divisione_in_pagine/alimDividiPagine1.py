#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Questo script divide le singole pagina in elementi XML <div>.
# Il suo otuput attualmente è STDOUT

import os
os.system('clear')

a=open('01','r')
#b=open('02','w')
t = ""
for line in a.readlines():
	if line.startswith("pag."):
		foo, p = line[:-1].split(" ")
		if p is not 1:
		print('<div n="'+p+'" type="page">'+t[:-1]+'</div>\n')
		#print('<div n="'+p+'" type="page">\n'+t+'\n</div>\n', file=b)
		t = ""
	else:
		t = t+line
#	if line.startswith("                    </td>") or line.startswith("IFTTT"):
#		print("Trovato!")
#		pr = False
#	if pr:
#		print(line[:-1], file=b)
a.close()
#b.close()
# L=[1,2,3,4,5,6,7]
# print L[0::2]
