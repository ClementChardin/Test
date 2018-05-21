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
        jj.jj_passe[key] = jj_aux
    cc.sauvegarder(lire_date())
    comp = s.compo()
    comp.sauvegarder(cc.nom + '_defaut', cc.nom, 'c')
