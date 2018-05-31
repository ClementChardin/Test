import selection as s

for nom in s.noms_clubs():
    cc = s.charger(nom, 'c')
    print '\n'
    print nom
    print cc.besoins
    if raw_input(u"Réinitialiser ? [y]/n ") in ('', 'y'):
        cc.besoins = []
    st = raw_input("Prochain besoin pour " + nom + " ? ")
    while not st == '':
        ll = st.split(' ')
        cc.besoins.append((ll[0], float(ll[1])))
        st = raw_input("Prochain besoin pour " + nom + " ? ")
    cc.sauvegarder()
    print nom, cc.besoins

        
