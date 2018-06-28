# -*- coding: cp1252 -*-
import biopopup as b
import selection as s
from PyQt4 import QtCore, QtGui
from choix_joueurs import MyTableWidgetItem
from couleurs import *
import sip
from ui.changement_poste_popup import ChangementPostePopup
#from plot_evolution import *
from plot_evolution_widget import PlotEvolutionWidget

class ChoixJoueursSelectionWidget(QtGui.QWidget):
    def __init__(self,
                 autre,
                 parent=None,
                 joueurs=[],
                 poste_filtre='all',
                 ev_filtre='Tous',
                 fatigue=False,
                 dat=None,
                 changement_poste_joueur_possible=False):
        super(ChoixJoueursSelectionWidget, self).__init__(parent)
        self.dat = dat
        self.changement_poste_joueur_possible = changement_poste_joueur_possible
        self.all_joueurs = joueurs
        self.poste_filtre = poste_filtre
        self.ev_filtre = ev_filtre
        self.fatigue = fatigue
        self.autre = autre
        #self.selected_joueurs = self.all_joueurs

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

        #click droit
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        self.colorer_table()

    def setup_ui(self):
        self.lay_options = QtGui.QHBoxLayout()
        """
        ComboBox pour les filtrages par postes
        """
        self.combo = QtGui.QComboBox()
        self.combo.setObjectName("Filtrer par poste")
        if self.poste_filtre == "all":
            self.combo.addItem("Tous")
        elif self.poste_filtre == "compo":
            self.combo.addItem("Tous")
        else:
            self.combo.addItem(self.poste_filtre)
        for poste in ["Tous", "Compo"] + s.postes:
            if not (poste == self.poste_filtre \
                    or poste == "Tous" and self.poste_filtre == "all" \
                    or poste == "Compo" and self.poste_filtre == "compo"):
                self.combo.addItem(poste)
        self.combo.activated['QString'].connect(self.filtrer_joueurs)
        self.lay_options.addWidget(self.combo)

        """
        Combo pour filtrage par EV
        """
        self.combo_ev = QtGui.QComboBox()
        self.combo_ev.setObjectName("Filtrer par EV")
        self.combo_ev.addItem("Tous")
        for ii in range(8, 13):
            self.combo_ev.addItem(str(ii))
        self.combo_ev.activated['QString'].connect(self.filtrer_joueurs_ev)
        self.lay_options.addWidget(self.combo_ev)

        self.lay.addLayout(self.lay_options)
        
        """
        Tableau Ev, postes, fatigue
        """
        self.setup_table()
        #self.filtrer_joueurs()

    def setup_table(self):
        self.hlabels = ['Nom', 'EV', 'Poste 1', 'Poste 2', 'Poste 3', 'C', 'D']
        self.table = QtGui.QTableWidget(len(self.selected_joueurs),
                                        len(self.hlabels))
        self.table.setHorizontalHeaderLabels(self.hlabels)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #self.table.setSortingEnabled(True)

        for ii, jj in enumerate(self.selected_joueurs):

            st_ev = '%0.2f' % jj.EV if self.poste_filtre in ('all', 'compo') \
                    else '%0.2f' % s.calc_EV(jj, self.poste_filtre,
                                             fatigue=self.fatigue)
            
            if jj.blessure == 0:
                lab = QtGui.QTableWidgetItem(jj.nom)
            else: #jj.blessure > 0
                lab = QtGui.QTableWidgetItem(jj.nom + " - " + str(jj.blessure))
            self.table.setItem(ii, 0, lab)
            
            lab = QtGui.QTableWidgetItem(st_ev)
            self.table.setItem(ii, 1, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(jj.postes[1])
            self.table.setItem(ii, 2, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(jj.postes[2])
            self.table.setItem(ii, 3, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(jj.postes[3])
            self.table.setItem(ii, 4, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(str(jj.C))
            self.table.setItem(ii, 5, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(str(jj.D))
            self.table.setItem(ii, 6, MyTableWidgetItem(lab))

        self.lay.addWidget(self.table)

        """
        Connections
        """
        self.table.doubleClicked.connect(self.selectionner_joueur)

        """
        Empecher d'editer les cases
        """
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        """
        Possibilite de trier
        Trier par poste 1 -> le 0 est la pour mettre dans le bon ordre
        """
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(2, 0)

        """
        Cacher les verticalHeaders
        """
        #self.table.verticalHeader().setVisible(False)

    @property
    def selected_joueurs(self):
        #Filtre par postes
        if self.poste_filtre == 'all':
            ll = self.all_joueurs

        elif self.poste_filtre == 'compo':
            ll = []
            for jj in self.all_joueurs:
                comp = self.parent().comp
                if jj.nom in comp.noms_titulaires or \
                   jj.nom in comp.noms_remplacants:
                    ll.append(jj)

        else:
            ll = []
            for jj in self.all_joueurs:
                vals = jj.postes
                if self.poste_filtre in vals or (self.poste_filtre in \
                                                 ("C1", "C2") and \
                                                 ("CE" in vals or \
                                                  "C1" in vals or \
                                                  "C2" in vals)):
                    ll.append(jj)

        #Filtre par ev
        if self.ev_filtre == 'Tous':
            lll = ll
        else:
            lll = []
            ev = int(self.ev_filtre)
            if self.poste_filtre in ('compo', 'all'):
                for jj in ll:
                    if jj.EV >= ev:
                        lll.append(jj)
            else:
                for jj in ll:
                    if s.calc_EV(jj, self.poste_filtre, self.fatigue) >= ev:
                        lll.append(jj)

        return lll

    def filtrer_joueurs(self, poste='Tous', n=0):
        self.lay.removeWidget(self.table)
        self.table.deleteLater()
        #sip.delete(self.table)
        if poste == 'Tous':
            self.poste_filtre = 'all'
        elif poste == 'Compo':
            self.poste_filtre = 'compo'
        else:
            self.poste_filtre = poste
        self.setup_table()
        self.colorer_table()
        if n < 1 and not self.autre is None:
            self.autre.filtrer_joueurs(poste, n=n+1)

    def filtrer_joueurs_ev(self, ev='Tous', n=0):
        self.lay.removeWidget(self.table)
        self.table.deleteLater()
        #sip.delete(self.table)
        self.ev_filtre = ev
        self.setup_table()
        self.colorer_table()
        if n < 1 and not self.autre is None:
            self.autre.filtrer_joueurs_ev(ev, n=n+1)

    def selectionner_joueur(self):
        nom = str(self.table.selectedItems()[0].text()).split(' - ')[0]
        for jj in  self.all_joueurs:
            if jj.nom == nom:
                jj_sel = jj
        self.parent().transferer_joueur(jj_sel, self, self.autre)
        self.filtrer_joueurs(poste=self.poste_filtre)
        self.filtrer_joueurs_ev(ev=self.ev_filtre)

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)

        ajouterAction = QtGui.QAction('Ajouter / enlever de la selection', self)
        ajouterAction.triggered.connect(self.ajouter_mult)
        self.menu.addAction(ajouterAction)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        plotevAction = QtGui.QAction(u'Plot évoltution', self)
        plotevAction.triggered.connect(self.plot_evolution)
        self.menu.addAction(plotevAction)

        if self.changement_poste_joueur_possible:
            changementPosteAction = QtGui.QAction('Changer de poste', self)
            changementPosteAction.triggered.connect(self.changer_poste)
            self.menu.addAction(changementPosteAction)

        self.menu.popup(QtGui.QCursor.pos())
        
    def ajouter_mult(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            for jj in  self.all_joueurs:
                if jj.nom == nom:
                    joueurs.append(jj)

        for jj in joueurs:
            self.parent().transferer_joueur(jj, self, self.autre)

    def afficher_bio(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            for jj in  self.all_joueurs:
                if jj.nom == nom:
                    joueurs.append(jj)

        self.pop = b.BioPopup(joueurs=joueurs, col3=self)
        self.pop.show()

    def plot_evolution(self):
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        #if len(rows) > 1:
        #    raise ValueError("Un seul joueur possible")
        #else:
        joueurs = []
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            #jj = self.parent().selection.get_joueur_from_nom(nom)
            jj = self.get_joueur_from_nom(nom)
            joueurs.append(jj)
        #plot_evolution(joueurs)
        self.pew = PlotEvolutionWidget(joueurs, dat=self.dat)

    def get_joueur_from_nom(self, nom):
        for jj in self.selected_joueurs:
            if jj.nom == nom:
                break
        return jj

    def changer_poste(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            for jj in  self.all_joueurs:
                if jj.nom == nom:
                    joueurs.append(jj)

        for jj in joueurs:
            self.pop = ChangementPostePopup(jj, dat=self.dat, choix_joueurs_selection=self)
            self.pop.show()

    def colorer_table(self):
        dd = dict()
        for ii, jj in enumerate(self.selected_joueurs):
            if not jj.blessure == 0:
                couleur = indian_red
            else:
                couleur = noir
                if jj.est_jeune():
                    couleur = vert
                elif jj.D <= s.date:
                    couleur = rouge
                elif jj.D == s.date + 1:
                    couleur = bleu

            dd[jj.nom] = couleur

        for rr in range(self.table.rowCount()):
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            for cc in range(self.table.columnCount()):
                self.table.item(rr, cc).setTextColor(dd[nom])
