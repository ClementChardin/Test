from PyQt4 import QtCore, QtGui
from ui.biopopup import JCaracsWidget
from generer_joueur.caracs_all_arm_rg import caracs_all_arm_rg
import selection as s

class CaracsArmeeWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CaracsArmeeWidget, self).__init__(parent)
        self.dd_jcaracs = {}
        self.fatigue = False

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.tab = QtGui.QTabWidget()
        self.lay.addWidget(self.tab)

        armees = [arm for arm in s.noms_armees]
        armees.remove('ULT')
        armees.remove('ULTB')
        armees.remove('Vide')

        for armee in armees:
            dd = caracs_all_arm_rg[armee]
            joueurs = []
            for rg in sorted(dd.keys(), key=lambda rg:s.rang_new(rg)):
                jj = s.joueur()
                jj.caracs_sans_fatigue = dd[rg]
                jj.caracs_sans_fatigue["RP_tot"] = 0
                jj.nom = rg
                joueurs.append(jj)

            jcarac = JCaracsWidget(joueurs, parent=self)
            self.dd_jcaracs[armee] = jcarac
            self.tab.addTab(jcarac, armee)

        self.setGeometry(QtCore.QRect(490, 110, 930, 810))
        self.show()

