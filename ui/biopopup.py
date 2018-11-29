from PyQt4 import QtCore, QtGui
import selection as s
from miscellaneous import carte_to_string
from ui.couleurs import *
from stats_uniquement_bonus_evolution import *

class BioPopup(QtGui.QWidget):
    def __init__(self, parent=None, joueurs=None, col3=None, dat=None, fatigue=True):
        super(BioPopup, self).__init__(parent)
        self.col3 = col3
        self.fatigue = fatigue
        self.joueurs = joueurs
        self.dat = s.date if dat is None else dat

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.tabs = QtGui.QTabWidget(self)
        self.lay.addWidget(self.tabs)

        self.car_tab = JCaracsWidget(joueurs=self.joueurs, parent=self)
        self.tabs.addTab(self.car_tab, "Caracs")

        self.info_tab = JInfosWidget(joueurs=self.joueurs, dat=self.dat)
        self.tabs.addTab(self.info_tab, "Infos")

        self.stats_saison_tab = JStatsWidget(joueurs=self.joueurs, s_ou_t='s')
        self.tabs.addTab(self.stats_saison_tab, "Statistiques Saison")

        self.stats_total_tab = JStatsWidget(joueurs=self.joueurs, s_ou_t='t')
        self.tabs.addTab(self.stats_total_tab, "Statistiques Total")

        self.evolution_saison_tab = JEvolutionWidget(joueurs=self.joueurs, dat=self.dat, dat_debut=self.dat-1)
        self.tabs.addTab(self.evolution_saison_tab, "Evolution saison")

        self.evolution_total_tab = JEvolutionWidget(joueurs=self.joueurs, dat=self.dat)
        self.tabs.addTab(self.evolution_total_tab, "Evolution totale")

        width = max(350, 120+150*len(self.joueurs))
        if width < 1200:
            self.setGeometry(100, 100, width, 900)
        else:
            self.resize(self.maximumSize())

