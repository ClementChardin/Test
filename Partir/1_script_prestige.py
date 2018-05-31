import selection as s

for nom in s.noms_clubs():
    cc = s.charger(nom, 'c')
    da = s.lire_date()
    cc.prestige_saison['s'+str(da)] = int(raw_input(nom+' '+str(da)+' ? '))
    cc.sauvegarder()
