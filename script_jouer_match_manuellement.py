# -*- coding: cp1252 -*-
from saison import *
import selection as s

nom_cal = 'amicaux'
cal = charger_calendrier(nom_cal)

def jouer_manuellement(cal, ii, jj):
    print u"""\nSéparer les valeurs des deux équipes par ' / ' ; les valeurs d'une même équipe par ' '\nNoter un ' à la place des espaces\n"""
    match = cal.matches[ii][jj]
    st_scores = raw_input('Scores ' + match + ' ? ')
    sc1 = int(st_scores.split(' / ')[0])
    sc2 = int(st_scores.split(' / ')[1])
    tu_scores = (sc1, sc2)

    st_jaunes = raw_input("Marqueurs de jaunes "+match+' ? ')
    if not st_jaunes == '':
        st_jaunes1 = st_jaunes.split(' / ')[0]
        dd_jaunes1 = {}
        ll_jaunes1 = st_jaunes1.split(' ')
        for nom in ll_jaunes1:
            if not nom == '':
                dd_jaunes1[nom] = ll_jaunes1.count(nom)
        st_jaunes2 = st_jaunes.split(' / ')[1] if ' / ' in st_jaunes else ''
        dd_jaunes2 = {}
        ll_jaunes2 = st_jaunes2.split(' ')
        for nom in ll_jaunes2:
            if not nom == '':
                dd_jaunes2[nom] = ll_jaunes2.count(nom)
    else:
        dd_jaunes1 = {}
        dd_jaunes2 = {}

    st_rouges = raw_input("Marqueurs de rouges "+match+' ? ')
    if not st_rouges == '':
        st_rouges1 = st_rouges.split(' / ')[0]
        dd_rouges1 = {}
        ll_rouges1 = st_rouges1.split(' ')
        for nom in ll_rouges1:
            if not nom == '':
                dd_rouges1[nom] = ll_rouges1.count(nom)
        st_rouges2 = st_rouges.split(' / ')[1] if ' / ' in st_rouges else ''
        dd_rouges2 = {}
        ll_rouges2 = st_rouges2.split(' ')
        for nom in ll_rouges2:
            if not nom == '':
                dd_rouges2[nom] = ll_rouges2.count(nom)
    else:
        dd_rouges1 = {}
        dd_rouges2 = {}

    st_blessures = raw_input("Marqueurs de blessures "+match+' ? ')
    if not st_blessures == '':
        st_blessures1 = st_blessures.split(' / ')[0]
        dd_blessures1 = {}
        ll_blessures1 = st_blessures1.split(' ')
        for nom in ll_blessures1:
            if not nom == '':
                dd_blessures1[nom] = ll_blessures1.count(nom)
        st_blessures2 = st_blessures.split(' / ')[1] if ' / ' in st_blessures else ''
        dd_blessures2 = {}
        ll_blessures2 = st_blessures2.split(' ')
        for nom in ll_blessures2:
            if not nom == '':
                dd_blessures2[nom] = ll_blessures2.count(nom)
    else:
        dd_blessures1 = {}
        dd_blessures2 = {}

    st_essais = raw_input("Marqueurs d'essais "+match+' ? ')
    if not st_essais == '':
        st_essais1 = st_essais.split(' / ')[0]
        dd_essais1 = {}
        ll_essais1 = st_essais1.split(' ')
        for nom in ll_essais1:
            if not nom == '':
                dd_essais1[nom] = ll_essais1.count(nom)
        st_essais2 = st_essais.split(' / ')[1] if ' / ' in st_essais else ''
        dd_essais2 = {}
        ll_essais2 = st_essais2.split(' ')
        for nom in ll_essais2:
            if not nom == '':
                dd_essais2[nom] = ll_essais2.count(nom)
    else:
        ll_essais1 = []
        ll_essais2 = []
        dd_essais1 = {}
        dd_essais2 = {}

    DD1 = {'transformations':{},
           'penalites':{},
           'drops':{},
           'transformation_ratees':{},
           'penalite_ratees':{},
           'drop_rates':{}}
    DD2 = {'transformations':{},
           'penalites':{},
           'drops':{},
           'transformation_ratees':{},
           'penalite_ratees':{},
           'drop_rates':{}}

    for attr in ('transformations', 'penalites', 'drops'):
        st = raw_input(attr + ' ?\nSous la forme joueur:N_reussis,N_rates joueur:N_reussis,N_rates / joueur:N_reussis,N_rates\n')
        """
        st est de la forme :
        joueur:N_reussis,N_rates joueur:N_reussis,N_rates / joueur:N_reussis,N_rates
        """
        if not st == '':
            sts = st.split(' / ') if ' / ' in st else [st, '']
            for nn in (0, 1):
                st_eq = sts[nn]
                if not st_eq == '':
                    DD = DD1 if nn == 0 else DD2
                    dd_reussis = DD[attr]
                    attr_rates = attr[:-1]+'_rates' if attr == 'drops' else \
                                 attr[:-1]+'_ratees'
                    dd_rates = DD[attr_rates]
                    ll_joueurs = st_eq.split(' ')
                    for st_jj in ll_joueurs:
                        nom_joueur = st_jj.split(':')[0]
                        N_reussis = int(st_jj.split(':')[1].split(',')[0])
                        N_rates = int(st_jj.split(':')[1].split(',')[1])

                        if N_reussis > 0:
                            if nom_joueur in dd_reussis.keys():
                                dd_reussis[nom_joueur] += N_reussis
                            else:
                                dd_reussis[nom_joueur] = N_reussis

                        if N_rates > 0:
                            if nom_joueur in dd_rates.keys():
                                dd_rates[nom_joueur] += N_rates
                            else:
                                dd_rates[nom_joueur] = N_rates

    cal.scores[ii][jj] = tu_scores
    cal.dicts_essais[ii][jj] = (dd_essais1, dd_essais2)
    """
    cal.dicts_transformations[ii][jj] = (dd_transformations1, dd_transformations2)
    cal.dicts_transformation_ratees[ii][jj] = (dd_transformation_ratees1, dd_transformation_ratees2)
    cal.dicts_penalites[ii][jj] = (dd_penalites1, dd_penalites2)
    cal.dicts_penalite_ratees[ii][jj] = (dd_penalite_ratees1, dd_penalite_ratees2)
    cal.dicts_drops[ii][jj] = (dd_drops1, dd_drops2)
    cal.dicts_drop_rates[ii][jj] = (dd_drop_rates1, dd_drop_rates2)
    """
    for attr in DD1.keys():
        dicts = getattr(cal, 'dicts_'+attr)
        dicts[ii][jj] = (DD1[attr], DD2[attr])
    cal.dicts_jaunes[ii][jj] = (dd_jaunes1, dd_jaunes2)
    cal.dicts_rouges[ii][jj] = (dd_rouges1, dd_rouges2)
    cal.dicts_blessures[ii][jj] = (dd_blessures1, dd_blessures2)

    eq1 = match.split(' v ')[0]
    eq2 = match.split(' v ')[1]

    cal.dict_joues[eq1] += 1
    cal.dict_joues[eq2] += 1

    cal.dict_pour[eq1] += sc1
    cal.dict_contre[eq1] += sc2
    cal.dict_pour[eq2] += sc2
    cal.dict_contre[eq2] += sc1

    if sc1 > sc2:
        cal.dict_gagnes[eq1] += 1
        cal.dict_perdus[eq2] += 1
        if sc1 - sc2 <= 7:
            cal.dict_bonus_defensifs[eq2] += 1
    elif sc1 < sc2:
        cal.dict_perdus[eq1] += 1
        cal.dict_gagnes[eq2] += 1
        if sc2 - sc1 <= 7:
            cal.dict_bonus_defensifs[eq1] += 1
    else:
        cal.dict_nuls[eq1] += 1
        cal.dict_nuls[eq2] += 1

    if len(ll_essais1) >= 4:
        cal.dict_bonus_offensifs[eq1] += 1
    if len(ll_essais2) >= 4:
        cal.dict_bonus_offensifs[eq2] += 1

