# -*- coding: cp1252 -*-
import selection as s
import miscellaneous as misc
from miscellaneous_jouer_match import *
from math import ceil

class Tournoi():
    def __init__(self,
                 noms_equipes=None,
                 n_poules=1,
                 phases_finales=False,
                 calendrier=dict()):
        self.calendrier = calendrier
        #keys : j1, j2, etc

        self.noms_equipes = noms_equipes
        self.equipes = []
        for nom in noms_equipes:
            self.equipes.append(EquipeTournoi(nom))
        
        self.matches_joues = dict()
        for jour in self.calendrier.keys():
            self.matches_joues[jour] = []
        self.prochain_match = self.calendrier['j1'][0]

        self.n_poules = n_poules
        self.phases_finales = phases_finales

    def maj_prochain_match(self):
        for key in sorted(self.calendrier.keys(), key=lambda k: int(k.split('j')[1])):
            match = self.calendrier(key)
            if not match in self.matches_joues.values():
                self.prochain_match = match

    def jouer_prochain_match(self):
        mat = self.prochain_match
        mat.jouer()
        jour = mat.journee
        num = mat.num
        self.matches_joues["j"+str(jour)].append(mat)

        self.attribuer_pts_equipes(mat)
        
        try:
            self.prochain_match = self.calendrier["j"+str(jour)][num+1]
        except IndexError:
            self.prochain_match = self.calendrier["j"+str(jour+1)][0]

    def attribuer_pts_equipes(self, match):
        eq1 = self.equipe(match.eq1.nom)
        eq2 = self.equipe(match.eq2.nom)
        gagnant = match.gagnant
        perdant = match.perdant
        for eq in (eq1, eq2):
            eq.joues += 1
            if gagnant is None:
                eq.nuls += 1
                eq.points_pour += match.eq1.score
                eq.points_contre += match.eq1.score
                for eqq in (match.eq1, match.eq2):
                    if eq.nom == eqq.nom and eq.bonus_off:
                        eq.bonus_off += 1
            elif eq.nom == gagnant.nom:
                eq.gagnes += 1
                eq.points_pour += gagnant.score
                eq.points_contre += perdant.score
                if gagnant.bonus_off:
                    eq.bonus_off += 1
            elif eq.nom == perdant.nom:
                eq.perdus += 1
                eq.points_pour += perdant.score
                eq.points_contre += gagnant.score
                if perdant.bonus_off:
                    eq.bonus_off += 1
                if perdant.bonus_def:
                    eq.bonus_def += 1
                    
    def attribuer_stats_equipes(self, match):
        pass

    def print_classement(self):
        print 'nom', 'J', 'G', 'N', 'P', 'D', 'Pts', 'diff'
        for eq in sorted(self.equipes, key = lambda eq: -eq.points):
            print eq.nom, eq.joues, eq.gagnes, eq.nuls, eq.perdus, eq.difference, eq.points, eq.difference

    def equipe(self, nom):
        idx = self.noms_equipes.index(nom)
        return self.equipes[idx]

    @property
    def noms_equipes(self):
        return [eq.nom for eq in self.equipes]

class EquipeTournoi():
    def __init__(self, nom):
        self.nom = nom
        self.joues = 0
        self.gagnes = 0
        self.nuls = 0
        self.perdus = 0
        self.bonus_off = 0
        self.bonus_def = 0
        self.points_pour = 0
        self.points_contre = 0
        #self.points = 0
        self.essais = dict()
        self.transformations = dict()
        self.drops = dict()
        self.penalites = dict()

    @property
    def difference(self):
        return self.points_pour - self.points_contre
    
    @property
    def points(self):
        return 4* self.gagnes + 2* self.nuls + self.bonus_off + self.bonus_def
    
class Calendrier():
    def __init__(self, n_journees, n_equipes, tournoi):
        self.tournoi = tournoi
        self.calendrier = dict(j1 = [])
        for jj in range(n_journees):
            match = Match(raw_input("Nom equipe 1 ? "),
                          raw_input("Nom equipe 2 ? "))
            self.calendrier['j'+str(jj)].append(match)

