from PyQt4 import QtGui, QtCore
from match import MatchWidget
from noms_all import *

class MatchSelectionWidget(MatchWidget):
    def __init__(self, saison, parent=None, ecran_precedant=None):
        super(MatchSelectionWidget, self).__init__(saison=saison,
                                                   parent=parent,
                                                   ecran_precedant=ecran_precedant,
                                                   c_ou_s='s')

        self.c_ou_s = 's'
        self.update_ui()

    def update_ui(self):
        """
        for cc in (self.col_eq1.col1, self.col_eq2.col1):
            for ii in range(cc.combo.count()):
                cc.combo.removeItem(0)
            for nom in noms_armees:
                cc.combo.addItem(nom)
        """

        ma = self.col_match
        ma.rad_championat.setChecked(False)
        ma.rad_championat.hide()
        ma.rad_coupe.setChecked(False)
        ma.rad_coupe.hide()

        ma.check_coupe_monde.show()
