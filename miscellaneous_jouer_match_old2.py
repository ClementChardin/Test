# -*- coding: cp1252 -*-
from miscellaneous import *
from numpy.random import random_integers
from selection import corres_num_poste, charger
from noms_all import *

coeffs_compo_old = dict(M = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=1, n7=1, n8=.5, n9=1.5, n10=1.5, n11=2.5, n12=1.5, n13=1.5, n14=2.5, n15=2, n16=0, n17=0, n18=0, n19=0, n20=.5, n21=.5, n22=1),
                        OplusAV = dict(n1=2, n2=2, n3=2, n4=2, n5=2, n6=1.5, n7=1.5, n8=2.5, n16=1, n17=1, n18=1, n19=.5, n20=0, n21=0, n22=0),
                        OplusAR = dict(n6=.5, n7=.5, n9=1.5, n10=1.5, n11=3, n12=2, n13=2.5, n14=3, n15=2.5, n16=0, n17=0, n18=0, n19=0, n20=.5, n21=1, n22=1.5))

def n_tps_forts(res, prolongation):
    if prolongation:
        if res < 0:
            return 1
        elif res < 30:
            return 2
        else:
            return 3
    else:
        if res < -80:
            return 2
        elif res <-40:
            return 3
        elif res < 20:
            return 4
        elif res < 8:
            return 3
        elif res <= 8:
            return 2
        elif res <= 30:
            return 4
        elif res <= 45:
            return 5
        elif res <= 83:
            return 6
        elif res <= 120:
            return 7
        else:
            return 7 + (res - 120)/40

def tps_fort(carte):

    """
    Identifie les temps forts - renvoie une liste
    de tuples (type, zone, av ou ar, malus bonus transfo)
    """
    types = []
    zones = []
    av_ars = []
    malus_bonus = []
    """
    Types
    """
    if carte["valeur"] == 1:
        types.append('melee')
    elif carte["valeur"] == 2:
        types.append('touche')
    elif carte["valeur"] == 3:
        types.append('penalite')
    elif carte["valeur"] == 4:
        types.append('penalite')
        malus_bonus.append('bonus')
    elif carte["valeur"] == 5:
        types.append('essai')
        malus_bonus.append('malus')
    elif carte["valeur"] == 6:
        types.append('penalite')
        types.append('penalite')
    elif carte["valeur"] == 7:
        types.append('essai')
        malus_bonus.append('bonus')
    elif carte["valeur"] == 8:
        types.append('essai')
        malus_bonus.append('malus')
        types.append('penalite')
    elif carte["valeur"] == 9:
        types.append('melee')
        types.append('penalite')
    elif carte["valeur"] == 10 or carte["valeur"] == 11:
        types.append('essai')
        types.append('penalite')
    elif carte["valeur"] == 12:
        if carte["couleur"] in (1,2):
            types.append('melee')
        elif carte["couleur"] in (3,4):
            types.append('touche')
        types.append('penalite')
    elif carte["valeur"] == 13:
        types.append('essai')
        types.append('penalite')
    elif carte["valeur"] == 14:
        types.append('essai')
        types.append('essai')

    """
    Zones
    """
    if carte["valeur"] == 12:
        if carte["couleur"] in (1,3):
            zones.append(1)
            zones.append(1)
        elif carte["couleur"] in (2,4):
            zones.append(2)
            zones.append(2)
    elif carte["valeur"] == 14:
        pass
    else:
        zones += [carte["couleur"]]*len(types)

    """
    AV ou AR
    """
    if carte["r_n"] == 'r':
        av_ars += ['av']*len(types)
    else:
        av_ars += ['ar']*len(types)

    res = []
    while len(zones) < len(types):
        zones.append(1)
    while len(av_ars) < len(types):
        av_ars.append("av")
    while len(malus_bonus) < len(types):
        malus_bonus.append("non")
    for i in range(len(types)):
        res.append((types[i], zones[i], av_ars[i], malus_bonus[i]))
    return res

