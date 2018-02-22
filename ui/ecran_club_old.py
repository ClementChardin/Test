import selection as s
import exempterpopup as ep
from classement_widget import *
from PyQt4 import QtGui, QtCore
from interface_qt import InterfaceWidget
from match import MatchWidget
from calendrier_widget import CalendrierWidget
from stats_widget import StatsWidget

class EcranClubWidget(QtGui.QWidget):
    def __init__(self, ecran_precedant=None, parent=None):
        super(EcranClubWidget, self).__init__(parent)
        self.ecran_precedant = ecran_precedant
        self.charger_clubs()

        self.initier_classements()
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()

    def initier_classements(self):
        """
        Avec vieux module classement_old.py
        
        self.classement_vieux_monde = ClassementWidget(clubs_tournoi=[cc for cc in self.clubs if cc.nom in s.noms_clubs_vieux_monde],
                                                       type_tournoi='championat',
                                                       parent=self)
        self.classement_nouveaux_mondes = ClassementWidget(clubs_tournoi=[cc for cc in self.clubs if cc.nom in s.noms_clubs_nouveaux_mondes],
                                                       type_tournoi='championat',
                                                       parent=self)
        for kk, C in enumerate(("coupe", "challenge")):
            for ii in range(1, 5):
                noms = getattr(s, "noms_clubs_"+C+"_poule_"+str(ii))
                setattr(self, "classement_"+C+"_poule_"+str(ii),
                        ClassementWidget(clubs_tournoi=[cc for cc in self.clubs if cc.nom in noms],
                                         type_tournoi='coupe',
                                         parent=self))
        """
        self.classements_widgets = []
        self.classement_vieux_monde = ClassementWidget("vieux_monde",
                                                       parent=self)
        self.classements_widgets.append(self.classement_vieux_monde)

        self.classement_nouveaux_mondes = ClassementWidget("nouveaux_mondes",
                                                           parent=self)
        self.classements_widgets.append(self.classement_nouveaux_mondes)
        for kk, C in enumerate(("coupe", "challenge")):
            for ii in range(1, 5):
                setattr(self, "classement_"+C+"_poule_"+str(ii),
                        ClassementWidget(C+"_poule_"+str(ii), parent=self))
                self.classements_widgets.append(getattr(self, "classement_"+C+"_poule_"+str(ii)))

        self.calendriers = []
        for w in self.classements_widgets:
            self.calendriers.append(w.calendrier)

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
        Classements championats
        """
        self.lay_classements = QtGui.QGridLayout()

        #Vieux Monde
        self.lay_vieux_monde = QtGui.QHBoxLayout()
        self.lab_vieux_monde = QtGui.QLabel("Vieux Monde")
        self.lay_vieux_monde.addWidget(self.lab_vieux_monde)
        self.but_vieux_monde = QtGui.QPushButton("Calendrier")
        self.but_vieux_monde.clicked.connect(self.aux_cal_vieux_monde)
        self.lay_vieux_monde.addWidget(self.but_vieux_monde)
        self.lay_classements.addLayout(self.lay_vieux_monde, 0, 0)
        self.lay_classements.addWidget(self.classement_vieux_monde, 1, 0)

        #Nouveaux_mondes
        self.lay_nouveaux_mondes = QtGui.QHBoxLayout()
        self.lab_nouveaux_mondes = QtGui.QLabel("Nouveaux Mondes")
        self.lay_nouveaux_mondes.addWidget(self.lab_nouveaux_mondes)
        self.but_nouveaux_mondes = QtGui.QPushButton("Calendrier")
        self.but_nouveaux_mondes.clicked.connect(self.aux_cal_nouveaux_mondes)
        self.lay_nouveaux_mondes.addWidget(self.but_nouveaux_mondes)
        self.lay_classements.addLayout(self.lay_nouveaux_mondes, 0, 1)
        self.lay_classements.addWidget(self.classement_nouveaux_mondes, 1, 1)

        """
        Classements coupe et challenge
        """
        for kk, C in enumerate(("coupe", "challenge")):
            setattr(self, "lay_"+C, QtGui.QHBoxLayout())
            setattr(self, "lab_"+C, QtGui.QLabel(C_majuscule(C)))
            self.lay_classements.addLayout(getattr(self, 'lay_'+C), 2, kk)
            setattr(self, "tab_"+C, QtGui.QTabWidget())
            getattr(self, 'lay_'+C).addWidget(getattr(self, 'lab_'+C))
            for ii in range(1, 5):
                setattr(self, 'but_'+C+str(ii+1), QtGui.QPushButton('Calendrier '+str(ii)))
                getattr(self, 'but_'+C+str(ii+1)).clicked.connect(getattr(self, 'aux_cal_'+C+'_'+str(ii)))
                getattr(self, 'lay_'+C).addWidget(getattr(self, 'but_'+C+str(ii+1)))
                getattr(self, "tab_"+C).addTab(getattr(self, "classement_"+C+"_poule_"+str(ii)),
                                               "Poule " + str(ii))
            self.lay_classements.addLayout(getattr(self, 'lay_'+C), 2, kk)
            self.lay_classements.addWidget(getattr(self, "tab_"+C), 3, kk)

        self.lay_aux.addLayout(self.lay_classements)

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
        self.match_widget = MatchWidget(parent=self,
                                        ecran_precedant=self.wid_aux,
                                        calendriers=self.calendriers)
        self.lay.addWidget(self.match_widget)
        self.match_widget.hide()

    def retour_ecran_precedant(self):
        self.wid_aux.hide()
        self.ecran_precedant.show()

    def voir_equipes(self):
        self.wid_aux.hide()
        self.interface_widget.show()

    def statistiques(self):
        self.stats_widget = StatsWidget(self.calendriers)
        self.stats_widget.show()

    def exempter(self):
        self.ex_popup = ep.ExempterPopup(ecran_classement=self)
        self.ex_popup.show()

    def jouer_prochain_match(self):
        self.wid_aux.hide()
        self.match_widget.show()

    def aux_cal_vieux_monde(self):
        self.show_calendrier('vieux_monde')

    def aux_cal_nouveaux_mondes(self):
        self.show_calendrier('nouveaux_mondes')

    def aux_cal_coupe_1(self):
        self.show_calendrier('coupe_poule_1')

    def aux_cal_coupe_2(self):
        self.show_calendrier('coupe_poule_2')

    def aux_cal_coupe_3(self):
        self.show_calendrier('coupe_poule_3')

    def aux_cal_coupe_4(self):
        self.show_calendrier('coupe_poule_4')

    def aux_cal_challenge_1(self):
        self.show_calendrier('challenge_poule_1')

    def aux_cal_challenge_2(self):
        self.show_calendrier('challenge_poule_2')

    def aux_cal_challenge_3(self):
        self.show_calendrier('challenge_poule_3')

    def aux_cal_challenge_4(self):
        self.show_calendrier('challenge_poule_4')

    def show_calendrier(self, nom):
        self.C = CalendrierWidget(nom)
        self.C.show()

    def charger_clubs(self):
        self.clubs = []
        for nom in s.noms_clubs:
            cc = s.charger(nom, 'c')
            self.clubs.append(cc)

    def maj(self):
        self.parent().ecran_club = EcranClubWidget(parent=self.parent(),
                                                   ecran_precedant=self.parent().ecran_accueil)
        #self.parent().ecran_club.ecran_precedant = self.parent().ecran_accueil
        #self.parent().match_widget.ecran_precedant = self.parent().ecran_classement
        self.parent().lay.addWidget(self.parent().ecran_club)
        self.deleteLater()

def C_majuscule(C):
    return "C" + C[1:]
