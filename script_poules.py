# -*- coding: cp1252 -*-
"""
Initalisation des poules de coupe et de challenge

Coupe : 4 poules de 4
Challenge : 5 poules de 4

Coupe :
- chapeau 1 : 1 & 2 de Vieux Monde & de Nouvzauw Mondes
- chapeau 2 : 3 & 4 de Vieux Monde & de Nouvzauw Mondes
- chapeau 3 : 5 & 6 de Vieux Monde & de Nouvzauw Mondes
- chapeau 4 : 7 de Vieux Monde & de Nouvzauw Mondes + 1 de Nord & de Sud

Challenge:
- chapeau 1 : 8 & 9 de Vieux Monde & de Nouveaux Mondes
              + meilleur 2ème de Nord & Sud
- chapeau 2 : 10 & 11 de Vieux Monde & de Nouveaux Mondes
              + moins bon 2ème de Nord & Sud
- chapeau 3 : 12 de Vieux Monde & de Nouveaux Mondes
              + 3 de Nord & de Sud
              + meilleur 4ème de Nord & Sud
- chapeau 4 : moins bon 4ème de Nord & Sud
              + 5 & 6 de Nord & de Sud
"""
from random import *

chap1 = ['TA', 'MRB', 'BRB', 'FS']
chap2 = ['MSL', 'QNL', 'KHR', 'KH']
chap3 = ['ALT', 'AL', 'HTH', 'ED']
chap4 = ['KAK', 'APA', 'AES', 'MRT']

chapch1 = ['PRG', 'BSK', 'MDL', 'TO', 'KKR']
chapch2 = ['DKW', 'TLB', 'SN', 'GP', 'BIL']
chapch3 = ['DKF', 'CAT', 'ERE', 'AHK', 'MAG']
chapch4 = ['FST', 'KIS', 'MDH', 'CPH', 'EKR']

for ll in (chap1, chap2, chap3, chap4, chapch1, chapch2, chapch3, chapch4):
    shuffle(ll)

for ii in range(4):
    print "\nCoupe poule", ii+1
    print chap1[ii]
    print chap2[ii]
    print chap3[ii]
    print chap4[ii]

for ii in range(5):
    print "\nChallenge poule", ii+1
    print chapch1[ii]
    print chapch2[ii]
    print chapch3[ii]
    print chapch4[ii]