def jouer_essai(Oplus_att, Omoins_def, bonus=0):
    """
    revoie un tuple (string : test essai ou essai auto ou interception ou non,
                     diff)
    """
    carte_att = tirer_carte()
    carte_def = tirer_carte()
    diff = Oplus_att +carte_att["valeur"] - Omoins_def - carte_def["valeur"] + bonus

    if carte_att["valeur"] == 14:
        st = "essai_auto"
    elif carte_def["valeur"] == 14:
        st = "interception"
        diff = 15 if carte_def["r_n"] == 'r' else 8
    
    elif diff <= 0:
        st = "non"
    else:
        st = "test_essai"

    print "att", Oplus_att, "carte", carte_att["valeur"], "bonus", bonus
    print "def", Omoins_def, "carte", carte_def["valeur"]
    print "resultat :", diff, st
    return (st, diff)

def essai_ou_pas(diff):
    carte = tirer_carte()
    if diff < 10:
        if carte["valeur"] <= diff:
            print diff, "; carte", carte["valeur"], True
            return True
        else:
            print diff, "; carte", carte["valeur"], False
            return False
    else:
        i = max(diff / 10 -1, 0)
        if carte["valeur"] <= min(carte["valeur"], 10 + i):
            print diff, "; carte", carte["valeur"], True
            return True
        else:
            print diff, "; carte", carte["valeur"], False
            return False

def jouer_touche_melee(comp_att, comp_def, t_ou_m):
    """
    renvoie un tuple (string : essai ou essai_auto ou penalite ou non,
                      bonus,
                      occase av ou ar)
    """
    if t_ou_m == 't':
        at = comp_att.caracs_old['TO_off']
        de = comp_def.caracs_old['TO_def']
    elif t_ou_m == 'm':
        at = comp_att.caracs_old['ME']
        de = comp_def.caracs_old['ME']
    else:
        raise ValueError("t_ou_m doit etre 't' ou 'm' !")

    carte_att = tirer_carte()
    if carte_att["r_n"] == "r":
        av_ar = "av"
    else:
        av_ar = "ar"
    carte_def = tirer_carte()
    diff = at + carte_att["valeur"] - de - carte_def["valeur"]
    
    if diff < 0 or carte_att["valeur"] == 1 or carte_def["valeur"] == 14:
        st, bonus = ('non', 0)
    elif carte_att["valeur"] == 14:
        st, bonus = ('essai_auto', 0)
    else:
        st, bonus = ('essai', min(diff, 15))

    print "Occase", t_ou_m, "att", at, "def", de, "carte att", carte_att["valeur"], "carte def", carte_def["valeur"], "diff", diff, "res", st
    return (st, bonus, av_ar)

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

def tester_M(comp_att, comp_def, bonus):
    M_att = comp_att.caracs_old["M"]
    M_def = comp_def.caracs_old["M"]
    carte_att = tirer_carte()
    carte_def = tirer_carte()
    if carte_att["valeur"] == 1 or carte_def["valeur"] == 14:
        return False
    elif carte_att["valeur"] == 14:
        return True
    else:
        return (M_att + carte_att["valeur"] - M_def - carte_def["valeur"]) > 0
    
