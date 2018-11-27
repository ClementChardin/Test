# -*- coding: cp1252 -*-
from joueur import *
from savefiles import *
from constantes import *
import pickle
import os.path as osp
import os
import selection as s

class club(object):
    def __init__(self, nom=None):
        if nom == None:
            self.nom = "Vide"#raw_input('Nom ? ')
        else:
            self.nom = nom
        self.joueurs = dict(PI = [],
                            TA = [],
                            DL = [],
                            TL = [],
                            N8 = [],
                            DM = [],
                            DO = [],
                            CE = [],
                            AI = [],
                            AR = [],
                            espoirs = [])

        self.valeur = 0
        self.masse_salariale = 0
        self.revenus = 0
        self.budget = 0
        self.compo_defaut = compo()
        self._compo_defaut_fatigue = None
        #self.compo_defaut.sauvegarder(self.nom+"_defaut", self.nom, "c")
        for at in ('joues', 'gagnes', 'nuls', 'perdus', 'bonus_offensif',
                   'bonus_defensif', 'pour', 'contre', 'difference'):
            setattr(self, at+'_championat', 0)
            setattr(self, at+'_coupe', 0)
        self.fatigue_prise_en_compte = True

        self.besoins = []
        self.avertissement = 0
        self.prestige_saison = {}

    def __call__(self):
        return self

    @property
    def points_championat(self):
        return 4*self.gagnes_championat + 2*self.nuls_championat + \
               self.bonus_offensif_championat + self.bonus_defensif_championat
    """
    @property
    def joues_championat(self):
        return self.gagnes_championat + self.nuls_championat + self.perdus_championat
    """

    def prestige(self, dat=None):
        """
        Donne le prestige du club au début de la saison demandée
        """
        dat = s.lire_date() if dat is None else dat
        pres = 0
        for da in range(dat-3, dat):
            key = 's'+str(da)
            if key in self.prestige_saison.keys():
                pres += self.prestige_saison[key]
        return pres

    def show(self):
        for poste in postes+['espoirs']:
            if poste != 'C1' and poste != 'C2':
                l = self.joueurs[poste]
                ll = []
                for j in l:
                    ll.append(j.nom)
                print poste, ll

    def get_all_joueurs(self):
        ll = []
        for poste in sorted(self.joueurs.keys(), key=lambda pp: s.ordre_postes[pp]):
            for jj in self.joueurs[poste]:
                ll.append(jj)
        return ll

    def show_joueurs(self):
        l = self.get_all_joueurs()
        for j in l:
            j.show()
    
    def sauvegarder(self, dat=None):
        save_dir = CLUBS_DIR_NAME(dat) + '/' + self.nom
        if not osp.isdir(save_dir):
            os.mkdir(save_dir)
        with open(save_dir+'/'+self.nom + '.clb', 'w') as f:
            pickle.dump(self, f)
        print self.nom, u"sauvegardé saison", dat

    def get_joueur_from_nom(self, nom):
        joueurs_all = self.get_all_joueurs()
        noms_all = []
        for j in joueurs_all:
            noms_all.append(j.nom)        
        if not (nom in noms_all):
            if nom == "":
                return creer_joueur_vide()
            else:
                raise ValueError("Ce joueur n'appartient pas a ce club !")
        else:
            for j in joueurs_all:
                if j.nom == nom:
                    return j

    def show_all_EV(self):
        for p in postes:
            if p != 'C1' and p != 'C2':
                l = self.joueurs[p]
                for j in l:
                    poste = j.postes[1]
                    poste2 = j.postes[2]
                    poste3 = j.postes[3]

                    s = ''
                    if j in self.compo_defaut.joueurs.values():
                        for num in self.compo_defautjoueurs.keys():
                            if self.compo_defaut.joueurs[num] == j:
                                s = num

                    if j.est_jeune():
                        s = s + ' ' + j.nom + ' (J) : '
                    elif j.en_declin():
                        s = s + ' ' + j.nom + ' (D) : '
                    else:
                        s = s + ' ' + j.nom + ' : '
                    
                    if poste == 'C1':
                        EVb = calc_EV(j, 'C2')
                        if poste2 != "":
                            EV2 = calc_EV(j, poste2)
                            if poste3 != "":
                                    EV3 = calc_EV(j, poste3)
                                    print s + poste + \
                                          " " + \
                                          str('%0.2f' % j.EV) + \
                                          " ; " + \
                                          "C2" + \
                                          " " + \
                                          str('%0.2f' % EVb) + \
                                          " ; " + \
                                          poste2 + \
                                          " " + \
                                          str('%0.2f' % EV2) + \
                                          " ; " + \
                                          poste3 + \
                                          " " + \
                                          str('%0.2f' % EV3)
                            else:
                                print s + poste + \
                                      " " + \
                                      str('%0.2f' % j.EV) + \
                                      " ; " + \
                                      "C2" + \
                                      " " + \
                                      str('%0.2f' % EVb) + \
                                      " ; " + \
                                      poste2 + \
                                      " " + \
                                      str('%0.2f' % EV2)
                        else:
                            print s + poste + \
                                  " " + \
                                  str('%0.2f' % j.EV) + \
                                  " ; " + \
                                  "C2" + \
                                  " " + \
                                  str('%0.2f' % EVb) + \
                                  " ; "

                    elif poste == 'C2':
                        EVb = calc_EV(j, 'C1')
                        if poste2 != "":
                            EV2 = calc_EV(j, poste2)
                            if poste3 != "":
                                    EV3 = calc_EV(j, poste3)
                                    print s + poste + " " + str('%0.2f' % j.EV) + " ; " + "C1" + " " + str('%0.2f' % EVb) + " ; " + poste2 + " " + str('%0.2f' % EV2) + " ; " + poste3 + " " + str('%0.2f' % EV3)
                            else:
                                print s + poste + " " + str('%0.2f' % j.EV) + " ; " + "C1" + " " + str('%0.2f' % EVb) + " ; " + poste2 + " " + str('%0.2f' % EV2)
                        else:
                            print s + poste + " " + str('%0.2f' % j.EV) + " ; " + "C1" + " " + str('%0.2f' % EVb) + " ; "
                    
                    else:
                        if poste2 != "":
                            if poste2 == 'CE':
                                EV2 = calc_EV(j, 'C1')
                                EV2b = calc_EV(j, 'C2')
                                if poste3 != "":
                                    EV3 = calc_EV(j, poste3)
                                    print s + poste + " " + str('%0.2f' % j.EV) + " ; " + 'C1' + " " + str('%0.2f' % EV2) + " ; " + 'C2' + " " + str('%0.2f' % EV2b) + " ; " + poste3 + " " + str('%0.2f' % EV3)
                                else:
                                    print s + poste + " " + str('%0.2f' % j.EV) + " ; " + 'C1' + " " + str('%0.2f' % EV2) + " ; " + 'C2' + " " + str('%0.2f' % EV2b)
                                
                            else:
                                EV2 = calc_EV(j, poste2)
                                if poste3 != "":
                                    if poste3 == 'CE':
                                        EV3 = calc_EV(j, 'C1')
                                        EV3b = calc_EV(j, 'C2')
                                        print s + poste + " " + str('%0.2f' % j.EV) + " ; " + poste2 + " " + str('%0.2f' % EV2) + " ; " + 'C1' + " " + str('%0.2f' % EV3) + " ; " + 'C2' + " " + str('%0.2f' % EV3b)
                                    else:
                                        EV3 = calc_EV(j, poste3)
                                        print s + poste + " " + str('%0.2f' % j.EV) + " ; " + poste2 + " " + str('%0.2f' % EV2) + " ; " + poste3 + " " + str('%0.2f' % EV3)
                                else:
                                    print s + poste + " " + str('%0.2f' % j.EV) + " ; " + poste2 + " " + str('%0.2f' % EV2)
                        else:
                            print s + poste + " " + str('%0.2f' % j.EV)
                print

    def show_une_carac(self,carac):
        for j in sorted(self.get_all_joueurs(), key = lambda j: j.caracs[carac]):
            print j.nom + " : " + str(j.caracs[carac])

    def set_compo_defaut(self):
        nom = self.nom + '_defaut'
        self.compo_defaut = faire_compo(self, 'c', nom=nom)
        self.sauvegarder()

    def calc_MS(self):
        MS = 0
        for j in self.get_all_joueurs():
            MS = MS + j.MS
        self.masse_salariale = MS
        print MS

    def calc_val(self):
        VAL = 0
        for j in self.get_all_joueurs():
            VAL = VAL + j.VAL
        self.valeur = VAL
        print VAL

    def compos_sauvees(self, dat=None):
        dat = s.lire_date() if dat is None else dat
        l = []
        for file in os.listdir(s.CLUBS_DIR_NAME(dat)+"/"+self.nom):
            if file.endswith(".comp"):
                l.append(file[:-5])
        return l

    @property
    def compo_defaut_fatigue(self):
        if self._compo_defaut_fatigue is None:
            defaut = self.compo_defaut
            comp = compo()
            for num, jj in defaut.joueurs.items():
                nom = jj.nom
                jj_fatigue = self.get_joueur_from_nom(nom)
                comp.joueurs[num] = jj_fatigue
            for rol, jj in defaut.roles.items():
                nom = jj.nom
                jj_fatigue = self.get_joueur_from_nom(nom)
                comp.roles[rol] = jj_fatigue

            set_caracs_old_compo(comp, self)
            #set_caracs_compo(comp, self)
            comp.calc_totaux_old()
            #comp.calc_totaux()
            self._compo_defaut_fatigue = comp
        return self._compo_defaut_fatigue

