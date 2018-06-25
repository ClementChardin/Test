# -*- coding: cp1252 -*-
import selection as s
from changement_saison import evolution_TAB

dat = s.lire_date()

for nom in s.noms_clubs(dat):
    print nom
    cc = s.charger(nom, 'c', dat)
    for jj in cc.get_all_joueurs():
        if not jj.C == dat: #Pour éviter les joueurs légendaires
            evolution_TAB(jj)
            if s.est_un_avant(jj):
                evolution_TAB(jj, car='JP')
                evolution_TAB(jj, car='P')
    cc.sauvegarder(dat)
