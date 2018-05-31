# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
from numpy.random import shuffle
from transferts_widget import MyTableWidgetItem
from plot_evolution_widget import PlotEvolutionWidget
from match import MyDialog
from couleurs import *
import selection as s
import biopopup as b
import os.path as osp
import pickle

class RecrutementsWidgetNew(QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 dat=None,
                 clubs=[],
                 all_joueurs=[],
                 classements={}):
        """
        classements est un dict qui contient en keys les noms des joueurs et
        en values le classement des propositions qui ont été faites au joueur

        Ces classements sont sous la forme de list
        Chaque item de la liste est un tuple
        (nom_club, val, ms, besoin, tps_laisse)
        """
        super(RecrutementsWidgetNew, self).__init__(parent)
        self.dat = s.lire_date() if dat is None else dat
        self.clubs = clubs
        self.all_joueurs = all_joueurs
        self.classements = classements

        self.charger_ordre_clubs()

        self.dd_joueurs_recrutes = {}
        self.dd_valides_definitivement = {}
        self.dd_temps_passe = {}
        for nom in self.noms_clubs:
            self.dd_valides_definitivement[nom] = False
            self.dd_temps_passe[nom] = {}
            self.dd_joueurs_recrutes[nom] = []

        for nom_joueur, classement in self.classements.items():
            nom_club = classement[0][0]
            self.dd_temps_passe[nom_club][nom_joueur] = 0

        self.idx_club = 0
        self.club = self.clubs[self.idx_club]
        self.joueurs = self.get_joueurs_interesses(self.club.nom)
        self.joueur_recrute_temp = None
        self.refuses = []

        self.setup_ui()

    def setup_ui(self):
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        """
        Nom club, budget, prévision et avertissement
        """
        self.lay_club = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_club)

        self.lab_nom = QtGui.QLabel(self.club.nom)
        self.lay_club.addWidget(self.lab_nom)

        self.lab_budget = QtGui.QLabel("Budget : "+str(self.club.budget))
        couleur = rouge if self.club.budget < 0 else noir
        colorer_qlabel(self.lab_budget, couleur)
        self.lay_club.addWidget(self.lab_budget)

        self.lab_prevision = QtGui.QLabel(u"Prévisions : "+str(self.prevision()))
        self.lay_club.addWidget(self.lab_prevision)

        self.lab_avertissement = QtGui.QLabel("Avertissement : "+\
                                              str(self.club.avertissement))
        couleur = rouge if self.club.avertissement > 1 else noir
        colorer_qlabel(self.lab_avertissement, couleur)
        self.lay_club.addWidget(self.lab_avertissement)

        """
        Nombre de joueurs par poste
        """
        self.lay_nb_joueurs = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_nb_joueurs)

        for poste in sorted(s.limite_poste.keys(), key=lambda pp: s.ordre_postes[pp]):
            if not poste == 'N8':
                st, couleur = self.st_lab_nb_joueurs(poste)
                lab = QtGui.QLabel(st)
                colorer_qlabel(lab, couleur)
                self.lay_nb_joueurs.addWidget(lab)
                setattr(self, 'lab_' + poste, lab)

        """
        Besoins
        """
        self.set_table_besoins()

        #self.lay.addStretch()

        """
        Table des joueurs intéressés
        """
        self.setup_table()

        """
        Bouttons club suivant et valider définitivement
        """
        self.lay_but = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_but)

        self.but_club_suivant = QtGui.QPushButton("Club suivant")
        self.but_club_suivant.clicked.connect(self.club_suivant)
        self.lay_but.addWidget(self.but_club_suivant)

        self.but_valider_definitivement = QtGui.QPushButton(u"Valider définitivement")
        self.but_valider_definitivement.clicked.connect(self.valider_definitivement)
        self.lay_but.addWidget(self.but_valider_definitivement)

    def setup_table(self):
        self.hlabels = ['Nom', 'EV', 'Poste 1', 'Poste 2', 'Poste 3', 'club',
                        u'Création', u'Déclin', 'Besoin', 'VAL', 'MS',
                        'Temps restant', 'Nb propositions']
        self.table = QtGui.QTableWidget(len(self.joueurs),
                                        len(self.hlabels))
        #self.lay.addWidget(self.table)
        self.lay.insertWidget(3, self.table)
        self.table.setHorizontalHeaderLabels(self.hlabels)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        for ii, jj in enumerate(self.joueurs):
            st_ev = '%0.2f' % jj.EV
            kk = 0
            
            lab = QtGui.QTableWidgetItem(jj.nom)
            self.table.setItem(ii, kk, lab)
            kk += 1
            
            lab = QtGui.QTableWidgetItem(st_ev)
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.postes[1])
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.postes[2])
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.postes[3])
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.club)
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(jj.C))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(jj.D))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1

            offre = self.classements[jj.nom][0]
            nom_club, val, ms, besoin, tps_laisse = offre
            
            lab = QtGui.QTableWidgetItem(str(besoin))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1

            lab = QtGui.QTableWidgetItem(str(val))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(ms))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(tps_laisse - \
                                             self.dd_temps_passe[nom_club][jj.nom]))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(len(self.classements[jj.nom])))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1

        """
        Connections
        """
        self.table.doubleClicked.connect(self.recruter)

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

        """
        geometry_besoins = self.table_besoins.geometry()
        geometry = self.table.geometry()
        rect_besoins = geometry_besoins.getRect()
        rect = geometry.getRect()
        self.table.setGeometry(rect_besoins[0]+50, rect[1], rect[2], rect[0])
        #self.table.verticalHeader()setStretchLastSection(True)

        p = QtGui.QSizePolicy()
        #p.setHorizontalPolicy(QtGui.QSizePolicy.Maximum)
        p.setVerticalPolicy(QtGui.QSizePolicy.Maximum)
        p.setHorizontalStretch(3)
        self.table.setSizePolicy(p)
        """

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        compAction = QtGui.QAction(u'Recruter', self)
        compAction.triggered.connect(self.recruter)
        self.menu.addAction(compAction)

        diagAction = QtGui.QAction('Diagramme etoile', self)
        diagAction.triggered.connect(self.diagramme_etoile)
        self.menu.addAction(diagAction)

        plotevAction = QtGui.QAction(u'Plot évoltution', self)
        plotevAction.triggered.connect(self.plot_evolution)
        self.menu.addAction(plotevAction)

        classementAction = QtGui.QAction(u'Voir classement', self)
        classementAction.triggered.connect(self.voir_classement)
        self.menu.addAction(classementAction)

        refuserAction = QtGui.QAction(u'Refuser', self)
        refuserAction.triggered.connect(self.refuser)
        self.menu.addAction(refuserAction)

        self.menu.popup(QtGui.QCursor.pos())

    def afficher_bio(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.get_joueur_from_nom(nom)
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
            joueur = self.get_joueur_from_nom(nom)
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
            jj = self.get_joueur_from_nom(nom)
            joueurs.append(jj)
        self.pew = PlotEvolutionWidget(joueurs)

    def refuser(self):
        rows = []
        joueurs = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.get_joueur_from_nom(nom)
            if jj in self.refuses:
                self.refuses.remove(jj)
            else:
                self.refuses.append(jj)
        self.colorer_table()

    def club_suivant(self):
        if not self.joueur_recrute_temp is None:
            self.dd_joueurs_recrutes[self.joueur_recrute_temp.nom] = self.club.nom

        for jj in self.get_joueurs_interesses(self.club.nom):
            self.dd_temps_passe[self.club.nom][jj.nom] += 1

        for jj in self.refuses:
            self.passer_offre(jj.nom)

        self.idx_club += 1

        if self.idx_club % len(self.clubs) == 0:
            for jj in self.all_joueurs:
                if not jj.nom in self.dd_joueurs_recrutes:
                    nom_club, val, ms, besoin, tps_laisse = self.classements[jj.nom][0]
                    if tps_laisse - self.dd_temps_passe[nom_club][jj.nom] < 0:
                        self.passer_offre(jj.nom)

        self.club = self.clubs[self.idx_club%len(self.clubs)]
        self.joueurs = self.get_joueurs_interesses(self.club.nom)
        self.joueur_recrute_temp = None
        self.refuses = []
        self.maj_labs_club()
        self.maj_table_besoins()
        self.maj_st_nb_joueurs()

        self.maj_table()

    def maj_table(self):
        self.lay.removeWidget(self.table)
        self.setup_table()
        self.colorer_table()

    def get_joueur_from_nom(self, nom):
        for jj in self.all_joueurs:
            if jj.nom == nom:
                break
        return jj

    def recruter(self):
        rows = []
        joueurs = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        if len(rows) > 1:
            raise ValueError(u"Trop de joueurs sélectionnés")
        rr = rows[0]
        nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
        jj = self.get_joueur_from_nom(nom)

        offre = self.classements[jj.nom][0]
        boo = self.recrutement_possible(offre)

        if boo:
            self.joueur_recrute_temp = jj
            self.colorer_table()
            val = self.classements[jj.nom][0][1]
            self.lab_budget.setText("Budget : "+str(self.club.budget-val))
        else:
            dial = MyDialog(u"Recrutement impossible")
            dial.exec_()

    def get_bool_avertissement(self):
        bool_avertissement = True
        nom_club, val, ms, besoin, tps_laisse = offre
        avertissement = self.club.avertissement
        if avertissement >= 2:
            if self.club.budget - val < 0:
                bool_avertissement = False
            else:
                bool_avertissement = True
        elif avertissement == 1:
            if self.club.budget + self.prevision() - val < 0:
                bool_avertissement = False
            else:
                bool_avertissement = True
        else:
            bool_avertissement = True
        return bool_avertissement

    def recrutement_possible(self, offre):
        valide_definitivement = self.dd_valides_definitivement[self.club.nom]

        bool_avertissement = self.get_bool_avertissement()

        print 'valide_definitivement', valide_definitivement
        print 'bool_avertissement', bool_avertissement

        return (not valide_definitivement) and bool_avertissement

    def prevision(self):
        nom_club = self.club.nom
        p = 0
        for jj in self.all_joueurs:
            if jj.club == nom_club and \
               not jj.nom in self.dd_joueurs_recrutes.keys():
                p += jj.VAL
        return p

    def colorer_table(self):
        dd = {}
        for jj in self.joueurs:
            if not self.joueur_recrute_temp is None:
                if jj.nom == self.joueur_recrute_temp.nom:
                    couleur = vert
                else:
                    couleur = blanc
            elif jj in self.refuses:
                couleur = rouge
            else:
                couleur = blanc

            if jj.retraite:
                couleur = gris
            dd[jj.nom] = couleur

        for rr in range(self.table.rowCount()):
            for cc in range(self.table.columnCount()):
                nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
                self.table.item(rr, cc).setBackgroundColor(dd[nom])

    def valider_definitivement(self):
        pass

    def maj_labs_club(self):
        self.lab_nom.setText(self.club.nom)
        self.lab_budget.setText("Budget : "+str(self.club.budget))
        couleur = rouge if self.club.budget < 0 else noir
        colorer_qlabel(self.lab_budget, couleur)
        self.lab_avertissement.setText("Avertissement : "+\
                                       str(self.club.avertissement))
        couleur = rouge if self.club.avertissement > 1 else noir
        colorer_qlabel(self.lab_avertissement, couleur)
        self.lab_prevision.setText(u"Prévisions : "+str(self.prevision()))

    def set_table_besoins(self):
        hlabels = [bes for bes in self.club.besoins]
        for bes in hlabels:
            while hlabels.count(bes) > 1:
                hlabels.remove(bes)
        hlabels.sort(key=lambda tu: s.ordre_postes[tu[0]])                
        self.table_besoins = QtGui.QTableWidget(1, len(hlabels))
        self.table_besoins.setHorizontalHeaderLabels([self.get_st_besoin(hlab) for hlab in hlabels])
        for kk in range(len(hlabels)):
            val = 0
            N = self.club.besoins.count(hlabels[kk])
            for nom in self.get_joueurs_recrutes(self.club.nom):
                offre = self.get_offre(self.club.nom, nom)
                if offre[3] == hlabels[kk]:
                    val += 1
            lab = QtGui.QTableWidgetItem(str(val))
            it = MyTableWidgetItem(lab)
            if val > N:
                couleur = orange
            elif val == N:
                couleur = vert
            elif val > 0:
                couleur = bleu
            else:
                couleur = noir
            it.setTextColor(couleur)
            self.table_besoins.setItem(0, kk, it)

        p = QtGui.QSizePolicy()
        #p.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
        p.setHorizontalPolicy(QtGui.QSizePolicy.Minimum)
        #p.setHorizontalStretch(10)
        self.table_besoins.setSizePolicy(p)

        self.lay.insertWidget(2, self.table_besoins)

        """
        geometry = self.table_besoins.geometry()
        rect = geometry.getRect()
        self.table_besoins.setGeometry(rect[0], rect[1], rect[2], rect[0]+34)
        self.table_besoins.verticalHeader().setStretchLastSection(True)
        """

    def maj_table_besoins(self):
        self.lay.removeWidget(self.table_besoins)
        self.set_table_besoins()

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
        st += ' : ' + str(nb) + ' / ' + str(s.limite_poste[poste])
        couleur = rouge if nb > s.limite_poste[poste] else noir
        return st, couleur

    def get_joueurs_interesses(self, nom_club):
        ll = []
        noms_recrutes = self.dd_joueurs_recrutes.keys()
        for jj in self.all_joueurs:
            classement = self.classements[jj.nom]
            offre_preferee = classement[0]
            if offre_preferee[0] == nom_club and not jj.nom in noms_recrutes:
                ll.append(jj)
        return ll

    def get_joueurs_recrutes(self, nom_club):
        ll = []
        for nom in self.dd_joueurs_recrutes[nom_club]:
            classement = self.classements[nom]
            offre_preferee = classement[0]
            if offre_preferee[0] == nom_club:
                ll.append(jj)
        return ll

    def get_offre(self, nom_club, nom_joueur):
        found = False
        for offre in self.classements[nom_joueur]:
            if offre[0] == nom_club:
                found = True
                break
        if found:
            return offre
        else:
            raise ValueError("Offre de "+nom_club+" pour "+nom_joueur+u" non trouvée")

    def get_st_besoin(self, besoin):
        poste, ev = besoin
        return poste + ' : ' + str(ev)

    def passer_offre(self, nom_joueur):
        ll = self.classements[nom_joueur]
        offre = ll[0]
        nom_club, val, ms, besoin, tps_laisse = offre

        ll.remove(offre)
        ll.append(offre)

        del(self.dd_temps_passe[nom_club][nom_joueur])
        nouvelle_offre = ll[0]
        nom_club, val, ms, besoin, tps_laisse = nouvelle_offre
        self.dd_temps_passe[nom_club][nom_joueur] = 0

    def sauver_ordre_clubs(self):
        with open(s.TRANSFERTS_DIR_NAME(self.dat)+'/ordre_clubs.oc', 'w') as ff:
            pickle.dump(self.noms_clubs, ff)
        print u"Ordre clubs sauvegardé\n"

    def charger_ordre_clubs(self):
        filename = s.TRANSFERTS_DIR_NAME(self.dat)+'/ordre_clubs.oc'
        if osp.isfile(filename):
            with open(filename, 'r') as ff:
                self.noms_clubs = pickle.load(ff)
            self.clubs.sort(key=lambda cc: self.noms_clubs.index(cc.nom))
            print u"Ordre clubs chargé\n"
        else:
            #On tire au hasard l'ordre de passage des clubs
            shuffle(self.clubs)
            self.noms_clubs = [cc.nom for cc in self.clubs]
            print u"Ordre clubs créé\n"
            self.sauver_ordre_clubs()

    def voir_classement(self):
        rows = []
        joueurs = []
        classements = {}
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.get_joueur_from_nom(nom)
            joueurs.append(jj)
            classements[nom] = self.classements[nom]
        C = ClassementOffresDialog(joueurs, classements)
        C.exec_()

class ClassementOffresDialog(QtGui.QDialog):
    def __init__(self, joueurs, classements, parent=None):
        super(ClassementOffresDialog, self).__init__(parent)
        self.joueurs = joueurs
        self.classements = classements

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.lay_joueurs = QtGui.QGridLayout()
        self.lay.addLayout(self.lay_joueurs)

        for nn, jj in enumerate(self.joueurs):
            self.lay_joueurs.addWidget(QtGui.QLabel(jj.nom), 0, 2*nn)

            grid = QtGui.QGridLayout()
            self.lay_joueurs.addLayout(grid, 1, 2*nn)

            for ii, offre in enumerate(self.classements[jj.nom]):
                for kk, it in enumerate(offre):
                    st = str(it)
                    lab = QtGui.QLabel(st)
                    grid.addWidget(lab, ii, kk)

            if not jj == self.joueurs[-1]:
                #self.lay_joueurs.addSpacing(50)
                self.lay_joueurs.addWidget(QtGui.QLabel('\t'), 0, 2*nn+1)

        self.but = QtGui.QPushButton("OK")
        self.but.clicked.connect(self.close)
        self.lay.addWidget(self.but)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Enter):
            self.close()
            event.accept()
        else:
            super(Dialog, self).keyPressEvent(event)
