import selection as s
from date import *
from miscellaneous import *
from constantes import *
from generer_joueur.caracs_all_arm_rg import *
from generer_joueur.caracs_evolution_joueur import *
from generer_joueur.val_armee import *
from numpy import mean
from numpy.random import random_integers

def retraite(joueur, dat=None):
    dat = s.lire_date() if dat is None else dat
    if joueur.D > dat:
        joueur.retraite = False
        joueur.points_retraite = 0
        joueur.rand_retraite = 10
    else:
        D = max(joueur.D, 11)
        key = 's'+str(D)
        EVD = joueur.jj_passe[key].EV if key in joueur.jj_passe.keys() \
              else joueur.EV

        N = dat - joueur.D + int(EVD - joueur.EV)
        joueur.points_retraite = N

        rand = random_integers(10)
        joueur.random_retraite = rand
        if rand < N:
            joueur.retraite = True
        else:
            joueur.retraite = False

def veut_partir(joueur):
    dernier_transfert = joueur.anciens_clubs.split(';')[-1]
    if dernier_transfert == '':
        dat = 0
    else:
        dat = int(dernier_transfert.split(' ')[1])
    score = score_partir(joueur)
    carte = tirer_carte()
    veut_partir = (carte['valeur'] > score or carte['valeur'] == 14) \
                  and dat < lire_date() - 1 and joueur.C < lire_date() - 1
    MS_probleme = bonus_MS(joueur) < 0
    return veut_partir, MS_probleme

def faire_offre(jj, priorite, poste):
    base_MS = MS_min(s.calc_EV(jj, poste))
    base_VAL = jj.VAL

    if priorite == 1:
        mult = 0.75
    elif priorite == 2:
        mult = 1.
    elif priorite == 3:
        mult = 1.25
    elif priorite == 4:
        mult = 1.5

    carte_MS = tirer_carte()
    carte_VAL = tirer_carte()

    MS = max(int(0.75 * base_MS * mult * (1 + carte_MS['valeur'] / 10.)),
             MS_min(s.calc_EV(jj, poste)))
    VAL = max(int(0.75 * base_VAL * mult * (1 + carte_VAL['valeur'] / 10.)),
              10*MS_min(s.calc_EV(jj, poste)))

    return VAL, MS

def score_offre(joueur, club, ms, poste):
    score = 0
    if club.nom == joueur.club:
        score += pts_matches_club(joueur)
    else:
        a_comparer = joueurs_a_comparer(joueur, club)
        pts = [pts_matches_club(jj) for jj in a_comparer]
        score += int(round(mean(pts)))

    score += int(club.prestige() / 3.)

    ms_min = MS_min(joueur.EV)
    coeff = 1. if ms_min < 20 else 5.

    if ms >= joueur.MS:
        if joueur.MS_probleme:
            score += int(2*(ms - ms_min))
        else:
            score += int(ms - ms_min)
    else:
        score -= int((joueur.MS - ms)/5.) + 1

    if poste == joueur.postes[1] or poste == 'tous' \
       or (joueur.postes[1] in ('C1', 'C2') and poste in ('C1', 'C2', 'CE')):
        score += 4

    return max(score, 1)

def choisir_offre(jj, offres):
    """
    jj = joueur
    offres = liste d'offres de la forme (club, VAL, MS, poste, tps_laisse)
    """
    scores = []
    tot = 0
    #print len(offres), "offres"
    for offre in offres:
        club, VAL, MS, poste, tps_laisse = offre
        score = score_offre(jj, club, MS, poste)
        scores.append(score)
        tot += score
        #print club.nom, VAL, MS, poste, tps_laisse, "--- score :", score, "---, total :", tot
    """
    offres_print = [(o[0].nom, o[1], o[2], o[3]) for o in offres]
    for ii in range(len(offres)):
        print offres_print[ii], '\t', scores[ii]
    """
    rand = random_integers(tot)
    #print "rand =", rand
    aux = 0
    for ii, sc in enumerate(scores):
        aux += sc
        #print ii, aux
        if aux >= rand:
            break
    #club, VAL, MS, poste, tps_laisse = offres[ii]
    #print "choisie :", club.nom, VAL, MS, poste, tps_laisse
    return offres[ii]

def attribuer_temps_laisse(offres):
    res = []
    for offre in offres:
        club, VAL, MS, poste = offre
        temps_laisse = 3 + d3_plus()
        res.append((club, VAL, MS, poste, temps_laisse))
    return res

