import selection as s

def selections(jj):
    res = 0
    for ii in range(1, 4):
        dd = getattr(jj, 'MJ'+str(ii))
        res += dd['ST'] + dd['SR']
    return res

clubs = []
for nom in s.noms_clubs:
    cc = s.charger(nom, 'c')
    clubs.append(cc)

noms_comps = ('OG_S_t', 'OG_S_t', 'HB_CV_t', 'HB_CV_t')
for ii, nom in enumerate(('OG', 'S', 'HB', 'CV')):
    sel = s.charger(nom, 's')
    comp = s.charger_compo(noms_comps[ii], nom, 's')
    for nn, jj in comp.joueurs.items():
        nom_club = jj.club
        cc = clubs[s.noms_clubs.index(nom_club)]
        jj_c = cc.get_joueur_from_nom(jj.nom)
        print jj_c.nom, '\t', jj_c.club, '\t', selections(jj_c)
        if int(nn[1:]) < 16:
            poste = s.corres_num_poste[nn]
            if poste in ('C1', 'C2'):
                poste = 'CE'
            if poste == 'CE' and jj_c.postes[1] in ('C1', 'C2'):
                poste = jj_c.postes[1]
            num_poste = jj_c.postes.index(poste)
            dd = getattr(jj_c, 'MJ'+str(num_poste))
            dd['ST'] -= 1
            setattr(jj_c, 'MJ'+str(num_poste), dd)
        else:
            postes = s.corres_num_poste[nn].split(' ')
            idx = random_integers(len(postes))
            essayer = True
            while essayer:
                poste = postes[idx-1]
                if poste == 'CE' and jj_c.postes[1] in ('C1', 'C2'):
                    poste = jj_c.postes[1]
                if not poste in jj_c.postes:
                    idx = random_integers(len(postes))
                else:
                    num_poste = jj_c.postes.index(poste)
                    dd = getattr(jj_c, 'MJ'+str(num_poste))
                    if dd['SR'] > 0:
                        essayer = False
                    else:
                        idx = random_integers(len(postes))
            
            poste = postes[idx-1]
            if poste == 'CE' and jj_c.postes[1] in ('C1', 'C2'):
                poste = jj_c.postes[1]
            num_poste = jj_c.postes.index(poste)
            dd = getattr(jj_c, 'MJ'+str(num_poste))
            dd['SR'] -= 1
            setattr(jj_c, 'MJ'+str(num_poste), dd)
        print jj_c.nom, '\t', jj_c.club, '\t', selections(jj_c)

"""
for cc in clubs:
    cc.sauvegarder()
"""
