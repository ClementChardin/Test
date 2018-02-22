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
        if jj.veut_partir and date <= 10:
            ll.append(jj)
ll.sort(key=lambda jj: s.ordre_postes[jj.postes[1]])

#prochain = 'Jens'
#prochain_atteint = False
lines = []
with open('Partir\offres2.txt', 'r') as ff:
    for line in ff.readlines():
        lines.append(line.split('\t'))

idx = 0
nom = lines[idx][0]
scores = []
nom_club = lines[idx][1]
club = clubs[noms_clubs.index(nom_club)]
for jj in ll:
    while nom == jj.nom and idx < len(lines):
        line = lines[idx]
        nom_club = lines[idx][1]
        club = clubs[noms_clubs.index(nom_club)]
        scores.append((nom,
                       score_offre(jj,
                                   club,
                                   int(line[3]),
                                   joue_coupe(line[1]))))
        idx += 1
        if idx < len(lines):
            nom = lines[idx][0]

with open('Partir\offres3.txt', 'w') as ff:
    for sc in scores:
        ff.write(str(sc[0])+'\t'+str(sc[1])+'\n')

totaux = [[lines[0][0], 2]]
# On ajoute 2 pts pour le cas où aucune offre ne convient
for tu in scores:
    if totaux[-1][0] == tu[0]:
        totaux[-1][1] += max(1, tu[1])
    else:
        totaux.append([tu[0], tu[1] + 2])

"""
with open('Partir\offres4.txt', 'w') as ff:
    for tu in totaux:
        ff.write(str(tu[0])+'\t'+str(tu[1])+'\n')
"""

offres_preferees = []
for tu in totaux:
    rand = random.random_integers(tu[1])
    for ii, line in enumerate(lines):
        if line[0] == tu [0]:
            rand -= scores[ii][1]
            if rand <= 0:
                offres_preferees.append(line)
                break
    if rand > 0:
        offres_preferees.append((tu[0], ''))

with open('Partir\offres_preferees.txt', 'w') as ff:
    for offre in offres_preferees:
        st = ''
        for ii in range(len(offre)):
            st += offre[ii] + '\t'
        ff.write(st)