def aux_offre(offre):
    """
    Transforme une offre (club, VAL, MS, poste, tps_laisse)
    en (nom_club, VAL, MS, poste, tps_laisse)
    """
    club, VAL, MS, poste, tps_laisse = offre
    return club.nom, VAL, MS, poste, tps_laisse

def classer_offres(jj, offres):
    classement = []
    offres = attribuer_temps_laisse(offres)
    while len(offres) > 0:
        preferee = choisir_offre(jj, offres)
        classement.append(aux_offre(preferee))
        offres.remove(preferee)
    return classement

def joueurs_meme_poste(joueur, cc=None):
    if cc is None:
        cc = s.charger(joueur.club, 'c')
    poste = poste_le_plus_joue(joueur)
    joueurs_meme_poste = []
    for jj in cc.get_all_joueurs():
        if not jj.nom == joueur.nom and poste_le_plus_joue(jj) == poste:
            joueurs_meme_poste.append(jj)

    return joueurs_meme_poste

def joueur_comparaison(joueur, cc=None):
    jmp = joueurs_meme_poste(joueur, cc)
    diff_EV = 100

    jj_comparaison = s.joueur()
    for jj in jmp:
        poste = poste_le_plus_joue(joueur)
        if not poste in ('C1', 'C2', 'CE'):
            EV_jj = s.calc_EV(jj, poste)
            EV_joueur = s.calc_EV(joueur, poste)
        else:
            EV_jj = max(s.calc_EV(jj, 'C1'), s.calc_EV(jj, 'C2'))
            EV_joueur = max(s.calc_EV(joueur, 'C1'), s.calc_EV(joueur, 'C2'))
        diff = abs(EV_jj - EV_joueur)
        if diff < diff_EV:
            jj_comparaison = jj
            diff_EV = diff
        elif diff == diff_EV:
            jj_comparaison = max(jj, jj_comparaison,
                                 key=lambda jjj:pts_matches_club(jjj))
    return jj_comparaison

def joueurs_a_comparer(joueur, cc=None):
    if cc is None:
        cc = s.charger(joueur.club, 'c')

    postes = [joueur.postes[ii] for ii in range(1, 4) \
              if not joueur.postes[ii] == '']
    if 'CE' in postes:
        postes.remove('CE')
        postes += ['C1', 'C2']
    elif 'C1' in postes:
        postes.append('C2')
    elif 'C2' in postes:
        postes.append('C1')

    joueurs = []
    for pp in postes:
        EV_joueur = s.calc_EV(joueur, pp)
        ppp = 'CE' if pp in ('C1', 'C2') else pp
        ll = cc.joueurs[ppp]
        for jj in ll:
            EV_jj = s.calc_EV(jj, pp)
            if EV_jj > EV_joueur - .5 and EV_jj < EV_joueur + .5 \
               and not jj in joueurs:
                joueurs.append(jj)

    if joueurs == []:
        poste = 'CE' if joueur.postes[1] in ('C1', 'C2') else joueur.postes[1]
        joueurs.append(min([jj for jj in cc.joueurs[poste]],
                           key=lambda jj: abs(s.calc_EV(jj, joueur.postes[1]) \
                                              - s.calc_EV(joueur, joueur.postes[1]))))
    return joueurs

def score_partir(joueur):
    bonus = 0
    jj_comparaison = joueur_comparaison(joueur)
    poste = poste_le_plus_joue(joueur)
    cc = s.charger(joueur.club, 'c')

    bonus += bonus_points_matches(joueur, jj_comparaison, poste)
    if bonus_evolution(joueur) > 0:
        bonus += 4

    if joueur.nom in cc.compo_defaut.noms_titulaires:
        bonus += 3
    elif joueur.nom in cc.compo_defaut.noms_remplacants:
        bonus += 1

    bonus += bonus_MS(joueur)

    if joueur.est_jeune():
        bonus += 6
    elif joueur.anciens_clubs == '':
        bonus += 2
    else:
        dernier_transfert = joueur.anciens_clubs.split(';')[-1]
        try:
            date = int(dernier_transfert[-2:-1])
        except ValueError:
            date = int(dernier_transfert[-1])
        if date >= s.date - 2:
            bonus += 6

    return bonus

