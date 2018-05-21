import selection as s

clubs = []
noms_clubs = []
for nom in s.noms_clubs:
    print nom
    cc = s.charger(nom, 'c')
    clubs.append(cc)
    noms_clubs.append(nom)

lines = []

with open('Partir\departs.txt', 'r') as ff:
    for line in ff.readlines():
        lines.append(line.split('\t'))

non_transferes = []
dernier = 'Jens'
dernier_atteint = False
for line in lines:
    if line[0] == dernier:
        dernier_atteint = True
    else:
        if dernier_atteint:
            club_depart = clubs[noms_clubs.index(line[1])]
            jj = club_depart.get_joueur_from_nom(line[0])
            if line[2] == '':
                club_arrivee = clubs[noms_clubs.index('vide')]
            else:
                club_arrivee = clubs[noms_clubs.index(line[2])]
            if club_arrivee == club_depart:
                if not line[4] == '\n':
                    jj.MS = int(line[4])
                if not club_arrivee.nom == 'vide':
                    jj.veut_partir = False
                    jj.MS_probleme = False
            else:
                try:
                    s.transfert(jj, club_depart, club_arrivee)
                    if not line[3] == '':
                        jj.VAL = int(line[3])
                    if not line[4] == '\n':
                        jj.MS = int(line[4])
                    if not club_arrivee.nom == 'vide':
                        jj.veut_partir = False
                        jj.MS_probleme = False
                except ValueError:
                    non_transferes.append(line)
        else:
            pass

n = 0
while len(non_transferes) > 0 and n < 10:
    ll = []
    for line in non_transferes:
        if line[0] == dernier:
            dernier_atteint = True
        else:
            if dernier_atteint:
                club_depart = clubs[noms_clubs.index(line[1])]
                jj = club_depart.get_joueur_from_nom(line[0])
                if line[2] == '':
                    club_arrivee = clubs[noms_clubs.index('vide')]
                else:
                    club_arrivee = clubs[noms_clubs.index(line[2])]
                if club_arrivee == club_depart:
                    if not line[4] == '\n':
                        jj.MS = int(line[4])
                    if not club_arrivee.nom == 'vide':
                        jj.veut_partir = False
                        jj.MS_probleme = False
                else:
                    try:
                        s.transfert(jj, club_depart, club_arrivee)
                        if not line[3] == '':
                            jj.VAL = int(line[3])
                        if not line[4] == '\n':
                            jj.MS = int(line[4])
                        if not club_arrivee.nom == 'vide':
                            jj.veut_partir = False
                            jj.MS_probleme = False
                    except ValueError:
                        ll.append(line)
            else:
                pass
    print n, len(ll)
    non_transferes = ll
    n += 1