ii0, jj0 = 1, 4#indices du premier match à jouer manuellement
II, JJ = 2, 0 #indices du match à partir duquel on s'arrête de jouer manuellement

ii, jj = ii0, jj0
while ii < II:
    while jj < len(cal.scores[ii]):
        jouer_manuellement(cal, ii, jj)
        cal.sauvegarder()
        jj += 1
    ii += 1

ii = II
jj = jj0 if ii0 == II else 0
while jj < JJ:
    jouer_manuellement(cal, ii, jj)
    cal.sauvegarder()
    jj += 1

"""
Correction des noms avec des espaces
"""

for ii in range(ii0, II+1):
    N = JJ if ii == II else len(cal.scores[ii])
    for jj in range(N):
        for kk in (0, 1):
            for attr in ('essais', 'transformations', 'transformation_ratees', 'penalites', 'penalite_ratees', 'drops', 'drop_rates', 'jaunes', 'rouges', 'blessures'):
                dd = getattr(cal, 'dicts_'+attr)[ii][jj][kk]
                for k in dd.keys():
                    if "'" in k:
                        st = raw_input(k+' y/[n] ? ')
                        if st in ('y', 'Y'):
                            k_new = k.split("'")[0]+' '+k.split("'")[1]
                            dd[k_new] = dd[k]
                            del(dd[k])
cal.sauvegarder()
