import selection as s
from changement_saison import *

def joue_coupe(nom):
    if nom in ('KHR', 'SN', 'FS', 'BRB', 'MDL', 'HTH',
               'MRB', 'ALT', 'KAK', 'TA', 'DKW', 'MSL'):
        return True
    elif nom in ('QNL', 'AL', 'TLB', 'DKF', 'PRG', 'BSK',
                 'APA', 'TO', 'CAT', 'KH', 'ED', 'GP', 'vide'):
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

lines_partir = []
lines_rester = []

with open('Partir\offres_rester.txt', 'r') as ff:
    for line in ff.readlines():
        lines_rester.append(line)

with open('Partir\offres_preferees.txt', 'r') as ff:
    for line in ff.readlines():
        lines_partir.append(line)
    
choix = []
noms_rester = [lines_rester[ii].split('\t')[0] for ii in range(len(lines_rester))]
noms_partir = [lines_partir[ii].split('\t')[0] for ii in range(len(lines_partir))]
for jj in ll:
    if jj.nom in noms_rester and jj.nom in noms_partir \
       and not lines_partir[noms_partir.index(jj.nom)].split('\t')[1] == '':
        idx_rester = noms_rester.index(jj.nom)
        idx_partir = noms_partir.index(jj.nom)
        nom_club = lines_partir[idx_partir].split('\t')[1]
        ms_partir = int(lines_partir[idx_partir].split('\t')[3])
        sc1 = score_offre(jj,
                            clubs[noms_clubs.index(nom_club)],
                            ms_partir,
                            joue_coupe(nom_club))
        ms_rester = int(lines_rester[idx_rester].split('\t')[1])
        sc2 = score_offre(jj,
                            clubs[noms_clubs.index(jj.club)],
                            ms_rester,
                            joue_coupe(jj.club))
        total = max(0, sc1) + max(1, sc2)
        rand = random.random_integers(total)
        if rand <= sc1:
            choix.append(lines_partir[noms_partir.index(jj.nom)])
        else:
            choix.append(lines_rester[noms_rester.index(jj.nom)])
    elif jj.nom in noms_rester:
        choix.append(lines_rester[noms_rester.index(jj.nom)])
    elif jj.nom in noms_partir:
        choix.append(lines_partir[noms_partir.index(jj.nom)])

with open('Partir\choix.txt', 'w') as ff:
    for ch in choix:
        ff.write(ch)