def bonus_points_matches(jj, jj_comparaison, poste):
    if not jj_comparaison.nom == 'nom':
        #correspont a joueur vide : pas de comparaison trouvee
        if not poste in ('C1', 'C2', 'CE'):
            EV_jj = s.calc_EV(jj, poste)
            EV_comparaison = s.calc_EV(jj_comparaison, poste)
        else:
            EV_jj = max(s.calc_EV(jj, 'C1'), s.calc_EV(jj, 'C2'))
            EV_comparaison = max(s.calc_EV(jj_comparaison, 'C1'),
                                 s.calc_EV(jj_comparaison, 'C2'))

        if abs(EV_jj - EV_comparaison) > 1:
            return 4
        else:
            diff_MJ = pts_matches_club(jj) - pts_matches_club(jj_comparaison)
            if diff_MJ > 3:
                return 4
            elif diff_MJ > -3:
                return 2
            elif diff_MJ > -8:
                return 0
            else:
                return -4
    else:
        return 4

def poste_le_plus_joue(jj):
    M = 0
    poste = jj.postes[1]
    for ii in range(1, 4):
        if pts_matches_club_poste(jj, ii) > M:
            poste = jj.postes[ii]
            M = pts_matches_club_poste(jj, ii)
    return poste

def pts_matches_club(jj):
    res = 0
    for ii in range(1, 4):
        res += getattr(jj, 'MJ'+str(ii))['CT'] + \
               getattr(jj, 'MJ'+str(ii))['CR']*.5
    return res

def pts_matches_club_poste(jj, num_poste):
    return getattr(jj, 'MJ'+str(num_poste))['CT'] + \
           getattr(jj, 'MJ'+str(num_poste))['CR']*.5

def pts_matches_total(jj):
    res = 0
    for ii in range(1, 4):
        res += getattr(jj, 'MJ'+str(ii))['CT'] + \
               getattr(jj, 'MJ'+str(ii))['CR']*.5
        res += getattr(jj, 'MJ'+str(ii))['ST'] + \
               getattr(jj, 'MJ'+str(ii))['SR']*.5
    return res

def bonus_evolution(jj):
    pts = pts_matches_total(jj)
    EV = int(jj.EV)
    if pts < EV-3 + EV-6:
        bonus = 0
    elif pts < EV-1 + EV-6:
        bonus = 1
    elif pts < EV+2 + EV-6:
        bonus = 2
    elif pts < EV+6 + EV-6:
        bonus = 3
    else:
        bonus = 4
    jj.bonus = bonus
    return bonus
        
def bonus_MS(jj, MS=None):
    if MS is None:
        MS = jj.MS

    if jj.EV < 7:
        if MS < 2:
            return 0
        elif MS < 5:
            return 1
        elif MS < 10:
            return 3
        elif MS < 20:
            return 5
        else:
            return 6

    elif jj.EV < 8:
        if MS < 2:
            return 0
        elif MS < 5:
            return 1
        elif MS < 10:
            return 3
        elif MS < 20:
            return 4
        elif MS < 50:
            return 5
        else:
            return 6

    elif jj.EV < 9:
        if MS < 2:
            return -1
        elif MS < 5:
            return 0
        elif MS < 10:
            return 1
        elif MS < 20:
            return 3
        elif MS < 50:
            return 4
        elif MS < 100:
            return 5
        else:
            return 6

    elif jj.EV < 10:
        if MS < 2:
            return -3
        elif MS < 5:
            return -1
        elif MS < 10:
            return 0
        elif MS < 20:
            return 1
        elif MS < 50:
            return 3
        elif MS < 100:
            return 4
        elif MS < 200:
            return 5
        else:
            return 6

    elif jj.EV < 11:
        if MS < 2:
            return -4
        elif MS < 5:
            return -2
        elif MS < 10:
            return -1
        elif MS < 20:
            return 0
        elif MS < 50:
            return 1
        elif MS < 100:
            return 2
        elif MS < 200:
            return 3
        elif MS < 300:
            return 4
        elif MS < 500:
            return 5
        else:
            return 6

    elif jj.EV < 12:
        if MS < 2:
            return -5
        elif MS < 5:
            return -4
        elif MS < 10:
            return -3
        elif MS < 20:
            return -1
        elif MS < 50:
            return 0
        elif MS < 100:
            return 1
        elif MS < 200:
            return 2
        elif MS < 300:
            return 3
        elif MS < 500:
            return 4
        elif MS < 800:
            return 5
        else:
            return 6

    elif jj.EV < 13:
        if MS < 2:
            return -6
        elif MS < 5:
            return -5
        elif MS < 10:
            return -4
        elif MS < 20:
            return -3
        elif MS < 50:
            return -1
        elif MS < 100:
            return 0
        elif MS < 200:
            return 1
        elif MS < 300:
            return 2
        elif MS < 500:
            return 3
        elif MS < 800:
            return 4
        elif MS < 1200:
            return 5
        else:
            return 6

    else:
        if MS < 2:
            return -6
        elif MS < 5:
            return -5
        elif MS < 10:
            return -4
        elif MS < 20:
            return -3
        elif MS < 50:
            return -2
        elif MS < 100:
            return -1
        elif MS < 200:
            return 0
        elif MS < 300:
            return 1
        elif MS < 500:
            return 2
        elif MS < 800:
            return 3
        elif MS < 1200:
            return 4
        elif MS < 1700:
                return 5
        else:
            return 6
        
