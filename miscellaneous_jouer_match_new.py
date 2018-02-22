from miscellaneous import *
from selection import *
"""
Algorithme pour occasion d'essai :

1. L'attaque fait un test LJ contre LJ (lecture du jeu)
   puis PA + A avec bonus = l'écart obtenu (même négatif)
        Possibilité de s'imposer un malus : en cas de réussite on gagne autant
        en bonus pour le test suivant (peut être négatif)

2. Si raté : terminé
   Si réussi : test O+_att contre O-_def

        2.a. Si gagné de pas beaucoup : placage haut (possible)
                                        donne un avantage (si balle perdue au
                                        test R on gagne une pénalité)

        2.b. Si perdu de pas beaucoup : passe après contact (possible)
                    On détermine qui fait la passe
                    Test PA avec malus = différence entre valeur requise et
                                         valeur obtenue au test O+ / O-
                    Si réussi : nouveau test O+ / O- avec bonus = différence 
                                        entre valeur requise et valeur obtenue
                                        au test PA

3. Si raté : Z3-4 : terminé
             Z1-2 : drop possible

   Si réussi : un test M donne le nombre de zones gagnées

4. Si Z_ini - Z_gagnées < 0 : essai

   Sinon: test R contre R

5. Si gagné par la défense :
            Z3-4 : terminé
            Z1-2 : la défense doit se dégager par un jeu au pied
                    Test JP pour touche trouvée
                    Test P pour zones gagnées
                        Si Z_ini + Z_gagnée < 4 et touche non trouvée :
                        nouvelle occase pour l'attaque

6. Si gagné par l'attaque : on recommence dans la nouvelle zone
"""

def test_carac_contre_carac(car_att, car_def, comp_att, comp_def, bonus=0):
    val_att = comp_att.caracs_old[car_att]
    val_def = comp_def.caracs_old[car_def]

    carte_att = tirer_carte()
    carte_def = tirer_carte()

    res = val_att + carte_att['valeur'] - val_def - carte_def['valeur'] + bonus

    print "\nTest", car_att, "contre", car_def, "- bonus =", bonus
    print "Attaque : val, carte", val_att, carte_att['valeur'] 
    print "Defense : val, carte", val_def, carte_def['valeur']
    print "Resultat :", res
    if res >= 0:
        print True
        return True, res
    else:
        print False
        return False, res

def test_carac_collectif(car, comp, car2=None, bonus=0):
    carte = tirer_carte()
    val1 = comp.caracs_old[car]/2 if car in ('A', 'R', 'LJ', 'E')\
           else comp.caracs_old[car]
    if not car2 is None:
        val2 = comp.caracs_old[car2]/2 if car2 in ('A', 'R', 'LJ', 'E')\
               else comp.caracs_old[car2]

    val = val1 if car2 is None else (val1 + val2)/2
    res = val/10. - carte['valeur'] + bonus
    #Test réussi si res est positif

    print "\nTest", car, "et ", car2, "- bonus =", bonus
    print "Val :", val, "- carte", carte['valeur']
    print "Resultat :", res

    if res >= 0:
        print True
        return True, res
    else:
        print False
        return False, res

def jouer_drop(eq_att, zone, bonus_malus=0, sauver=True, clubs=None, c_ou_s='c'):
    #On identifie le joueur a tester
    comp = eq_att.comp
    carte = tirer_carte()
    if carte["valeur"] in range(1,7):
        jj = comp.joueurs["n10"]
    elif carte["valeur"] in range(7, 10):
        jj = comp.roles["drop1"]
    elif carte["valeur"] in range(10, 13):
        jj = comp.roles["drop2"]
    elif carte["valeur"] in range(13, 15):
        jj = comp.roles["drop3"]

    if jouer_tab(jj, zone, bonus_malus, 'JP'):
        marque("drop", jj, eq_att, sauver, clubs, c_ou_s)
    else:
        marque("drop_rate", jj, eq_att, sauver, clubs, c_ou_s)

def jouer_tab(buteur, zone, bonus_malus, car):
    TB = buteur.caracs[car]
    P = buteur.caracs["P"]
    carte = tirer_carte()

    test = carte_to_test_tb(carte) - malus_tab(P, zone) + bonus_malus
    if test <= tab_rate(TB):
        return False
    else:
        return True

def attribuer_essai(comp_XV, av_ar, Oplus_M):
    if Oplus_M == 'M' :
        car = 'M'
        car_joueur = 'M'
        fixe = 15
        nums = range(1, 23)
    else:
        if av_ar == 'AR':
            car = 'OplusAR'
            car_joueur = 'RP_tot'
            fixe = 23
            nums = [6, 7] + range(9, 16) + range(20, 23)
        else:
            car = 'OplusAV'
            car_joueur = 'RP_tot'
            fixe = 23
            nums = range(1, 9) + range(16, 20)

    joueurs = comp_XV.joueurs
    dd = coeffs_compo_old[car]
            
    nn = random.random_integers(comp_XV.caracs_old[car]*2 + fixe)

    if nn <= fixe:
        num = attribuer_essai_fixe(av_ar, Oplus_M, nn)
    else:
        nn -= fixe
        nums_idx = 0
        num = nums[nums_idx]
        cumul = max(0, (joueurs['n'+str(num)].caracs[car_joueur] - 7) \
                    * dd['n'+str(num)]*2)
        while cumul < nn:
            nums_idx +=1
            num = nums[nums_idx]
            cumul += max(0, (joueurs['n'+str(num)].caracs[car_joueur] - 7) \
                         * dd['n'+str(num)]*2)

    return comp_XV.joueurs['n'+str(num)]

