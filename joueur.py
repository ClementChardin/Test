# -*- coding: cp1252 -*-
import numpy as np
from matplotlib import pyplot as plt
from date import *

postes = ['PI', 'TA', 'DL', 'TL', 'N8', 'DM', 'DO', 'C1', 'C2', 'AI', 'AR']

ordre_caracs_joueurs= dict(M=1,
                            PL=2,
                            PA=3,
                            JP=4,
                            TB=5,
                            P=6,
                            RP1=7,
                            RP2=8,
                            RP_tot=9,
                            ME=10,
                            R=11,
                            TO=12,
                            TA=13,
                            A=14,
                            E=15)

caracs_avant = ['M', 'PL', 'PA', 'RP1', 'RP2', 'ME', 'R', 'TO', 'TA', 'A', 'E']
caracs_arriere = ['M', 'PL', 'PA', 'JP', 'P', 'RP1', 'RP2', 'R', 'A', 'E']

def coeffs_EV_poste(poste):
    d = dict()
    if poste == 'PI':
        d["M"] = .5
        d["PL"] = 2
        d["PA"] = .5
        d["JP"] = 0
        d["TB"] = 0
        d["P"] = 0
        d["RP_tot"] = 2
        d["ME"] = 2.5
        d["R"] = 3
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 1
        d["E"] = 2
        
    if poste == 'TA':
        d["M"] = .5
        d["PL"] = 2
        d["PA"] = .5
        d["JP"] = 0
        d["TB"] = 0
        d["P"] = 0
        d["RP_tot"] = 2
        d["ME"] = 1.5
        d["R"] = 3
        d["TO"] = 0
        d["TA"] = 2
        d["A"] = 1
        d["E"] = 2
        
    if poste == 'DL':
        d["M"] = .5
        d["PL"] = 2
        d["PA"] = .5
        d["JP"] = 0
        d["TB"] = 0
        d["P"] = 0
        d["RP_tot"] = 2
        d["ME"] = 2
        d["R"] = 3.5
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 1
        d["E"] = 2

    if poste == 'TL':
        d["M"] = 1
        d["PL"] = 3
        d["PA"] = .5
        d["JP"] = 0
        d["TB"] = 0
        d["P"] = 0
        d["RP_tot"] = 2
        d["ME"] = 1
        d["R"] = 4.5
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 1.5
        d["E"] = 2

    if poste == 'N8':
        d["M"] = .5
        d["PL"] = 2.5
        d["PA"] = .5
        d["JP"] = 0
        d["TB"] = 0
        d["P"] = 0
        d["RP_tot"] = 2.5
        d["ME"] = 1.5
        d["R"] = 3.5
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 1.5
        d["E"] = 2

    if poste == 'DM':
        d["M"] = 1.5
        d["PL"] = 1.5
        d["PA"] = 3
        d["JP"] = 1.5
        d["TB"] = 0
        d["P"] = 1.5
        d["RP_tot"] = 1.5
        d["ME"] = 0
        d["R"] = .5
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 1.5
        d["E"] = 2

    if poste == 'DO':
        d["M"] = 1.5
        d["PL"] = 2
        d["PA"] = 2.5
        d["JP"] = 2.5
        d["TB"] = 0
        d["P"] = 2.5
        d["RP_tot"] = 1.5
        d["ME"] = 0
        d["R"] = .5
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 1.5
        d["E"] = 2

    if poste == 'C1':
        d["M"] = 1.5
        d["PL"] = 2.5
        d["PA"] = 2
        d["JP"] = 1
        d["TB"] = 0
        d["P"] = 1
        d["RP_tot"] = 2
        d["ME"] = 0
        d["R"] = 1
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 2
        d["E"] = 2

    if poste == 'C2':
        d["M"] = 1.5
        d["PL"] = 2.5
        d["PA"] = 2
        d["JP"] = .5
        d["TB"] = 0
        d["P"] = .5
        d["RP_tot"] = 2.5
        d["ME"] = 0
        d["R"] = 1
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 2
        d["E"] = 2

    if poste == 'AI':
        d["M"] = 2.5
        d["PL"] = 2
        d["PA"] = 1.5
        d["JP"] = .5
        d["TB"] = 0
        d["P"] = .5
        d["RP_tot"] = 3
        d["ME"] = 0
        d["R"] = .5
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 3
        d["E"] = 2

    if poste == 'AR':
        d["M"] = 2
        d["PL"] = 3
        d["PA"] = 1.5
        d["JP"] = 1
        d["TB"] = 0
        d["P"] = 1
        d["RP_tot"] = 2.5
        d["ME"] = 0
        d["R"] = .5
        d["TO"] = 0
        d["TA"] = 0
        d["A"] = 3
        d["E"] = 2

    return d