class JCaracsWidget(QtGui.QWidget):
    def __init__(self, joueurs, parent=None, dat=None, evolution=False):
        self.dat = dat
        super(JCaracsWidget, self).__init__(parent)
        self.evolution = evolution
        self.joueurs = joueurs
        self.caracs = []
        for jj in self.joueurs:
            self.caracs.append(s.get_caracs(jj, self.parent().fatigue))
            """
            if dat is None:
                self.caracs.append(s.get_caracs(jj, self.parent().fatigue))
            else:
                #self.caracs.append(getattr(jj, "caracs_saison_"+str(date)))
                jj.jj_passe['s'+str(dat)].caracs_sans_fatigue
            """

        rows = 15 if self.evolution else 10
        self.mod = QtGui.QStandardItemModel(rows, len(self.joueurs))
        self.setup_model()
        
        self.setup_ui()

    def setup_model(self):
        r = 0
        c = 0
        r_header = ['EV poste 1', 'EV poste 2', 'EV poste 3']
        c_header = []
        for jj in self.joueurs:
            caracs_jj = self.caracs[self.joueurs.index(jj)]
            r = 0
            for k in range(1,4):
                poste = jj.postes[k]
                if poste != '':
                    if poste in ['C1', 'CE']:
                        self.mod.setItem(r, c, QtGui.QStandardItem('C1 : ' + '%0.2f' % s.calc_EV(jj, 'C1', fatigue=self.parent().fatigue, caracs=caracs_jj) + '\n' + \
                                                                   'C2 : ' + '%0.2f' % s.calc_EV(jj, 'C2', fatigue=self.parent().fatigue, caracs=caracs_jj)))
                    elif poste == 'C2':
                        self.mod.setItem(r, c, QtGui.QStandardItem('C2 : ' + '%0.2f' % s.calc_EV(jj, 'C2', fatigue=self.parent().fatigue, caracs=caracs_jj) + '\n' + \
                                                                   'C1 : ' + '%0.2f' % s.calc_EV(jj, 'C1', fatigue=self.parent().fatigue, caracs=caracs_jj)))
                    else :
                        self.mod.setItem(r, c, QtGui.QStandardItem(poste + ' : ' + '%0.2f' % s.calc_EV(jj, poste, fatigue=self.parent().fatigue, caracs=caracs_jj)))
                    if not jj.postes_maitrises[k]:
                        MJ = getattr(jj, 'MJ'+str(k))
                        nb_matches = MJ['CT']+MJ['ST'] + .5*(MJ['CR']+MJ['SR'])
                        seuil = 0 if jj.nom == '' else s.matches_pour_maitriser_poste(jj.postes[1], jj.postes[k])
                        if nb_matches >= seuil:
                            couleur = noir
                        elif nb_matches >= seuil / 2.:
                            couleur = orange
                        else:
                            couleur = rouge
                        self.mod.setData(self.mod.index(r, c), QtGui.QBrush(couleur), QtCore.Qt.TextColorRole)
                r += 1
                
            c_header.append(jj.nom)
            for car in sorted(s.ordre_caracs_joueurs, key=lambda car: s.ordre_caracs_joueurs[car]):
                self.mod.setItem(r, c, QtGui.QStandardItem(str(caracs_jj[car])))
                r += 1

            if self.evolution:
                for attr in ('carte_evolution', 'bonus', 'evolution'):
                    att = getattr(jj, attr)
                    st = carte_to_string(att) if type(att) == dict else str(att)
                    self.mod.setItem(r, c, QtGui.QStandardItem(st))
                    r += 1

                try:
                    dat = jj.nom.split(' - ')[-1] if ' - ' in jj.nom else self.dat
                except ValueError:
                    dat = self.dat
                declin = str(jj.D <= dat)
                self.mod.setItem(r, c, QtGui.QStandardItem(declin))
                r += 1

                self.mod.setItem(r, c, QtGui.QStandardItem(jj.RG.rang))
                r += 1

            c += 1
            
        for car in sorted(s.ordre_caracs_joueurs, key=lambda car: s.ordre_caracs_joueurs[car]):
            r_header.append(car)

        if self.evolution:
            r_header += [u'Carte évolution', 'Bonus', 'Evolution', u'Déclin', 'Rang']
            
        self.mod.setHorizontalHeaderLabels(c_header)
        self.mod.setVerticalHeaderLabels(r_header)

    def setup_ui(self):
        self.vue = QtGui.QTableView()
        self.vue.setModel(self.mod)
        self.vue.setWordWrap(True)
        #self.vue.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.vue.setTextElideMode(QtCore.Qt.ElideNone) 
        #self.vue.resizeRowsToContents()
        row_header = self.vue.verticalHeader()
        for row in range(self.mod.rowCount()):
            row_header.setResizeMode(row, QtGui.QHeaderView.ResizeToContents)

        #Couleurs min et max
        if len(self.joueurs) > 1:
            self.color_min_max()

        #Largeur des colones et des lignes
        self.vue.resizeColumnsToContents()
        self.vue.resizeRowsToContents()

        rec = QtCore.QRect(300, 100, self.vue.width(), self.vue.height())
        self.setGeometry(rec)
        
        #Valeurs non editables
        self.vue.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        #Selection par lignes
        self.vue.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumns)        

        self.pop_lay = QtGui.QVBoxLayout()
        self.pop_lay.addWidget(self.vue)
        self.setLayout(self.pop_lay)

        #Connect double clic
        self.vue.doubleClicked.connect(self.maj_compo_aux)

    def maj_compo_aux(self):
        c = self.vue.currentIndex().column()
        nom = str(self.mod.horizontalHeaderItem(c).text())

        self.parent().parent().parent().col3.maj_compo_aux_2(nom)
        
    def color_min_max(self):
        b = s.est_un_avant(self.joueurs[0])# or self.evolution
        N = 18
        #Min
        for row in range(3, N):
            car = str(self.mod.verticalHeaderItem(row).text())
            min = 100
            rs = []
            cs = []
            for col in range(self.mod.columnCount()):
                item = self.mod.item(row, col)
                val = int(item.text())
                if val <= min:
                    min = val
            b_TA = car == 'TA' and 'TA' in self.joueurs[0].postes
            if (b and car in s.caracs_avant) or (not b and car in s.caracs_arriere) or self.evolution:
                if b_TA or car != 'TA':
                    for col in range(self.mod.columnCount()):
                        item = self.mod.item(row, col)
                        val = int(item.text())        
                        if val == min:
                            self.mod.setData(
                                self.mod.index(row, col),
                                QtGui.QColor(QtCore.Qt.red),
                                QtCore.Qt.BackgroundColorRole)
                        
        #Max
        for row in range(3, N):
            car = str(self.mod.verticalHeaderItem(row).text())
            max = 0
            rs = []
            cs = []
            for col in range(self.mod.columnCount()):
                item = self.mod.item(row, col)
                val = int(item.text())
                if val >= max:
                    max = val
            if (b and car in s.caracs_avant) or (not b and car in s.caracs_arriere) or self.evolution:
                if b_TA or car != 'TA':
                    for col in range(self.mod.columnCount()):
                        item = self.mod.item(row, col)
                        val = int(item.text())        
                        if val == max:
                            self.mod.setData(
                                self.mod.index(row, col),
                                QtGui.QColor(QtCore.Qt.green),
                                QtCore.Qt.BackgroundColorRole)
            