def attribuer_essai_fixe(av_ar, Oplus_M, nn):
    """
    Part fixe d'attribution des essais:
    si M : tout le monde a un poids 1
    si AV : les AV on poids 1, les AR ont poids 0.5
    si AR : les AR on poids 1, les AV ont poids 0.5
    """
    if Oplus_M == 'M':
        nums = range(1, 16)
    elif Oplus_M == 'Oplus':
        if av_ar == 'ar':
            nums = range(1, 16) + range(9, 16)
        else:
            nums = range(1, 16) + range(1, 9)

    return nums[(nn+1)/2]

def marque(typ, joueur, eq, sauver=True, clubs=None, c_ou_s='c'):
    attr = "dict_" + typ + "s"
    dd = getattr(eq, attr)
    dd[joueur.nom] = dd[joueur.nom]+1 if joueur.nom in dd.keys() else 1
    print joueur.nom, "marque", typ
    print c_ou_s, "clubs is None :", clubs is None, "sauver :", sauver

    if sauver:
        equipe = eq.equipe
        comp = eq.comp
        clubs_a_sauver = []
        if c_ou_s == 'c':
            jj_club = joueur
        else:
            cc = identifier_club(joueur, clubs)
            jj_club = cc.get_joueur_from_nom(joueur.nom)
            if not cc in clubs_a_sauver:
                clubs_a_sauver.append(cc)

        attr_joueur_saison = typ + "s_saison"
        attr_joueur_total = typ + "es_total" if typ == "drop_rate" \
                            else typ + "s_total"

        #print attr_joueur_saison, getattr(jj_club, attr_joueur_saison)

        setattr(jj_club, attr_joueur_saison,
                getattr(jj_club, attr_joueur_saison) + 1)
        setattr(jj_club, attr_joueur_total,
                getattr(jj_club, attr_joueur_total) + 1)

        if c_ou_s == 'c':
            equipe.sauvegarder()
        else:
            for cc in clubs_a_sauver:
                cc.sauvegarder()
            jj_club = cc.get_joueur_from_nom(joueur.nom)
            #print attr_joueur_saison, getattr(jj_club, attr_joueur_saison)

def transformer(eq, sauver=True, clubs=None, c_ou_s='c'):
    buteur = eq.comp_XV.roles["B1"]
    zone = 1
    bonus_malus = 0
    if jouer_tab(buteur, zone, bonus_malus, 'TB'):
        marque("transformation", buteur, eq, sauver, clubs, c_ou_s)
    else:
        marque("transformation_ratee", buteur, eq, sauver, clubs, c_ou_s)

def jouer_tab(buteur, zone, bonus_malus, car):
    TB = buteur.caracs[car]
    P = buteur.caracs["P"]
    carte = tirer_carte()

    test = carte_to_test_tb(carte) - malus_tab(P, zone) + bonus_malus
    if test <= tab_rate(TB):
        return False
    else:
        return True

def tab_rate(TB):
    if TB <= 8:
        return 4 + (8-TB)*2
    else:
        return 4 - (TB-8)

def malus_tab(P,zone):
    P_pairs = [-1, -3, -6, -10]
    P_impairs = [-2, -4, -8, -13]
    if zone < zone_malus_tab(P):
        return 0
    else:
        ll = P_pairs if P%2 == 0 else P_impairs
        return ll[zone - zone_malus_tab(P)]
    
def zone_malus_tab(P):
    """
    donne la zone a partir de laquelle il y a un malus,
    en fonction de la P du buteur
    """
    if P <= 6:
        return 1
    elif P >= 13:
        return 5
    else:
        return (P+1)/2 -2

def carte_to_test_tb(carte):
    val = carte["valeur"]
    if val > 1:
        return val
    else:
        if carte["r_n"] == 'r': #As de coeur ou carreau
            return val
        elif carte["couleur"] == 2: #As de trefle
            return 0
        else: #As de pique
            return -100

def degagement(eq):
    botteur = determiner_botteur(eq)
    carte_JP = tirer_carte()
    JP = botteur.caracs['JP']
    if carte_JP['valeur'] == 1:
        touche_trouvee = True
    elif carte_JP['valeur'] == 14:
        touche_trouvee = False
    elif carte_JP['valeur'] <= JP:
        touche_trouvee = True
    else:
        touche_trouvee = False
    print "Degagement de", botteur.nom
    print "JP :", JP, "; carte :", carte_JP['valeur'], "; touche trouvée :", touche_trouvee

    carte_P = tirer_carte()
    P = botteur.caracs['P']
    zones_gagnees = zones_gagnees_degagement(P, carte_P['valeur'])
    print "P :", P, "; carte :", carte_P['valeur'], "; zones gagnées :", zones_gagnees

    return touche_trouvee, zones_gagnees