def ajouter_joueur(joueur, club, espoir=False, forcer_ajout=False):
    poste = 'espoirs' if espoir else joueur.postes[1]
    nom = joueur.nom
    if poste in ["C1", "C2"]:
        poste = "CE"
    l = club.joueurs[poste]
    lim = 10000 if club.nom == "vide" else limite_poste[poste]
    if poste == "TL":
        lim = lim - len(club.joueurs["N8"])
    elif poste == "N8":
        lim = lim - len(club.joueurs["TL"])

    if len(l) >= lim and not forcer_ajout:
        raise ValueError("poste plein !")
    else:
        l.append(joueur)
        club.valeur = club.valeur + joueur.VAL
        club.masse_salariale = club.masse_salariale + joueur.MS
        joueur.club = club.nom
    print nom + " ajoute"

def creer_club():
    c = club()
    b = raw_input('Ajouter joueur ? (nom ou n) ')

    while b != 'n' and b != '':
        j = creer_joueur(nom=b)
        ajouter_joueur(j, c)
        b = raw_input('Ajouter joueur ? (nom ou n) ')
        c.sauvegarder()

    return c

def supprimer_joueur(joueur, club):
    poste = joueur.postes[1]
    nom = joueur.nom
    if poste in ['C1','C2']:
        poste = 'CE'
    l = club.joueurs[poste]
    b = False
    if joueur in l:
        l.remove(joueur)
        b = True
    else:
        for ll in club.joueurs.values():
            if joueur in ll:
                ll.remove(joueur)
                b = True
    if b:
        print nom + " supprime"
    else:
        print nom + " pas trouve"
    
