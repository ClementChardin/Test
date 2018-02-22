from PyQt4 import QtCore, QtGui
import calendrier as cal
from constantes import *
from noms_all import *

class ClassementWidget(QtGui.QWidget):
    def __init__(self, nom_tournoi, parent=None):
        super(ClassementWidget, self).__init__(parent)
        self.nom_tournoi = nom_tournoi
        try:
            self.calendrier = cal.charger_calendrier(self.nom_tournoi)
        except IOError:
            self.calendrier = cal.calendrier(nom_tournoi)

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.init_ui()

    def init_ui(self):
        self.hlabels = ['nom', 'J', 'G', 'N', 'P', 'BO', 'BD', 'Pour', 'Contre',
                        'Diff', 'Pts']
        self.table = QtGui.QTableWidget(len(self.calendrier.noms_clubs),
                                        len(self.hlabels))

        self.table.setHorizontalHeaderLabels(self.hlabels)
        self.lay.addWidget(self.table)

        """
        Empecher d'editer les cases
        """
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.setup_ui()

    def setup_ui(self):
        for ii, nom in enumerate(self.calendrier.get_classement()):
            it = QtGui.QTableWidgetItem(noms_complets[nom])
            self.table.setItem(ii, 0, it)
            for jj, key in enumerate(('joues', 'gagnes', 'nuls', 'perdus',
                                      'bonus_offensifs', 'bonus_defensifs',
                                      'pour', 'contre', 'difference',
                                      'points')):
                xx = getattr(self.calendrier, "dict_"+key)[nom]
                st = str(xx)
                it = QtGui.QTableWidgetItem(st)
                self.table.setItem(ii, jj+1, it)

        for ii in range(len(self.hlabels)):
            self.table.setColumnWidth(ii, 53)

        self.table.resizeColumnToContents(0)
        