def MS_min(EV):
    if EV < 8:
        return 1
    elif EV < 9:
        return 2
    elif EV < 10:
        return 5
    elif EV < 11:
        return 10
    elif EV < 12:
        return 20
    elif EV < 13:
        return 50
    else:
        return 100

def evolution_joueur(jj):
    print "Evolution " + jj.nom
    setattr(jj, "caracs_saison_"+str(date-1), dict())
    setattr(jj, "EV_saison_"+str(date-1), jj.EV)
    #dd = getattr(jj, "caracs_saison_"+str(date-1))
    #for car, val in jj.caracs_sans_fatigue.items():
    #    dd[car] = val
    bonus = bonus_evolution(jj)
    carte = tirer_carte()
    jj.carte_evolution = carte
    sgn = -1 if (carte['r_n'] == 'r' or jj.D <= s.date) else 1
    print jj.nom, "signe :", sgn, "; valeur :", carte['valeur']
    if jj.RG < jj.RG_max:
        upgrade_rang(jj)

    if carte['valeur'] == 14 \
       and sgn == -1 \
       and jj.RG.type_nb < 5 \
       and not jj.D <= s.date:
        jj.evolution = 'rang'
        upgrade_rang(jj)
    else:
        nb = d3_plus(carte)
        jj.evolution = sgn * nb
        for ii in range(nb):
            evoluer_carac_hasard(jj, sgn)

    jj.EV = s.calc_EV(jj, jj.postes[1], fatigue=False)
    print getattr(jj, "EV_saison_"+str(date-1)), jj.EV

def upgrade_rang(jj):
    rangs_possibles = []
    nn = 1
    while len(rangs_possibles) == 0 and nn < 5:
        for rg in caracs_all_arm_rg[jj.ARM].keys():
            if s.rang_new(rg).type_nb == jj.RG.type_nb + nn \
               and not():
                rangs_possibles.append(s.rang_new(rg))
        nn += 1
    if jj.RG_max in rangs_possibles:
        nouveau_rg = jj.RG_max
    else:
        if jj.ARM == 'EN' \
           and 'x' in [rg.rang for rang in rangs_possibles] \
           and not jj.RG_max.rang == 'x':
            for rg in rangs_possibles:
                if rg.rang == 'x':
                    rangs_possibles.remove(rg)
        idx = random.random_integers(len(rangs_possibles)) - 1
        nouveau_rg = rangs_possibles[idx]
    caracs = caracs_all_arm_rg[jj.ARM][nouveau_rg.rang]
    if jj.RG.rang in caracs_all_arm_rg[jj.ARM].keys():
        rang_old = jj.RG.rang
    else:
        rangs_old_possibles = []
        nn = 0
        while len(rangs_old_possibles) == 0 and nn < 5:
            for rg in caracs_all_arm_rg[jj.ARM].keys():
                if s.rang_new(rg).type_nb == jj.RG.type_nb - nn:
                    rangs_old_possibles.append(s.rang_new(rg))
            nn += 1
        idx = random.random_integers(len(rangs_old_possibles))-1
        rang_old = rangs_old_possibles[idx].rang
    caracs_old = caracs_all_arm_rg[jj.ARM][rang_old]

    for car in caracs.keys():
        if caracs[car] > caracs_old[car]:
            jj.caracs_sans_fatigue[car] += caracs[car] - caracs_old[car]
    jj.caracs_sans_fatigue['RP_tot'] = max(jj.caracs_sans_fatigue['RP1'],
                                           jj.caracs_sans_fatigue['RP2']) \
                                       + max(0,
                                             min(jj.caracs_sans_fatigue['RP1'],
                                                 jj.caracs_sans_fatigue['RP2'])-7)

    jj.VAL += max(0, val_armee[jj.ARM][nouveau_rg.rang] - \
                  val_armee[jj.ARM][rang_old])
    
    jj.MS += int(max(0, val_armee[jj.ARM][nouveau_rg.rang] - \
                     val_armee[jj.ARM][rang_old]) / 10.)

    jj.RG = nouveau_rg

