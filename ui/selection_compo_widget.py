import selection as s
from PyQt4 import QtGui, QtCore
from choix_joueurs import ChoixJoueursWidget
from interface_qt import InterfaceWidget
from noms_all import *

class SelectionCompoWidget(InterfaceWidget):#QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 selection=s.selection(),
                 saison=None,
                 ecran_precedant=None):
        super(SelectionCompoWidget, self).__init__(parent,
                                                   saison=saison,
                                                   c_ou_s='s')
        self.set_club(selection.nom)
        self.ecran_precedant=ecran_precedant
        self.update_ui()

    def update_ui(self):
        """
        Fait les changements necessaires dans l'ui
        """

        """
        col1
        """
        c1 = self.col1
        for ii in range(c1.combo.count()):
            c1.combo.removeItem(0)
        for nom in noms_armees:
            if nom == c1.club.nom:
                c1.combo.insertItem(0, nom)
                c1.combo.setCurrentIndex(0)
            else:
                c1.combo.addItem(nom)

    def charger(self, nom):
        """
        Charge un club ou une selection
        La fonction est re ecrite pour la classe SelectionCompoWidget
        """
        return s.charger(nom, 's')

"""

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()

    def setup_ui(self):
        self.col3 = ChoixJoueursWidget(club=self.selection)
        self.lay.addWidget(self.col3)

class ChoixJoueursSelectionCompoWidget(ChoixJoueursWidget):
    def __init__(self, parent=None, selection=s.selection, poste_filtre='all'):
        super(ChoixJoueursSelectionCompoWidget, self).__init__(parent, club=selection)
        self.poste_filtre = poste_filtre
"""
