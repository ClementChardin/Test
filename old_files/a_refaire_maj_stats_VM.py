import selection as s

for nom in s.noms_clubs:
    print nom
    cc = s.charger(nom, 'c')
    st = nom
    while not st == "":
        st = raw_input("suivant ?")
        if not st == "":
            ll = st.split(";")
            nom_j = ll[0]
            st_pts = ll[1]
            st_rat = ll[2]
            
            jj = cc.get_joueur_from_nom(nom_j)
            
            for attr in ('essais', 'transformations', 'penalites',
                         'drops', 'jaunes', 'rouges','penalite_ratees',
                         'transformation_ratees'):
                if not getattr(jj, attr+'_saison') == 0:
                    setattr(jj, attr+'_saison', 0)
                    setattr(jj, attr+'_total', getattr(jj, attr+'_total')-st.count(attr[0]))

                setattr(jj, attr, getattr(jj, attr+'_saison') + st_pts.count(attr[0]))
                setattr(jj, attr, getattr(jj, attr+'_total') + st_pts.count(attr[0]))

            if not getattr(jj, 'drop_rates_saison') == 0:
                setattr(jj, 'drop_rates_saison', 0)
                setattr(jj, 'drop_ratees_saison', getattr(jj, attr+'_total')-st.count(attr[0]))

            setattr(jj, attr, getattr(jj, 'drop_rates_saison') + st_pts.count(attr[0]))
            setattr(jj, attr, getattr(jj, 'drop_ratees_total') + st_pts.count(attr[0]))

    cc.sauvegarder()


            


            
