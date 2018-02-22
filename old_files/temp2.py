import selection as s

for nom in s.noms_clubs_vieux_monde:
    print nom
    cc = s.charger(nom, 'c')
    for ii, attr in enumerate(('joues_championat',
                               'gagnes_championat',
                               'nuls_championat',
                               'perdus_championat',
                               'bonus_offensif_championat',
                               'bonus_defensif_championat',
                               'pour_championat',
                               'contre_championat',
                               'difference_championat')):
        setattr(cc, attr, dict_clubs[cc.nom][ii])

    for jj in cc.get_all_joueurs():
        for ii, attr in enumerate(('essais_saison',
                                   'essais_total',
                                   'transformations_saison',
                                   'transformations_total',
                                   'transformation_ratees_saison',
                                   'transformation_ratees_total',
                                   'penalites_saison',
                                   'penalites_total',
                                   'penalite_ratees_saison',
                                   'penalite_ratees_total',
                                   'drops_saison',
                                   'drops_total',
                                   'drop_rates_saison',
                                   'drop_ratees_total',
                                   'jaunes_saison',
                                   'jaunes_total',
                                   'rouges_saison',
                                   'rouges_total')):
            setattr(jj, attr, dict_joueurs[jj.nom][ii])
    cc.sauvegarder()
    print cc.nom, 'sauvegarde'
