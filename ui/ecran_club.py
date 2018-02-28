import selection as s
import exempterpopup as ep
from classement_widget import *
from PyQt4 import QtGui, QtCore
from interface_qt import InterfaceWidget
from match import MatchWidget
from calendrier_widget import CalendrierWidget
from stats_widget import StatsWidget
from saison import *

class EcranClubWidget(QtGui.QWidget):
    def __init__(self, dat=None, ecran_precedant=None, parent=None):
        super(EcranClubWidget, self).__init__(parent)
        #print "nom saison =", nom_saison
        self.dat = dat
        self.nom_saison = None if self.dat is None \
                          else 'saison_' + str(self.dat) + '_c'
        self.saison = charger_saison(self.nom_saison, self.dat)
        self.ecran_precedant = ecran_precedant
        #self.charger_clubs()

        self.initier_classements()
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()

    def initier_classements(self):
        self.classements_widgets = []
        self.classements_widgets_championnats = []
        self.classements_widgets_coupes = []
        self.calendriers = self.saison.calendriers
        self.noms_championnats = []
        self.noms_coupes = []
        self.noms_calendriers = []
        for cal in self.calendriers:
            clas = ClassementWidget(cal.nom_championnat, parent=self, dat=self.dat)
            self.classements_widgets.append(clas)
            if 'poule' in cal.nom_championnat \
               or 'quarts' in cal.nom_championnat \
               or 'demie' in cal.nom_championnat \
               or 'finale' in cal.nom_championnat:
                self.noms_coupes.append(cal.nom_championnat)
                self.classements_widgets_coupes.append(clas)
            else:
                self.noms_championnats.append(cal.nom_championnat)
                self.classements_widgets_championnats.append(clas)
            self.noms_calendriers.append(cal.nom_championnat)
            setattr(self, 'classement_'+cal.nom_championnat, clas)
        self.idx_coupe = 0
        self.idx_championnat = 0

    def setup_ui(self):
        """
        Widget auxiliaire
        """
        self.wid_aux = QtGui.QWidget(parent=self)
        self.lay_aux = QtGui.QVBoxLayout()
        self.wid_aux.setLayout(self.lay_aux)
        self.lay.addWidget(self.wid_aux)
        
        """
        Boutons
        """
        self.lay_but = QtGui.QHBoxLayout()

        self.retour = QtGui.QPushButton("Retour a l'ecran precedant")
        self.retour.clicked.connect(self.retour_ecran_precedant)
        self.lay_but.addWidget(self.retour)

        self.voir = QtGui.QPushButton("Voir equipes")
        self.voir.clicked.connect(self.voir_equipes)
        self.lay_but.addWidget(self.voir)

        self.stats = QtGui.QPushButton("Statistiques")
        self.stats.clicked.connect(self.statistiques)
        self.lay_but.addWidget(self.stats)

        self.exemp = QtGui.QPushButton("Exempter de match")
        self.exemp.clicked.connect(self.exempter)
        self.lay_but.addWidget(self.exemp)

        self.jouer = QtGui.QPushButton("Jouer prochain match")
        self.jouer.clicked.connect(self.jouer_prochain_match)
        self.lay_but.addWidget(self.jouer)

        self.lay_aux.addLayout(self.lay_but)
            
        """
        Classements
        """
        self.lay_classements = QtGui.QVBoxLayout()
        self.lay_aux.addLayout(self.lay_classements)

        #Championnats
        self.lay_championnats = QtGui.QHBoxLayout()
        self.lay_classements.addLayout(self.lay_championnats)

        self.but_champ_precedent = QtGui.QPushButton(u"Précendent")
        self.but_champ_precedent.clicked.connect(self.championnat_precedent)
        self.lay_championnats.addWidget(self.but_champ_precedent)

        self.lab_champ = QtGui.QLabel(self.noms_championnats[0])
        self.lay_championnats.addWidget(self.lab_champ)

        self.but_champ_suivant = QtGui.QPushButton(u"Suivant")
        self.but_champ_suivant.clicked.connect(self.championnat_suivant)
        self.lay_championnats.addWidget(self.but_champ_suivant)

        self.but_cal_champ = QtGui.QPushButton("Calendrier")
        self.but_cal_champ.clicked.connect(self.aux_cal_championnat)
        self.lay_championnats.addWidget(self.but_cal_champ)

        for ii, nom in enumerate(self.noms_championnats):
            wid = self.classements_widgets_championnats[ii]
            self.lay_classements.addWidget(wid)
            if not nom == self.noms_championnats[0]:
                wid.hide()

        #Coupes
        self.lay_coupes = QtGui.QHBoxLayout()
        self.lay_classements.addLayout(self.lay_coupes)

        self.but_coupe_precedent = QtGui.QPushButton(u"Précendent")
        self.but_coupe_precedent.clicked.connect(self.coupe_precedent)
        self.lay_coupes.addWidget(self.but_coupe_precedent)

        self.lab_coupe = QtGui.QLabel(self.noms_coupes[0])
        self.lay_coupes.addWidget(self.lab_coupe)

        self.but_coupe_suivant = QtGui.QPushButton(u"Suivant")
        self.but_coupe_suivant.clicked.connect(self.coupe_suivant)
        self.lay_coupes.addWidget(self.but_coupe_suivant)

        self.but_cal_coupe = QtGui.QPushButton("Calendrier")
        self.but_cal_coupe.clicked.connect(self.aux_cal_coupe)
        self.lay_coupes.addWidget(self.but_cal_coupe)

        for ii, nom in enumerate(self.noms_coupes):
            wid = self.classements_widgets_coupes[ii]
            self.lay_classements.addWidget(wid)
            if not nom == self.noms_coupes[0]:
                wid.hide()

        """
        Interface widget
        """
        self.interface_widget = InterfaceWidget(parent=self,
                                                ecran_precedant=self.wid_aux)
        self.lay.addWidget(self.interface_widget)
        self.interface_widget.hide()

        """
        Match Widget
        """
        self.match_widget = MatchWidget(saison=self.saison,
                                        parent=self,
                                        ecran_precedant=self.wid_aux)
        self.lay.addWidget(self.match_widget)
        self.match_widget.hide()

    def retour_ecran_precedant(self):
        self.wid_aux.hide()
        self.ecran_precedant.show()

    def voir_equipes(self):
        self.wid_aux.hide()
        self.interface_widget.show()

    def statistiques(self):
        self.stats_widget = StatsWidget(self.saison)
        self.stats_widget.show()

    def exempter(self):
        self.ex_popup = ep.ExempterPopup(ecran_classement=self, dat=self.saison.dat)
        self.ex_popup.show()

    def jouer_prochain_match(self):
        self.wid_aux.hide()
        self.match_widget.show()

    def aux_cal_championnat(self):
        self.show_calendrier(self.noms_championnats[self.idx_championnat], self.dat)

    def aux_cal_coupe(self):
        self.show_calendrier(self.noms_coupes[self.idx_coupe], self.dat)

    def show_calendrier(self, nom, dat):
        self.C = CalendrierWidget(nom, dat=dat)
        self.C.show()

    def championnat_precedent(self):
        self.idx_championnat -= 1
        if self.idx_championnat < 0:
            self.idx_championnat = len(self.noms_championnats) + self.idx_championnat
        self.maj_championnats()

    def championnat_suivant(self):
        self.idx_championnat += 1
        if self.idx_championnat >= len(self.noms_championnats):
            self.idx_championnat = self.idx_championnat - len(self.noms_championnats)
        self.maj_championnats()

    def coupe_precedent(self):
        self.idx_coupe -= 1
        if self.idx_coupe < 0:
            self.idx_coupe = len(self.noms_coupes) + self.idx_coupe
        self.maj_coupes()

    def coupe_suivant(self):
        self.idx_coupe += 1
        if self.idx_coupe >= len(self.noms_coupes):
            self.idx_coupe = self.idx_coupe - len(self.noms_coupes)
        self.maj_coupes()

    def maj_championnats(self):
        for ii, wid in enumerate(self.classements_widgets_championnats):
            if ii == self.idx_championnat:
                wid.show()
            else:
                wid.hide()
        self.lab_champ.setText(self.noms_championnats[self.idx_championnat])

    def maj_coupes(self):
        for ii, wid in enumerate(self.classements_widgets_coupes):
            if ii == self.idx_coupe:
                wid.show()
            else:
                wid.hide()
        self.lab_coupe.setText(self.noms_coupes[self.idx_coupe])

    def charger_clubs(self):
        self.clubs = []
        for nom in s.noms_clubs:
            cc = s.charger(nom, 'c')
            self.clubs.append(cc)

    def maj(self):
        self.parent().ecran_club = EcranClubWidget(dat=self.dat,
                                                   parent=self.parent(),
                                                   ecran_precedant=self.parent().ecran_accueil)
        #self.parent().ecran_club.ecran_precedant = self.parent().ecran_accueil
        #self.parent().match_widget.ecran_precedant = self.parent().ecran_classement
        self.parent().lay.addWidget(self.parent().ecran_club)
        self.deleteLater()

def C_majuscule(C):
    return "C" + C[1:]