def determiner_botteur(eq):
    rand = random.random_integers(1, 15)
    N = 15 - rand
    for nn in range(9, 16):
        N -= 2*coeffs_caracs(eq.comp_XV)['JP']['n'+str(nn)]
        if N < 0:
            break
    return eq.comp_XV.joueurs['n' + str(nn)]

def zones_gagnees_degagement(P, val):
    if val == 1:
        return 0
    elif val == 2:
        return 0 if P < 8 else 1
    elif val == 14:
        return 4
    else:
        if val < P - 2 * (P - 5):
            return 0
        elif val < P + 4 - 2 * (P - 5):
            return 1
        elif val < P + 9 - 2 * (P - 5):
            return 2
        elif val < P + 13 - 2 * (P - 5):
            return 3
        else:
            return 4

def jouer_action(typ,
                 eq_att,
                 eq_def,
                 zone,
                 AV_AR,
                 bonus_voulu=0,
                 sauver=True,
                 clubs=None,
                 c_ou_s='c'):
    if not AV_AR in ('AV', 'AR'):
        raise ValueError("Mauvaise valeur de AV_AR : " + str(AV_AR))
    """
    #Etape 1
    boo, res = test_carac_contre_carac(car_att='LJ',
                                       car_def='LJ',
                                       comp_att=eq_att.comp_XV,
                                       comp_def=eq_def.comp_XV,
                                       bonus=0)
    """
    res = 0
    boo, res = test_carac_collectif(car='PA',
                                    comp=eq_att.comp_XV,
                                    car2='A',
                                    bonus=res-bonus_voulu)
    #Etape 2
    if not boo:
        pass
    else: #le test est reussi
        car_att = 'OplusAV' if AV_AR == 'AV' else 'OplusAR'
        car_def = 'OmoinsAV' if AV_AR == 'AV' else 'OmoinsAR'
        boo, res = test_carac_contre_carac(car_att=car_att,
                                           car_def=car_def,
                                           comp_att=eq_att.comp_XV,
                                           comp_def=eq_def.comp_XV,
                                           bonus=bonus_voulu)

        #Pour le moment pas de 2.a. et 2.b.

        #Etape 3
        if not boo:
            if zone in (3, 4):
                pass
            elif zone in (1, 2):
                jouer_drop(eq_att=eq_att,
                           zone=zone,
                           bonus_malus=0,
                           sauver=sauver,
                           clubs=clubs,
                           c_ou_s=c_ou_s)
        else: #le test Oplus est reussi
            boo, res = test_carac_contre_carac(car_att='M',
                                               car_def='M',
                                               comp_att=eq_att.comp_XV,
                                               comp_def=eq_def.comp_XV,
                                               bonus=res)
            #L'attaque gagne toujours au moins un zone
            #Après tout elle a percé !
            if boo:
                zones_gagnees = int(res/10) + 1
            else:
                zones_gagnees = 1
            nouvelle_zone = zone - zones_gagnees
            print "Zones gagnées", zones_gagnees, "Nouvelle zone", nouvelle_zone
            if nouvelle_zone <= 0:
                joueur = attribuer_essai(eq_att.comp_XV, AV_AR, 'M')
                marque('essai',
                       joueur,
                       eq_att,
                       sauver=sauver,
                       clubs=clubs,
                       c_ou_s=c_ou_s)
                transformer(eq_att, sauver=sauver, clubs=clubs, c_ou_s=c_ou_s)

            #Etape 4
            else:
                boo, res = test_carac_contre_carac(car_att='R',
                                                   car_def='R',
                                                   comp_att=eq_att.comp_XV,
                                                   comp_def=eq_def.comp_XV,
                                                   bonus=max(0, res))
                if not boo: #test R perdu par l'attaque : la défense se dégage
                    boo, zones_perdues = degagement(eq_def)
                    nouvelle_zone = nouvelle_zone + zones_perdues
                    if nouvelle_zone > 4 or (nouvelle_zone == 4 and boo):
                        #dégagement efficace
                        pass
                    else:
                        #dégagement non efficace
                        if boo:
                            #touche trouvée
                            typ = 'touche'
                            AV_AR = ['AV', 'AR'][random.random_integers(2)-1]
                        else:
                            #touche non trouvée
                            typ = 'essai'
                            AV_AR = 'AR'
                        jouer_action(typ,
                                     eq_att,
                                     eq_def,
                                     nouvelle_zone,
                                     AV_AR,
                                     bonus_voulu=0,
                                     sauver=sauver,
                                     clubs=clubs,
                                     c_ou_s=c_ou_s)
                else: #Test R gagné par l'attaque
                    typ = 'essai'
                    AV_AR = ['AV', 'AR'][random.random_integers(2)-1]
                    jouer_action(typ,
                                 eq_att,
                                 eq_def,
                                 nouvelle_zone,
                                 AV_AR,
                                 bonus_voulu=0,
                                 sauver=sauver,
                                 clubs=clubs,
                                 c_ou_s=c_ou_s)



