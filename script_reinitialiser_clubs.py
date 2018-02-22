import selection as s

for nom in s.noms_clubs:
    #print nom
    cc = s.charger(nom, 'c')
    cc.gagnes_championat = 0
    cc.gagnes_coupe = 0
    cc.perdus_championat = 0
    cc.perdus_coupe = 0
    cc.nuls_championat = 0
    cc.nuls_coupe = 0
    cc.bonus_defensif_championat = 0
    cc.bonus_defensif_coupe = 0
    cc.bonus_offensif_championat = 0
    cc.bonus_offensif_coupe = 0
    cc.contre_championat = 0
    cc.contre_coupe = 0
    cc.pour_championat = 0
    cc.pour_coupe = 0
    cc.difference_championat = 0
    cc.difference_coupe = 0
    cc.joues_championat = 0
    cc.joues_coupe = 0
    cc.sauvegarder()
