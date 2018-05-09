# -*- coding: cp1252 -*-
from club import *
from noms_all import *
from savefiles import *
from constantes import *
import pickle

vide = creer_joueur_vide()

def get_clubs_all():
    ll = []
    for nom in noms_clubs():
        cc = charger(nom, 'c')
        ll.append(cc)
    return ll

def get_joueurs_all(arm):
    clubs = get_clubs_all()
    ll = []
    if arm in ('ULT', 'ULTB'):
        for cc in clubs:
            ll += cc.get_all_joueurs()
    else:
        for cc in clubs:
            joueurs = cc.get_all_joueurs()
            for jj in joueurs:
                if jj.ARM == arm:
                    ll.append(jj)
    return ll

def get_joueur_from_nom_arm(nom, arm, joueurs=None):
    if joueurs == None:
        joueurs = get_joueurs_all(arm)
    for j in joueurs:
        if j.nom == nom:
            return j

def set_j_ev_min(meilleurs, evals, poste):
    ev_min = max(evals)      
    j_min = vide
    for j in meilleurs:
        if j.caracs_sans_fatigue == vide.caracs_sans_fatigue:
            ev_min = 0
            j_min = vide
        elif calc_EV(j, poste) < ev_min:
            ev_min = calc_EV(j, poste)
            j_min = j
    return (j_min, ev_min)

def j_vide_poste(poste):
    jj = vide
    jj.postes = ('Dummy', poste, '', '')
    return jj

def n_meilleurs(arm, poste, n=5, ret=True, show=False):
    joueurs = get_joueurs_all(arm)
    j_vide = j_vide_poste(poste)
    meilleurs = [j_vide]*n
    evals = [0]*n
    ev_min = 0
    j_min = j_vide

    for jj in joueurs:
        if (poste in jj.postes) or \
           (poste in ['C1', 'C2'] and ('CE' in jj.postes \
            or 'C1' in jj.postes or 'C2' in jj.postes)):
            
            EV = calc_EV(jj, poste)
            if EV >= ev_min:
                evals.remove(ev_min)
                evals.append(EV)
                
                meilleurs.remove(j_min)
                meilleurs.append(jj)

                (j_min, ev_min) = set_j_ev_min(meilleurs, evals, poste)

    meilleurs = sorted(meilleurs, key=lambda j: calc_EV(j, poste))
    meilleurs.reverse()

    if show:
        ult = selec_ultime_poste(poste)
        ult_noms = []
        for j in ult:
            ult_noms.append(j.nom)
        for m in meilleurs:
            s = m.nom
            if m != j_vide:
                if m.est_jeune():
                    s = s + ' (J)'
                elif m.en_declin():
                    s = s + ' (D)'

                s = s + ' : ' + m.club + ' ' + str(calc_EV(m, poste))
                if m.nom in ult_noms:
                    idx = ult_noms.index(m.nom)
                    s = s + ' classe ' + str(idx+1)
                    print s
                else:
                    print s

    if ret:
        return meilleurs
                
class selection(club):
    def __init__(self, nom="Vide", joueurs=[]):
        super(selection, self).__init__(nom=nom)
        self.nom = nom
        self.joueurs = joueurs
        self.compo_defaut = compo()

        self.points = 0

    def sauvegarder(self):
        save_dir = SELECTIONS_DIR_NAME() + '/' + self.nom
        if not osp.isdir(save_dir):
            os.mkdir(save_dir)
        with open(save_dir+'/'+self.nom+'.sel', 'w') as f:
            pickle.dump(self, f)
        print self.nom + u" sauvegardé"

    def get_all_joueurs(self):
        return self.joueurs

    def get_joueurs_noms(self):
        for j in self.joueurs:
            print j.nom

    def compos_sauvees(self):
        l = []
        for file in os.listdir(s.SELECTIONS_DIR_NAME()+"/"+self.nom):
            if file.endswith(".comp"):
                l.append(file[:-5])
        return l

    def show_all_ev(self):
        for jj in sorted(self.joueurs,
                         key = lambda jj: postes.index(jj.postes[1])):
            if jj.est_jeune():
                st = jj.nom + ' (J) :'
            elif jj.en_declin():
                st = jj.nom + ' (D) :'
            else:
                st = jj.nom + ' : '
            for k in range(1,4):
                p = jj.postes[k]
                if p != '':
                    if p in ['C1', 'CE']:
                        st = st + ' ' + 'C1' + ' ' + str('%0.2f' % calc_EV(jj, 'C1')) + ' ; '
                        st = st + ' ' + 'C2' + ' ' + str('%0.2f' % calc_EV(jj, 'C2')) + ' ; '
                    elif p == 'C2':
                        st = st + ' ' + 'C2' + ' ' + str('%0.2f' % calc_EV(jj, 'C2')) + ' ; '
                        st = st + ' ' + 'C1' + ' ' + str('%0.2f' % calc_EV(jj, 'C1')) + ' ; '
                    
                    else:
                        st = st + ' ' + p + ' ' + str('%0.2f' % calc_EV(jj, p)) + ' ; '
            print st

