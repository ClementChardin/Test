﻿from selection import *
from miscellaneous import *
from date import *
from caracs_all_arm_rg import *
from coeffs_creation import *
from val_armee import *
from rang_arm import *
from noms_all import *
from ui.biopopup import BioPopup
				   
caracs = ['M', 'PL', 'PA', 'JP', 'TB', 'P', 'RP1', 'RP2', 'ME', 'R', 'TO', 'TA', 'A', 'E']

def generer_rangs(armee, jeune=False):
    """
    Retourne un tuple (RG, RG_max) pour l'armee donnée
    prend en compte le fait que si le joueur est jeune il ne peut pas etre heros
    """
    carte_rg = tirer_carte()
    rg = rang_armee(armee, carte_rg)
    carte_rg_max = tirer_carte()
    rg_max = rang_armee(armee, carte_rg_max)

    RG = rg
    RG_max = rg_max
    if jeune:
        if rg_max < rg:
            RG_max = rg
            RG = rg_max
        if RG >= rang_new('*'):
            rangs_possibles = [rg for rg in caracs_all_arm_rg[armee].keys() \
                               if rang_new(rg).type_nb == 3]
            if rangs_possibles == []:
                rangs_possibles = [rg for rg in caracs_all_arm_rg[armee].keys() \
                               if rang_new(rg).type_nb == 2]
            rg = rangs_possibles[random.random_integers(len(rangs_possibles))-1]
            RG = rang_new(rg)

    if RG >= RG_max:
        RG_max = RG
    elif RG < RG_max and not jeune:
        RG = RG_max
    return (RG, RG_max)

def generer_caracs_joueur(poste, armee, rang, jeune=True):
    if poste in ('C1', 'C2'):
        poste = 'CE'
    coeffs = coeffs_creation[poste]
    dd = caracs_all_arm_rg[armee][rang.rang]
    caracs_joueur = dict()
    dict_fonctions = dict()
    for carac in caracs:
        coeff = coeffs[carac]
        if coeff == 0:
            dict_fonctions[carac] = d0_plus
            caracs_joueur[carac] = dd[carac] + dict_fonctions[carac]()
        else:
            if abs(coeff) == 1:
                    dict_fonctions[carac] = d1_plus
            elif abs(coeff) == 2:
                    dict_fonctions[carac] = d2_plus
            elif abs(coeff) == 3:
                    dict_fonctions[carac] = d3_plus
            caracs_joueur[carac] = dd[carac] + coeff/abs(coeff) * dict_fonctions[carac]()
        caracs_joueur[carac] = max(0, caracs_joueur[carac])

    #M = max(caracs_joueur['RP1'], caracs_joueur['RP2'])
    #m = min(caracs_joueur['RP1'], caracs_joueur['RP2'])
    #caracs_joueur['RP_tot'] = M + max(0, m-7)
    RPmin = min(caracs_joueur["RP1"], caracs_joueur["RP2"])
    RPmax = max(caracs_joueur["RP1"], caracs_joueur["RP2"])
    if RPmin <= 7:
        m = 0
    elif RPmin <= 10:
        m = 1
    else:
        m = 2
    if RPmax <= 7:
        N = 1
    elif RPmax <= 10:
        N = 2
    else:
        N = 3
    caracs_joueur["RP_tot"] = RPmax + max(m, RPmin - (RPmax - N))
    return caracs_joueur

def generer_creation():
    carte = tirer_carte()
    if carte['valeur'] <= 10:
        return lire_date() - carte['valeur']
    else:
        return lire_date()

def generer_delta_declin():
    carte = tirer_carte()
    if carte['valeur'] < 7:
        return 7 + carte['valeur']
    else:
        return carte['valeur']

def generer_val_ms(armee, rg):
    val = val_armee[armee][rg.rang]
    ms = val / 10.
    carte_val = tirer_carte()
    VAL = val * (1 + carte_val['valeur']/10.)
    carte_ms = tirer_carte()
    MS = ms * (1 + carte_val['valeur']/10.)
    return int(VAL), int(MS)

def generer_joueur(poste, armee, saison_en_cours=True, nom_club=''):
    creation = lire_date() if saison_en_cours else generer_creation()
    declin = creation + generer_delta_declin()
    jeune = creation in (lire_date(), lire_date()-1)

    RG, RG_max = generer_rangs(armee, jeune)
    VAL, MS = generer_val_ms(armee, RG)
    caracs = generer_caracs_joueur(poste, armee, RG, jeune)

    jj = creer_joueur_vide()
    jj.caracs_sans_fatigue = caracs
    jj.caracs = caracs
    jj.C = creation
    jj.D = declin
    jj.RG = RG
    jj.RG_max = RG_max
    jj.VAL = VAL
    jj.MS = MS
    jj.postes = ('dummy', poste, '', '')
    jj.ARM = armee

    if not saison_en_cours:
        for dat in range(max(11, jj.C), 13):
            jj_aux = s.joueur()
            jj_aux.nom = jj.nom
            jj_aux.caracs_sans_fatigue = jj.caracs_sans_fatigue
            jj_aux.postes = jj.postes
            jj_aux.club = nom_club
            jj.jj_passe['s'+str(dat)] = jj_aux

    return jj

def generer_ajouter_joueur_complet(poste,
                                   armee,
                                   saison_en_cours=True,
                                   club=None,
                                   nom_club="vide",
                                   payer=True,
                                   espoir=False):
    if club is None:
        if not nom_club in s.noms_clubs():
            raise ValueError("Ce club n'existe pas !")
        else:
            club = charger(nom_club, 'c')
    else:
        nom_club = club.nom
    jj = generer_joueur(poste,
                        armee,
                        saison_en_cours=saison_en_cours,
                        nom_club=nom_club)

    #bp = BioPopup(joueurs=[jj])
    #bp.show()
    jj.show()

    nb_postes = max(1, min(d2_plus(), 3))
    if poste == 'CE':
        N = nb_postes
        poste = raw_input("C1 ou C2 ? ")
    ll = [poste, "", ""]

    if nb_postes > 1:
        N = nb_postes - 1
        for ii in range(N):
            ll[ii+1] = raw_input("Poste " + str(ii+2) + " / " + str(N+1)+" ? ")

    jj.postes = ("dummy", ll[0], ll[1], ll[2])
    jj.EV = calc_EV(jj, jj.postes[1])

    n_lettre = random.random_integers(26)
    nom = raw_input(chr(96 + n_lettre) + ', ' + armee + ' ? ')
    jj.nom = nom

    s.ajouter_joueur(jj, club, espoir)

    if payer:
        club.budget -= jj.VAL

    club.sauvegarder()