def evoluer_carac_hasard(jj, sgn):
    """
    Fait evoluer une carac au hasard, en plus si sgn == 1, en moins si sgn == -1
    """
    poste = poste_le_plus_joue(jj) if pts_matches_total(jj) >= 5 \
            else jj.postes[1]
    if poste == 'CE':
        poste = 'C' + str(random.random_integers(2))
    dd = caracs_evolution[poste]
    if sgn == 1:
        carte = tirer_carte()
        for car, val in dd.items():
            if carte['valeur'] in val:
                break
        if car == 'RP':
            car = 'RP' + str(random.random_integers(2))
        """
        On retire la carte si :
            14 <= carac <= 16 et carte noire
            17 <= carac et couleur autre que coeur
        """
        if jj.caracs_sans_fatigue[car] >= 17 and carte['couleur'] != 2:
            evoluer_carac_hasard(jj, 1)
        elif jj.caracs_sans_fatigue[car] >= 14 and carte['r_n'] == 'n':
            evoluer_carac_hasard(jj, 1)
        else:
            jj.caracs_sans_fatigue[car] += 1
            if car in ('RP1', 'RP2'):
                jj.caracs_sans_fatigue['RP_tot'] = max(jj.caracs_sans_fatigue['RP1'], jj.caracs_sans_fatigue['RP2']) \
                                                   + max(0, min(jj.caracs_sans_fatigue['RP1'], jj.caracs_sans_fatigue['RP2']) - 7)
    elif sgn == -1:
        caracs_utiles = [car for car in dd.keys() if dd[car] != ()]
        nn = random.random_integers(len(caracs_utiles)) - 1
        car = caracs_utiles[nn]
        if car == 'RP':
            car = 'RP' + str(random.random_integers(2))
        jj.caracs_sans_fatigue[car] -= 1
        jj.caracs_sans_fatigue['RP_tot'] = max(jj.caracs_sans_fatigue['RP1'], jj.caracs_sans_fatigue['RP2']) \
                                           + max(0, min(jj.caracs_sans_fatigue['RP1'], jj.caracs_sans_fatigue['RP2']) - 7)

    else:
        raise ValueError("Signe n'est pas 1 ou -1 !")

def evolution_TAB(jj, car='TB'):
    carte = tirer_carte()
    if jj.caracs[car] < 7:
        pass
    else:
        if jj.caracs[car] <= 7:
            if carte['valeur'] == 1:
                jj.caracs[car] = jj.caracs[car] - 1
            elif carte['valeur'] >= 9:
                jj.caracs[car] = jj.caracs[car] + 1
        elif jj.caracs[car] <= 8:
            if carte['valeur'] <= 2:
                jj.caracs[car] = jj.caracs[car] - 1
            elif carte['valeur'] >= 9:
                jj.caracs[car] = jj.caracs[car] + 1
        elif jj.caracs[car] <= 9:
            if carte['valeur'] <= 3:
                jj.caracs[car] = jj.caracs[car] - 1
            elif carte['valeur'] >= 10:
                jj.caracs[car] = jj.caracs[car] + 1
        elif jj.caracs[car] <= 10:
            if carte['valeur'] <= 4:
                jj.caracs[car] = jj.caracs[car] - 1
            elif carte['valeur'] >= 11:
                jj.caracs[car] = jj.caracs[car] + 1
        elif jj.caracs[car] <= 11:
            if carte['valeur'] <= 4:
                jj.caracs[car] = jj.caracs[car] - 1
            elif carte['valeur'] >= 12:
                jj.caracs[car] = jj.caracs[car] + 1
        elif jj.caracs[car] <= 12:
            if carte['valeur'] <= 5:
                jj.caracs[car] = jj.caracs[car] - 1
            elif carte['valeur'] >= 13:
                jj.caracs[car] = jj.caracs[car] + 1
        elif jj.caracs[car] <= 13:
            if carte['valeur'] <= 5:
                jj.caracs[car] = jj.caracs[car] - 1
            elif carte['valeur'] >= 14:
                jj.caracs[car] = jj.caracs[car] + 1
        else:
            if carte['valeur'] <= 5:
                jj.caracs[car] = jj.caracs[car] - 1

        if car == 'TB':
            if jj.transformations_total + jj.penalites_total >= 80 \
               and jj.caracs[car] < 9:
                jj.caracs[car] = 9
            elif jj.transformations_total + jj.penalites_total >= 200 \
               and jj.caracs[car] < 10:
                jj.caracs[car] = 10
            elif jj.transformations_total + jj.penalites_total >= 500 \
               and jj.caracs[car] < 11:
                jj.caracs[car] = 11

        jj.EV = s.calc_EV(jj, jj.postes[1], fatigue=False)
