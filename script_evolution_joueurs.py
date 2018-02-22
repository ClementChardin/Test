import selection as s
from changement_saison import *

clubs_saison_prec = []
for nom in s.noms_clubs:
    cc = s.charger(nom, 'c', lire_date()-1)
    clubs_saison_prec.append(cc)

for nom in s.noms_clubs:
    print nom
    cc = s.charger(nom, 'c')
    for jj in cc.get_all_joueurs():
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
                     'fatigue'):
            setattr(jj, attr, 0)
        jj.MJ1 = {'CR': 0, 'CT': 0, 'SR': 0, 'ST': 0}
        jj.MJ2 = {'CR': 0, 'CT': 0, 'SR': 0, 'ST': 0}
        jj.MJ3 = {'CR': 0, 'CT': 0, 'SR': 0, 'ST': 0}
        cc_prec = clubs_saison_prec[s.noms_clubs.index(club_saison_prec(jj))]
        jj.jj_passe['s'+str(lire_date()-1)] = cc_prec.get_joueur_from_nom(jj.nom)
    cc.sauvegarder()

