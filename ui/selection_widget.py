import selection as s
import os.path as osp
from PyQt4 import QtGui, QtCore
from choix_joueurs_selection import *
from savefiles import *

class SelectionWidget(QtGui.QWidget):
    def __init__(self, parent=None, ecran_precedant=None, dat=None):
        super(SelectionWidget, self).__init__(parent)
        self.ecran_precedant = ecran_precedant
        self.dat = s.mire_date() if dat is None else dat

        self.points_selection = 0.

        self.joueurs_choix = []
        self.joueurs_choisis = []
        self.selection = s.selection()
        self.nom = ""
        self.poste_filtre_choix = 'all'
        self.poste_filtre_choisis = 'all'
        self.ev_filtre_choix = 'Tous'
        self.ev_filtre_choisis = 'Tous'

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.choix = ChoixJoueursSelectionWidget(autre=None,
                                                 parent=None,
                                                 joueurs=self.joueurs_choix,
                                                 poste_filtre=self.poste_filtre_choix,
                                                 ev_filtre=self.ev_filtre_choix,
                                                 fatigue=False)
        self.lay.addWidget(self.choix)

        self.milieu = MilieuWidget(parent=self)
        self.lay.addWidget(self.milieu)

        self.choisis = ChoixJoueursSelectionWidget(autre=None,
                                                   parent=None,
                                                   joueurs=self.joueurs_choisis,
                                                   poste_filtre=self.poste_filtre_choisis,
                                                   ev_filtre=self.ev_filtre_choisis,
                                                   fatigue=False)
        self.lay.addWidget(self.choisis)
        self.choisis.autre = self.choix
        self.choix.autre = self.choisis


    def clean_ui(self):
        self.lay.removeWidget(self.choix)
        self.choix.deleteLater()

        self.lay.removeWidget(self.choisis)
        self.choisis.deleteLater()

        self.lay.removeWidget(self.milieu)
        self.milieu.deleteLater()

    def maj(self):
        self.clean_ui()
        self.setup_ui()

    def choix_armee(self, arm):
        self.joueurs_choix = s.get_joueurs_all(arm, self.dat)
        self.joueurs_choisis = []
        self.nom = self.milieu.combo_armees.currentText()
        if self.nom == 'ULTB' and osp.isfile(SELECTIONS_DIR_NAME() + '/ULT/ULT.sel'):
            ult = s.charger('ULT', 's')
            self.joueurs_exclus = ult.joueurs
        else:
            self.joueurs_exclus = []
        if osp.isfile(SELECTIONS_DIR_NAME() + "/" + self.nom + '/' + self.nom + ".sel"):
            self.selection = s.charger(self.nom, 's')
            self.points_selection = self.selection.points
            self.joueurs_choisis = self.selection.joueurs
            for jj in self.joueurs_choisis + self.joueurs_exclus:
                for jj2 in self.joueurs_choix:
                    if jj.nom == jj2.nom:
                        self.joueurs_choix.remove(jj2)
        self.maj()

    def transferer_joueur(self, jj, source, cible):
        self.poste_filtre_choix = self.choix.poste_filtre
        self.poste_filtre_choisis = self.choisis.poste_filtre
        self.ev_filtre_choix = self.choix.ev_filtre
        self.ev_filtre_choisis = self.choisis.ev_filtre
        if jj in self.joueurs_choix:
            self.joueurs_choix.remove(jj)
            self.joueurs_choisis.append(jj)
        else:
            self.joueurs_choix.append(jj)
            self.joueurs_choisis.remove(jj)
        self.maj()

class MilieuWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MilieuWidget, self).__init__(parent)
        self.lay_milieu = QtGui.QVBoxLayout()
        self.setLayout(self.lay_milieu)

        """
        Combo pour choix de l'armee
        """
        self.combo_armees = QtGui.QComboBox()
        if self.parent().nom == "":
            for nom in s.noms_armees:
                if nom == self.parent().nom:
                    self.combo_armees.insertItem(0, nom)
                    self.combo_armees.setCurrentIndex(0)
                else:
                    self.combo_armees.addItem(nom)
        else:
            self.combo_armees.addItem(self.parent().nom)
            for nom in s.noms_armees:
                if nom != self.parent().nom:
                    self.combo_armees.addItem(nom)
        self.combo_armees.activated['QString'].connect(self.parent().choix_armee)
        self.lay_milieu.addWidget(self.combo_armees)

        """
        Boutton pour sauvegarder
        """
        self.but_sauver = QtGui.QPushButton("Sauvegarder Selection")
        self.but_sauver.clicked.connect(self.sauvegarder_selection)
        self.lay_milieu.addWidget(self.but_sauver)

        """
        Boutton pour reinitialiser
        """
        self.but_reset = QtGui.QPushButton("Reinitialiser")
        self.but_reset.clicked.connect(self.reset)
        self.lay_milieu.addWidget(self.but_reset)

        """
        Boutton pour faire la compo
        """
        self.but_compo = QtGui.QPushButton("Faire la compo")
        self.but_compo.clicked.connect(self.ouvrir_ecran_compo)
        self.lay_milieu.addWidget(self.but_compo)

        """
        Boutton retour
        """
        if not self.parent().ecran_precedant is None:
            self.but_retour = QtGui.QPushButton("Retour a l'ecran precedant")
            self.but_retour.clicked.connect(self.retour)
            self.lay_milieu.addWidget(self.but_retour)

    def sauvegarder_selection(self):
        dial = SauvegarderDialog(parent=self, arm=self.combo_armees.currentText())
        dial.exec_()
        if dial.ok:
            self.selection = s.selection(nom=str(self.combo_armees.currentText()),
                                         joueurs=self.parent().joueurs_choisis)
            self.selection.points = self.points_selection
            self.selection.sauvegarder()

    def reset(self):
        self.parent().joueurs_choisis = []
        self.parent().joueurs_choix = s.get_joueurs_all(self.parent().nom)
        if self.parent().nom == 'ULTB' \
           and osp.isfile(SELECTIONS_DIR_NAME() + '/ULT/ULT.sel'):
            ult = s.charger('ULT', 's')
            self.parent().joueurs_exclus = ult.joueurs
        else:
            self.parent().joueurs_exclus = []
        self.parent().maj()

    def ouvrir_ecran_compo(self):
        self.parent().hide()
        self.parent().parent().selection_compo_widget.ecran_precedant = self.parent()
        self.parent().parent().selection_compo_widget.show()
        self.parent().parent().selection_compo_widget.set_club(self.parent().selection.nom)
        self.parent().parent().selection_compo_widget.compo.nom = self.parent().selection.nom + '_defaut'

    def retour(self):
        self.parent().hide()
        self.parent().parent().selection_compo_widget.ecran_precedant = self.parent().parent().wid_aux
        self.parent().ecran_precedant.show()

class SauvegarderDialog(QtGui.QDialog):
    def __init__(self, parent=None, arm=""):
        super(SauvegarderDialog, self).__init__(parent)
        self.arm = arm
        self.ok = False
        
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle("Sauvegarder")

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        """
        Entrer le nom
        """
        self.lay_quest = QtGui.QHBoxLayout()
        
        self.lab = QtGui.QLabel("Sauvegarder sous :")
        self.lay_quest.addWidget(self.lab)
        
        self.edit = QtGui.QLineEdit(self.arm)
        self.lay_quest.addWidget(self.edit)
        
        self.lab2 = QtGui.QLabel(".sel")
        self.lay_quest.addWidget(self.lab2)
        
        self.lay.addLayout(self.lay_quest)

        """
        Bouttons pour valider ou annuler
        """
        self.lay_but = QtGui.QHBoxLayout()
        self.but_annuler = QtGui.QPushButton("Annuler")
        self.but_annuler.clicked.connect(self.annuler)
        self.lay_but.addWidget(self.but_annuler)

        self.but_ok = QtGui.QPushButton("OK")
        self.but_ok.clicked.connect(self.valider)
        self.lay_but.addWidget(self.but_ok)

        self.lay.addLayout(self.lay_but)

    def annuler(self):
        self.close()

    def valider(self):
        self.ok = True
        self.accept()
        
