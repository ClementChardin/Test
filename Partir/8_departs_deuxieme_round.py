import selection as s

clubs = []
noms_clubs = []
for nom in s.noms_clubs:
    print nom
    cc = s.charger(nom, 'c')
    clubs.append(cc)
    noms_clubs.append(nom)

lines = []

with open('Partir\departs_deuxieme_round.txt', 'r') as ff:
    for line in ff.readlines():
        lines.append(line.split('\t'))

non_transferes = []
dernier = 'Dyomendal'
dernier_atteint = False
for line in lines:
    if line[1] == dernier:
        dernier_atteint = True
    else:
        if dernier_atteint:
            club_depart = clubs[noms_clubs.index('vide')]
            jj = club_depart.get_joueur_from_nom(line[1])
            club_arrivee = clubs[noms_clubs.index(line[3])]
            try:
                s.transfert(jj, club_depart, club_arrivee)
                jj.VAL = int(line[4])
                jj.MS = int(line[5])
                jj.veut_partir = False
                jj.MS_probleme = False
                jj.anciens_clubs = jj.anciens_clubs.replace(';' + 'vide ' + str(s.date), '')
            except ValueError:
                non_transferes.append(line)
        else:
            pass

n = 0
while len(non_transferes) > 0 and n < 10:
    ll = []
    for line in non_transferes:
        if line[1] == dernier:
            dernier_atteint = True
        else:
            if dernier_atteint:
                club_depart = clubs[noms_clubs.index('vide')]
                jj = club_depart.get_joueur_from_nom(line[1])
                club_arrivee = clubs[noms_clubs.index(line[3])]
                try:
                    s.transfert(jj, club_depart, club_arrivee)
                    jj.VAL = int(line[4])
                    jj.MS = int(line[5])
                    jj.veut_partir = False
                    jj.MS_probleme = False
                    jj.anciens_clubs = jj.anciens_clubs.replace(';' + 'vide ' + str(s.date), '')
                except ValueError:
                    ll.append(line)
            else:
                pass
    print n, len(ll)
    non_transferes = ll
    n += 1

for cc in clubs:
    cc.sauvegarder()

