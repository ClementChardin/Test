import selection as s
from matplotlib.pyplot import *

def get_all_joueurs():
    ll = []
    for nom in s.noms_clubs_vieux_monde + s.noms_clubs_nouveaux_mondes:
        cc = s.charger(nom, 'c')
        for jj in cc.get_all_joueurs():
            ll.append(jj)
    return ll

def plot_EV_poste(arm, poste, uniquement_poste1=False):
    if poste == "all":
        lab = arm
        evs = []
        for po in s.postes:
            evs += get_all_EV_poste(arm, po, uniquement_poste1)
    else:
        lab = poste
        evs = get_all_EV_poste(arm, poste, uniquement_poste1)

    res = []
    xx = range(min(evs), max(evs)+1)
    for i in xx:
        res.append(evs.count(i))

    plot(xx, res, label=lab)
    legend()

def get_all_EV_poste(arm, poste, uniquement_poste1=False):
    joueurs = s.get_joueurs_all(arm)
    evs = []
    if uniquement_poste1:
        for jj in joueurs:
            if jj.postes[1] == poste or \
               (poste == 'CE' and jj.postes[1] in ('C1', 'C2')):
                evs.append(int(jj.EV))
    else:
        for jj in joueurs:
            if poste in jj.postes or \
               (poste in ('C1', 'C2') and 'CE' in jj.postes):
                evs.append(int(s.calc_EV(jj, poste)))

    return evs

def EV_poste(poste, uniquement_poste1=False):
    ll = []
    for nom in s.noms_clubs_vieux_monde + s.noms_clubs_nouveaux_mondes:
        cc = s.charger(nom, 'c')
        for jj in cc.get_all_joueurs():
            bb = poste == jj.postes[1] if uniquement_poste1 else poste in jj.postes
            if bb:
                ll.append(jj.EV)
    return ll

def top_n(stat, saison=True, n=10, all_joueurs=None):
    """
    Retourne les n joueurs avec la stat la plus elevee.
    Stat = "essais", "penalites", etc
    """
    if all_joueurs is None:
        all_joueurs = get_all_joueurs()

    attr = stat + "_saison" if saison else stat + "_total"

    ll = []
    for jj in all_joueurs:
        if getattr(jj, attr) > 0:
            ll.append(jj)

    return sorted(ll, key=lambda jj:(getattr(jj, attr), jj.nom))[-n:]