def jouer_essai_complet(eq_att,
                        eq_def,
                        bonus,
                        av_ar,
                        test_M=False,
                        sauver=False,
                        clubs=None,
                        c_ou_s='c'):
    #print "JOUER_ESSAI_COMPLET", c_ou_s, clubs is None, sauver
    key = "AV" if av_ar == "av" else "AR"
    Oplus_att = eq_att.comp.caracs_old["Oplus"+key]
    Omoins_def = eq_def.comp.caracs_old["Omoins"+key]

    st, diff = jouer_essai(Oplus_att, Omoins_def, bonus)

    if st == "non":
        pass
    elif st == "interception":
        eq_att, eq_def = jouer_essai_complet(eq_def, eq_att, diff, 'ar', True, sauver, c_ou_s)
    elif st == "essai_auto":
        jj = attribuer_essai(eq_att.comp,av_ar, "Oplus")
        if c_ou_s == 'c':
            eq_att = marque("essai", jj, eq_att, sauver, clubs, c_ou_s)
        buteur = eq_att.comp.roles["B1"]
        zone = 1
        bonus_malus = 0
        if jouer_tab(buteur, zone, bonus_malus, 'TB'):
            if c_ou_s == 'c':
                eq_att = marque("transformation", buteur, eq_att, sauver, clubs, c_ou_s)
        else:
            if c_ou_s == 'c':
                eq_att = marque("transformation_ratee", buteur, eq_att, sauver, clubs, c_ou_s)
    else: #st = "test_essai"
        if essai_ou_pas(diff): #Test essai reussi
            if not test_M or (test_M and tester_M(eq_att.comp, eq_def.comp, min(10, bonus))):
                Oplus_M = "M" if test_M else "Oplus"
                jj = attribuer_essai(eq_att.comp,av_ar, Oplus_M)
                if c_ou_s == 'c':
                    eq_att = marque("essai", jj, eq_att, sauver, clubs, c_ou_s)
                buteur = eq_att.comp.roles["B1"]
                zone = 1
                bonus_malus = 0
                if jouer_tab(buteur, zone, bonus_malus, 'TB'):
                    eq_att = marque("transformation", buteur, eq_att, sauver, clubs, c_ou_s)
                else:
                    eq_att = marque("transformation_ratee", buteur, eq_att, sauver, clubs, c_ou_s)
        else:
            eq_att = jouer_drop(eq_att, zone=1, bonus_malus=0, sauver=sauver, clubs=clubs, c_ou_s=c_ou_s)

    return eq_att, eq_def

def jouer_drop(eq_att, zone, bonus_malus=0, sauver=True, clubs=None, c_ou_s='c'):
    """
    On identifie le joueur a tester
    """
    #print "!!!!!!!!!!!!! DROP !!!!!!!!!!!!!", c_ou_s
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
        eq_att = marque("drop", jj, eq_att, sauver, clubs, c_ou_s)
    else:
        eq_att = marque("drop_rate", jj, eq_att, sauver, clubs, c_ou_s)
    return eq_att
        
def jouer_tps_fort(eq_att, eq_def, tps_fort, sauver=True, clubs=None, c_ou_s='c'):
    """
    tps_fort est un tuple (type, zone, av ou ar, malus bonus transfo ou test mouvement)
    """
    print "\n", tps_fort
    comp_att = eq_att.comp
    comp_def = eq_def.comp
    typ = tps_fort[0]

    #Si Melee ou Touche
    if typ in ("melee", "touche"):
        tupl = ("", 0, "")
        if typ == 'melee':
            tupl = jouer_touche_melee(comp_att, comp_def, 'm')
            eq_att.occase_melee += 1
        elif typ == 'touche':
            tupl = jouer_touche_melee(comp_att, comp_def, 't')
            eq_att.occase_touche += 1

        if tupl[0] == "non":
            pass
        elif tupl[0] == "essai_auto":
            buteur = comp_att.roles["B1"]
            zone = 1
            bonus_malus = 0
            if typ == 'touche':
                eq_att = marque("essai", comp_att.joueurs["n2"], eq_att, sauver, clubs, c_ou_s)
            elif typ == 'melee':
                eq_att = marque("essai", comp_att.joueurs["n8"], eq_att, sauver, clubs, c_ou_s)
            if jouer_tab(buteur, zone, bonus_malus, 'TB'):
                eq_att = marque("transformation", buteur, eq_att, sauver, clubs, c_ou_s)
            else:
                eq_att = marque("transformation_ratee", buteur, eq_att, sauver, clubs, c_ou_s)
        else: #tupl[0] == "essai"
            bonus = tupl[1]
            av_ar = tupl[2]
            #print "AVANT JOUER_ESSAI_COMPLET 1", c_ou_s
            eq_att, eq_def = jouer_essai_complet(eq_att, eq_def, bonus, av_ar, test_M=False, sauver=sauver, clubs=clubs, c_ou_s=c_ou_s)

    #Si Penalite
    elif typ == "penalite":
        eq_att.occase_penalite += 1
        zone = tps_fort[1]
        buteur = comp_att.roles["B"+str(zone)]
        bonus_malus = 0
        if jouer_tab(buteur, zone, bonus_malus, 'TB'):
            eq_att = marque("penalite", buteur, eq_att, sauver, clubs, c_ou_s)
        else:
            eq_att = marque("penalite_ratee", buteur, eq_att, sauver, clubs, c_ou_s)

    #Si essai
    elif typ == "essai":
        eq_att.occase_essai += 1
        bonus = 0
        av_ar = tps_fort[2]
        test_M = (tps_fort[1] >= 3)
        #print "AVANT JOUER_ESSAI_COMPLET 2", c_ou_s
        eq_att, eq_def = jouer_essai_complet(eq_att, eq_def, bonus, av_ar, test_M, sauver,clubs=clubs, c_ou_s=c_ou_s)

    else:
        raise ValueError("Le temps fort donne est de type inconnu !")

    return eq_att, eq_def