def est_un_avant(joueur):
    postes = joueur.postes
    if ("PI" in postes) or ("TA" in postes) or ("DL" in postes) or \
       ("TL" in postes) or ("N8" in postes):
        return True
    else:
        return False

def est_un_arriere(joueur):
    postes = joueur.postes
    if ("DM" in postes) or ("DO" in postes) or ("C1" in postes) or \
       ("C2" in postes) or ("CE" in postes) or ("AI" in postes) or \
       ("AR" in postes):
       return True
    else:
        return False

class joueur:
    
    def __init__(self):
        self.nom = "nom"
        self.caracs_sans_fatigue = dict(M = 0,
                                        PL = 0,
                                        PA = 0,
                                        JP = 0,
                                        TB = 0,
                                        P = 0,
                                        RP1 = 0,
                                        RP2 = 0,
                                        RP_tot=0,
                                        ME = 0,
                                        R = 0,
                                        TO = 0,
                                        TA = 0,
                                        A = 0,
                                        E = 0)
        self.caracs = self.caracs_sans_fatigue
        self.postes = ("dummy", "", "", "")
        #la valeur dummy sert a avoir poste 1 = poste[1], etc
        
        self.RG = rang_new('')
        self.EV = 0.
        self.C = 0
        self.anciens_clubs = ""
        self.changements_postes = ''
        
        self.ARM = ""
        
        self.VAL = 0
        self.MS = 0
        self.RG_max = rang_new("")
        self.D = 0
        self.club = ""
        self.fatigue = 0

        self.blessure = 0

        self.veut_partir = False
        self.MS_probleme = False

        """
        MJi = matches joues poste i cette saison
        MJTi = matches joues poste i depuis creation
        CT = club tit
        CR = club remp
        ST = sel tit
        SR = sel remp

        XP = experience aux postes : CT + 0.5*CR + 2*(ST + 0.5*SR)
        """
        self.MJ1 = dict(CT=0,
                        CR=0,
                        ST=0,
                        SR=0)

        self.MJ2 = dict(CT=0,
                        CR=0,
                        ST=0,
                        SR=0)

        self.MJ3 = dict(CT=0,
                        CR=0,
                        ST=0,
                        SR=0)

        self.MJ1_total = dict(CT=0,
                        CR=0,
                        ST=0,
                        SR=0)

        self.MJ2_total = dict(CT=0,
                        CR=0,
                        ST=0,
                        SR=0)

        self.MJ3_total = dict(CT=0,
                        CR=0,
                        ST=0,
                        SR=0)

        #Pour l'évolution
        self.nouveau_bonus_evolution = True
        self.experience_saison = 0
        self.experience_total = 0
        self.residu_experience = 0
        self.num_dernier_bonus = 0

        #Résultats de l'évolution
        self.bonus = 0
        self.carte_evolution = {'valeur':0, 'couleur':1, 'r_nr':'n'}
        self.evolution = 0

        #Cette saison
        self.essais_saison = 0
        self.transformations_saison = 0
        self.penalites_saison = 0
        self.drops_saison = 0
        
        self.transformation_ratees_saison = 0
        self.penalite_ratees_saison = 0
        self.drop_rates_saison = 0
        
        self.jaunes_saison = 0
        self.rouges_saison = 0

        self.blessures_saison = 0

        #Depuis la creation
        self.essais_total = 0
        self.transformations_total = 0
        self.penalites_total = 0
        self.drops_total = 0
        
        self.transformation_ratees_total = 0
        self.penalite_ratees_total = 0
        self.drop_ratees_total = 0
        
        self.jaunes_total = 0
        self.rouges_total = 0

        self.blessures_total = 0

        self.jj_passe = {}
        self.retraite = False

    def set_EV(self):
        EV = calc_EV(self, self.postes[1], False) 
        self.EV = EV

    def show(self):
        print self.nom
        for car in sorted(ordre_caracs_joueurs.keys(),
                          key=lambda k:ordre_caracs_joueurs[k]):
            print car, self.caracs_sans_fatigue[car]
        print self.postes
        print 'RG : ' + self.RG.rang
        print 'EV : ' + str(self.EV)
        print 'C : ' + str(self.C) 
        print 'ARM : ' + self.ARM        
        print 'VAL : ' + str(self.VAL)
        print 'MS : ' + str(self.MS)
        print 'RG_max : ' + self.RG_max.rang
        print 'D : ' + str(self.D)

    def est_jeune(self, dat=None):
        dat = lire_date() if dat is None else dat
        return self.RG < self.RG_max or ((dat - self.C) < 2)

    def en_declin(self):
        return date >= self.D

    def joue_centre(self):
        res = False
        for p in ['C1', 'C2', 'CE']:
            if p in self.postes:
                res = True
                break
        return res

    def diagramme_etoile(self,
                         N_points_cercles=100,
                         texte=True,
                         label_TO=None,
                         label_TA=None,
                         label_TB=None,
                         force_av_ar=None,
                         ax=None):
        if ax is None:
            ax = plt.subplot(111)
        caracs_a_ploter = []
        noms = []
        
        if est_un_avant(self):
            poste = 'AV'
        elif est_un_arriere(self):
            poste = 'AR'
            label_TB = True

        if force_av_ar == 'AV':
            poste = 'AV'
        elif force_av_ar == 'AR':
            poste = 'AR'

        if poste == 'AV':
            jeu_courant = (self.caracs_sans_fatigue['M'] + \
                           self.caracs_sans_fatigue['PA'] + \
                           self.caracs_sans_fatigue['A'])/3
            caracs_a_ploter.append(jeu_courant)
            noms.append('jeu courant')
            
            defense = self.caracs_sans_fatigue['PL']
            caracs_a_ploter.append(defense)
            noms.append('defense')
            
            puissance = self.caracs_sans_fatigue['RP_tot']
            caracs_a_ploter.append(puissance)
            noms.append('puissance')

            melee = self.caracs_sans_fatigue['ME']
            caracs_a_ploter.append(melee)
            noms.append('melee')

            regroupements = self.caracs_sans_fatigue['R']
            caracs_a_ploter.append(regroupements)
            noms.append('regroupements')

            if label_TO == None and (self.caracs_sans_fatigue['TO'] >= self.EV \
                                     or self.caracs_sans_fatigue['TO'] >= 9):
                touche = self.caracs_sans_fatigue['TO']
                caracs_a_ploter.append(touche)
                noms.append('touche')
            elif label_TO == True:
                touche = self.caracs_sans_fatigue['TO']
                caracs_a_ploter.append(touche)
                noms.append('touche')
            elif label_TO == False:
                pass

            if label_TA == None and 'TA' in self.postes:
                talonnage = self.caracs_sans_fatigue['TA']
                caracs_a_ploter.append(talonnage)
                noms.append('talonnage')
            elif label_TA == True:
                talonnage = self.caracs_sans_fatigue['TA']
                caracs_a_ploter.append(talonnage)
                noms.append('talonnage')
            elif label_TA == False:
                pass

        elif poste == 'AR':
            attaque = (self.caracs_sans_fatigue['M'] + self.caracs_sans_fatigue['RP_tot'])/2
            caracs_a_ploter.append(attaque)
            noms.append('attaque')

            defense = self.caracs_sans_fatigue['PL']
            caracs_a_ploter.append(defense)
            noms.append('defense')
            
            technique = (self.caracs_sans_fatigue['PA'] + self.caracs_sans_fatigue['A'])/2
            caracs_a_ploter.append(technique)
            noms.append('technique')
            
            jeu_pied = (self.caracs_sans_fatigue['JP'] + self.caracs_sans_fatigue['P'])/2
            caracs_a_ploter.append(jeu_pied)
            noms.append('jeu au pied')
            
            regroupements = self.caracs_sans_fatigue['R']
            caracs_a_ploter.append(regroupements)
            noms.append('regroupements')

        esprit = self.caracs_sans_fatigue['E']
        caracs_a_ploter.append(esprit)
        noms.append('esprit')

        if label_TB == None and (self.caracs_sans_fatigue['TB'] >= self.EV \
                                 or self.caracs_sans_fatigue['TB'] >=9):
            tir_but = self.caracs_sans_fatigue['TB']
            caracs_a_ploter.append(tir_but)
            noms.append('tir au but')
        elif label_TB == True:
            tir_but = self.caracs_sans_fatigue['TB']
            caracs_a_ploter.append(tir_but)
            noms.append('tir au but')
        elif label_TB == False:
            pass
            
        car_max = max(caracs_a_ploter)
        xx = []
        yy = []
        for i,c in enumerate(caracs_a_ploter):
            angle = 2*i*np.pi/len(caracs_a_ploter)
            x = c*np.cos(angle)
            xx.append(x)
            y = c*np.sin(angle)
            yy.append(y)
            ax.plot([0, (car_max+1)*np.cos(angle)],[0, (car_max+1)*np.sin(angle)], linestyle='--', color='k')
            if texte:
                ax.text((car_max+2)*np.cos(angle), (car_max+2)*np.sin(angle), noms[i])

        xx.append(caracs_a_ploter[0])
        yy.append(0)

        ax.plot(xx, yy, label=self.nom) #
        ax.legend()

        for i in range(1,car_max+2):
            cercle_x = []
            cercle_y = []
            for k in range(N_points_cercles+1):
                cercle_x.append(i*np.cos(2*k*np.pi/N_points_cercles))
                cercle_y.append(i*np.sin(2*k*np.pi/N_points_cercles))
            if i%5 ==0:
                ax.plot(cercle_x, cercle_y, color='k')
            else:
                ax.plot(cercle_x, cercle_y, color='k', linestyle='--')
        
