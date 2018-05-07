# -*- coding: cp1252 -*-
from PyQt4 import QtCore, QtGui
from tournoi import exempter_de_match
import selection as s
from noms_all import *

class ExempterPopup(QtGui.QWidget):
    def __init__(self, parent=None, ecran_classement=None, c_ou_s='c', dat=None):
        super(ExempterPopup, self).__init__(parent)
        self.ecran_classement = ecran_classement
        self.c_ou_s = c_ou_s
        self.dat=dat
        self.a_exempter = []

        if self.c_ou_s == 'c':
            self.noms = noms_clubs(self.dat)
        elif self.c_ou_s == 's':
            self.noms = []
            for nom in noms_armees:
                if not nom in ('ULT', 'ULTB', 'Vide'):
                    self.noms.append(nom)
        else:
            raise ValueError(u"c_ou_s doit être 'c' ou 's' !")

        self.clubs = None if self.c_ou_s == 'c' else []
        if self.c_ou_s == 's':
            for nom in noms_clubs(self.dat):
                self.clubs.append(s.charger(nom, 'c'))

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()
        #self.show()

    def setup_ui(self):
        if self.c_ou_s == 'c':
            self.lay_check = QtGui.QHBoxLayout()

            self.lay_vieux_monde = QtGui.QVBoxLayout()
            self.lay_nouveaux_mondes = QtGui.QVBoxLayout()
            self.lay_nord = QtGui.QVBoxLayout()
            self.lay_sud = QtGui.QVBoxLayout()

            for nom in self.noms:
                setattr(self, 'check_'+nom, QtGui.QCheckBox(nom))
                if nom in noms_clubs_vieux_monde:
                    self.lay_vieux_monde.addWidget(getattr(self, 'check_'+nom))
                elif nom in noms_clubs_nouveaux_mondes:
                    self.lay_nouveaux_mondes.addWidget(getattr(self, 'check_'+nom))
                if nom in noms_clubs_nord:
                    self.lay_nord.addWidget(getattr(self, 'check_'+nom))
                if nom in noms_clubs_sud:
                    self.lay_sud.addWidget(getattr(self, 'check_'+nom))

            self.lay_check.addLayout(self.lay_vieux_monde)
            self.lay_check.addLayout(self.lay_nouveaux_mondes)
            self.lay_check.addLayout(self.lay_nord)
            self.lay_check.addLayout(self.lay_sud)

        elif self.c_ou_s == 's':
            self.lay_check = QtGui.QGridLayout()

            for ii, nom in enumerate(self.noms):
                setattr(self, 'check_'+nom, QtGui.QCheckBox(nom))
                self.lay_check.addWidget(getattr(self, 'check_'+nom),
                                         ii%4,
                                         ii/4)

        self.lay.addLayout(self.lay_check)

        self.lay_but = QtGui.QHBoxLayout()

        self.coch_tout = QtGui.QPushButton("Tout selectionner")
        self.coch_tout.clicked.connect(self.cocher_tout)
        self.lay_but.addWidget(self.coch_tout)

        self.decoch_tout = QtGui.QPushButton("Tout deselectionner")
        self.decoch_tout.clicked.connect(self.decocher_tout)
        self.lay_but.addWidget(self.decoch_tout)

        self.lay.addLayout(self.lay_but)

        self.exemp = QtGui.QPushButton("Exempter les equipes selectionnees")
        self.exemp.clicked.connect(self.exempter)
        self.lay.addWidget(self.exemp)

    def exempter(self):
        self.a_exempter = []
        for nom in self.noms:
            check = getattr(self, 'check_'+nom)
            if check.isChecked():
                self.a_exempter.append(nom)
        
        question = "Etes-vous sur de vouloir exempter "
        for ii, nom in enumerate(self.a_exempter):
            if ii < len(self.a_exempter)-1:
                question += nom + ", "
            else:
                question += 'et ' + nom + ' ?'
                
        mb = QtGui.QMessageBox()
        if mb.question(None, "Question", question, "Non", "Oui") == 1:
            for nom in self.a_exempter:
                ll = exempter_de_match(nom,
                                       c_ou_s=self.c_ou_s,
                                       clubs=self.clubs)
                if ll == 0:
                    #Cas c_ou_s == 'c'
                    pass
                else:
                    self.clubs = ll
            if not self.clubs is None:
                for cc in ll:
                    cc.sauvegarder()
            if (not self.ecran_classement is None) and self.c_ou_s == 'c':
                self.ecran_classement.maj()
            self.close()

    def cocher_tout(self):
        for nom in self.noms:
            check = getattr(self, 'check_'+nom)
            check.setChecked(True)

    def decocher_tout(self):
        for nom in self.noms:
            check = getattr(self, 'check_'+nom)
            check.setChecked(False)
