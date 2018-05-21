# -*- coding: cp1252 -*-
from changement_saison import *

"""
Script qui décide des départs et des retraites
A lancer avant le changement de date !
"""

res = ''
ll = []
for nom in s.noms_clubs():
    print '\n' + nom
    cc = s.charger(nom, 'c')
    for jj in cc.get_all_joueurs():
        vp, msp = veut_partir(jj)
        jj.veut_partir = vp
        jj.MS_probleme = msp
        retraite(jj, dat=s.lire_date()+1)
    cc.sauvegarder()

    for jj in cc.get_all_joueurs():
        line = ''
        if jj.veut_partir:
            for it in (jj.postes[1], jj.postes[2], jj.postes[3], jj.RG.rang, jj.RG_max.rang,
                       jj.C, jj.D, jj.MS_probleme, jj.VAL, jj.MS, jj.club, jj.nom, jj.EV):
                line += str(it) + '\t'
            line += '\n'
            ll.append(line)

vide = s.charger('vide', 'c')
for jj in vide.get_all_joueurs():
    line = ''
    vp, msp = veut_partir(jj)
    jj.veut_partir = vp
    jj.MS_probleme = msp
    for st in (jj.postes[1], jj.postes[2], jj.postes[3], jj.RG.rang, jj.RG_max.rang,
               jj.C, jj.D, jj.MS_probleme, jj.VAL, jj.MS, jj.club, jj.nom, jj.EV):
        line += str(st) + '\t'
    line += '\n'
    ll.append(line)

ll.sort(key=lambda st: ordre_postes[st[:2]])
for line in ll:
    res += line + '\n'

with open('departs.txt', 'w') as ff:
    ff.write(res)
