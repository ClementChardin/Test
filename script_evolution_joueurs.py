# -*- coding: cp1252 -*-
import selection as s
from changement_saison import *

dat = s.lire_date()
"""
Plus besoin des clubs de la saison précédente : ce script est maintenant
utilisé après la création de la nouvelle saison

clubs_saison_prec = []
for nom in s.noms_clubs:
    cc = s.charger(nom, 'c', dat-1)
    clubs_saison_prec.append(cc)
"""
for nom in s.noms_clubs(dat):
    print nom
    cc = s.charger(nom, 'c', dat)
    for jj in cc.get_all_joueurs():
        if not jj.C == dat: #pour éviter joueurs légendaires
            evolution_joueur(jj)
            for attr in ('drop_rates_saison',
                         'essais_saison',
                         'penalite_ratees_saison',
                         'transformations_saison',
                         'penalites_saison',
                         'blessures_saison',
                         'rouges_saison',
                         'drops_saison',
                         'transformation_ratees_saison',
                         'jaunes_saison',
                         'blessure',
                         'fatigue',
                         'experience_saison'):
                setattr(jj, attr, 0)
            jj.MJ1 = {'CR': 0, 'CT': 0, 'SR': 0, 'ST': 0}
            jj.MJ2 = {'CR': 0, 'CT': 0, 'SR': 0, 'ST': 0}
            jj.MJ3 = {'CR': 0, 'CT': 0, 'SR': 0, 'ST': 0}
            #cc_prec = clubs_saison_prec[s.noms_clubs.index(club_saison_prec(jj))]
            #jj.jj_passe['s'+str(lire_date()-1)] = cc_prec.get_joueur_from_nom(jj.nom)
            #jj.jj_passe['s'+str(lire_date()-1)].EV = s.calc_EV(jj.jj_passe['s'+str(lire_date()-1)],
            #                                                   jj.jj_passe['s'+str(lire_date()-1)].postes[1],
            #                                                   fatigue=False)
    cc.sauvegarder(dat)

