import selection as s
from changement_saison import *

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
clubs = []
noms_clubs = []
for nom in s.noms_clubs:
    print nom
    cc = s.charger(nom, 'c')
    clubs.append(cc)
    noms_clubs.append(nom)
    for jj in cc.get_all_joueurs():
        dernier_transfert = jj.anciens_clubs.split(';')[-1]
        if dernier_transfert == '':
            date = 0
        else:
            try:
                date = int(dernier_transfert[-2:-1])
            except ValueError:
                date = int(dernier_transfert[-1])
        if jj.veut_partir and date <= 10 and jj.MS_probleme:
            ll.append(jj)
ll.sort(key=lambda jj: s.ordre_postes[jj.postes[1]])

prochain = 'Denen'
prochain_atteint = False
offres = []

with open('Partir\offres_rester.txt', 'w') as ff:
    for jj in ll:
        prochain_atteint = prochain_atteint or jj.nom == prochain
        if prochain_atteint:
            cc = clubs[noms_clubs.index(jj.club)]
            comp = cc.compo_defaut
            if jj.club == 'vide':
                priorite = 4
            else:
                if jj.nom in comp.noms_titulaires:
                    inf = 'tit'
                elif jj.nom in comp.noms_remplacants:
                    inf = 'remp'
                else:
                    inf = ''
                st = raw_input(jj.nom + ' ' + \
                               jj.club + ' ' + \
                               str(round(jj.EV, 2)) + ' ' + \
                               "D = " + str(jj.D) + ' ' + \
                               inf + ' ' + \
                               str(pts_matches_club(jj)) + ' ? ')
                priorite = 0 if st == '' else int(st)
            if not priorite == 0:
                poste = jj.postes[1]
                offre = faire_offre(jj, priorite, poste)
                offres.append((jj.nom, offre[1]))
                wr = jj.nom + '\t' + str(offre[1])
                ff.write(wr)