class JInfosWidget(QtGui.QWidget):
    def __init__(self, joueurs, dat=None):
        QtGui.QWidget.__init__(self)
        self.joueurs = joueurs
        self.dat = s.lire_date() if dat is None else dat

        self.mod = QtGui.QStandardItemModel(9, len(self.joueurs))
        self.setup_model()
        
        self.setup_ui()

    def setup_model(self):
        c_header = []
        r_header = ['Poste 1', 'Poste 2', 'Poste 3', 'Armee', 'Rang',
                    'Creation', 'Valeur', 'MS', 'Rang max', 'Declin', 'Club',
                    'Anciens clubs', 'Changements de postes', 'Nouveaux Bonus',
                    'Bonus Avant', 'Bonus Saison', 'XP manquante']
        r = 0
        c = 0

        for jj in self.joueurs:
            r = 0
            for k in range(1,4):
                poste = jj.postes[k]
                if poste != '':
                    if poste in ['C1', 'CE']:
                        self.mod.setItem(r, c, QtGui.QStandardItem('C1 : ' + '%0.2f' % s.calc_EV(jj, 'C1') + '\n' + 
                                                                   'C2 : ' + '%0.2f' % s.calc_EV(jj, 'C2')))
                    elif poste == 'C2':
                        self.mod.setItem(r, c, QtGui.QStandardItem('C2 : ' + '%0.2f' % s.calc_EV(jj, 'C2') + '\n' + 
                                                                   'C1 : ' + '%0.2f' % s.calc_EV(jj, 'C1')))
                    else :
                        self.mod.setItem(r, c, QtGui.QStandardItem(poste + ' : ' + '%0.2f' % s.calc_EV(jj, poste)))
                r += 1
                
            c_header.append(jj.nom)
            
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.ARM)))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.RG.rang)))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.C)))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.VAL)))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.MS)))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.RG_max.rang)))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.D)))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.club)))
            r += 1
            st = str(jj.anciens_clubs.replace(';', '\n'))
            self.mod.setItem(r, c, QtGui.QStandardItem(st))
            r += 1
            st = str(jj.changements_postes)
            self.mod.setItem(r, c, QtGui.QStandardItem(st))
            r += 1

            st = str(jj.nouveau_bonus_evolution)
            self.mod.setItem(r, c, QtGui.QStandardItem(st))
            r += 1
            if jj.nouveau_bonus_evolution:
                avant, residus = bonus_atteint_avant_debut_saison(jj, self.dat)
                st = str(avant)
                self.mod.setItem(r, c, QtGui.QStandardItem(st))
                r += 1
                saison, residus, tot = bonus_atteints_saison_en_cours(jj, self.dat)
                st = str(saison)
                self.mod.setItem(r, c, QtGui.QStandardItem(st))
                r += 1
                manquante = xp_manquante_prochain_bonus(jj, self.dat)
                st = str(manquante)
                self.mod.setItem(r, c, QtGui.QStandardItem(st))
                r += 1
            else:
                st = 'NA'
                self.mod.setItem(r, c, QtGui.QStandardItem(st))
                r += 1
                self.mod.setItem(r, c, QtGui.QStandardItem(st))
                r += 1
                self.mod.setItem(r, c, QtGui.QStandardItem(st))
                r += 1

            c += 1

        self.mod.setHorizontalHeaderLabels(c_header)
        self.mod.setVerticalHeaderLabels(r_header)

        """
        A ajouter : experience, matches joues cette saison, infos contrat, cartons
            -> dans un autre onglet ?
        """

    def setup_ui(self):
        self.vue = QtGui.QTableView()
        self.vue.setModel(self.mod)
        self.vue.setWordWrap(True)
        self.vue.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.vue.resizeRowsToContents()
        
        #Largeur des colones
        self.vue.resizeColumnsToContents()
        self.vue.resizeRowsToContents()

        rec = QtCore.QRect(300, 100, self.vue.width(), self.vue.height())
        self.setGeometry(rec)
        
        #Valeurs non editables
        self.vue.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.pop_lay = QtGui.QVBoxLayout()
        self.pop_lay.addWidget(self.vue)
        self.setLayout(self.pop_lay)