class Match():
    def __init__(self,
                 nom_1,
                 nom_2,
                 comp1,
                 comp2,
                 type_tournoi=None,
                 terrain_neutre=False,
                 journee=1,
                 num=1,
                 c_ou_s='c'):
        self.c_ou_s = c_ou_s
        self.eq1 = EquipeMatch(nom_1, comp1, self, c_ou_s=self.c_ou_s)
        self.eq2 = EquipeMatch(nom_2, comp2, self, c_ou_s=self.c_ou_s)
        self.nom = nom_1 + '/' + nom_2
        self.type_tournoi = type_tournoi
        self.terrain_neutre = terrain_neutre
        self.joue = False
        if self.c_ou_s == 'c':
            self.clubs = None
        else:
            self.clubs = []
            for nom in s.noms_clubs:
                self.clubs.append(s.charger(nom, 'c'))
        """
        self.journee = journee
        self.num = num
        """

    def jouer_test(self, sauver=True):
        self.eq1.score = int(raw_input("Score equipe 1 ? "))
        self.eq2.score = int(raw_input("Score equipe 2 ? "))
        bo1 = raw_input("Bonus offensif pour " + self.eq1.nom + " ? y/[n] ")
        self.eq1.bonus_off = True if bo1=='y' else False
        bo2 = raw_input("Bonus offensif pour " + self.eq2.nom + " ? y/[n] ")
        self.eq2.bonus_off = True if bo2=='y' else False

        self.gagnant, self.perdant = (self.eq1, self.eq2) if self.eq1.score > self.eq2.score \
                                     else (self.eq2, self.eq1) if self.eq2.score > self.eq1.score \
                                     else (None, None)
        if not self.perdant is None:
            bd = raw_input("Bonus defensif pour " + self.perdant.nom + " ? y/[n] ")
            self.perdant.bonus_def = True if bd == "y" else False

    def jouer(self,
              sauver=True,
              phase_finale=False,
              prolongation=False):
        #print sauver
        """
        Si prolongation, on commence par re calculer les caracs et totaux des
        compos avec les nouvelles fatigues
        """
        if prolongation:
            s.set_caracs_old_compo(self.eq1.comp, self.eq1.equipe, fatigue=True)
            self.eq1.comp.calc_totaux_old()
            s.set_caracs_old_compo(self.eq2.comp, self.eq2.equipe, fatigue=True)
            self.eq2.comp.calc_totaux_old()

        """
        Evenements du match
        """
        evs1 = attribuer_evenements(prolongation)
        evs2 = attribuer_evenements(prolongation)
        evs_tot1 = 0
        evs_tot2 = 0
        for ev in evs1:
            if ev == "blessure":
                jouer_blessure(self.eq1, sauver, clubs=self.clubs, c_ou_s=self.c_ou_s)
            elif ev in ("jaune", "rouge", "jocker"):
                evs_tot1 += jouer_evenement_sauf_blessure(ev, self.eq1, sauver=sauver, clubs=self.clubs, c_ou_s=self.c_ou_s, prolongation=prolongation)
            else:
                raise ValueError("Evenement " + str(ev) + " non valide !")
        for ev in evs2:
            if ev == "blessure":
                jouer_blessure(self.eq2, sauver, clubs=self.clubs, c_ou_s=self.c_ou_s)
            elif ev in ("jaune", "rouge", "jocker"):
                evs_tot2 += jouer_evenement_sauf_blessure(ev, self.eq2, sauver=sauver, clubs=self.clubs, c_ou_s=self.c_ou_s, prolongation=prolongation)
            else:
                raise ValueError("Evenement " + str(ev) + " non valide !")
        
        """
        On determine le nombre de temps forts pour chaque equipe
        """
        l1 = [misc.tirer_carte()]*3
        l2 = [misc.tirer_carte()]*3
        if self.terrain_neutre:
            bonus_domicile = 0
        else:
            bonus_domicile = 7 + misc.d6_plus()

        print self.eq1.nom, ceil(self.eq1.comp.totaux_old['T1']) + l1[0]["valeur"], \
              ceil(self.eq1.comp.totaux_old['T2']) + l1[1]["valeur"], \
              ceil(self.eq1.comp.totaux_old['T3']) + l1[2]["valeur"], \
              evs_tot1, bonus_domicile
        print self.eq2.nom, ceil(self.eq2.comp.totaux_old['T1']) + l2[0]["valeur"], \
              ceil(self.eq2.comp.totaux_old['T2']) + l2[1]["valeur"], \
              ceil(self.eq2.comp.totaux_old['T3']) + l2[2]["valeur"], \
              evs_tot2

        tot1 = ceil(self.eq1.comp.totaux_old['T1']) + l1[0]["valeur"] + \
               ceil(self.eq1.comp.totaux_old['T2']) + l1[1]["valeur"] + \
               ceil(self.eq1.comp.totaux_old['T3']) + l1[2]["valeur"] + \
               evs_tot1 + bonus_domicile
        tot2 = ceil(self.eq2.comp.totaux_old['T1']) + l2[0]["valeur"] + \
               ceil(self.eq2.comp.totaux_old['T2']) + l2[1]["valeur"] + \
               ceil(self.eq2.comp.totaux_old['T3']) + l2[2]["valeur"] + \
               evs_tot2

        res1 = tot1 - tot2
        res2 = tot2 - tot1

        res_egal_0 = True if res1 == 0 else False

        n1 = int(n_tps_forts(res1, prolongation))
        n2 = int(n_tps_forts(res2, prolongation))

        print self.eq1.nom, "tot", tot1, "tps forts", n1
        print self.eq2.nom, "tot", tot2, "tps forts", n2
        print "resultat 1", res1, "resultat 2", res2

        """
        On identifie les temps forts - la fonction auxiliaire renvoie une liste
        de tuples (type, zone, av ou ar, malus bonus transfo ou test mouvement)
        """

        cartes1 = [misc.tirer_carte()]*n1
        cartes2 = [misc.tirer_carte()]*n2
        
        tps_forts1 = []
        tps_forts2 = []
        for carte in cartes1:
            tps_forts1 += tps_fort(carte)
        for carte in cartes2:
            tps_forts2 += tps_fort(carte)

        """
        On joue les tps forts
        """
        for tt in tps_forts1:
            jouer_tps_fort(self.eq1, self.eq2, tt, sauver=sauver, clubs=self.clubs, c_ou_s=self.c_ou_s)
        for tt in tps_forts2:
            jouer_tps_fort(self.eq2, self.eq1, tt, sauver=sauver, clubs=self.clubs, c_ou_s=self.c_ou_s)

        """
        On attribue gagnant et perdant
        On fait jouer les prolongations si besoin
        """
        self.declarer_gagnant_perdant()
        if phase_finale and self.gagnant is None:
            self.jouer(sauver, phase_finale=True, prolongation=True)

        """
        On attribue la fatigue
        on fait evoluer les blessures
        et on maj le classement
        """
        if sauver:
            res = attribuer_fatigue(self.eq1, self.c_ou_s, self.clubs, prolongation)
            if not res == 0:
                self.clubs = merge_clubs(self.clubs, res)

            res = attribuer_fatigue(self.eq2, self.c_ou_s, self.clubs, prolongation)
            if not res == 0:
                self.clubs = merge_clubs(self.clubs, res)

            if not prolongation:
                res = attribuer_matches(self.eq1, self.c_ou_s, self.clubs)
                if not res == 0:
                    self.clubs = merge_clubs(self.clubs, res)

                res = attribuer_matches(self.eq2, self.c_ou_s, self.clubs)
                if not res == 0:
                    self.clubs = merge_clubs(self.clubs, res)

                res = evoluer_blessures(self.eq1, self.c_ou_s, self.clubs)
                if not res == 0:
                    self.clubs = merge_clubs(self.clubs, res)

                res = evoluer_blessures(self.eq2, self.c_ou_s, self.clubs)
                if not res == 0:
                    self.clubs = merge_clubs(self.clubs, res)

                if self.c_ou_s == 's':
                    for cc in self.clubs:
                        cc.sauvegarder()

                if ((not phase_finale) and self.c_ou_s == 'c') or \
                   (self.c_ou_s == 's' and (not phase_finale) \
                    and self.type_tournoi == 'coupe'):
                    self.attribuer_bonus_def()
                    self.maj_classement(self.eq1)
                    self.maj_classement(self.eq2)
                if self.c_ou_s == 's':
                    lieu1 = "neutre" if self.terrain_neutre else "domicile"
                    lieu2 = "neutre" if self.terrain_neutre else "exterieur"
                    pts1 = self.eq1.equipe.points
                    pts2 = self.eq2.equipe.points
                    self.maj_classement_selections(self.eq1,
                                                   pts1,
                                                   pts2,
                                                   lieu=lieu1)
                    self.maj_classement_selections(self.eq2,
                                                   pts2,
                                                   pts1,
                                                   lieu=lieu2)

    def declarer_gagnant_perdant(self):
        s1 = self.eq1.score
        s2 = self.eq2.score
        self.gagnant, self.perdant = (self.eq1, self.eq2) if s1>s2 \
                                     else (self.eq2, self.eq1) if s2>s1 \
                                     else (None, None)

        if self.gagnant is not None:
            print "gagnant", self.gagnant.nom, "perdant", self.perdant.nom
        else:
            print "Match nul !"

    def attribuer_bonus_def(self):
        #On verifie d'abord que ce n'est pas un match nul
        if not self.gagnant is None:
            if self.gagnant.score - self.perdant.score <= 7:
                self.perdant.bonus_def = True

    def maj_classement(self, eq):
        """
        Uniquement si on veut sauvegarder !!!
        Sert a maj les attributs "joues_tournoi", "gagnes_tournoi", etc du club
        (class Club !)
        /!\ Ici l'argument eq est de class EquipeTournoi.
        """
        cc = eq.equipe
        setattr(cc,
                'joues_'+self.type_tournoi,
                getattr(cc, 'joues_'+self.type_tournoi) + 1)
        if self.gagnant == eq:
            setattr(cc,
                    'gagnes_'+self.type_tournoi,
                    getattr(cc, 'gagnes_'+self.type_tournoi) + 1)
        elif self.perdant == eq:
            setattr(cc,
                    'perdus_'+self.type_tournoi,
                    getattr(cc, 'perdus_'+self.type_tournoi) + 1)
        else:
            setattr(cc,
                    'nuls_'+self.type_tournoi,
                    getattr(cc, 'nuls_'+self.type_tournoi) + 1)

        if eq.bonus_off:
            setattr(cc,
                    'bonus_offensif_'+self.type_tournoi,
                    getattr(cc, 'bonus_offensif_'+self.type_tournoi) + 1)

        if eq.bonus_def:
            setattr(cc,
                    'bonus_defensif_'+self.type_tournoi,
                    getattr(cc, 'bonus_defensif_'+self.type_tournoi) + 1)

        pour = eq.score
        contre = eq.autre_equipe.score
        setattr(cc,
                'pour_'+self.type_tournoi,
                getattr(cc, 'pour_'+self.type_tournoi) + pour)
        setattr(cc,
                'contre_'+self.type_tournoi,
                getattr(cc, 'contre_'+self.type_tournoi) + contre)
        setattr(cc,
                'difference_'+self.type_tournoi,
                getattr(cc, 'difference_'+self.type_tournoi) + pour - contre)
        eq.equipe.sauvegarder()

    def maj_classement_selections(self, eq, pts_eq, pts_autre, lieu):
        if lieu == 'domicile':
            B = 3
        elif lieu == 'exterieur':
            B = -3
        elif lieu == 'neutre':
            B = 0
        D = pts_eq - pts_autre + B
        if D > 10:
            D = 10
        elif D < -10:
            D = -10

        if self.gagnant == eq:
            P = 1 - D/10.
        elif self.perdant == eq:
            P = -1 - D/10.
        else:
            P = -D/10.

        if abs(eq.score - eq.autre_equipe.score) <= 15:
            C = 2 if self.type_tournoi == "coupe_monde" else 1
        else:
            C = 3 if self.type_tournoi == "coupe_monde" else 1.5

        eq.equipe.points += round(C*P, 2) #arrondi au centième
        eq.equipe.sauvegarder()