#        plt.axhline(0, linestyle='--', color='k')
#        plt.axvline(0, linestyle='--', color='k')
        
def creer_joueur2():
    jj = joueur()

    st = raw_input("Entrer la ligne du joueur en separant les donnees pas un espace /!\ 'anciens clubs' ")
    ll = st.split(" ")

    jj.nom = ll[0]

    jj.caracs_sans_fatigue["M"] = int(ll[1])
    jj.caracs_sans_fatigue["PL"] = int(ll[2])
    jj.caracs_sans_fatigue["PA"] = int(ll[3])
    jj.caracs_sans_fatigue["JP"] = int(ll[4])
    jj.caracs_sans_fatigue["TB"] = int(ll[5])
    jj.caracs_sans_fatigue["P"] = int(ll[6])
    jj.caracs_sans_fatigue["RP1"] = int(ll[7])
    jj.caracs_sans_fatigue["RP2"] = int(ll[8])
    RPmin = min(jj.caracs_sans_fatigue["RP1"], jj.caracs_sans_fatigue["RP2"])
    RPmax = max(jj.caracs_sans_fatigue["RP1"], jj.caracs_sans_fatigue["RP2"])
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
    jj.caracs_sans_fatigue["RP_tot"] = RPmax + max(m, RPmin - (RPmax - N))
    #jj.caracs_sans_fatigue["RP_tot"] = jj.caracs_sans_fatigue["RP1"] + max(0, jj.caracs_sans_fatigue["RP2"]-7)
    jj.caracs_sans_fatigue["ME"] = int(ll[9])
    jj.caracs_sans_fatigue["R"] = int(ll[10])
    jj.caracs_sans_fatigue["TO"] = int(ll[11])
    jj.caracs_sans_fatigue["TA"] = int(ll[12])
    jj.caracs_sans_fatigue["A"] = int(ll[13])
    jj.caracs_sans_fatigue["E"] = int(ll[14])

    jj.caracs = dict()

    p1 = ll[15]
    p2 = "" if ll[16] == "-" else ll[16]
    p3 = "" if ll[17] == "-" else ll[17]
    jj.postes = ('dummy', p1, p2,p3)

    jj.RG = rang_new(ll[18])
    jj.C = int(ll[19])
    jj.anciens_clubs = "" if ll[20] == "-" else ll[20]

    jj.VAL = int(ll[21])
    jj.MS = int(ll[22])
    jj.ARM = ll[23]

    jj.essais_total = 0 if ll[24] == "-" else int(ll[24])
    jj.penalites_total = 0 if ll[25] == "-" else int(ll[25])
    jj.drops_total = 0 if ll[26] == "-" else int(ll[26])
    jj.transformations_total = 0 if ll[27] == "-" else int(ll[27])

    jj.RG_max = rang_new(ll[28])
    jj.D = int(ll[29])

    jj.set_EV()
    print jj.nom, jj.EV
    return jj

