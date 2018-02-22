from PyQt4 import QtGui, QtCore
import selection as s
import os.path as osp
import sip
import pickle
from date import *
from savefiles import *
from couleurs import *
from biopopup import BioPopup
from choix_joueurs import MyTableWidgetItem


class RecrutementWidget(QtGui.QWidget):
    def __init__(self, parent=None, noms_clubs=s.noms_clubs, dat=None, vague=0):
        super(RecrutementWidget, self).__init__(parent)

        self.dat = dat
        self.vague = vague

        self.noms_clubs = noms_clubs
        self.clubs = []
        self.val_recrutements = {}
        self.recrutements = {}
        for nom in self.noms_clubs:
            self.clubs.append(s.charger(nom, 'c'))
            self.val_recrutements[nom] = 0
            self.recrutements[nom] = {}
        self.club = self.clubs[0]

        self.clubs_saison_suivante = []
        for nom in self.noms_clubs:
            self.clubs_saison_suivante.append(s.charger(nom, 'c', self.dat+1))

        if osp.isfile(TRANSFERTS_DIR_NAME(self.dat)+'/choix' + str(self.vague) + '.prop'):
            self.choix = self.charger_choix()
        else:
            self.choix = {}
        if osp.isfile(TRANSFERTS_DIR_NAME(self.dat)+'/propositions' + str(self.vague) + '.prop'):
            self.propositions, self.val_propositions = self.charger_propositions_et_val()
        else:
            self.propositions, self.val_propositions = {}, {}
            for nom in self.noms_clubs:
                self.propositions[nom] = {}
                self.val_propositions[nom] = 0
        if osp.isfile(TRANSFERTS_DIR_NAME(self.dat)+'/recrutements' + str(self.vague) + '.prop'):
            self.recrutements, self.val_recrutements = self.charger_recrutements_et_val()
        if osp.isfile(TRANSFERTS_DIR_NAME(self.dat)+'/en_attente' + str(self.vague) + '.prop'):
            self.en_attente = self.charger_en_attente()

        self.all_joueurs = []
        for cc in self.clubs:
            for jj in cc.get_all_joueurs():
                if jj.nom in self.choix.keys() and jj.veut_partir:
                    self.all_joueurs.append(jj)
        self.selected_joueurs = []

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()
        self.setup_table()
        self.filtrer_joueurs()

    def setup_ui(self):
        """
        Choix club + infos budget
        """
        self.lay_club = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_club)

        self.combo_club = QtGui.QComboBox()
        #self.combo_club.addItem('Tous')
        for nom in self.noms_clubs:
            self.combo_club.addItem(nom)
        self.combo_club.setCurrentIndex(0)
        self.combo_club.activated['QString'].connect(self.choix_club)
        self.lay_club.addWidget(self.combo_club)

        self.lab_budget = QtGui.QLabel("Budget disponnible :")
        self.lay_club.addWidget(self.lab_budget)

        self.lab_val_budget = QtGui.QLabel(str(self.club.budget))
        self.lay_club.addWidget(self.lab_val_budget)

        self.lab_previsions = QtGui.QLabel(u'Prévisions')
        self.lay_club.addWidget(self.lab_previsions)

        self.lab_val_previsions = QtGui.QLabel(str(self.previsions_club()))
        self.lay_club.addWidget(self.lab_val_previsions)

        self.lab_temps_reel = QtGui.QLabel(u"Temps réel")
        self.lay_club.addWidget(self.lab_temps_reel)

        tps_reel = self.club.budget - self.valeurs_recrutements_club()
        self.lab_val_temps_reel = QtGui.QLabel(str(tps_reel))
        self.lay_club.addWidget(self.lab_val_temps_reel)

        self.lab_avertissement = QtGui.QLabel("Avertissement")
        self.lay_club.addWidget(self.lab_avertissement)

        self.lab_val_avertissement = QtGui.QLabel(str(self.club.avertissement))
        self.lay_club.addWidget(self.lab_val_avertissement)

        """
        Nombre de joueurs par poste
        """
        self.lay_nb_joueurs = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_nb_joueurs)

        for poste in sorted(s.limite_poste.keys(), key=lambda pp: s.ordre_postes[pp]):
            if not poste == 'N8':
                st = self.st_lab_nb_joueurs(poste)
                lab = QtGui.QLabel(st)
                self.lay_nb_joueurs.addWidget(lab)
                setattr(self, 'lab_' + poste, lab)

        """
        Bouttons
        """
        self.lay_buts = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_buts)

        self.but_sauver = QtGui.QPushButton("Sauvegarder recrutements")
        self.but_sauver.clicked.connect(self.sauvegarder_recrutements)
        self.lay_buts.addWidget(self.but_sauver)

        self.but_effectuer = QtGui.QPushButton("Effectuer transferts")
        self.but_effectuer.clicked.connect(self.effectuer_transferts)
        self.lay_buts.addWidget(self.but_effectuer)

    def setup_table(self):
        self.labs = ['nom', u'Club départ', 'EV', 'Poste 1', 'Poste 2',
                     'Poste 3', 'VAL proposition', 'MS proposition', 'Besoin']
        numlin = len(self.selected_joueurs)
        numcol = len(self.labs)
        self.table = QtGui.QTableWidget(numlin, numcol)
        self.table.setHorizontalHeaderLabels(self.labs)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        for ii, jj in enumerate(self.selected_joueurs):
            proposition = self.propositions[self.club.nom][jj.nom]
            val, ms, bes = proposition
            poste = bes[0]

            it = QtGui.QTableWidgetItem(jj.nom)
            self.table.setItem(ii, 0, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(jj.club)
            self.table.setItem(ii, 1, MyTableWidgetItem(it))

            st_ev = str(round(s.calc_EV(jj, poste, fatigue=False), 2))
            it = QtGui.QTableWidgetItem(st_ev)
            self.table.setItem(ii, 2, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(jj.postes[1])
            self.table.setItem(ii, 3, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(jj.postes[2])
            self.table.setItem(ii, 4, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(jj.postes[3])
            self.table.setItem(ii, 5, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(str(val))
            self.table.setItem(ii, 6, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(str(ms))
            self.table.setItem(ii, 7, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(str(bes))
            self.table.setItem(ii, 8, MyTableWidgetItem(it))

        self.lay.addWidget(self.table)

        """
        Connection
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
        self.table.sortByColumn(3, 0)

        """
        Colorer table
        """
        self.colorer_table()

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

        numcol = self.table.columnCount()
        for rr in range(self.table.rowCount()):
            nom = str(self.table.item(rr, 0).text())
            for cc in range(numcol):
                if not self.table.item(rr, cc) is None:
                    self.table.item(rr, cc).setTextColor(dd[nom])
            if nom in self.recrutements[self.club.nom].keys():
                for cc in range(numcol):
                    if not self.table.item(rr, cc) is None:
                        self.table.item(rr, cc).setBackground(QtGui.QColor(0, 255, 0))

    def st_lab_nb_joueurs(self, poste):
        st = poste
        nb = len(self.club.joueurs[poste])
        if poste == 'TL':
            st = 'TL / N8'
            nb += len(self.club.joueurs['N8'])
        st += ' : ' + str(nb) + ' / ' + str(s.limite_poste[poste])
        return st

    def choix_club(self, nom):
        nom = str(self.combo_club.currentText())
        cc = self.clubs[self.noms_clubs.index(nom)]
        self.club = cc
        self.lab_val_budget.setText(str(cc.budget))
        if cc.budget < 0:
            self.lab_val_budget.setStyleSheet('color: red')
        else:
            self.lab_val_budget.setStyleSheet('color: black')

        tps_reel = self.club.budget - self.valeurs_recrutements_club()
        self.lab_val_temps_reel.setText(str(tps_reel))
        if tps_reel < 0:
            self.lab_val_temps_reel.setStyleSheet('color: red')
        else:
            self.lab_val_temps_reel.setStyleSheet('color: black')

        self.lab_val_previsions.setText(str(self.previsions_club()))

        for poste in s.limite_poste.keys():
            if not poste == 'N8':
                lab = getattr(self, 'lab_'+poste)
                st = self.st_lab_nb_joueurs(poste)
                lab.setText(st)

        self.filtrer_joueurs()

        self.maj()

    def filtrer_joueurs(self):
        self.selected_joueurs = []
        for jj in self.all_joueurs:
            if self.choix[jj.nom][0].nom == self.club.nom:
                self.selected_joueurs.append(jj)

    def maj(self):
        tps_reel = self.club.budget - self.valeurs_recrutements_club()
        self.lab_val_temps_reel.setText(str(tps_reel))
        if tps_reel < 0:
            self.lab_val_temps_reel.setStyleSheet('color: red')

        self.lay.removeWidget(self.table)
        sip.delete(self.table)
        self.setup_table()

    def previsions_club(self):
        res = 0
        for jj in self.all_joueurs:
            if jj.club == self.club.nom:
                res += jj.VAL
        return res

    def valeurs_recrutements_club(self):
        return self.val_recrutements[self.club.nom]

    def recruter(self):
        selected_idx = self.table.selectedIndexes()
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        if len(rows) > 1:
            raise ValueError("""On ne peut recruter les joueurs que 1 par 1\n
                             Ici plusieurs joueurs selectionnés :\n
                             len(rows) = """+str(len(selected_idx)))
        rr = rows[0]

        nom = str(self.table.item(rr, 0).text())
        nom_club = str(self.table.item(rr, 1).text())
        self.recrutements[self.club.nom][nom] = self.propositions[self.club.nom][nom]
        if not nom_club == self.club.nom:
            self.val_recrutements[self.club.nom] += self.propositions[self.club.nom][nom][0]

        #self.maj()

        numcol = self.table.columnCount()
        for cc in range(numcol):
            self.table.item(rr, cc).setBackground(QtGui.QColor(0, 255, 0))
        tps_reel = self.club.budget - self.valeurs_recrutements_club()
        self.lab_val_temps_reel.setText(str(tps_reel))

    def effectuer_transferts(self):
        mb = QtGui.QMessageBox()
        if mb.question(None,
                       "Question",
                       u"""Effectuer les transferts ?\n
                           Attention, plus de retour posible !"""
                       , "Non", "Oui") == 1:
            self.en_attente = []
            for jj in self.all_joueurs:
                cc, val, ms, poste =  self.choix[jj.nom]
                if jj.nom in self.recrutements[cc.nom]:
                    cc_old = self.clubs_saison_suivante[self.noms_clubs.index(jj.club)]
                    if jj.club == cc.nom:
                        cc_old.masse_salariale -= jj.MS
                        cc_old.masse_salariale += ms
                        jj.MS = ms
                    else:
                        cc_new = self.clubs_saison_suivante[self.noms_clubs.index(cc.nom)]
                        try:
                            s.transfert(jj.nom, cc_old, cc_new, val, ms)
                        except ValueError:
                            self.en_attente.append((jj, self.choix[jj.nom]))

            for cc in self.clubs_saison_suivante:
                cc.sauvegarder(dat=self.dat+1)

            self.sauvegarder_en_attente()

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        diagAction = QtGui.QAction('Diagramme etoile', self)
        diagAction.triggered.connect(self.diagramme_etoile)
        self.menu.addAction(diagAction)

        propAction = QtGui.QAction('Recruter', self)
        propAction.triggered.connect(self.recruter)
        self.menu.addAction(propAction)

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
            nom_club = str(self.table.item(rr, 1).text()).split(" - ")[0]
            cc = self.clubs[self.noms_clubs.index(nom_club)]
            jj = cc.get_joueur_from_nom(nom)
            joueurs.append(jj)
        
        self.pop = BioPopup(joueurs=joueurs, col3=self, fatigue=False, dat=self.dat)
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
            nom_club = str(self.table.item(rr, 1).text()).split(" - ")[0]
            cc = self.clubs[self.noms_clubs.index(nom_club)]
            joueur = cc.get_joueur_from_nom(nom)
            joueurs.append(joueur)
            TO.append(joueur.caracs_sans_fatigue['TO'])
            TB.append(joueur.caracs_sans_fatigue['TB'])
            TA = TA or 'TA' in joueur.postes
            AV = AV or s.est_un_avant(joueur)
        label_TO = True if max(TO) >= 8 and AV \
                   else False
        label_TA = True if TA \
                   else False
        label_TB = True if max(TB) >= 8 \
                   else False
        
        for nn, jj in enumerate(joueurs):
            texte = True if nn == 0 else False
            jj.diagramme_etoile(texte=texte,
                                label_TO=label_TO,
                                label_TA=label_TA,
                                label_TB=label_TB)

    def charger_propositions_et_val(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/propositions' + str(self.vague) + '.prop', 'r') as ff:
            prop = pickle.load(ff)
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/val_propositions' + str(self.vague) + '.prop', 'r') as ff:
            val = pickle.load(ff)
        return prop, val

    def charger_recrutements_et_val(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/recrutements' + str(self.vague) + '.prop', 'r') as ff:
            recrutements = pickle.load(ff)
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/val_recrutements' + str(self.vague) + '.prop', 'r') as ff:
            val = pickle.load(ff)
        return recrutements, val

    def charger_choix(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/choix' + str(self.vague) + '.prop', 'r') as ff:
            choix = pickle.load(ff)
        return choix

    def charger_en_attente(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/en_attente' + str(self.vague) + '.prop', 'r') as ff:
            en_attente = pickle.load(ff)
        return en_attente

    def sauvegarder_recrutements(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/recrutements' + str(self.vague) + '.prop', 'w') as ff:
            choix = pickle.dump(self.recrutements, ff)
        print u"Recrutements sauvegardés"
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/val_recrutements' + str(self.vague) + '.prop', 'w') as ff:
            choix = pickle.dump(self.val_recrutements, ff)
        print u"Valeurs recrutements sauvegardées"

    def sauvegarder_en_attente(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/en_attente' + str(self.vague) + '.prop', 'w') as ff:
            choix = pickle.dump(self.en_attente, ff)
        print u"Transferts en attente sauvegardés"