def mettre_a_jour_joueur(joueur, club):
    poste = joueur.postes[1]
    if poste in ["C1", "C2"]:
        poste = "CE"
    nom = joueur.nom
    ll = club.joueurs[poste]
    for jj in ll:
        if jj.nom == nom:
            supprimer_joueur(jj, club)
    ajouter_joueur(joueur, club)
    print nom + " mis a jour"

def transfert(nom,
              club_old,
              club_new,
              val,
              ms,
              transfert_argent=True,
              forcer_ajout=False,
              espoir=False):
    joueur = club_old.get_joueur_from_nom(nom)

    if transfert_argent:
        club_new.budget -= val
        club_old.budget += int(.75 * val)
        club_old.masse_salariale -= joueur.MS
        club_new.masse_salariale += ms

        joueur.VAL = val
        joueur.MS = ms
    ajouter_joueur(joueur, club_new, espoir=espoir, forcer_ajout=forcer_ajout)
    supprimer_joueur(joueur, club_old)
    if not club_old.nom == club_new.nom:
        if joueur.anciens_clubs == '':
            joueur.anciens_clubs = club_old.nom + ' ' + str(date)
        else:
            joueur.anciens_clubs += ';' + club_old.nom + ' ' + str(date)
    if club_new.nom == 'vide':
        joueur.veut_partir = True
    else:
        joueur.veut_partir = False
        joueur.MS_probleme = False
    print "transfert de", nom, "effectue depuis", club_old.nom, "vers", club_new.nom

def charger(nom_equipe, c_ou_s, date=None):
    if c_ou_s == 'c':
        save_dir = CLUBS_DIR_NAME(date) + '/' + nom_equipe
        extension = '.clb'
    elif c_ou_s == 's':
        save_dir = s.SELECTIONS_DIR_NAME(date) + '/' + nom_equipe
        extension = '.sel'
    else:
        raise ValueError("c_ou_s doit etre 'c' pour club ; 's' pour selection !")
    with open(save_dir+'/'+ nom_equipe + extension, 'r') as f:
        cc = pickle.load(f)
    if c_ou_s == 's':
        s.maj_joueurs(cc, date)
    return cc
     
class compo:
    def __init__(self):
        j = creer_joueur_vide()
        self.joueurs = dict(n1 = j,
                            n2 = j,
                            n3 = j,
                            n4 = j,
                            n5 = j,
                            n6 = j,
                            n7 = j,
                            n8 = j,
                            n9 = j,
                            n10 = j,
                            n11 = j,
                            n12 = j,
                            n13 = j,
                            n14 = j,
                            n15 = j,
                            n16 = j,
                            n17 = j,
                            n18 = j,
                            n19 = j,
                            n20 = j,
                            n21 = j,
                            n22 = j)

        self.remplacements = dict(n16 = 'n0',
                                  n17 = 'n0',
                                  n18 = 'n0',
                                  n19 = 'n0',
                                  n20 = 'n0',
                                  n21 = 'n0',
                                  n22 = 'n0')
        
        self.roles = dict(cap = j,
                          B1 = j,
                          B2 = j,
                          B3 = j,
                          B4 = j,
                          RJL = j,
                          RJC = j,
                          SA_pcp1 = j,
                          SA_pcp2 = j,
                          SA_scd = j,
                          SA_remp1 = j,
                          SA_remp2 = j,
                          drop1 = j,
                          drop2 = j,
                          drop3 = j)

        self.caracs = dict(M = 0,
                           OplusAV = 0,
                           OplusAR = 0,
                           OmoinsAV = 0,
                           OmoinsAR = 0,
                           ME = 0,
                           R = 0,
                           TO_def = 0,
                           TO_off = 0,
                           PA = 0,
                           JP = 0,
                           A = 0,
                           E = 0)

        self.caracs_old = dict(M = 0,
                           OplusAV = 0,
                           OplusAR = 0,
                           OmoinsAV = 0,
                           OmoinsAR = 0,
                           ME = 0,
                           R = 0,
                           TO_def = 0,
                           TO_off = 0,
                           PA = 0,
                           JP = 0,
                           A = 0,
                           E = 0)

        self.totaux = dict(T1 = 0,
                           T2 = 0,
                           T3 = 0)

        self.totaux_old = dict(T1 = 0,
                           T2 = 0,
                           T3 = 0)

        self.nom = ''

    def __call__(self):
        return self

    @property
    def noms_titulaires(self):
        l = []
        for i in range(1, 16):
            jj = self.joueurs["n"+str(i)]
            l.append(jj.nom)
        return l
    
    @property
    def noms_remplacants(self):
        l = []
        for i in range(16, 23):
            jj = self.joueurs["n"+str(i)]
            l.append(jj.nom)
        return l

    def get_joueurs_compo(self):
        l = []
        for j in self.joueurs.values():
            l.append(j)
        return l

    def ajouter_remplacement(self, remplacant, remplace):
        self.remplacements[remplacant]=remplace

    def calc_totaux(self):
        self.totaux["T1"] = .5 * (self.caracs["ME"] + self.caracs["R"] + .5*(self.caracs["TO_off"] + self.caracs["TO_def"]))
        self.totaux["T2"] = .5 * (self.caracs["PA"] + self.caracs["JP"] + self.caracs["A"])
        self.totaux["T3"] = .5 * self.caracs["E"]

    def calc_totaux_old(self):
        self.totaux_old["T1"] = arrondi_quart(.5 * (self.caracs_old["ME"] + self.caracs_old["R"] + .5*(self.caracs_old["TO_off"] + self.caracs_old["TO_def"])))
        self.totaux_old["T2"] = arrondi_quart(.5 * (self.caracs_old["PA"] + self.caracs_old["JP"] + self.caracs_old["A"]))
        self.totaux_old["T3"] = arrondi_quart(.5 * self.caracs_old["E"])

    def sauvegarder(self, nom, nom_equipe, c_ou_s, dat=None):
        dat = lire_date() if dat is None else dat
        self._compo_defaut_fatigue = None
        if c_ou_s == 'c':
            save_dir = CLUBS_DIR_NAME(dat) + '/' + nom_equipe
        elif c_ou_s == 's':
            save_dir = s.SELECTIONS_DIR_NAME(dat) + '/' + nom_equipe
        else:
            raise ValueError("c_ou_s doit etre 'c' pour club ; 's' pour selection !")

        if not osp.isdir(save_dir):
            os.mkdir(save_dir)

        self.nom = nom
        with open(save_dir+'/'+nom+'.comp', 'w') as f:
            pickle.dump(self, f)

        if nom == nom_equipe+'_defaut':
            try:
                clb = charger(nom_equipe, c_ou_s, dat)
                clb.compo_defaut = self
                clb.sauvegarder(dat)
            except IOError:
                pass

        print "compo", nom, u"sauvegardée pour", nom_equipe, "("+c_ou_s+"), dat =", dat

    def get_joueurs_noms(self):
        l = self.joueurs.keys()
        d = dict()
        for n in sorted(self.joueurs.keys(), key = lambda st: int(st.split("n")[1])):
            d[n] =  self.joueurs[n].nom
        return d

    def get_roles_noms(self):
        l = self.roles.values()
        ll = []
        for j in l:
            ll.append(j.nom)
        return ll

    def get_remplacements_noms(self):
        l = self.remplacements.values()
        ll = []
        for n in l:
            j = self.joueurs[n]
            ll.append(j.nom)
        return ll

    def EV_moyenne(self, fatigue=True):
        ll = []
        for kk, jj in self.joueurs.items():
            ll_postes = s.corres_num_poste[kk].split(' ')
            centre = ('C1' in jj.postes or 'C2' in jj.postes or 'CE' in jj.postes)
            postes = []
            for poste in ll_postes:
                if not (poste in jj.postes or (poste in ('C1', 'C2', 'CE') and centre)):
                    pass
                elif poste == 'CE' and centre:
                    postes.append('C1')
                    postes.append('C2')
                else:
                    postes.append(poste)
            num = int(kk[1:])
            if num < 16:
                ll.append(max([float(calc_EV(jj, poste, fatigue)) for poste in postes]))
            else:
                ll.append(max([float(calc_EV(jj, poste, fatigue)) / 2. for poste in postes]))
        return sum(ll) / 18.5
    