def creer_joueur(nom=None):
    #jj.caracs_sans_fatigue["M"] = jj[1]
    j = joueur()
    if nom==None:
        j.nom = raw_input("nom?")
    else:
        j.nom = nom
    
    j.caracs_sans_fatigue["M"] = int(raw_input("M ?"))
    j.caracs_sans_fatigue["PL"] = int(raw_input("PL ?"))
    j.caracs_sans_fatigue["PA"] = int(raw_input("PA ?"))
    j.caracs_sans_fatigue["JP"] = int(raw_input("JP ?"))
    j.caracs_sans_fatigue["TB"] = int(raw_input("TB ?"))
    j.caracs_sans_fatigue["P"] = int(raw_input("P ?"))
    j.caracs_sans_fatigue["RP1"] = int(raw_input("RP1 ?"))
    j.caracs_sans_fatigue["RP2"] = int(raw_input("RP2 ?"))
    j.caracs_sans_fatigue["ME"] = int(raw_input("ME ?"))
    j.caracs_sans_fatigue["R"] = int(raw_input("R ?"))
    j.caracs_sans_fatigue["TO"] = int(raw_input("TO ?"))
    j.caracs_sans_fatigue["TA"] = int(raw_input("TA ?"))
    j.caracs_sans_fatigue["A"] = int(raw_input("A ?"))
    j.caracs_sans_fatigue["E"] = int(raw_input("E ?"))

    j.caracs = j.caracs_sans_fatigue
    
    j.postes[1] = raw_input("poste 1 ?")
    j.postes[2] = raw_input("poste 2 ?")
    j.postes[3] = raw_input("poste 3 ?")
    
    j.RG = rang_new(raw_input("rang ?"))
    j.set_EV()
    j.C = int(raw_input("C ?"))
    j.anciens_clubs = raw_input("anciens clubs ?")

    j.VAL = int(raw_input("VAL ?"))
    j.MS = int(raw_input("MS ?"))
    j.ARM = raw_input("armee ?")
    
    j.essais_total = int(raw_input("essais ? "))
    j.penalites_total = int(raw_input("penalites ? "))
    j.drops_total = int(raw_input("drops ? "))
    j.transformations_total = int(raw_input("transformations ? "))
    j.RG_max = rang_new(raw_input("rang max ?"))
    j.D = int(raw_input("D ?"))
    j.fatigue = 0
    print j.EV
    return j

