import pickle
from date import *
from savefiles import *
from calendrier import *
import noms_all

class saison(object):
    """
    Classe contenant le programme de toute une saison, avec tous les tournois
    """
    def __init__(self,
                 noms_championats,
                 nom=None,
                 dat=None,
                 c_ou_s='c'):
        print '__init__ saison'
        self.noms_championats = noms_championats
        self.dat = lire_date() if dat is None else dat
        self.c_ou_s = c_ou_s
        self.nom = 'saison_' + str(self.dat) + '_' + self.c_ou_s if nom is None\
                   else nom
        self.calendriers = []
        self.dict_indice_journees = {}
        for nom in self.noms_championats:
            self.calendriers.append(charger_calendrier(nom, self.dat))
            self.dict_indice_journees[nom] = 0

        self._journees = None
        self.journees = self.get_journees()

        self.nombre_journees_repos = self.journees.count('repos')
        self.repos_effectues = [False]*self.nombre_journees_repos

        """
        self.quarts_inities = False
        self.demies_initiees = False
        self.finale_initiee = False
        """
        self.quarts_inities = {}
        self.demies_initiees = {}
        self.finale_initiee = {}
        for nom in noms_all.noms_coupes:
            self.quarts_inities[nom] = False
            self.demies_initiees[nom] = False
            self.finale_initiee[nom] = False

    def get_journees(self):
        if self._journees is None:
            file_name = CALENDRIERS_DIR_NAME(self.dat) + '/' + self.nom + '.txt'
            st = ''
            with open(file_name, 'r') as ff:
                for line in ff.readlines():
                    st += line
            journees = st.split('\n\n')
            self._journees = journees
        return self._journees

    @property
    def journee_jouee(self):
        ll = []
        n_repos = 0
        ll_misc = []
        for kk in range(len(self.journees)):
            journee = self.journees_calendriers(kk)
            for st in journee:
                for stt in st.split('\n'):
                    ll_misc.append(stt)
            for nn in range(len(journee)):
                nom = journee[nn]
                if nom in self.noms_championats:
                    ii = ll_misc.count(nom) - 1
                    cal = self.calendriers[self.noms_championats.index(nom)]
                    boo = not None in cal.scores[ii]
                elif nom == 'repos':
                    boo = self.repos_effectues[n_repos]
                    n_repos += 1
                else:
                    boo = False
            ll.append(boo)
        return ll

    def cal_indices_prochain_match(self):
        for kk in range(len(self.journees)):
            if self.journee_jouee[kk]:
                pass
            else:
                break
        journee = self.journees_calendriers(kk)
        if journee == ['repos']:
            return 'repos', 0, 0
        else:
            """
            if True in ['quarts' in  st for st in journee] and not self.quarts_inities:
                self.init_quarts()
            elif True in ['demies' in  st for st in journee] and not self.demies_initiees:
                self.init_demies()
            elif True in ['finale' in  st for st in journee] and not self.finale_initiee:
                self.init_finale()
            """
            for jou in journee:
                if 'quarts' in jou:
                    nom_champ = jou.split('_')[0]
                    if not self.quarts_inities[nom_champ]:
                        self.init_quarts(nom_champ)
                elif 'demies' in jou:
                    nom_champ = jou.split('_')[0]
                    if not self.demies_initiees[nom_champ]:
                        self.init_demies(nom_champ)
                elif 'finale' in jou:
                    nom_champ = jou.split('_')[0]
                    if not self.finale_initiee[nom_champ]:
                        self.init_finale(nom_champ)

            noms = [journee[nn] for nn in range(len(journee))]
            cals = [self.calendriers[self.noms_championats.index(nom)] \
                    for nom in noms]
            ll = []
            for jou in self.journees[:kk+1]:
                ll += jou.split('\n')

            for nn, cal in enumerate(cals):
                #num = self.dict_indice_journees[cal.nom_championnat]
                num2 = ll.count(cal.nom_championnat) - 1
                ii, jj = cal.indices_prochain_match()
                if ii == num2 and cal.scores[ii][jj] is None:
                    break
            return cal, ii, jj

    def match_joue(self, nom_eq1, nom_eq2, cal):
        ii, jj = cal.indices_prochain_match()
        if jj == len(cal.scores[ii])-1 and not cal.scores[ii][jj] is None:
            self.dict_indice_journees[cal.nom_championnat] += 1

    def prochain_match(self):
        cal, ii, jj = self.cal_indices_prochain_match()
        if cal == 'repos':
            return 'repos'
        else:
            return cal.matches[ii][jj]

    def journees_calendriers(self, kk):
        """
        Retourne un liste des noms de championats à jouer dans la journee kk
        de la saison
        """
        journee = self.journees[kk].split('\n')
        return journee

    def get_classement(self, nom_championat):
        cals = []
        for nom in self.noms_championats:
            if nom_championat in nom and \
               (not 'quarts' in nom or 'demies' in nom or 'finale' in nom):
                cals.append(self.calendriers[self.noms_championats.index(nom)])
        ll = []
        for cal in cals:
            for nom in cal.noms_clubs:
                tu = (nom, cal.get_points(nom), cal.get_difference(nom))
                ll.append(tu)
        ll.sort(key=lambda tu: (tu[1], tu[2]))
        classement = [ll[ii][0] for ii in range(len(ll))]
        classement.reverse()
        return classement

    def init_quarts(self, nom_championat):
        #for nom_championat in noms_all.noms_coupes:
        classement = self.get_classement(nom_championat)
        cal_name = nom_championat + '_quarts'
        filename = CALENDRIERS_DIR_NAME(self.dat) + '/calendrier_' + \
                cal_name + '.txt'
        with open(filename, 'w') as ff:
            for ii in (0, 3, 1, 2):
                st = classement[ii] + ' v ' + classement[7 - ii]
                ff.write(st)
                if not ii == 2: #Pour ne pas ajouter une ligne vide à la fin
                    ff.write('\n')

        cal = calendrier(cal_name, self.dat)
        cal.sauvegarder()
        self.noms_championats.append(cal_name)
        self.calendriers.append(cal)
        self.dict_indice_journees[cal_name] = 0
        self.quarts_inities[nom_championat] = True
        self.sauvegarder()

    def init_demies(self, nom_championat):
        #for nom_championat in noms_all.noms_coupes:
        quart = self.calendriers[self.noms_championats.index(nom_championat + '_quarts')]
        vainqueurs = []
        for jj in range(4):
            match = quart.matches[0][jj]
            noms = match.split(' v ')
            vainc = noms[0] if quart.scores[0][jj][0] > quart.scores[0][jj][1] \
                    else noms[1]
            vainqueurs.append(vainc)

        cal_name = nom_championat + '_demies'
        filename = CALENDRIERS_DIR_NAME(self.dat) + '/calendrier_' + \
                cal_name + '.txt'
        with open(filename, 'w') as ff:
            for ii in range(2):
                st = vainqueurs[2*ii] + ' v ' + vainqueurs[2*ii+1]
                ff.write(st +'\n')

        cal = calendrier(cal_name, self.dat)
        cal.sauvegarder()
        self.noms_championats.append(cal_name)
        self.calendriers.append(cal)
        self.dict_indice_journees[cal_name] = 0
        self.demies_initiees[nom_championat] = True
        self.sauvegarder()

    def init_finale(self, nom_championat):
        #for nom_championat in noms_all.noms_coupes:
        demie = self.calendriers[self.noms_championats.index(nom_championat + '_demies')]
        vainqueurs = []
        for jj in range(2):
            match = demie.matches[0][jj]
            noms = match.split(' v ')
            vainc = noms[0] if demie.scores[0][jj][0] > demie.scores[0][jj][1] \
                    else noms[1]
            vainqueurs.append(vainc)

        cal_name = nom_championat + '_finale'
        filename = CALENDRIERS_DIR_NAME(self.dat) + '/calendrier_' + \
                cal_name + '.txt'
        with open(filename, 'w') as ff:
            st = vainqueurs[0] + ' v ' + vainqueurs[+1]
            ff.write(st +'\n')

        cal = calendrier(cal_name, self.dat)
        cal.sauvegarder()
        self.noms_championats.append(cal_name)
        self.calendriers.append(cal)
        self.dict_indice_journees[cal_name] = 0
        self.finale_initiee[nom_championat] = True
        self.sauvegarder()

    def get_classement_joueurs(self, attr, nom_championat):
        if nom_championat == 'Saison':
            cals = self.calendriers
        else:
            cals = []
            for ii, nom in enumerate(self.noms_championats):
                if nom_championat == nom or \
                   (nom_championat in ('coupe', 'challenge', 'nordsud') and \
                    nom_championat in nom):
                    cals.append(self.calendriers[ii])
        dd = {}
        for cal in cals:
            clas = cal.get_classement_joueurs(attr)
            for tu in clas:
                if tu[0] in dd.keys():
                    tuu = dd[tu[0]]
                    if attr == 'pourcentage':
                        val_old = tuu[2][0]
                        tot_old = tuu[2][1]
                        val = tu[2][0]
                        tot = tu[2][1]
                        tot_new = tot + tot_old
                        val_new = round((val*tot + val_old*tot_old) / tot_new, 2)
                        dd[tu[0]] = (tu[0], tu[1], (val_new, tot_new))
                    else:
                        dd[tu[0]] = (tu[0], tu[1], tuu[2] + tu[2])
                else:
                    dd[tu[0]] = (tu[0], tu[1], tu[2])
        ll = dd.values()
        ll.sort(key=lambda tu: tu[2])
        ll.reverse()
        return ll

    def get_calendrier_equipe(self, nom):
        ll = []
        dd = {}
        for champ in self.noms_championats:
            dd[champ] = 0

        ddd = {}
        if self.c_ou_s == 'c':
            for st in ('coupe', 'challenge', 'nordsud'):
                noms = []
                for ii in range(1, 5):
                    cal = self.calendriers[self.noms_championats.index(st+'_poule_'+str(ii))]
                    noms += cal.noms_clubs
                ddd[st] = noms
        elif self.c_ou_s == 's':
            cal = self.calendriers[self.noms_championats.index('tournoi_quarts')]
            noms = cal.noms_clubs
            ddd['tournoi'] = noms

        for jou in self.journees:
            if jou == 'repos':
                ll.append(('Repos', None, None))
            else:
                trouve = False
                champs = jou.split('\n')
                for champ in champs:
                    if champ == '':
                        pass
                    elif not champ in self.noms_championats:
                        if nom in ddd[champ.split('_')[0]]:
                            trouve = True
                            ll.append((champ, None, None))
                    else:
                        idx = self.noms_championats.index(champ)
                        cal = self.calendriers[idx]
                        if nom in cal.noms_clubs:
                            matches = cal.matches[dd[champ]]
                            for ii, mat in enumerate(matches):
                                if nom in mat.split(' v '):
                                    sc = cal.scores[dd[champ]][ii]
                                    ll.append((champ, mat, sc))
                                    trouve = True
                            if not trouve:
                                ll.append((champ, None, None))
                                trouve = True
                        dd[champ] += 1
                if not trouve:
                    ll.append(('Repos', None, None))
        return ll

    def sauvegarder(self):
        with open(CALENDRIERS_DIR_NAME(self.dat) + '/' + self.nom + '.sais', 'w') \
             as f:
            pickle.dump(self, f)
        print 'saison', self.nom, u'sauvegardée'

def charger_saison(nom=None, dat=None, c_ou_s='c'):
    if dat is None:
        dat = lire_date()
    if nom is None:
        nom = 'saison_' + str(dat) + '_' + c_ou_s
    filename = CALENDRIERS_DIR_NAME(dat) + '/' + nom + '.sais'
    with open(filename, 'r') \
         as f:
        sais = pickle.load(f)
    return sais