titulaires = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9', 'n10', 'n11', 'n12', 'n13', 'n14', 'n15']
remplacants = ['n16', 'n17', 'n18', 'n19', 'n20', 'n21', 'n22']

coeffs_caracs_remplaces = dict(M = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=.5, n7=.5, n8=.5, n9=.5, n10=.5, n11=1, n12=.5, n13=.5, n14=1, n15=.5),
                               OplusAV = dict(n1=1, n2=1, n3=1, n4=1, n5=1, n6=.5, n7=.5, n8=1.5),
                               OplusAR = dict(n6=.5, n7=.5, n9=.5, n10=.5, n11=1.5, n12=.5, n13=1, n14=1.5, n15=1),
                               OmoinsAV = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=1, n7=1, n8=.5),
                               OmoinsAR = dict(n9=.5, n10=1, n11=.5, n12=1, n13=1, n14=.5, n15=1.5),
                               ME = dict(n1=1.5, n2=1, n3=1.5, n4=1, n5=1, n6=.5, n7=.5, n8=.5), #/!\ ME du TA !!
                               R = dict(n1=1, n2=1, n3=1, n4=1.5, n5=1.5, n6=2, n7=2, n8=1.5, n9=.5, n10=.5, n11=.5, n12=.5, n13=.5, n14=.5, n15=.5),
                               TO_off=dict(),
                               TO_def=dict(),
                               PA = dict(n9=1.5, n10=1, n11=.5, n12=.5, n13=1, n14=.5, n15=.5),
                               JP = dict(n9=.5, n10=1, n12=.5, n15=.5),
                               A = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=.5, n7=.5, n8=.5, n9=.5, n10=1, n11=1, n12=1, n13=1, n14=1, n15=1),
                               E = dict(n1=1, n2=1, n3=1, n4=1, n5=1, n6=1, n7=1, n8=1, n9=1, n10=1, n11=1, n12=1, n13=1, n14=1, n15=1))