def get_caracs(jj, fatigue=True):
    if fatigue:
        dd = dict()
        if jj.fatigue >= 15:
            for car in jj.caracs_sans_fatigue.keys():
                dd[car] = jj.caracs_sans_fatigue[car] -  1
        elif jj.fatigue >= 8:
            for car in jj.caracs_sans_fatigue.keys():
                if car in ["PL", "A", "R"]:
                    dd[car] = jj.caracs_sans_fatigue[car] -  1
                else:
                    dd[car] = jj.caracs_sans_fatigue[car]
        else:
            for car in jj.caracs_sans_fatigue.keys():
                dd[car] = jj.caracs_sans_fatigue[car]
        return dd
    else:
        return jj.caracs_sans_fatigue

def calc_EV(joueur, poste, fatigue=True, caracs=None):
    dd = get_caracs(joueur, fatigue) if caracs is None else caracs

    if poste == '':
        return 0

    elif poste in ('C1', 'C2', 'CE'):
        if (not ("C1" in joueur.postes)) and (not ("C2" in joueur.postes)) \
           and (not ("CE" in joueur.postes)):
            print "/!\ " + joueur.nom + " ne joue pas " + poste
        else:
            coeffs = coeffs_EV_poste(poste)
            temp = 0
            tot = 0
            #dd["RP_tot"] = max(dd["RP1"], dd["RP2"]) + max(0, min(dd["RP1"], dd["RP2"])-7)
            RPmin = min(dd["RP1"], dd["RP2"])
            RPmax = max(dd["RP1"], dd["RP2"])
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
            dd["RP_tot"] = RPmax + max(m, RPmin - (RPmax - N))

            for i in dd.keys():
                if i != "RP1" and i != "RP2":
                    temp = temp + coeffs[i] * dd[i]
                    tot = tot + coeffs[i]

            EV = temp / tot
            
            if dd["TB"] > EV:
                temp = temp + dd["TB"]
                tot = tot + 1
                EV = temp / tot

            if dd["TO"] > EV and est_un_avant(joueur) and poste != "TA":
                temp = temp + dd["TO"]*3.5
                tot = tot + 3.5
                EV = temp / tot

            if dd["TA"] > EV and "TA" in [joueur.postes[2],
                                          joueur.postes[3]]:
                temp = temp + dd["TA"]
                tot = tot + 1
                EV = temp / tot

            return EV

    elif not (poste in joueur.postes):
        print "/!\ " + joueur.nom + " ne joue pas " + poste
    else:
        coeffs = coeffs_EV_poste(poste)
        temp = 0
        tot = 0
        #dd["RP_tot"] = max(dd["RP1"], dd["RP2"]) + max(0, min(dd["RP1"], dd["RP2"])-7)
        RPmin = min(dd["RP1"], dd["RP2"])
        RPmax = max(dd["RP1"], dd["RP2"])
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
        dd["RP_tot"] = RPmax + max(m, RPmin - (RPmax - N))

        for car in dd.keys():
            if car != "RP1" and car != "RP2":
                temp = temp + coeffs[car] * dd[car]
                tot = tot + coeffs[car]

        EV = temp / tot
        
        if dd["TB"] > EV:
            temp = temp + dd["TB"]
            tot = tot + 1
            EV = temp / tot

        if dd["TO"] > EV and est_un_avant(joueur) and poste != "TA":
            temp = temp + dd["TO"]*3.5
            tot = tot + 3.5
            EV = temp / tot

        if dd["TA"] > EV and "TA" in [joueur.postes[2],
                                      joueur.postes[3]]:
            temp = temp + dd["TA"]
            tot = tot + 1
            EV = temp / tot

        return EV