class JStatsWidget(QtGui.QWidget):
    def __init__(self, s_ou_t, parent=None, joueurs=None):
        super(JStatsWidget, self).__init__(parent)
        self.joueurs = joueurs
        self.s_ou_t = s_ou_t
        
        self.mod = QtGui.QStandardItemModel(7, len(self.joueurs))
        self.setup_model()
        
        self.setup_ui()

    def setup_model(self):
        c_header = []
        r_header = ['Essais', 'Transformations', u'Pénalites', 'Drops', 'Points',
                    u'Matches joués\nen club\n(dont tit)', 'Total club',
                    u'Sélections', u'Total sélections', u'Expérience']
        r = 0
        c = 0

        for jj in self.joueurs:
            r = 0
            c_header.append(jj.nom)

            for attr in ('essais', 'transformations', 'penalites', 'drops'):
                if self.s_ou_t == 's':
                    attr += '_saison'
                elif self.s_ou_t == 't':
                    attr += '_total'
                else:
                    raise ValueError("s_ou_t doit etre 's' ou 't', "+str(self.s_ou_t)+" recu")
                self.mod.setItem(r, c, QtGui.QStandardItem(str(getattr(jj, attr))))
                r += 1

            pts = 5*int(self.mod.item(0, c).text()) + \
                  2*int(self.mod.item(1, c).text()) + \
                  3*int(self.mod.item(2, c).text()) + \
                  3*int(self.mod.item(3, c).text())
            self.mod.setItem(r, c, QtGui.QStandardItem(str(pts)))
            r += 1
            
            st = ""
            sts = ""
            tot_tit_club = 0
            tot_club = 0
            tot_tit_sel = 0
            tot_sel = 0
            for ii in (1, 2, 3):
                if self.s_ou_t == 's':
                    dd = getattr(jj, "MJ"+str(ii))
                elif self.s_ou_t == 't':
                    dd = getattr(jj, "MJ"+str(ii)+"_total")
                else:
                    raise ValueError("s_ou_t doit etre 's' ou 't', "+str(self.s_ou_t)+" recu")
                poste = jj.postes[ii]
                if not poste == "":
                    st += poste + " " + str(dd['CT'] + dd['CR']) + ' (' + \
                          str(dd['CT']) + ')'
                    sts += poste + " " + str(dd['ST'] + dd['SR']) + ' (' + \
                          str(dd['ST']) + ')'
                    if ii < 3:
                        st += '\n'
                        sts += '\n'
                    tot_club += dd['CT'] + dd['CR']
                    tot_tit_club += dd['CT']
                    tot_sel += dd['ST'] + dd['SR']
                    tot_tit_sel += dd['ST']
                    st_tot_club = str(tot_club) + ' (' + str(tot_tit_club) + ')'
                    st_tot_sel = str(tot_sel) + ' (' + str(tot_tit_sel) + ')'
            self.mod.setItem(r, c, QtGui.QStandardItem(st))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(st_tot_club))
            r += 1

            self.mod.setItem(r, c, QtGui.QStandardItem(sts))
            r += 1
            self.mod.setItem(r, c, QtGui.QStandardItem(st_tot_sel))
            r += 1

            st_xp = str(jj.xp_saison) if self.s_ou_t == 's' else str(jj.xp_total)
            self.mod.setItem(r, c, QtGui.QStandardItem(st_xp))
            r += 1

            c += 1

        self.mod.setHorizontalHeaderLabels(c_header)
        self.mod.setVerticalHeaderLabels(r_header)       

    def setup_ui(self):
        self.vue = QtGui.QTableView()
        self.vue.setModel(self.mod)
        
        #Largeur des colones
        self.vue.resizeColumnsToContents()
        self.vue.resizeRowsToContents()
        
        rec = QtCore.QRect(300, 100, self.vue.width(), self.vue.height())
        self.setGeometry(rec)
            
        #Valeurs non editables
        self.vue.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        #Adapter la taille des lignes (notamment pour les matches joues avec
        #avec des '\n'
        self.vue.resizeRowsToContents()

        self.lay = QtGui.QVBoxLayout()
        self.lay.addWidget(self.vue)
        self.setLayout(self.lay)

class JEvolutionWidget(QtGui.QWidget):
    def __init__(self, joueurs, dat=s.lire_date(), dat_debut=None, parent=None):
        super(JEvolutionWidget, self).__init__(parent)
        self.joueurs = joueurs
        self.fatigue = False
        self.dat = dat
        self.dat_debut = 11 if dat_debut is None else dat_debut

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()

    def setup_ui(self):
        jjs = []
        for jj in self.joueurs:
            for date in range(max(self.dat_debut, jj.C), self.dat):
                jj_aux = jj.jj_passe['s'+str(date)]#s.joueur()
                jj_aux.nom = jj.nom + ' (' + str(date) + ')'
                #jj.nom = jj.nom.split(' (')[0]
                """
                jj_aux.caracs_sans_fatigue = jj.jj_passe['s'+str(date)].caracs_sans_fatigue \
                                             if date < s.date \
                                             else jj.caracs_sans_fatigue
                jj_aux.postes = jj.jj_passe['s'+str(date)].postes \
                                             if date < s.date \
                                             else jj.postes
                """
                jjs.append(jj_aux)
            jjs.append(jj)
        self.lay.addWidget(JCaracsWidget(joueurs=jjs, parent=self, evolution=True, dat=self.dat))