class EquipeMatch():
    def __init__(self, nom, comp, match=None, c_ou_s='c'):
        self.nom = nom
        self.comp = comp
        self.match = match
        self.c_ou_s = c_ou_s
        self.equipe = s.charger(nom, self.c_ou_s)
        if self.c_ou_s == 's':
            self.points_championat = self.equipe.points_championat
        self.bonus_def = False

        #Les points sont notes sous forme de liste de dict (k=nom, v=nombre)
        self.dict_essais = dict()
        self.dict_transformations = dict()
        self.dict_transformation_ratees = dict()
        self.dict_drops = dict()
        self.dict_drop_rates = dict()
        self.dict_penalites = dict()
        self.dict_penalite_ratees = dict()
        self.dict_rouges = dict()
        self.dict_jaunes = dict()
        self.dict_blessures = dict()

        #Pour les stats
        self.occase_essai = 0
        self.occase_penalite = 0
        self.occase_melee = 0
        self.occase_touche = 0

    @property
    def autre_equipe(self):
        return self.match.eq1 if self.match.eq2==self else self.match.eq2

    @property
    def essais(self):
        res = 0
        for n in self.dict_essais.values():#nombres:
            res += n
        return res
    
    @property
    def transformations(self):
        res = 0
        for n in self.dict_transformations.values():#nombres:
            res += n
        return res
    
    @property
    def drops(self):
        res = 0
        for n in self.dict_drops.values():#nombres:
            res += n
        return res
    
    @property
    def penalites(self):
        res = 0
        for n in self.dict_penalites.values():#nombres:
            res += n
        return res

    @property
    def bonus_off(self):
        return True if self.essais >= 4 else False
    
    @property
    def score(self):
        return 5*self.essais + 2*self.transformations + 3*(self.drops + self.penalites)

    def set_dict_score(self, option, separateur=', '):
        if not option in ["essais", "transformations", "drops", "penalites"]:
            raise ValueError("Wrong option ! Got " + option)
        attribut = self.dict_essais if option=="essais" \
                   else self.dict_transformations if option=="transformations" \
                   else self.dict_drops if option=="drops" \
                   else self.dict_penalites

        l = raw_input("Lister les joueurs aillant marque des " \
                      + option \
                      + " pendant le match " \
                      + " pour " \
                      + self.nom \
                      + " ")
        for nom in l.split(separateur):
            if nom in attribut.keys():
                attribut[nom] += 1
            else:
                attribut[nom] = 1

def merge_clubs(ini, a_changer):
    ll_noms = [cc.nom for cc in a_changer]
    for cc in ini:
        if cc.nom in ll_noms:
            ini.remove(cc)
    return ini + a_changer

def exempter_de_match(nom, c_ou_s='c', clubs=None):
    equipe = s.charger(nom, c_ou_s)
    clubs_a_sauver = []
    if c_ou_s == 'c':
        for jj in equipe.get_all_joueurs():
            jj.fatigue = max(0, jj.fatigue - 5)
            jj.blessure = max(0, jj.blessure - 1)
        equipe.sauvegarder()
        return 0
    else:
        for jj in equipe.get_all_joueurs():
            cc = identifier_club(jj, clubs)
            clubs_a_sauver.append(cc)
            jj_club = cc.get_joueur_from_nom(jj.nom)
            jj_club.fatigue = max(0, jj_club.fatigue - 5)
            jj_club.blessure = max(0, jj_club.blessure - 1)
        return clubs_a_sauver

"""
Reste a ecrire :
    - class EquipeMatch -> score, BO, BD
    - finir Match.jouer() -> mettre dans matches joues, etc
    - finir Calendrier -> matches joues, prochain match, etc
    - adapter Tournoi ?
"""




        
