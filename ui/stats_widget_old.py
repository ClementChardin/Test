import selection as s
from PyQt4 import QtGui, QtCore
from stats import *

class StatsWidget(QtGui.QWidget):
    def __init__(self, nom="", parent=None):
        super(StatsWidget, self).__init__(parent)

        self.nom = nom
        self.selection = s.selection() if self.nom == "" \
                         else s.charger(nom, 's')

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.tabs = QtGui.QTabWidget()
        self.lay.addWidget(self.tab)

        self.tab_joueurs_saison = JoueursStatsWidget(saison=True)
        self.tab.addTab(self.tab_joueurs, "Individuelles Saison")

class JoueursStatsWidget(QtGui.QWidget):
    def __init__(self, saison=True, parent=None):
        super(JoueursStatsWidget, self).__init__(parent)

        self.saison = saison

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        pass