def attribuer_essai(comp, av_ar, Oplus_M):
    if Oplus_M == 'M' :
        car = 'M'
        car_joueur = 'M'
        fixe = 18.5
        nums = range(1, 23)
    else:
        if av_ar == 'ar':
            car = 'OplusAR'
            car_joueur = 'RP_tot'
            fixe = 10
            nums = [6, 7] + range(9, 16) + range(20, 23)
        else:
            car = 'OplusAV'
            car_joueur = 'RP_tot'
            fixe = 10
            nums = range(1, 9) + range(16, 20)

    joueurs = comp.joueurs
    d = coeffs_compo_old[car]
            
    n = random_integers(comp.caracs_old[car]*2 + fixe)
    #print n, car, car_joueur, fixe, comp.caracs_old[car]*2
    if n <= fixe*2:
        num = attribuer_essai_fixe(av_ar, Oplus_M, n)
    else:
        n -= fixe
        nums_idx = 0
        num = nums[nums_idx]
        cumul = max(0, (joueurs['n'+str(num)].caracs[car_joueur] - 7) * d['n'+str(num)]*2)
        while cumul < n:
            nums_idx +=1
            num = nums[nums_idx]
            cumul += max(0, (joueurs['n'+str(num)].caracs[car_joueur] - 7) * d['n'+str(num)]*2)
            #print cumul, '/', n, num, joueurs['n'+str(num)].nom

    return comp.joueurs['n'+str(num)]

def attribuer_essai_fixe(av_ar, Oplus_M, n):
    if Oplus_M == 'M':
        nums = range(1, 23)
        lim_tit = 15
        remp = [16, 17, 18, 19, 20, 21, 22]
    elif Oplus_M == 'Oplus':
        if av_ar == 'ar':
            nums = [6, 7] + range(9, 16) + range(20, 23)
            lim_tit = 15
            remp = [6, 7, 20, 21, 22]
        else:
            nums = range(1, 9) + range(16, 20)
            lim_tit = 8
            remp = [16, 17, 18, 19]

    if n <= lim_tit*2:
        return (n+1)/2
    else:
        return remp[n - lim_tit*2 - 1]

