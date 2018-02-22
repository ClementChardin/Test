import selection as s
from changement_saison import evolution_TAB

for nom in s.noms_clubs:
    print nom
    cc = s.charger(nom, 'c')
    for jj in cc.get_all_joueurs():
        evolution_TAB(jj)
        if s.est_un_avant(jj):
            evolution_TAB(jj, car='JP')
            evolution_TAB(jj, car='P')
    cc.sauvegarder()
