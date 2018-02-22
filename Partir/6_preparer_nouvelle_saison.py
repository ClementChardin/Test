import selection as s
from date import *

clubs = []
for nom in s.noms_clubs:
    print nom
    cc = s.charger(nom, 'c', lire_date())
    clubs.append(cc)

incrementer_date()

for cc in clubs:
    for jj in cc.get_all_joueurs():
        key = 's'+str(lire_date()-1)
        if key in cc.jj_passe.keys():
            raise ValueError()
        jj.jj_passe[key] = jj
    cc.sauvegarder(lire_date())
    comp = s.compo()
    comp.sauvegarder(cc.nom + '_defaut', cc.nom, 'c')
