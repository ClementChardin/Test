import selection as s

def maj_stat_total_joueur(attr, jj):
    st = raw_input(jj.nom + " ? ")
    val = 0 if st == "" else int(st)
    val += getattr(jj, attr.split('_')[0] + '_saison')
    setattr(jj, attr.split('_')[0]+"_total", val)

def maj_stat_total(attr):
    for nom in ('AL', 'ALT', 'BSK', 'DKF', 'DKW', 'KAK', 'MRB', 'MSL', 'PRG',
                'QNL', 'TA', 'TLB'):
        print nom
        cc = s.charger(nom, 'c')

        for poste in s.postes:
            if not poste == 'C2':
                print poste
                if poste == 'C1':
                    poste = 'CE'
                for jj in cc.joueurs[poste]:
                    maj_stat_total_joueur(attr, jj)
        cc.sauvegarder()

def maj_stat_saison(attr):
    for nom in ('KAK', 'BSK', 'QNL', 'TLB', 'MSL', 'PRG', 'AL', 'TA', 'ALT',
                'MRB', 'DKF', 'DKW'):
        print nom
        cc = s.charger(nom, 'c')
        for jj in cc.get_all_joueurs():
            setattr(jj, attr, 0)

        st = raw_input(attr + " ? ")
        ll = st.split(', ')

        for nom_jj in ll:
            jj = cc.get_joueur_from_nom(nom_jj)
            setattr(jj, attr, getattr(jj, attr)+1)
            print nom_jj, getattr(jj, attr)

        cc.sauvegarder()
        print nom, "sauvegarde"

def correction():
    for nom in s.noms_clubs_nouveaux_mondes:
        print nom
        cc = s.charger(nom, 'c')
        for jj in cc.get_all_joueurs():
            for attr in ('essais', 'penalites', 'drops', 'transformations',
                         'penalite_ratees', 'transformation_ratees', 'drop_rates'):
                if not getattr(jj, attr+'_saison') == 0:
                    st = raw_input(jj.postes[1] + ' ' + jj.nom + ' ' + attr + ' ancien ? ')
                    val = int(st)
                    setattr(jj, attr+'_total', getattr(jj, attr+'_saison')+val)
        cc.sauvegarder()

"""
attributs faits :

essais_saison
/!\ essais_saison efface pour les equipes du NM...
drops_saison
penalites_saison
transformations_saison
transformation_ratees_saison
penalite_ratees_saison
drop_rates_saison
jaunes_saison
rouges_saison

essais_total
drops_total
penalites_total
transformations_total
"""
