from PyQt4 import QtGui, QtCore
import os.path as osp
import os
from savefiles import *

class EcranAccueilWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(EcranAccueilWidget, self).__init__(parent)

        self.setup_ui()

    def setup_ui(self):
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.lay_but = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_but)
        """
        self.but_voir = QtGui.QPushButton("Voir equipes")
        self.lay_but.addWidget(self.but_voir)
        self.but_voir.clicked.connect(self.voir_equipes)

        self.but_amical = QtGui.QPushButton("Match amical")
        self.lay_but.addWidget(self.but_amical)
        self.but_amical.clicked.connect(self.match_amical)
        """
        self.but_clubs = QtGui.QPushButton("Clubs")
        self.lay_but.addWidget(self.but_clubs)
        self.but_clubs.clicked.connect(self.clubs)

        self.but_selections = QtGui.QPushButton("Selections")
        self.lay_but.addWidget(self.but_selections)
        self.but_selections.clicked.connect(self.selections)

        #self.lab = QtGui.QLabel()
        self.pix = QtGui.QPixmap(IMAGES_DIR + "/clubs.png")
        #self.lab.setPixmap(self.pix)
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(self.pix)
        self.vue = QtGui.QGraphicsView(self.scene)
        self.lay.addWidget(self.vue)

        #self.setStyleSheet("QLabel {font-size : 400px; color : blue; background-image: url(IMAGES_DIR + '/terrain.png');}")
    """
    def voir_equipes(self):
        self.parent().ecran_accueil.hide()
        self.parent().interface_widget.ecran_precedant = self
        self.parent().interface_widget.show()

    def match_amical(self):
        self.parent().ecran_accueil.hide()
        self.parent().match_amical_widget.col_match.sauv_check.setEnabled(False)
        self.parent().match_amical_widget.col_match.rad_championat.setChecked(False)
        self.parent().match_amical_widget.col_match.rad_championat.setEnabled(False)
        self.parent().match_amical_widget.col_match.rad_coupe.setEnabled(False)
        self.parent().match_amical_widget.show()
    """
    def clubs(self):
        self.parent().ecran_accueil.hide()
        #self.parent().ecran_club.maj()
        self.parent().ecran_club.show()

    def selections(self):
        self.parent().ecran_accueil.hide()
        self.parent().ecran_selection.show()
