import selection as s
from changement_saison import *

"""
Une fois que les départs sont faits,
Tous les joueurs n'aillant pas choisi de nouveau club sont dans Vide
"""

def joue_coupe(nom):
    if nom in ('KHR', 'SN', 'FS', 'BRB', 'MDL', 'HTH',
               'MRB', 'ALT', 'KAK', 'TA', 'DKW', 'MSL'):
        return True
    elif nom in ('QNL', 'AL', 'TLB', 'DKF', 'PRG', 'BSK',
                 'APA', 'TO', 'CAT', 'KH', 'ED', 'GP'):
        return False
    else:
        raise ValueError()

ll = []
vide = s.charger('vide', 'c')
for jj in vide.get_all_joueurs():
    dernier_transfert = jj.anciens_clubs.split(';')[-1]
    if dernier_transfert == '':
        date = 0
    else:
        try:
            date = int(dernier_transfert[-2:-1])
        except ValueError:
            date = int(dernier_transfert[-1])
    if jj.veut_partir and date <= 10:
        ll.append(jj)
ll.sort(key=lambda jj: s.ordre_postes[jj.postes[1]])

prochain = 'Klendaeth'
prochain_atteint = False
with open('Partir\offres_deuxieme_round.txt', 'w') as ff:
    for jj in ll:
        prochain_atteint = prochain_atteint or jj.nom == prochain
        if prochain_atteint:
            st = raw_input(jj.nom + ' ? ')
            while st != 'n':
                lll = st.split(' ')
                nom_club = lll[0]
                priorite = int(lll[1])
                if len(lll) < 3:
                    poste = jj.postes[1]
                else:
                    poste = lll[2]
                club = s.charger(nom_club,'c')
                offre = faire_offre(jj, priorite, poste)
                wr = jj.nom + ' ' + nom_club + ' ' +  str(offre[0]) + ' ' + \
                     str(offre[1]) + ' ' \
                     + str(score_offre(jj, club, offre[1], joue_coupe(nom_club))) \
                     +'\n'
                print wr
                ff.write(wr)
                st = raw_input(jj.nom + ' ? ')


