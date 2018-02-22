import match as m
import ecran_accueil as ea
import ecran_club as ec
import ecran_selection as es
from PyQt4 import QtGui, QtCore

class MasterWidget(QtGui.QWidget):
    def __init__(self, dat=None, parent=None):
        super(MasterWidget, self).__init__(parent)
        self.dat = dat

        self.set_ui()

        self.ecran_precedant = self.ecran_accueil

    def set_ui(self):
        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.ecran_accueil = ea.EcranAccueilWidget(parent=self)
        self.lay.addWidget(self.ecran_accueil)

        nom_saison_c = None if self.dat is None \
                       else 'saison_' + str(self.dat) + '_c'
        self.ecran_club = ec.EcranClubWidget(parent=self,
                                            ecran_precedant=self.ecran_accueil,
                                             nom_saison=nom_saison_c)
        self.lay.addWidget(self.ecran_club)
        self.ecran_club.hide()
        """
        self.match_amical_widget = m.MatchWidget(parent=self)
        self.match_amical_widget.ecran_precedant = self.ecran_accueil
        self.lay.addWidget(self.match_amical_widget)
        self.match_amical_widget.hide()

        self.match_widget = m.MatchWidget(parent=self)
        self.match_widget.ecran_precedant = self.ecran_classement
        self.lay.addWidget(self.match_widget)
        self.match_widget.hide()
        
        self.interface_widget = m.iqt.InterfaceWidget(parent=self)
        self.lay.addWidget(self.interface_widget)
        self.interface_widget.hide()
        """
        
        self.ecran_selection = es.EcranSelectionWidget(parent=self,
                                                       ecran_precedant=self.ecran_accueil)
        self.lay.addWidget(self.ecran_selection)
        self.ecran_selection.hide()
        

        self.showMaximized()
