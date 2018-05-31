import selection as s
from date import *
import os

clubs = []
for nom in s.noms_clubs():
    print nom
    cc = s.charger(nom, 'c', lire_date())
    clubs.append(cc)

incrementer_date()

os.mkdir(s.SELECTIONS_DIR_NAME())
os.mkdir(s.CLUBS_DIR_NAME())
os.mkdir(s.TRANSFERTS_DIR_NAME())
os.mkdir(s.CALENDRIERS_DIR_NAME())


for cc in clubs:
    for jj in cc.get_all_joueurs():
        key = 's'+str(lire_date()-1)
        if key in jj.jj_passe.keys():
            raise ValueError()
        jj_aux = s.joueur()
        jj_aux.caracs_sans_fatigue = jj.caracs_sans_fatigue
        jj_aux.EV = jj.EV
        jj_aux.nom = jj.nom
        jj_aux.club = jj.club
        jj_aux.postes = jj.postes
        jj.jj_passe[key] = jj_aux
        jj_aux.MJ1 = jj.MJ1
        jj_aux.MJ1_total = jj.MJ1_total
        jj_aux.MJ2 = jj.MJ2
        jj.MJ2_total = jj.MJ2_total
        jj_aux.MJ3 = jj.MJ3
        jj_aux.MJ3_total = jj.MJ3_total
        jj_aux.essais_saison = jj.essais_saison
        jj_aux.transformations_saison = jj.transformations_saison
        jj_aux.transformation_ratees_saison = jj.transformation_ratees_saison
        jj_aux.penalites_saison = jj.penalites_saison
        jj_aux.penalite_ratees_saison = jj.penalite_ratees_saison
        jj_aux.drops_saison = jj.drops_saison
        jj_aux.drop_rates_saison = jj.drop_rates_saison


    cc.sauvegarder(lire_date())
    comp = s.compo()
    comp.sauvegarder(cc.nom + '_defaut', cc.nom, 'c')