def changer_poste_joueur(jj, poste_new, dat=None):
    if not (poste_new in jj.postes or poste_new in ('C1', 'C2') and \
            'CE' in jj.postes):
        raise ValueError("""Mauvais postes :\n
                            postes possibles :""" + str(jj.postes) + \
                         "\nnouveau poste :" + poste_new)
    else:
        poste_old = 'CE' if jj.postes[1] in ('C1', 'C2') else jj.postes[1]
        if dat is None:
            dat = lire_date()
        idx = jj.postes.index('CE') if poste_new in ('C1', 'C2') \
              else jj.postes.index(poste_new)
        print jj.postes, poste_new, idx
        MJ_temp = jj.MJ1
        MJ_tot_temp = jj.MJ1_total

        tu = ('dummy', poste_new, poste_old, jj.postes[3]) if idx == 2 \
             else ('dummy', poste_new, jj.postes[2], poste_old)

        jj.MJ1 = getattr(jj, 'MJ'+str(idx))
        jj.MJ1_total = getattr(jj, 'MJ'+str(idx)+'_total')

        setattr(jj, 'MJ'+str(idx), MJ_temp)
        setattr(jj, 'MJ'+str(idx)+'_total', MJ_tot_temp)

        jj.postes = tu
        print jj.postes
        jj.EV = calc_EV(jj, poste_new, fatigue=False)

        if jj.changements_postes == '':
            jj.changements_postes = poste_old + ' -> ' + poste_new + ' : ' + str(dat)

