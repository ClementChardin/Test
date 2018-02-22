import match as m
for nom in m.s.noms_clubs:
    if not nom in ["APA", "BRB", "AL", "ALT", "BSK", "CAT", "DKF", "DKW", "ED",
                   "FS", "GP", "HTH", "KAK", "KH", "KHR", "MDH", "MDL", "MRB",
                   "MSL", "PRG", ]:
        print nom
        cc = m.s.charger(nom, 'c')
        for ll in cc.joueurs.values():
            for jj in ll:
                st = raw_input(jj.nom + " " + jj.postes[1] + " ? ")
                ll = st.split(" ")
                es = int(ll[0])
                try:
                    pe = int(ll[1])
                except IndexError:
                    pe = 0
                try:
                    dr = int(ll[2])
                except IndexError:
                    dr = 0
                try:
                    tr = int(ll[3])
                except IndexError:
                    tr = 0
                jj.essais_total = es
                jj.penalites_total = pe
                jj.drops_total = dr
                jj.transformations_total = tr
        cc.sauvegarder()

import selection as s
st = raw_input("suivant ? ")
clubs = []
for nom in s.noms_clubs:
    clubs.append(s.charger(nom, 'c'))
armees = []
for nom in s.noms_armees:
    armees.append(s.charger(nom, 's'))
while st != "N":
    ll = st.split(" ")
    arm = ll[0]
    nom = ll[1]
    try:
        es = int(ll[2])
    except IndexError:
        es = 0
    try:
        tr = int(ll[3])
        trr = int(ll[4])
    except IndexError:
        tr = 0
        trr = 0
    try:
        pe = int(ll[5])
        per = int(ll[6])
    except IndexError:
        pe = 0
        per = 0
    try:
        dr = int(ll[7])
        drr = int(ll[8])
    except IndexError:
        dr = 0
        drr = 0
    sel = armees[s.noms_armees.index(arm)]
    jj_s = sel.get_joueur_from_nom(nom)
    cc = clubs[s.noms_clubs.index(jj_s.club)]
    jj_c = cc.get_joueur_from_nom(nom)

    jj_c.essais_saison += es
    jj_c.transformations_saison += tr
    jj_c.transformation_ratees_saison += trr
    jj_c.penalites_saison += pe
    jj_c.penalite_ratees_saison += per
    jj_c.drops_saison += dr
    jj_c.drop_rates_saison +=drr
    
    jj_c.essais_total += es
    jj_c.transformations_total += tr
    jj_c.transformation_ratees_total += trr
    jj_c.penalites_total += pe
    jj_c.penalite_ratees_total += per
    jj_c.drops_total += dr
    jj_c.drop_ratees_total +=drr

    st = raw_input("suivant ? ")