def creer_selection(arm, dict_joueurs):
    l = []
    s = selection()
    s.nom = arm
    joueurs = get_joueurs_all(arm)

    noms_joueurs = []
    for ll in dict_joueurs.values():
        for nn in ll:
            noms_joueurs.append(nn)

    for nom in noms_joueurs:
        j = get_joueur_from_nom_arm(nom, arm)
        l.append(j)

    if len(noms_joueurs) < 30:
        N = 30 - len(noms_joueurs)
        for i in range(N):
            nom = raw_input('Nom ? ')
            j = get_joueur_from_nom_arm(nom, arm)
            l.append(j)

    s.joueurs = sorted(l, key = lambda j: j.postes[1])
    s.sauvegarder()

    s.show_all_ev()

    nom_comp = raw_input('Nom compo ? ')
    s.compo_defaut = faire_compo(s, 's', nom=nom_comp)


    return s

def selec_ultime_poste(poste, ret=True, show=False, n=10):
    d= dict()
    for ar in noms_armees:
        d[ar] = n_meilleurs(ar, poste, min(6, n), ret=True, show=False)
    ll = []
    for l_arm in d.values():
        ll += l_arm
    ll = sorted(ll, key=lambda j: calc_EV(j, poste))

    if n>0:
        ll = ll[-n:]
        
    ll.reverse()

    if show:
        for i,jj in enumerate(ll):
            print i+1, jj.nom + ' ' + str('%0.2f' % calc_EV(jj, poste)) + \
                  ' / ' + str('%0.2f' % jj.EV) + ' ' + jj.ARM + ' ' + \
                  jj.club + ' ' + str(jj.C)
        
    if ret:
        return ll

def salaire_moyen_arm_rg(arm, rg):
    joueurs = []
    if arm == 'all':
        for ar in armees:
            joueurs = joueurs + get_joueurs_all(ar)
    else:
        joueurs = get_joueurs_all(arm)
    nb_j = 0
    tot = 0

    for j in joueurs:
        if j.RG == rg:
            tot = tot + j.MS
            nb_j = nb_j + 1

    moy = tot / nb_j

    return moy
    
def nouveau_rg():
    for n in noms_clubs():
        c = charger(n)
        for l in c.joueurs.values():
            for j in l:
                try:
                    rg_max = rang(j.RG_max)
                    j.RG_max = rg_max
                except AttributeError:
                    print c.nom + ' RG_max pas renseigne'
        c.sauvegarder()

def selec_ultime_poste_joue(poste, ret=True, show=False, n=10):
    d = dict()
    j_vide = j_vide_poste(poste)
    for ar in armees:
        d[ar] = n_meilleurs(ar, poste, 6, ret=True)
    l = []
    for ll in d.values():
        for jj in ll:
            if jj != j_vide:
                clb = charger(jj.club)
                for num in corres_poste_num[poste]:
                    if clb.compo_defaut.joueurs[num].nom == jj.nom:
                        l.append(jj)
    l = sorted(l, key=lambda j: calc_EV(j, poste))

    if n>0:
        l = l[-n:]
        
    l.reverse()
        
    if ret:
        return l

    if show:
        for i,j in enumerate(l):
            print i+1, j.nom + ' ' + str('%0.2f' % calc_EV(j, poste)) + ' / ' + str('%0.2f' % j.EV) + ' ' + j.ARM + ' ' + j.club + ' ' + str(j.C)

def selec_ultime_poste_prefere(poste, ret=True, show=False, n=10):
    d = dict()
    j_vide = j_vide_poste(poste)
    for ar in armees:
        d[ar] = n_meilleurs(ar, poste, 6, ret=True)
    l = []
    for ll in d.values():
        for jj in ll:
            if jj != j_vide:
                if jj.postes[1] == poste:
                    l.append(jj)
    l = sorted(l, key=lambda j: calc_EV(j, poste))

    if n>0:
        l = l[-n:]
        
    l.reverse()
        
    if ret:
        return l

    if show:
        for i,j in enumerate(l):
            print i+1, j.nom + ' ' + str('%0.2f' % calc_EV(j, poste)) + ' ' + j.ARM + ' ' + j.club + ' ' + str(j.C)

def maj_joueurs(sel):
    all_joueurs = get_joueurs_all(sel.nom)
    for jj in all_joueurs:
        for jjj in sel.joueurs:
            if jjj.nom == jj.nom:
                sel.joueurs.remove(jjj)
                sel.joueurs.append(jj)
        for nn in sel.compo_defaut.joueurs.keys():
            if sel.compo_defaut.joueurs[nn].nom == jj.nom:
                sel.compo_defaut.joueurs[nn] = jj
        for role in sel.compo_defaut.roles.keys():
            if sel.compo_defaut.roles[role].nom == jj.nom:
                sel.compo_defaut.roles[role] = jj
