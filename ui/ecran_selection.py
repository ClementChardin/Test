from PyQt4 import QtGui, QtCore
from selection_widget import SelectionWidget
from selection_compo_widget import SelectionCompoWidget
from match_selection import MatchSelectionWidget
from savefiles import *
from saison import *
from date import *
import exempterpopup as ep

class EcranSelectionWidget(QtGui.QWidget):
    def __init__(self,
                 nom_saison=None,
                 parent=None,
                 ecran_precedant=None,
                 dat=None):
        super(EcranSelectionWidget, self).__init__(parent)
        self.dat = lire_date() if dat is None else dat
        self.saison = charger_saison(nom=nom_saison, c_ou_s='s', dat=self.dat)
        self.ecran_precedant = ecran_precedant

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        """
        Widget auxiliaire
        """
        self.wid_aux = QtGui.QWidget()
        self.lay_aux = QtGui.QVBoxLayout()
        self.wid_aux.setLayout(self.lay_aux)
        self.lay.addWidget(self.wid_aux)

        """
        Bouttons
        """
        self.wid_but = QtGui.QWidget()
        self.lay_aux.addWidget(self.wid_but)
        self.lay_but = QtGui.QHBoxLayout()
        self.wid_but.setLayout(self.lay_but)
        #Retour a l'ecran precedant
        if not self.ecran_precedant is None:
            self.but_retour = QtGui.QPushButton("Retour a l'ecran precedant")
            self.but_retour.clicked.connect(self.retour)
            self.lay_but.addWidget(self.but_retour)

        #Choisir joueurs
        self.but_choix = QtGui.QPushButton("Choisir joueurs")
        self.but_choix.clicked.connect(self.choisir)
        self.lay_but.addWidget(self.but_choix)

        #Faire compo
        self.but_compo = QtGui.QPushButton("Faire compo")
        self.but_compo.clicked.connect(self.faire_compo)
        self.lay_but.addWidget(self.but_compo)

        #Exempter de match
        self.but_exemp = QtGui.QPushButton("Exempter de match")
        self.but_exemp.clicked.connect(self.exempter)
        self.lay_but.addWidget(self.but_exemp)

        #Jouer match
        self.but_match = QtGui.QPushButton("Jouer un match")
        self.but_match.clicked.connect(self.jouer_match)
        self.lay_but.addWidget(self.but_match)

        """
        Choix des joueurs
        """
        self.selection_widget = SelectionWidget(parent=self,
                                                ecran_precedant=self.wid_aux)
        self.lay.addWidget(self.selection_widget)
        self.selection_widget.hide()

        """
        Compo
        """
        self.selection_compo_widget = SelectionCompoWidget(saison=self.saison,
                                                           ecran_precedant=self.wid_aux,
                                                           dat=self.dat)#parent=self,
        self.lay.addWidget(self.selection_compo_widget)
        self.selection_compo_widget.hide()

        """
        Match
        """
        self.match_selection_widget = MatchSelectionWidget(parent=self,
                                                           saison=self.saison,
                                                           ecran_precedant=self.wid_aux,
                                                           dat=self.dat)
        self.lay.addWidget(self.match_selection_widget)
        self.match_selection_widget.hide()

        """
        Image
        """
        self.pix = QtGui.QPixmap(IMAGES_DIR + "/blasons.png")
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(self.pix)
        self.vue = QtGui.QGraphicsView(self.scene)
        self.lay_aux.addWidget(self.vue)

    def retour(self):
        self.hide()
        self.ecran_precedant.show()

    def choisir(self):
        self.wid_aux.hide()
        self.selection_widget.show()

    def faire_compo(self):
        self.wid_aux.hide()
        self.selection_compo_widget.show()

    def exempter(self):
        self.ex_popup = ep.ExempterPopup(ecran_classement=self, c_ou_s='s')
        self.ex_popup.show()

    def jouer_match(self):
        self.wid_aux.hide()
        self.match_selection_widget.show()
