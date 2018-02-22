import selection as s

dict_clubs = dict()
dict_joueurs = dict()
for nom in s.noms_clubs_vieux_monde:
    print nom
    cc = s.charger(nom, 'c')
    dict_clubs[nom] = (cc.joues_championat,
                       cc.gagnes_championat,
                       cc.nuls_championat,
                       cc.perdus_championat,
                       cc.bonus_offensif_championat,
                       cc.bonus_defensif_championat,
                       cc.pour_championat,
                       cc.contre_championat,
                       cc.difference_championat)

    for jj in cc.get_all_joueurs():
        dict_joueurs[jj.nom] = (jj.essais_saison,
                                jj.essais_total,
                                jj.transformations_saison,
                                jj.transformations_total,
                                jj.transformation_ratees_saison,
                                jj.transformation_ratees_total,
                                jj.penalites_saison,
                                jj.penalites_total,
                                jj.penalite_ratees_saison,
                                jj.penalite_ratees_total,
                                jj.drops_saison,
                                jj.drops_total,
                                jj.drop_rates_saison,
                                jj.drop_ratees_total,
                                jj.jaunes_saison,
                                jj.jaunes_total,
                                jj.rouges_saison,
                                jj.rouges_total)
