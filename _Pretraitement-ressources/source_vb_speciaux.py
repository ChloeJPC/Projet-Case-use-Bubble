# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 21:21:38 2021

@author: Pauline Mas

Tri d'une liste de verbes en trois fichiers séparés suivant le cas attribué à leur complément.
"""

fileSource = open("source_vb_speciaux.txt", encoding="utf8", mode='r')
contentFile = fileSource.readlines()
fileSource.close()


lignes = [ line.strip("\n").split(" ") for line in contentFile]
tabA = ""
tabD = ""
tabG = ""
#print(lignes[0])
for line in lignes:
	if line[1] == "+A" or line[2] == "+A" or line[3] == "+A":
		tabA += line[0] + "\n"
	if line[1] == "+D" or line[2] == "+D" or line[3] == "+D":
		tabD += line[0] + "\n"
	if line[1] == "+G" or line[2] == "+G" or line[3] == "+G":
		tabG += line[0] + "\n"

productA = open("vb_acc.txt", encoding="utf8", mode='w')
productA.write(tabA[:-1])
productA.close()

productD = open("vb_dat.txt", encoding="utf8", mode='w')
productD.write(tabD[:-1])
productD.close()

productG = open("vb_gen.txt", encoding="utf8", mode='w')
productG.write(tabG[:-1])
productG.close()