def coeffs_caracs(compo):
    d = dict(M = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=1, n7=1, n8=.5, n9=1.5, n10=1.5, n11=2.5, n12=1.5, n13=1.5, n14=2.5, n15=2, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             OplusAV = dict(n1=2, n2=2, n3=2, n4=2, n5=2, n6=1.5, n7=1.5, n8=2.5, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             OplusAR = dict(n6=.5, n7=.5, n9=1.5, n10=1.5, n11=3, n12=2, n13=2.5, n14=3, n15=2.5, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             OmoinsAV = dict(n1=2, n2=2, n3=2, n4=2, n5=2, n6=2.5, n7=2.5, n8=2, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             OmoinsAR = dict(n6=.5, n7=.5, n9=1.5, n10=2, n11=2, n12=2.5, n13=2.5, n14=2, n15=3, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             ME = dict(n1=2.5, n2=1.5, n3=2.5, n4=2, n5=2, n6=1, n7=1, n8=1.5, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0), #/!\ ME du TA !!
             R = dict(n1=3, n2=3, n3=3, n4=3.5, n5=3.5, n6=4.5, n7=4.5, n8=3.5, n9=.5, n10=.5, n11=.5, n12=1, n13=1, n14=.5, n15=.5, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             TO_def = dict(SA_pcp1=4, SA_pcp2=4, SA_scd=3.5, SA_remp=2, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             TO_off = dict(SA_pcp1=4, SA_pcp2=4, SA_scd=3.5, SA_remp=2, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),  #/!\ TA !!
             PA = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=.5, n7=.5, n8=.5, n9=3, n10=2.5, n11=1.5, n12=2, n13=2, n14=1.5, n15=1.5, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             JP = dict(n9=1.5, n10=2.5, n11=.5, n12=1, n13=.5, n14=.5, n15=1, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0), #/!\ RJC & RJL !!
             A = dict(n1=1, n2=1, n3=1, n4=1, n5=1, n6=1.5, n7=1.5, n8=1.5, n9=1.5, n10=1.5, n11=3, n12=2, n13=2, n14=3, n15=3, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0),
             E = dict(n1=2, n2=2, n3=2, n4=2, n5=2, n6=2, n7=2, n8=2, n9=2, n10=2, n11=2, n12=2, n13=2, n14=2, n15=2, n16=0, n17=0, n18=0, n19=0, n20=0, n21=0, n22=0)) #/!\ capitaine !!

    for remplacant in compo.remplacements.keys(): #remplacant est de la forme n_i
        remplace = compo.remplacements[remplacant] #remplace aussi
        if remplacant in titulaires:
            for carac in d.keys():
                if not remplacant in d[carac].keys():
                    d[carac][remplacant] = 0
                if not remplacant in coeffs_caracs_remplaces[carac].keys():
                    coeffs_caracs_remplaces[carac][remplacant] = 0
                d[carac][remplacant] = d[carac][remplacant] - coeffs_caracs_remplaces[carac][remplacant]

        for carac in d.keys():
            if not remplacant in d[carac].keys():
                d[carac][remplacant] = 0
            if not remplace in coeffs_caracs_remplaces[carac].keys():
                coeffs_caracs_remplaces[carac][remplace] = 0
            d[carac][remplacant] = d[carac][remplacant] + coeffs_caracs_remplaces[carac][remplace]

    return d

def set_roles(comp, equipe, c_ou_s):
    if c_ou_s == 's':
        joueurs = s.get_joueurs_all(equipe.nom)

    for k in sorted(comp.roles.keys()):
        if k == 'drop':
            nom1 = raw_input('nom drop 1 ? ')
            nom2 = raw_input('nom drop 2 ? ')
            nom3 = raw_input('nom drop 3 ? ')
            if c_ou_s == 'c':
                comp.roles[k] = [equipe.get_joueur_from_nom(nom1), equipe.get_joueur_from_nom(nom2), equipe.get_joueur_from_nom(nom3)]
            elif c_ou_s == 's':
                comp.roles[k] = [s.get_joueur_from_nom_arm(nom1, equipe.nom, joueurs=joueurs), s.get_joueur_from_nom_arm(nom2, equipe.nom, joueurs = joueurs), s.get_joueur_from_nom_arm(nom3, equipe.nom, joueurs=joueurs)]
            else:
                raise ValueError("c_ou_s doit etre 'c' pour club ; 's' pour selection !")
        else:
            nom = raw_input('nom '+ k + ' ? ')
            if c_ou_s == 'c':
                comp.roles[k] = equipe.get_joueur_from_nom(nom)
            elif c_ou_s == 's':
                comp.roles[k] = s.get_joueur_from_nom_arm(nom, equipe.nom, joueurs=joueurs)
            else:
                raise ValueError("c_ou_s doit etre 'c' pour club ; 's' pour selection !")

def set_remplacements(comp, club):
    l = comp.remplacements.keys()
    for remplacant in sorted(l):
        remplace = raw_input(str(remplacant) + ' Remplace (forme n1) ? ')
        comp.remplacements[remplacant] = remplace
    
    b = raw_input('Ajouter remplacement ? y/n ')
    while b == 'y':
        remplacant = raw_input('Remplacant (numero) ? ')
        remplace = raw_input('Remplace (numero) ? ')
        comp.ajouter_remplacement(remplacant, remplace)
        b = raw_input('Ajouter remplacement ? y/n ')

correspondance = dict(M="M",
                      OplusAV="RP_tot",
                      OplusAR="RP_tot",
                      OmoinsAV="PL",
                      OmoinsAR="PL",
                      ME="ME",
                      R="R",
                      TO_def="TO",
                      TO_off="TO",
                      PA="PA",
                      JP="JP",
                      A="A",
                      E="E")

def set_caracs_compo(comp, club):
    d = coeffs_caracs(comp)
    
    """
    Réinitialisation
    """
    for carac in comp.caracs.keys():
        comp.caracs[carac] = 0
        
    """
    Debut calcul des caracs de la compo
    """
    for carac in comp.caracs.keys():
        car = correspondance[carac]
        if carac in ['TO_off', 'TO_def']:
            SA_pcp1 = comp.roles['SA_pcp1']
            SA_pcp2 = comp.roles['SA_pcp2']
            SA_scd = comp.roles['SA_scd']
            SA_remp1 = comp.roles['SA_remp1']
            SA_remp2 = comp.roles['SA_remp2']
            comp.caracs[carac] = 4*(max(0, SA_pcp1.caracs['TO']-5) + max(0, SA_pcp2.caracs['TO'])) + 3.5*max(0, SA_scd.caracs['TO'] -5) + 2*(max(0, SA_remp1.caracs['TO']-5) + max(0, SA_remp1.caracs['TO']-10))
        else:
            for n in comp.joueurs.keys():
                if not n in d[carac].keys():
                    d[carac][n] = 0
                if carac in ['OplusAV', 'OplusAR', 'OmoinsAV', 'OmoinsAR']:
                    comp.caracs[carac] = comp.caracs[carac] + d[carac][n] * max(0,(comp.joueurs[n].caracs[car] - 7))
                if carac == 'JP':
                    comp.caracs[carac] = comp.caracs[carac] + d[carac][n] * max(0,(comp.joueurs[n].caracs['P'] - 5))
                else:
                    comp.caracs[carac] = comp.caracs[carac] + d[carac][n] * max(0,(comp.joueurs[n].caracs[car] - 5))

    """
    Cas particuliers (TA, RJC, RJL...)
    """
    comp.caracs['JP'] = comp.caracs['JP'] + (comp.roles['RJL'].caracs['P']-5) + (comp.roles['RJC'].caracs['JP']-5)
    
    remp_TA = ""
    for remplacant in comp.remplacements.keys():
        if comp.remplacements[remplacant] == 'n2':
            remp_TA = remplacant

    comp.caracs['ME'] = comp.caracs['ME'] + max(0, comp.joueurs['n2'].caracs['TA']-5) + max(0, comp.joueurs[remp_TA].caracs['TA']-5)*.5

    comp.caracs['E'] = comp.caracs['E'] + max(0, comp.roles['cap'].caracs['E']-5)

    comp.caracs['TO_off'] = comp.caracs['TO_off'] + max(0, comp.joueurs['n2'].caracs['TA']-5) + max(0, comp.joueurs[remp_TA].caracs['TA']-5)*.5
    
def charger_compo(nom_compo,nom_equipe, c_ou_s, date=None):
    if c_ou_s == 'c':
        save_dir = CLUBS_DIR_NAME(date) + '/' + nom_equipe
    elif c_ou_s == 's':
        save_dir = SELECTIONS_DIR_NAME(date) + '/' + nom_equipe
    else:
        raise ValueError("c_ou_s doit etre 'c' pour club ; 's' pour selection !")
    with open(save_dir+'/'+nom_compo+'.comp', 'r') as f:
         c = pickle.load(f)
    if not 'nom' in c.__dict__.keys():
        c.nom = nom_compo
    return c    

coeffs_compo_old = dict(M = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=1, n7=1, n8=.5, n9=1.5, n10=1.5, n11=2.5, n12=1.5, n13=1.5, n14=2.5, n15=2, n16=0, n17=0, n18=0, n19=0, n20=.5, n21=.5, n22=1),
                        OplusAV = dict(n1=2, n2=2, n3=2, n4=2, n5=2, n6=1.5, n7=1.5, n8=2.5, n16=1, n17=1, n18=1, n19=.5, n20=0, n21=0, n22=0),
                        OplusAR = dict(n6=.5, n7=.5, n9=1.5, n10=1.5, n11=3, n12=2, n13=2.5, n14=3, n15=2.5, n16=0, n17=0, n18=0, n19=0, n20=.5, n21=1, n22=1.5),
                        OmoinsAV = dict(n1=2, n2=2, n3=2, n4=2, n5=2, n6=2.5, n7=2.5, n8=2, n16=.5, n17=.5, n18=.5, n19=1.5, n20=0, n21=0, n22=0),
                        OmoinsAR = dict(n6=.5, n7=.5, n9=1.5, n10=2, n11=2, n12=2.5, n13=2.5, n14=2, n15=3, n16=0, n17=0, n18=0, n19=0, n20=.5, n21=1, n22=1),
                        ME = dict(n1=2.5, n2=1.5, n3=2.5, n4=2, n5=2, n6=1, n7=1, n8=1.5, n16=1, n17=1.5, n18=1, n19=.5, n20=0, n21=0, n22=0), #/!\ ME du TA !!
                        R = dict(n1=3, n2=3, n3=3, n4=3.5, n5=3.5, n6=4.5, n7=4.5, n8=3.5, n9=.5, n10=.5, n11=.5, n12=1, n13=1, n14=.5, n15=.5, n16=1, n17=1, n18=1.5, n19=2, n20=.5, n21=.5, n22=.5),
                        TO_def = dict(),
                        TO_off = dict(),  #/!\ TA !!
                        PA = dict(n1=.5, n2=.5, n3=.5, n4=.5, n5=.5, n6=.5, n7=.5, n8=.5, n9=3, n10=2.5, n11=1.5, n12=2, n13=2, n14=1.5, n15=1.5, n16=0, n17=0, n18=0, n19=0, n20=1, n21=.5, n22=.5),
                        JP = dict(n9=1.5, n10=2.5, n11=.5, n12=1, n13=.5, n14=.5, n15=1, n16=0, n17=0, n18=0, n19=0, n20=1, n21=.5, n22=0), #/!\ RJC & RJL !!
                        A = dict(n1=1, n2=1, n3=1, n4=1, n5=1, n6=1.5, n7=1.5, n8=1.5, n9=1.5, n10=1.5, n11=3, n12=2, n13=2, n14=3, n15=3, n16=.5, n17=.5, n18=.5, n19=.5, n20=.5, n21=1, n22=1),
                        E = dict(n1=2, n2=2, n3=2, n4=2, n5=2, n6=2, n7=2, n8=2, n9=2, n10=2, n11=2, n12=2, n13=2, n14=2, n15=2, n16=1, n17=1, n18=1, n19=1, n20=1, n21=1, n22=1)) #/!\ capitaine !!

def set_caracs_old_compo(comp, equipe, fatigue=True):
    dd = coeffs_compo_old
    
    """
    Réinitialisation
    """
    for carac in comp.caracs_old.keys():
        comp.caracs_old[carac] = 0

    """
    Prise en compte de la fatigue et de la maîtrise du poste
    """
    for num, jj in comp.joueurs.items():
        jj.caracs = s.get_caracs(jj, fatigue)
        poste_maitrise = False
        for poste in s.corres_num_poste[num].split(' '):
            if poste in jj.postes or (s.est_poste_centre(poste) and jj.joue_centre()):
                if jj.postes[1] in ('C1', 'C2') and s.est_poste_centre(poste):
                    poste = jj.postes[1]
                elif poste in ('C1', 'C2') and jj.joue_centre():
                    poste = 'CE'
                poste_maitrise = poste_maitrise or jj.postes_maitrises[jj.postes.index(poste)]
        if not poste_maitrise and not jj.nom == "":
            idx = 2 if not jj.postes[2] in s.corres_num_poste[num].split(' ') and not jj.postes_maitrises[2] else 3
            MJ = getattr(jj, 'MJ'+str(idx))
            nb_matches = MJ['CT']+MJ['ST'] + .5*(MJ['CR']+MJ['SR'])
            seuil = 0 if jj.nom == '' else matches_pour_maitriser_poste(jj.postes[1], jj.postes[idx])
            if nb_matches >= seuil:
                malus = 0
            elif nb_matches >= seuil / 2.:
                malus = .5
            else:
                malus = 1
        else:
            malus = 0

        #for car in jj.caracs.keys():
        #    jj.caracs[car] -= malus
        
        #On vérifie que le joueur est à son poste, sinon toutes les caracs subissent un -1
        postes = corres_num_poste[num].split(" ")
        boo = ne_joue_pas(postes, jj)
        if boo:
            if not jj.nom == "":
                print "set_caracs_old_compo", jj.nom + " ne joue pas " + str(postes) + " !"
                malus += 1
        if malus > 0:
            print u"Poste non maîtrisé ou non joué :", jj.nom, postes, "; Malus =", malus
            for car in jj.caracs.keys():
                jj.caracs[car] = jj.caracs[car] - malus
        
    """
    Debut calcul des caracs de la compo
    """
    for carac in comp.caracs_old.keys():
        car = correspondance[carac]
        if carac in ['TO_off', 'TO_def']:
            SA_pcp1 = comp.roles['SA_pcp1']
            SA_pcp2 = comp.roles['SA_pcp2']
            SA_scd = comp.roles['SA_scd']
            SA_remp1 = comp.roles['SA_remp1']
            SA_remp2 = comp.roles['SA_remp2']
            comp.caracs_old[carac] = 4*(max(0, SA_pcp1.caracs['TO']-5) + max(0, SA_pcp2.caracs['TO']-5)) + 3.5*max(0, SA_scd.caracs['TO'] -5) + 2*(max(0, SA_remp1.caracs['TO']-5) + max(0, SA_remp2.caracs['TO']-5))
        else:
            for n in sorted(comp.joueurs.keys(), key=lambda kk: int(kk[1:])):
                jj = comp.joueurs[n]

                if not n in dd[carac].keys():
                    dd[carac][n] = 0

                if carac in ['OplusAV', 'OplusAR', 'OmoinsAV', 'OmoinsAR', 'M']:
                    comp.caracs_old[carac] = comp.caracs_old[carac] + dd[carac][n] * jj.caracs[car] / 2.
                elif carac == 'JP':
                    comp.caracs_old[carac] = comp.caracs_old[carac] + dd[carac][n] * jj.caracs['P'] / 2.
                    comp.caracs_old[carac] = comp.caracs_old[carac] + dd[carac][n] * jj.caracs[car] / 2.
                else:
                    comp.caracs_old[carac] = comp.caracs_old[carac] + dd[carac][n] * jj.caracs[car] / 2.

    """
    Cas particuliers (TA, RJC, RJL...)
    """
    comp.caracs_old['JP'] = comp.caracs_old['JP'] + comp.roles['RJL'].caracs['P'] / 2. + comp.roles['RJC'].caracs['JP'] / 2.
    comp.caracs_old['ME'] = comp.caracs_old['ME'] + comp.joueurs['n2'].caracs['TA'] / 2. + comp.joueurs['n16'].caracs['TA']*.5 / 2.
    comp.caracs_old['E'] = comp.caracs_old['E'] + comp.roles['cap'].caracs['E'] / 2.
    comp.caracs_old['TO_off'] = comp.caracs_old['TO_off'] + comp.joueurs['n2'].caracs['TA'] / 2. + comp.joueurs['n16'].caracs['TA']*.5 / 2.

    #comp.fatigue_prise_en_compte = True

def faire_compo(equipe, c_ou_s, nom=None):
    comp = compo()
    if nom is None:
        nom_comp = raw_input('Nom compo ? ')
    else:
        nom_comp = nom

    if c_ou_s == 'c':
        for n in sorted(comp.joueurs.keys(), key = lambda st: int(st.split("n")[1])):
            nom = raw_input(n + ' ? ')
            comp.joueurs[n] = equipe.get_joueur_from_nom(nom)
    elif c_ou_s == 's':
        joueurs = s.get_joueurs_all(equipe.nom)
        for n in sorted(comp.joueurs.keys(), key = lambda st: int(st.split("n")[1])):
            nom = raw_input(n + ' ? ')
            comp.joueurs[n] = s.get_joueur_from_nom_arm(nom, equipe.nom, joueurs=joueurs)
    else:
        raise ValueError("c_ou_s doit etre 'c' pour club ; 's' pour selection !")

    #manque la vérification du poste
    comp.sauvegarder(nom_comp, equipe.nom, c_ou_s)
    
    set_roles(comp, equipe, c_ou_s)
    comp.sauvegarder(nom_comp, equipe.nom, c_ou_s)

    set_remplacements(comp, equipe)
    comp.sauvegarder(nom_comp, equipe.nom, c_ou_s)

    set_caracs_compo(comp, equipe)
    comp.sauvegarder(nom_comp, equipe.nom, c_ou_s)

    comp.calc_totaux()
    comp.sauvegarder(nom_comp, equipe.nom, c_ou_s)

    set_caracs_old_compo(comp, equipe)
    comp.sauvegarder(nom_comp, equipe.nom, c_ou_s)

    comp.calc_totaux_old()
    comp.sauvegarder(nom_comp, equipe.nom, c_ou_s)

    #manque la fatigue

    print 'caracs old'
    print comp.caracs_old
    print 'totaux old'
    print comp.totaux_old
    
    return comp

def faire_compo_from_defaut(equipe, c_ou_s, nom_compo):
    comp = equipe.compo_defaut
    comp.nom = nom_compo
    
    f = None
    if c_ou_s == 'c':
        f = equipe.get_joueur_from_nom
    elif c_ou_s == 's':
        joueurs = s.get_joueurs_all(equipe.nom)
        f = s.get_joueur_from_nom_arm(arm=equipe.nom, joueurs=joueurs)
    
    b = raw_input("Changer joueur ? (num ou n) ")

    while not b in ['', 'n']:
        num = b
        nom = raw_input("Nom nouveau joueur ? ")
        j = f(nom)
        comp.joueurs[num] = j
        b = raw_input("Changer joueur ? (num ou n) ")
    d = comp.get_joueurs_noms()
    noms = d.values()
    for n in noms:
        count = noms.count(n)
        if count > 1:
            print ('/!\ ' + n + ' est present ' + str(count) + ' fois dans joueurs')

    d = comp.get_joueurs_noms()
    noms = d.values()
    print 'compo :'
    for k, v in sorted(d.items(), key = lambda (k,v): int(k.split("n")[1])):
        print k.split("n")[1], v

    print 'anciens remplacements :'
    for k, v in sorted(comp.remplacements.items(), key = lambda (k,v): int(k.split("n")[1])):
        print k.split("n")[1], '->', v.split("n")[1]
                       
    bb = raw_input("Changer remplacement ? y/n ")
    while bb == 'y':
        remplacant = raw_input("Remplacant ? (forme n1) ")
        remplace = raw_input("Remplace ? (forme n1) ")
        comp.remplacements[remplacant] = remplace
        bb = raw_input("Changer remplacement ? y/n ")
    ll = comp.get_remplacements_noms()
    for n in ll:
        if ll.count(n) > 1:
            print ('/!\ ' + n + ' est present deux fois dans remplacements')

    for role in sorted(comp.roles.keys()):
        if not comp.roles[role].nom in noms:
            nom = raw_input("Nom nouveau joueur " + role + " ? ")
            j = f(nom)
            comp.roles[role] = j              

    bbb = raw_input("Changer role ? y/n ")
    while bbb == 'y':
        role = raw_input("Role ? ")
        nom = raw_input("Nom nouveau joueur ? ")
        j = f(nom)
        comp.roles[role] = j
        bbb = raw_input("Changer role ? y/n ")

    set_caracs_compo(comp, equipe)
    comp.calc_totaux()
        
    set_caracs_old_compo(comp, equipe)
    comp.calc_totaux_old()

#    print comp.caracs, comp.totaux
    print comp.caracs_old
    print comp.totaux_old

    return comp

def changer_un_joueur(jj, comp, num, club):
    if jj in comp.joueurs.values():
        print jj.nom + ' est deja dans la compo !'
    if comp.joueurs[num] in comp.roles.values():
        print comp.joueurs[num].nom + ' avait un role !'
    if jj.blessure > 0:
        print jj.nom + ' est blesse pour encore ' + str(jj.blessure) + ' matches !'
    comp.joueurs[num] = jj

    #set_caracs_compo(comp, club)
    set_caracs_old_compo(comp, club)

    #comp.calc_totaux()
    comp.calc_totaux_old()

    return comp
    
def ne_joue_pas(postes, jj):
    boo = True #vaudra True ssi le joueur n'est pas à son poste
    if len(postes) > 1:
        bools = []
        for poste in postes:
            if poste in ('C1', 'C2', 'CE'):
                bools.append(not('C1' in jj.postes or 'C2' in jj.postes or 'CE' in jj.postes))
            else:
                bools.append(not poste in jj.postes)
        for bb in bools:
            boo = boo and bb
    else:
        poste = postes[0]
        if poste in ('C1', 'C2', 'CE'):
            boo = (not('C1' in jj.postes or 'C2' in jj.postes or 'CE' in jj.postes))
        else:
            boo = (not poste in jj.postes)
    return boo

def arrondi_quart(n):
        return round(n * 4) / 4.
