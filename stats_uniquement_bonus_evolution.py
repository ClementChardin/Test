# -*- coding: cp1252 -*-
import selection as s

def bonus_atteint_avant_debut_saison(jj, dat=None):
    if dat is None:
        dat = s.lire_date()
    """
    print jj.nom, u'création :', jj.C
    print 'xp avant saison :', jj.xp_total-jj.xp_saison
    """
    atteints = 0
    residus = 0
    xp = 0
    for da in range(max(jj.C, 11), dat):
        key = 's'+str(da)
        jjj = jj.jj_passe[key]
        seuil = 1 + atteints + da - jj.C

        atteints_sais = 0

        xp = jjj.xp_saison + residus
        while xp >= seuil:
            #print 'Pour atteindre', atteints+1, '; seuil =', seuil, '; xp =', xp, 'OK, reste', xp-seuil
            xp -= seuil
            seuil += 1
            atteints += 1
            atteints_sais += 1
        #print 'Pour atteindre', atteints+1, '; seuil =', seuil, '; xp =', xp, 'NON'

        residus = xp
        #print 'saison', da, ': bonus atteints :', atteints_sais, '; residus :', residus, '\n'

    residus = xp
    """
    print 'atteints :', atteints
    print 'residus', residus, '\n'
    """
    return atteints, residus

def bonus_atteints_saison_en_cours(jj, dat=None):
    if dat is None:
        dat = s.lire_date()

    atteints, residus = bonus_atteint_avant_debut_saison(jj, dat)
    seuil = 1 + atteints + dat - jj.C
    atteints_saison = 0

    xp = jj.xp_saison + residus
    while xp >= seuil:
        xp -= seuil
        seuil += 1
        atteints += 1
        atteints_saison += 1
    """
    print jj.nom, u'création :', jj.C
    print 'xp saison :', jj.xp_saison
    print 'residus avant :', residus
    print 'atteints tot :', atteints
    print 'atteints saison :', atteints_saison
    print 'residus apres', xp, '\n'
    """
    residus = xp
    return atteints_saison, residus, atteints

def xp_manquante_prochain_bonus(jj, dat=None):
    if dat is None:
        dat = s.lire_date()

    atteints_saison, residus, atteints_total = bonus_atteints_saison_en_cours(jj, dat)
    seuil = 1 + atteints_total + dat - jj.C
    """
    print jj.nom, u'création :', jj.C
    print 'xp manquante :', abs(seuil - residus), '\n'
    """
    return abs(seuil - residus)