def creer_joueur_vide():
    j = joueur()
    j.nom = ""
    """
    caracs_keys = ['M', 'PL', 'PA', 'JP', 'TB', 'P', 'RP1', 'RP2', 'RP_tot', 'ME', 'TO', 'TA', 'A', 'E']
    for key in caracs_keys:
        j.caracs[key] = 0
    j.M = 0
    j.PL = 0
    j.PA = 0
    j.JP = 0
    j.TB = 0
    j.P = 0
    j.RP1 = 0
    j.RP2 = 0
    j.RP_tot = 0
    j.ME = 0
    j.R = 0
    j.TO = 0
    j.TA = 0
    j.A = 0
    j.E = 0
    """
    j.poste1 = ""
    j.poste2 = ""
    j.poste3 = ""
    
    j.RG = rang_new("")
    j.EV = 0
    j.C = 0
    j.anciens_clubs = ""
    
    j.ARM = ""
    
    j.VAL = 0
    j.MS = 0
    j.RG_max = rang_new("")
    j.D = 0
    j.club = ""
    return j

class rang():
    def __init__(self, rg):
        self.rang = rg
        
        if rg in ['^', '<', '>']:
            self.type = 'base'
            self.type_nb = 1
        elif rg in ['^^', '<<']:
            self.type = 'special'
            self.type_nb = 2
        elif rg in ['^^^', '<<<']:
            self.type = 'rare'
            self.type_nb = 3
        elif rg in ['*', 'x']:
            self.type = 'heros'
            self.type_nb = 4
        elif rg in ['**', 'xx']:
            self.type = 'seigneur'
            self.type_nb = 5
        elif rg == '***':
            self.type = 'personnage'
            self.type_nb = 6

    def __lt__(self, other):
        return self.type_nb < other.type_nb

    def __le__(self, other):
        return self.type_nb <= other.type_nb

    def __gt__(self, other):
        return self.type_nb > other.type_nb

    def __ge__(self, other):
        return self.type_nb >= other.type_nb

    def __eq__(self, other):
        return self.type_nb == other.type_nb

class rang_new(object):
    def __init__(self, rg):
        self.rang = rg
        
        if rg in ['^', '<', '>']:
            self.type = 'base'
            self.type_nb = 1
        elif rg in ['^^', '<<']:
            self.type = 'special'
            self.type_nb = 2
        elif rg in ['^^^', '<<<']:
            self.type = 'rare'
            self.type_nb = 3
        elif rg in ['*', 'x']:
            self.type = 'heros'
            self.type_nb = 4
        elif rg in ['**', 'xx']:
            self.type = 'seigneur'
            self.type_nb = 5
        elif rg == '***':
            self.type = 'personnage'
            self.type_nb = 6

    def __lt__(self, other):
        return self.type_nb < other.type_nb

    def __le__(self, other):
        return self.type_nb <= other.type_nb

    def __gt__(self, other):
        return self.type_nb > other.type_nb

    def __ge__(self, other):
        return self.type_nb >= other.type_nb

    def __eq__(self, other):
        return self.type_nb == other.type_nb

def est_poste_centre(poste):
    if poste in ['C1', 'C2', 'CE']:
        return True
    else:
        return False
    
def get_club_11(jj):
    anciens_clubs = jj.anciens_clubs
    if anciens_clubs == '':
        return jj.club
    else:
        ll = anciens_clubs.split(';')
        st = ll[-1]
        if st.split(' ')[1] == '12':
            return st.split(' ')[0]
        else:
            return jj.club

def club_saison_prec(jj, dat=None):
    if dat is None:
        dat = lire_date()
    if jj.anciens_clubs == '':
        return jj.club
    else:
        trans = jj.anciens_clubs.split(';')[-1]
        datt = trans.split(' ')[1]
        return trans.split(' ')[0] if int(datt) == dat else jj.club
