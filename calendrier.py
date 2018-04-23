import pickle
from date import *
from savefiles import *
import noms_all
import os.path as osp

def match_exemption(st):
    """
    Renvoie True si le match représenté par tu est une exemption,
    Faslse sinon
    """
    bb = False
    ll = st.split(' v ')
    for xx in ll:
        try:
            dummy = int(xx)
            bb = True
        except ValueError:
            pass
    return bb

class calendrier(object):
    def __init__(self, nom_championnat, dat=None):
        super(calendrier, self).__init__()
        self.nom_championnat = nom_championnat
        self.dat = dat
        self._journees = None
        self.journees = self.get_journees()
        self.matches = self.get_matches()
        self.scores = self.init_scores()
        self.noms_clubs = self.init_noms_clubs()
        for attr in ('essais', 'transformations', 'transformation_ratees',
                     'drops', 'drop_rates', 'penalites', 'penalite_ratees',
                     'rouges', 'jaunes', 'blessures'):
            setattr(self, 'dicts_'+attr, self.init_dicts(attr))
        for attr in ('joues', 'gagnes', 'nuls', 'perdus', 'bonus_offensifs',
                     'bonus_defensifs', 'pour', 'contre'):
            dd = dict()
            for nom in self.noms_clubs:
                dd[nom] = 0
            setattr(self, 'dict_'+attr, dd)

    def get_journees(self):
        if self._journees is None:
            file_name = CALENDRIERS_DIR_NAME(self.dat) + '\calendrier_' + \
                        self.nom_championnat + '.txt'
            st = ''
            with open(file_name, 'r') as ff:
                for line in ff.readlines():
                    st += line
            journees = st.split('\n\n')
            if journees[-1][-1] == '\n':
                journees[-1] = journees[-1][:-1]
            self._journees = journees
        return self._journees

    def init_scores(self):
        scores = []
        for ii in range(len(self.journees)):
            ll = []
            for jj in range(len(self.get_matches()[ii])):
                ll.append(None)
            scores.append(ll)
        return scores

    def init_dicts(self, attr):
        """
        Initialise la liste des dictionnaires de stats pour chaque match
        Retourne une liste en 2 dimensions N*M
        N = nombre de journees
        M = nombre de matches dans chaque journee
        valeur initiale pour chaque entree : None
        """
        dicts = []
        for ii in range(len(self.journees)):
            ll = []
            for jj in range(len(self.get_matches()[ii])):
                ll.append(None)
            dicts.append(ll)
        return dicts

    def get_matches(self):
        matches = []
        for ii in range(len(self.journees)):
            st = self.journees[ii]
            ll = st.split('\n')
            #On ignore les matches qui représentent des exemptions
            #Ils sont sous la forme "nom_equipe v N_eq +1"
            for mm in ll:
                if match_exemption(mm):
                    ll.remove(mm)
            matches.append(ll)
        return matches

    def init_noms_clubs(self):
        st = self.journees[0]
        st = st.replace('\n', ' v ')
        ll = st.split(' v ')
        for nom in ll:
            try:
                dummy = int(nom)
                ll.remove(nom)
            except ValueError:
                continue
        return ll

    def indices_prochain_match(self):
        for ii in range(len(self.journees)):
            continuer = True
            for jj in range(len(self.scores[ii])):
                if self.scores[ii][jj] is None:
                    continuer = False
                    break
            if not continuer:
                break
        return ii, jj

    def prochain_match(self):
        ii, jj = self.indices_prochain_match()
        return self.matches[ii][jj]

    def est_le_prochain_match(self, match):
        prochain_match = self.prochain_match()
        nom_1 = prochain_match.split(' v ')[0]
        nom_2 = prochain_match.split(' v ')[1]
        return (nom_1 == match.eq1.equipe.nom and nom_2 == match.eq2.equipe.nom)

    def set_scores(self, match):
        if not self.est_le_prochain_match(match):
            raise ValueError("Les noms d'equipes ne correspondent pas !")
        else:
            ii, jj = self.indices_prochain_match()
            self.scores[ii][jj] = (match.eq1.score, match.eq2.score)

    def set_dicts(self, match, attr):
        if not self.est_le_prochain_match(match):
            raise ValueError("Les noms d'equipes ne correspondent pas !")
        else:
            ii, jj = self.indices_prochain_match()
            ll = getattr(self, 'dicts_'+attr)
            ll[ii][jj] = (getattr(match.eq1, 'dict_'+attr),
                          getattr(match.eq2, 'dict_'+attr))

    def enregistrer_resultats(self, match):
        for attr in ('essais', 'transformations', 'transformation_ratees',
                     'drops', 'drop_rates', 'penalites', 'penalite_ratees',
                     'rouges', 'jaunes', 'blessures'):
            self.set_dicts(match, attr)
        self.set_scores(match)

        for eq in (match.eq1, match.eq2):
            self.dict_joues[eq.equipe.nom] += 1
            if match.gagnant == eq:
                self.dict_gagnes[eq.equipe.nom] += 1
            elif match.perdant == eq:
                self.dict_perdus[eq.equipe.nom] += 1
            else:
                self.dict_nuls[eq.equipe.nom] += 1

            if eq.bonus_off:
                self.dict_bonus_offensifs[eq.equipe.nom] += 1

            if eq.bonus_def:
                self.dict_bonus_defensifs[eq.equipe.nom] += 1

            self.dict_pour[eq.equipe.nom] += eq.score
            self.dict_contre[eq.equipe.nom] += eq.autre_equipe.score
        return self.indices_prochain_match()

    def sauvegarder(self):
        save_dir = CALENDRIERS_DIR_NAME(self.dat)
        with open(save_dir+'/calendrier_'+self.nom_championnat + '.cal', 'w') as f:
            pickle.dump(self, f)
        print "calendrier", self.nom_championnat, "sauvegarde"

    def get_points(self, nom_eq):
        return self.dict_gagnes[nom_eq]*4 + self.dict_nuls[nom_eq]*2 + \
               self.dict_bonus_offensifs[nom_eq] + \
               self.dict_bonus_defensifs[nom_eq]

    @property
    def dict_difference(self):
        dd = dict()
        for nom in self.noms_clubs:
            dd[nom] = self.get_difference(nom)
        return dd

    @property
    def dict_points(self):
        dd = dict()
        for nom in self.noms_clubs:
            dd[nom] = self.get_points(nom)
        return dd

    def get_difference(self, nom_eq):
        return self.dict_pour[nom_eq] - self.dict_contre[nom_eq]

    def get_classement(self):
        ll = self.noms_clubs
        ll.sort(key=lambda nom: (self.get_points(nom),
                                 self.get_difference(nom)))
        ll.reverse()
        return ll

    def get_classement_joueurs(self, attr):
        if attr == 'pourcentage':
            ll_reussis = []
            ll_rates = []
            noms_reussis = []
            noms_rates = []
            for nn, dicts in enumerate((self.dicts_tab_reussis, self.dicts_tab_rates)):
                ll = (ll_reussis, ll_rates)[nn]
                noms = (noms_reussis, noms_rates)[nn]
                for ii in range(len(dicts)):
                    for jj in range(len(dicts[ii])):
                        if dicts[ii][jj] is None:
                            continue
                        else:
                            dd1, dd2 = dicts[ii][jj]
                            noms_clubs = self.matches[ii][jj].split(' v ')
                            for kk, dd in enumerate((dd1, dd2)):
                                for nom, val in dd.items():
                                    if nom in noms:
                                        idx = noms.index(nom)
                                        old = ll[idx]
                                        ll[idx] = (nom, noms_clubs[kk], old[2] + val)
                                    else:
                                        ll.append((nom, noms_clubs[kk], val))
                                        noms.append(nom)
            for tu in ll_reussis:
                if not tu[0] in noms_rates:
                    ll_rates.append((tu[0], tu[1], 0))
                    noms_rates.append(tu[0])
            for tu in ll_rates:
                if not tu[0] in noms_reussis:
                    ll_reussis.append((tu[0], tu[1], 0))
                    noms_reussis.append(tu[0])

            ll = []
            for ii in range(len(ll_reussis)):
                tu = ll_reussis[ii]
                nom = tu[0]
                nom_club = tu[1]
                reussis = tu[2]
                idx = noms_rates.index(nom)
                tot = tu[2] + ll_rates[idx][2]
                val = (round(100. * reussis / tot, 2))
                ll.append((nom, nom_club, (val, tot)))
            for ii, nom in enumerate(noms_rates):
                if not nom in [tu[0] for tu in ll]:
                    tu = ll_rates[ii]
                    ll.append((tu[0], tu[1], (0, tu[2])))
            ll.sort(key=lambda tu: tu[2][1])

        else:
            if attr == 'points':
                attr += '_joueurs'
            dicts = getattr(self, 'dicts_'+attr)
            ll = []
            noms = []
            for ii in range(len(dicts)):
                for jj in range(len(dicts[ii])):
                    if dicts[ii][jj] is None:
                        continue
                    else:
                        dd1, dd2 = dicts[ii][jj]
                        noms_clubs = self.matches[ii][jj].split(' v ')
                        for kk, dd in enumerate((dd1, dd2)):
                            for nom, val in dd.items():
                                if nom in noms:
                                    idx = noms.index(nom)
                                    old = ll[idx]
                                    ll[idx] = (nom, noms_clubs[kk], old[2] + val)
                                else:
                                    ll.append((nom, noms_clubs[kk], val))
                                    noms.append(nom)
            ll.sort(key=lambda tu: tu[2])

        ll.reverse()
        return ll

    @property
    def dicts_points_joueurs(self):
        ll = []
        for ii in range(len(self.matches)):
            ll.append([])
            for jj in range(len(self.matches[ii])):
                if not self.scores[ii][jj] is None:
                    dd0 = {}
                    dd1 = {}
                    for kk in range(2):
                        dd = {}
                        for nom in self.dicts_essais[ii][jj][kk].keys() + \
                            self.dicts_penalites[ii][jj][kk].keys() + \
                            self.dicts_transformations[ii][jj][kk].keys() + \
                            self.dicts_drops[ii][jj][kk].keys():
                            dd[nom] = 0
                        for (nom, val) in self.dicts_essais[ii][jj][kk].items():
                            dd[nom] += val*5
                        for (nom, val) in self.dicts_transformations[ii][jj][kk].items():
                            dd[nom] += val*2
                        for (nom, val) in self.dicts_penalites[ii][jj][kk].items():
                            dd[nom] += val*3
                        for (nom, val) in self.dicts_drops[ii][jj][kk].items():
                            dd[nom] += val*3
                        if kk == 0:
                            dd0 = dd
                        elif kk == 1:
                            dd1 = dd
                    tu = (dd0, dd1)
                    ll[ii].append(tu)
        return ll

    @property
    def dicts_tab_reussis(self):
        ll = []
        for ii in range(len(self.matches)):
            ll.append([])
            for jj in range(len(self.matches[ii])):
                if not self.scores[ii][jj] is None:
                    dd0 = {}
                    dd1 = {}
                    for kk in range(2):
                        dd = {}
                        for nom in self.dicts_penalites[ii][jj][kk].keys() + \
                            self.dicts_transformations[ii][jj][kk].keys():
                            dd[nom] = 0
                        for (nom, val) in self.dicts_transformations[ii][jj][kk].items():
                            dd[nom] += val
                        for (nom, val) in self.dicts_penalites[ii][jj][kk].items():
                            dd[nom] += val
                        if kk == 0:
                            dd0 = dd
                        elif kk == 1:
                            dd1 = dd
                    tu = (dd0, dd1)
                    ll[ii].append(tu)
        return ll

    @property
    def dicts_tab_rates(self):
        ll = []
        for ii in range(len(self.matches)):
            ll.append([])
            for jj in range(len(self.matches[ii])):
                if not self.scores[ii][jj] is None:
                    dd0 = {}
                    dd1 = {}
                    for kk in range(2):
                        dd = {}
                        for nom in self.dicts_penalite_ratees[ii][jj][kk].keys() + \
                            self.dicts_transformation_ratees[ii][jj][kk].keys():
                            dd[nom] = 0
                        for (nom, val) in self.dicts_transformation_ratees[ii][jj][kk].items():
                            dd[nom] += val
                        for (nom, val) in self.dicts_penalite_ratees[ii][jj][kk].items():
                            dd[nom] += val
                        if kk == 0:
                            dd0 = dd
                        elif kk == 1:
                            dd1 = dd
                    tu = (dd0, dd1)
                    ll[ii].append(tu)
        return ll

def charger_calendrier(nom, dat=None):
    datt = lire_date() if dat is None else dat
    filename = CALENDRIERS_DIR_NAME(datt) + '\calendrier_' + nom + '.cal'
    if osp.isfile(filename):
        with open(filename, 'r') \
             as f:
            cal = pickle.load(f)
    else:
        cal = calendrier(nom, dat)
    return cal