def marque(typ, joueur, eq, sauver=True, clubs=None, c_ou_s='c'):
    attr = "dict_" + typ + "s"
    dd = getattr(eq, attr)
    dd[joueur.nom] = dd[joueur.nom]+1 if joueur.nom in dd.keys() else 1
    print joueur.nom, "marque", typ
    #print c_ou_s, "clubs is None :", clubs is None, "sauver :", sauver

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
        """
        if c_ou_s == 'c':
            return eq
            #equipe.sauvegarder()
        else:
        """
        if c_ou_s == 's':
            for cc in clubs_a_sauver:
                cc.sauvegarder()
            jj_club = cc.get_joueur_from_nom(joueur.nom)
            #print attr_joueur_saison, getattr(jj_club, attr_joueur_saison)
    return eq

def attribuer_fatigue(eq, c_ou_s, clubs=None, prolongation=False):
    """
    eq est de la classe EquipeMatch
    club est en fait une instance de classe club OU selection
    """
    equipe = eq.equipe
    comp = eq.comp
    clubs_a_sauver = []
    for jj in equipe.get_all_joueurs():
        if c_ou_s == 'c':
            jj_club = jj
        else:
            cc = identifier_club(jj, clubs)
            jj_club = cc.get_joueur_from_nom(jj.nom)
            if not cc in clubs_a_sauver:
                clubs_a_sauver.append(cc)

        if prolongation and jj_club.nom in comp.get_joueurs_noms.values():
            jj_club.fatigue += d3_plus()
        else:
            if jj_club.nom in comp.noms_titulaires:
                jj_club.fatigue += 1 + d3_plus()
            elif jj_club.nom in comp.noms_remplacants:
                jj_club.fatigue += d2_plus()
            else:
                jj_club.fatigue -= 5
                if jj_club.fatigue < 0:
                    jj_club.fatigue = 0
    comp.fatigue_prise_en_compte = False
    if c_ou_s == 'c':
        equipe.sauvegarder()
        return 0
    else:
        return clubs_a_sauver

def identifier_club(jj, clubs=None):
    if clubs is None:
        return charger(jj.club, 'c')
    else:
        res = 0
        for cc in clubs:
            if cc.nom == jj.club:
                res = cc
        return res

def evoluer_blessures(eq, c_ou_s='c', clubs=None):
    """
    eq est de la classe EquipeMatch
    """
    equipe = eq.equipe
    clubs_a_sauver = []
    for jj in equipe.get_all_joueurs():
        if jj.blessure > 0:
            if c_ou_s == 'c':
                jj_club = jj
            else:
                cc = identifier_club(jj, clubs)
                jj_club = cc.get_joueur_from_nom(jj.nom)
                if not cc in clubs_a_sauver:
                    clubs_a_sauver.append(cc)
            jj_club.blessure = max(0, jj_club.blessure - 1)
    if c_ou_s == 'c':
        equipe.sauvegarder()
        return 0
    else:
        return clubs_a_sauver

def evenement(n):
    couleur_max_evenement = 4 - n    
    carte = tirer_carte()
    if carte["valeur"] == 14:
        ev = "jocker"
    elif carte["valeur"] > 4 or carte["couleur"] > couleur_max_evenement:
        ev = "non"
    elif carte["valeur"] > 2:
        ev = "jaune"
    elif carte["valeur"] == 2:
        ev = "blessure"
    else:
        ev = "rouge"

    return ev

def attribuer_evenements(prolongation=False):
    n = 0
    ll = []
    n_max = 1 if prolongation else 4
    while n < n_max:
        ev = evenement(n)
        if not ev == "non":
            ll.append(ev)
        n += 1
    return ll

def jouer_evenement_sauf_blessure(ev,
                                  eq,
                                  sauver=True,
                                  clubs=None,
                                  c_ou_s='c',
                                  prolongation=False):
    if ev == "jocker":
        print "!!! jocker pour", eq.nom, "!!!"
        return 25
    elif ev == "jaune":
        rand = random_integers(37)
        if rand <= 15:
            num = rand
        elif rand <= 30:
            num = rand - 15
        else:
            num = 15 + rand - 30
        if c_ou_s == 'c':
            eq = marque("jaune", eq.comp.joueurs["n"+str(num)], eq, sauver, clubs, c_ou_s)
        return -10
    elif ev == "rouge":
        num = random_integers(15)
        if c_ou_s == 'c':
            eq = marque("rouge", eq.comp.joueurs["n"+str(num)], eq, sauver, clubs, c_ou_s)
        if prolongation:
            res = d3_plus()*-10
        else:
            res = d6_plus()*-10
        print "!!! rouge :", res, "!!!"
        return res

    return eq

