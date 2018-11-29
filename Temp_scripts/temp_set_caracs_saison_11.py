clubs = []
clubs_11= []
noms = []
for nom in s.noms_clubs:
    cc = s.charger(nom, 'c')
    cc_11 = s.charger(nom, 'c', 11)
    noms.append(nom)
    clubs.append(cc)
    clubs_11.append(cc_11)
for cl in clubs:
    print '\n\n\n'+cl.nom
    for jj in cl.get_all_joueurs():
        if jj.C == 12:
            print jj.nom, u"créé à la saison 12"
        else:
            ll = jj.anciens_clubs.split(';')
            if ll[0] == '':
                nom_club = jj.club
            else:
                transfert = ll[-1]
                if ' ' in transfert:
                    date_transfert = int(transfert.split(' ')[1])
                    nom_club = transfert.split(' ')[0] if date_transfert == 12 \
                               else jj.club
                else:
                    try:
                        date_transfert = int(transfert[-2:])
                        ii = -2
                    except ValueError:
                        date_transfert = int(transfert[-1:])
                        ii = -1
                    nom_club = transfert[:ii] if date_transfert == 12 \
                               else jj.club

            print jj.nom, "- club saison 11 :", nom_club
            idx = noms.index(nom_club)
            cl_11 = clubs_11[idx]
            jj_11 = cl_11.get_joueur_from_nom(jj.nom)
            jj.caracs_saison_11 = jj_11.caracs_sans_fatigue
            print jj.nom, "- EV_11 :", jj_11.EV, "- EV_12 :", jj.EV

    cl.sauvegarder()
