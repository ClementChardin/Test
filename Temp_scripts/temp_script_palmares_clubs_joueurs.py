# -*- coding: cp1252 -*-
import selectionas s

def get_club(jj, dat):
    if dat < jj.C:
        raise ValueError(u"Date antérieure à la création du joueur")
    else:
        if jj.anciens_clubs == '':
            return jj.club
        else:
            transferts = jj.anciens_clubs.split(';')
            ll = []
            for st in transferts:
                if int(st.split(' ')[1]) > dat:
                    ll.append((st.split(' ')[0], int(st.split(' ')[1])))
            if ll == []:
                return jj.club
            else:
                return min(ll, key=lambda tu:tu[1])[0]

clubs = []
noms_clubs = s.noms_clubs()
tournois = ['Vieux Monde',
            'Nouveaux Mondes',
            'Coupe',
            'Challenge',
            'Nord',
            'Sud',
            'Nordsud',
            'Division 1',
            'Division 2']
for nom in noms_clubs:
    cc = s.charger(nom, 'c')
    cc.palmares = {}
    for key in tournois:
        ll = [int(st) for st in raw_input(nom+' '+key+' ? ').split(' ')]
        cc.palmares[key] = ll
    ll.append(cc)

for cc in ll:
    for jj in cc.get_all_joueurs():
        jj.palmares = {}
        for dat in range(jj.C, s.lire_date()+1):
            nom = get_club(jj, dat)
            cc_aux = clubs[noms_clubs.index(nom)]
            for key in tournois:
                jj.palmares[key] = []
                if dat in cc_aux.palmares[key]:
                    jj.palmares[key].append(dat)
    cc.sauvegarder()