def jouer_blessure(eq, sauver=True, clubs=None, c_ou_s='c'):
    pts_fatigue = 0
    for jj in eq.comp.joueurs.values():
        pts_fatigue += pts_fatigue_joueur(jj)

    rand = random_integers(37 + pts_fatigue)
    temp = 0
    for num in range(1, 23):
        temp += pts_fatigue_joueur(eq.comp.joueurs["n"+str(num)])
        if num <= 15:
            temp += 2
        else:
            temp += 1
        if temp >= rand:
            break
    jj = eq.comp.joueurs["n"+str(num)]
    if sauver:
        jj_club = eq.equipe.get_joueur_from_nom(jj.nom)
        jj_club.blessure = d6_plus()
        if c_ou_s == 's':
            eq.equipe.sauvegarder()
        
    if c_ou_s == 'c':
        eq = marque("blessure", jj, eq, sauver, clubs, c_ou_s)

    return eq

def pts_fatigue_joueur(jj):
    if jj.fatigue < 8:
        return 0
    elif jj.fatigue < 15:
        return 1
    else:
        return 2 + (jj.fatigue - 15) / 10

def attribuer_matches(eq, c_ou_s='c', clubs=None):
    """
    Utilisee uniquement dans le cas sauver=True
    """
    print 'attribuer_matches', eq.equipe.nom, c_ou_s, '; clubs is None :', clubs is None
    equipe = eq.equipe
    clubs_a_sauver = []
    for (num, jj) in eq.comp.joueurs.items():
        if c_ou_s == 'c':
            jj_club = equipe.get_joueur_from_nom(jj.nom)
            clubs_a_sauver.append(equipe)
        else:
            cc = identifier_club(jj, clubs)
            jj_club = cc.get_joueur_from_nom(jj.nom)
            if not cc in clubs_a_sauver:
                clubs_a_sauver.append(cc)

        numeros_postes_possibles = []
        num_to_postes = corres_num_poste[num].split(' ')

        for poste in jj.postes:
            if poste in num_to_postes or \
               (poste in ['C1', 'C2', 'CE'] and \
                ('C1' in num_to_postes or \
                 'C2' in num_to_postes or \
                 'CE' in num_to_postes)):
                #numeros_postes_possibles.append(key.split("poste")[1])
                numeros_postes_possibles.append(jj.postes.index(poste))

        k = random_integers(0, len(numeros_postes_possibles)-1) if \
            len(numeros_postes_possibles) > 1 else 0
        numero_poste = numeros_postes_possibles[k]
        lettre1 = "S" if eq.c_ou_s == 's' else "C"
        lettre2 = "T" if int(num.split('n')[1]) <= 15 else "R"
        key_final = lettre1 + lettre2

        attr_saison = getattr(jj_club, "MJ"+str(numero_poste))
        attr_total = getattr(jj_club, "MJ"+str(numero_poste)+"_total")

        attr_saison[key_final] += 1
        attr_total[key_final] += 1

        setattr(jj_club, "MJ"+str(numero_poste), attr_saison)
        setattr(jj_club, "MJ"+str(numero_poste)+"_total", attr_total)

    if c_ou_s == 'c':
        equipe.sauvegarder()
        return 0
    else:
        return clubs_a_sauver

def merge_clubs(ini, a_changer):
    ll_noms = [cc.nom for cc in a_changer]
    for cc in ini:
        if cc.nom in ll_noms:
            ini.remove(cc)
    return ini + a_changer
