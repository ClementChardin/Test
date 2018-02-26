from PyQt4 import QtGui, QtCore
import calendrier as cal
from noms_all import *

class CalendrierWidget(QtGui.QWidget):
    def __init__(self, nom_championnat, parent=None, dat=None):
        super(CalendrierWidget, self).__init__(parent)
        self.nom_championnat = nom_championnat
        self.dat = dat

        try:
            self.calendrier = cal.charger_calendrier(self.nom_championnat, dat=self.dat)
        except IOError:
            self.calendrier = cal.calendrier(nom_championnat, dat=self.dat)
        self.nombre_equipes_impair = len(self.calendrier.noms_clubs) % 2 == 1

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

        self.setWindowTitle(self.nom_championnat)
        self.tabs.setFont(QtGui.QFont('defaut', 12))
        self.show()

    def setup_ui(self):
        self.tabs = QtGui.QTabWidget(self)
        self.journees = []
        for ii in range(len(self.calendrier.journees)):
            matches_journee = self.calendrier.matches[ii]
            scores_journee = self.calendrier.scores[ii]
            journee = JourneeWidget(matches_journee,
                                    scores_journee,
                                    self.nombre_equipes_impair,
                                    self.calendrier.noms_clubs)
            self.journees.append(journee)
            self.tabs.addTab(journee, u'Journée ' + str(ii+1))
        self.lay.addWidget(self.tabs)

    def clean_ui(self):
        for jou in self.journees:
            self.tabs.removeTab(0)
            jou.deleteLater()
        self.tabs.deleteLater()

    def maj(self):
        self.clean_ui()
        self.setup_ui()

class JourneeWidget(QtGui.QWidget):
    def __init__(self,
                 matches_journee,
                 scores_journee,
                 nombre_equipes_impair,
                 noms_clubs,
                 parent=None):
        super(JourneeWidget, self).__init__(parent)
        self.matches = matches_journee
        self.scores = scores_journee
        self.nombre_equipes_impair = nombre_equipes_impair
        self.noms_clubs = noms_clubs
        if '' in self.matches:
            self.matches.remove('')

        self.lay = QtGui.QGridLayout()#len(self.matches), 5)
        self.setLayout(self.lay)

        for ii in range(len(self.matches)):
            nom_1 = self.matches[ii].split(' v ')[0]
            nom_2 = self.matches[ii].split(' v ')[1]
            score_1 = '' if self.scores[ii] is None else str(self.scores[ii][0])
            score_2 = '' if self.scores[ii] is None else str(self.scores[ii][1])
            self.lay.addWidget(QtGui.QLabel(noms_complets[nom_1]), ii, 0)
            self.lay.addWidget(QtGui.QLabel(score_1), ii, 1)
            self.lay.addWidget(QtGui.QLabel('/'), ii, 2)
            self.lay.addWidget(QtGui.QLabel(score_2), ii, 3)
            self.lay.addWidget(QtGui.QLabel(noms_complets[nom_2]), ii, 4)
        if self.nombre_equipes_impair:
            nom = ''
            for ma in self.matches:
                for nn in self.noms_clubs:
                    if nn in ma:
                        continue
                    else:
                        nom = nn
                        break
                break
            self.lay.addWidget(QtGui.QLabel(nom), ii+1, 0)
            self.lay.addWidget(QtGui.QLabel('Exempte'), ii+1, 2)
