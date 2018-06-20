# -*- coding: cp1252 -*-
from PyQt4 import QtCore, QtGui
from ui.choix_joueurs import MyTableWidgetItem
from plot_evolution_widget import PlotEvolutionWidget
from couleurs import *
from diagramme_joueurs_widget import DiagrammeJoueursWidget
import selection as s
import biopopup as b
import os.path as osp
import sip
import json

class EspoirsWidget(QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 clubs=[],
                 dat=None):
        super(EspoirsWidget, self).__init__(parent)
        self.dat = s.lire_date() if dat is None else dat
        self.clubs = clubs
        self.noms_clubs = [cc.nom for cc in self.clubs]

        self.club = self.clubs[0]
        self.joueurs = self.club.joueurs['espoirs']

        self.charger_decisions(self.club.nom)

        self.setup_ui()

    def setup_ui(self):
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        """
        Choix club & Nombre de joueurs par poste & Boutton sauvegarder
        """
        self.lay_nb_joueurs = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_nb_joueurs)

        self.combo_club = QtGui.QComboBox()
        for nom in self.noms_clubs:
            self.combo_club.addItem(nom)
        self.combo_club.setCurrentIndex(0)
        self.combo_club.activated['QString'].connect(self.choix_club)
        self.lay_nb_joueurs.addWidget(self.combo_club)

        self.but_sauvegarder = QtGui.QPushButton(u"Sauvegarder décisions")
        self.but_sauvegarder.clicked.connect(self.sauvegarder_decisions)
        self.lay_nb_joueurs.addWidget(self.but_sauvegarder)

        for poste in sorted(s.limite_poste.keys(), key=lambda pp: s.ordre_postes[pp]):
            if not poste == 'N8':
                st, couleur = self.st_lab_nb_joueurs(poste)
                lab = QtGui.QLabel(st)
                colorer_qlabel(lab, couleur)
                self.lay_nb_joueurs.addWidget(lab)
                setattr(self, 'lab_' + poste, lab)

        self.but_effectuer = QtGui.QPushButton("Effectuer les changements")
        self.but_effectuer.clicked.connect(self.effectuer_changements)
        self.lay_nb_joueurs.addWidget(self.but_effectuer)

        self.setup_table()
        self.colorer_table()

    def setup_table(self):
        self.hlabels = ['Nom', 'EV', 'Poste 1', 'Poste 2', 'Poste 3',
                        u'Création', u'Déclin', 'Rang', 'Rang Max',
                        u'Matches joués', 'Total']
        self.table = QtGui.QTableWidget(len(self.joueurs),
                                        len(self.hlabels))
        self.lay.addWidget(self.table)
        self.table.setHorizontalHeaderLabels(self.hlabels)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #self.table.setSortingEnabled(True)

        for ii, jj in enumerate(self.joueurs):
            st_ev = '%0.2f' % jj.EV
            
            lab = QtGui.QTableWidgetItem(jj.nom)
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
            
            lab = QtGui.QTableWidgetItem(jj.RG.rang)
            self.table.setItem(ii, 7, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(jj.RG_max.rang)
            self.table.setItem(ii, 8, MyTableWidgetItem(lab))

            st, st_tot = self.matches_joues(jj)
            
            lab = QtGui.QTableWidgetItem(st)
            self.table.setItem(ii, 9, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(st_tot)
            self.table.setItem(ii, 10, MyTableWidgetItem(lab))

        """
        Connections
        """
        self.table.doubleClicked.connect(self.decider)

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

        """
        Resize
        """
        #self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def choix_club(self, nom):
        nom = str(self.combo_club.currentText())
        cc = self.clubs[self.noms_clubs.index(nom)]
        self.club = cc
        self.joueurs = self.club.joueurs['espoirs']

        self.charger_decisions(self.club.nom)

        self.maj()

    def maj(self):
        for poste in s.limite_poste.keys():
            if not poste == 'N8':
                lab = getattr(self, 'lab_'+poste)
                st, couleur = self.st_lab_nb_joueurs(poste)
                lab.setText(st)
                colorer_qlabel(lab, couleur)

        self.lay.removeWidget(self.table)
        #sip.delete(self.table)

        self.setup_table()
        self.colorer_table()

        self.maj_st_nb_joueurs()

    def colorer_table(self):
        dd = {}
        for jj in self.joueurs:
            if jj in self.passent_pro:
                couleur = vert
            elif jj in self.partent:
                couleur = rouge
            else:
                couleur = noir
            dd[jj.nom] = couleur

        for rr in range(self.table.rowCount()):
            for cc in range(self.table.columnCount()):
                nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
                self.table.item(rr, cc).setTextColor(dd[nom])

    def maj_st_nb_joueurs(self):
        for poste in sorted(s.limite_poste.keys(), key=lambda pp: s.ordre_postes[pp]):
            if not poste == 'N8':
                st, couleur = self.st_lab_nb_joueurs(poste)
                lab = getattr(self, 'lab_' + poste)
                lab.setText(st)
                colorer_qlabel(lab, couleur)

    def st_lab_nb_joueurs(self, poste):
        st = poste
        nb = len(self.club.joueurs[poste])
        if poste == 'TL':
            st = 'TL / N8'
            nb += len(self.club.joueurs['N8'])
        if not poste == 'espoirs':
            for jj in self.passent_pro:
                if jj.postes[1] == poste or \
                   (jj.postes[1] in ('TL', 'N8') and poste in ('TL', 'N8')):
                        nb += 1
        else:
            for jj in self.passent_pro + self.partent:
                nb -= 1
        st += ' : ' + str(nb) + ' / ' + str(s.limite_poste[poste])
        couleur = rouge if nb > s.limite_poste[poste] else noir
        return st, couleur

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        compAction = QtGui.QAction(u'Décider', self)
        compAction.triggered.connect(self.decider)
        self.menu.addAction(compAction)

        diagAction = QtGui.QAction('Diagramme etoile', self)
        diagAction.triggered.connect(self.diagramme_etoile)
        self.menu.addAction(diagAction)

        plotevAction = QtGui.QAction(u'Plot évoltution', self)
        plotevAction.triggered.connect(self.plot_evolution)
        self.menu.addAction(plotevAction)

        self.menu.popup(QtGui.QCursor.pos())

    def decider(self):
        rows = []
        joueurs = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.club.get_joueur_from_nom(nom)
            joueurs.append(jj)

        for jj in joueurs:
            dw = DecisionWidget(jj, parent=self)
            res = dw.exec_()
            
            if res == 1:
                if dw.rad_partir.isChecked():
                    arrivee = self.partent
                elif dw.rad_pro.isChecked():
                    arrivee = self.passent_pro
                else:
                    arrivee =  self.restent_espoirs

                if jj in self.restent_espoirs:
                    depart = self.restent_espoirs
                elif jj in self.passent_pro:
                    depart = self.passent_pro
                elif jj in self.partent:
                    depart = self.partent

                if arrivee == depart:
                    pass
                else:
                    arrivee.append(jj)
                    depart.remove(jj)
            else:
                pass
            

        self.maj()

    def afficher_bio(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.club.get_joueur_from_nom(nom)
            joueurs.append(jj)
        
        self.pop = b.BioPopup(joueurs=joueurs, col3=self, fatigue=False)
        self.pop.show()

    def diagramme_etoile(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)

        TA = False
        TB = []
        TO = []
        AV = False
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            joueur = self.club.get_joueur_from_nom(nom)
            joueurs.append(joueur)
            TO.append(joueur.caracs_sans_fatigue['TO'])
            TB.append(joueur.caracs_sans_fatigue['TB'])
            TA = TA or 'TA' in joueur.postes
            AV = AV or est_un_avant(joueur)
        label_TO = True if max(TO) >= 8 and AV \
                   else False
        label_TA = True if TA \
                   else False
        label_TB = True if max(TB) >= 8 \
                   else False
        self.djw = DiagrammeJoueursWidget(joueurs,
                                     label_TO=label_TO,
                                     label_TA=label_TA,
                                     label_TB=label_TB)

    def plot_evolution(self):
        rows = []
        joueurs = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.club.get_joueur_from_nom(nom)
            joueurs.append(jj)
        self.pew = PlotEvolutionWidget(joueurs)

    def matches_joues(self, jj):
        st = ""
        tot_tit_club = 0
        tot_club = 0
        for ii in (1, 2, 3):
            dd = getattr(jj, "MJ"+str(ii))
            poste = jj.postes[ii]
            if not poste == "":
                st += poste + " " + str(dd['CT'] + dd['CR']) + ' (' + \
                      str(dd['CT']) + ')'
                if ii < 3:
                    st += '\n'
                tot_club += dd['CT'] + dd['CR']
                tot_tit_club += dd['CT']
                st_tot_club = str(tot_club) + ' (' + str(tot_tit_club) + ')'
        return st, st_tot_club

    def sauvegarder_decisions(self):
        dirname = s.TRANSFERTS_DIR_NAME(self.dat)
        dd = {}
        for jj in self.restent_espoirs:
            dd[jj.nom] = 'espoir'
        for jj in self.passent_pro:
            dd[jj.nom] = 'pro'
        for jj in self.partent:
            dd[jj.nom] = 'part'
        with open(dirname+'/'+self.club.nom+'_espoirs.txt', 'w') as ff:
            json.dump(dd, ff)

    def charger_decisions(self, nom_club):
        self.passent_pro = []
        self.restent_espoirs = []
        self.partent = []
        dirname = s.TRANSFERTS_DIR_NAME(self.dat)
        filename = dirname+'/'+nom_club+'_espoirs.txt'
        if osp.isfile(filename):
            with open(filename, 'r') as ff:
                dd = json.load(ff)
            for jj in self.joueurs:
                if dd[jj.nom] == 'espoir':
                    self.restent_espoirs.append(jj)
                elif dd[jj.nom] == 'pro':
                    self.passent_pro.append(jj)
                elif dd[jj.nom] == 'part':
                    self.partent.append(jj)
                else:
                    raise ValueError("Mauvaise valeur pour "+jj.nom+" dans "+filename)
        else:
            self.restent_espoirs = [jj for jj in self.joueurs]
            self.passent_pro = []
            self.partent = []

    def effectuer_changements(self):
        mb = QtGui.QMessageBox()
        if mb.question(None,
                       "Question",
                       "Effectuer les changements puis fermer ?",
                       "Non",
                       "Oui") == 1:
            dd = {}
            for nom in self.noms_clubs:
                self.club = self.clubs[self.noms_clubs.index(nom)]
                dirname = s.TRANSFERTS_DIR_NAME(self.dat)
                filename = dirname+'/'+nom+'_espoirs.txt'
                if osp.isfile(filename):
                    with open(filename, 'r') as ff:
                        dd[nom] = json.load(ff)
                #self.charger_decisions(nom)
                #print self.passent_pro

                for jj in self.club.joueurs['espoirs']:
                    if dd[nom][jj.nom] == 'pro':
                        print jj.nom, 'passe pro'
                        poste = 'CE' if jj.postes[1] in ('C1', 'C2') else jj.postes[1]
                        self.club.joueurs[poste].append(jj)
                        self.club.joueurs['espoirs'].remove(jj)
                        jj.passage_pro = self.dat
                    elif dd[nom][jj.nom] == 'part':
                        print jj.nom, 'part'
                        jj.veut_partir = True
                self.club.sauvegarder()
            self.close()

class DecisionWidget(QtGui.QDialog):
    def __init__(self, joueur, parent=None):
        super(DecisionWidget, self).__init__(parent)
        self.joueur = joueur

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.lay_rad = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_rad)

        self.rad_partir = QtGui.QRadioButton('Partir')
        self.lay_rad.addWidget(self.rad_partir)

        self.rad_espoir = QtGui.QRadioButton('Rester espoir')
        self.rad_espoir.setChecked(True)
        self.lay_rad.addWidget(self.rad_espoir)

        self.rad_pro = QtGui.QRadioButton('Passer pro')
        self.lay_rad.addWidget(self.rad_pro)

        self.lay_but = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_but)

        self.but_no = QtGui.QPushButton('Annuler')
        self.lay_but.addWidget(self.but_no)
        self.but_no.clicked.connect(self.reject)

        self.but_yes = QtGui.QPushButton('Valider')
        self.lay_but.addWidget(self.but_yes)
        self.but_yes.clicked.connect(self.accept)

