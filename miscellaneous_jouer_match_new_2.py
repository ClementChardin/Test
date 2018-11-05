# -*- coding: cp1252 -*-
from miscellaneous import *
from numpy.random import random_integers
import selection as s
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

def tps_fort(carte, N_tps_forts, prolongation=False):
    """
    Identifie les temps forts - renvoie une liste
    de tuples (type, zone, av ou ar, malus bonus tab, chrono)
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
    # largeur : touches en 0 et 60
    # distance : ligne d'essai en 0
    zones = []
    bonus_malus = []
    for typ in types:
        largeur = random_integers(59)
        distance = random_integers(60)
        print typ, 'distance =', distance, '; largeur =', largeur
        if typ == 'penalite':
            if largeur < 5 or largeur > 55:
                if distance <= 22:
                    bonus_malus.append(-2)
                else:
                    bonus_malus.append(-3)
            elif largeur < 10 or largeur > 50:
                if distance <= 22:
                    bonus_malus.append(-1)
                else:
                    bonus_malus.append(-2)
            elif largeur < 15 or largeur > 45:
                if distance <= 15:
                    bonus_malus.append(0)
                else:
                    bonus_malus.append(-1)
            elif largeur < 25 or largeur > 35:
                if distance <= 15:
                    bonus_malus.append(1)
                else:
                    bonus_malus.append(0)
            else:
                if distance <= 15:
                    bonus_malus.append(2)
                elif distance <= 22:
                    bonus_malus.append(1)
                else:
                    bonus_malus.append(0)
        else:
            if distance <= 5:
                zones.append(1)
            elif distance <= 22:
                zones.append(2)
            elif distance <= 35:
                zones.append(3)
            else:
                zones.append(4)
            bonus_malus.append(

    """
    AV ou AR
    """
    if carte["r_n"] == 'r':
        av_ars += ['av']*len(types)
    else:
        av_ars += ['ar']*len(types)

    """
    Chrono
    """
    if prolongation:
        N1 = max(N_tps_forts, 4)
        N2 = int(20./N1)
        offset = 80
    else:
        N1 = max(N_tps_forts, 8)
        N2 = int(80./N1)
        offset = 0
    n1 = random_integers(0, N1-1)
    chronos = []
    for typ in types:
        n2 = random_integers(0, N2-1)
        chronos.append(offset + n1*N2 + n2)

    res = []
    while len(zones) < len(types):
        zones.append(1)
    while len(av_ars) < len(types):
        av_ars.append("av")
    while len(malus_bonus) < len(types):
        malus_bonus.append("non")
    for i in range(len(types)):
        res.append((types[i], zones[i], av_ars[i], malus_bonus[i], chronos[i]))
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
    val = carte["valeur"]
    seuil = diff if diff < 10 else min(diff, 10 + max(int(diff / 10 -1), 0))
    res = seuil - val
    boo = res >= 0
    print u'différence :', diff, "; seuil", seuil, "; carte", val
    print u"résultat :", boo, "; bonus M :", int(res)
    return boo, int(res)

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
    """ A modifier !!! """
    if TB <= 8:
        return 4 + (8-TB)*2
    else:
        return 4 - (TB-8)


