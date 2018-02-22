# -*- coding: cp1252 -*-
import selection as s
from PyQt4 import QtCore, QtGui

"""
/!\ Copie - Colle pour championat et coupe /!\
"""

def points_championat(cc):
    return 4*cc.gagnes_championat + 2*cc.nuls_championat + \
           cc.bonus_offensif_championat + cc.bonus_defensif_championat

def joues_championat(cc):
    return cc.gagnes_championat + cc.nuls_championat + cc.perdus_championat

def print_classement_championat(noms_clubs_championat):
    ll = classement_championat(noms_clubs_championat)
    print 'nom', 'J', 'G', 'N', 'P', 'BO', 'BD', 'pts'
    for cc in ll:
        print cc.nom, cc.joues_championat, cc.gagnes_championat, \
              cc.perdus_championat, cc.bonus_offensif_championat, \
              cc.bonus_defensif_championat, points_championat(cc)

def points_coupe(cc):
    return 4*cc.gagnes_coupe + 2*cc.nuls_coupe + \
           cc.bonus_offensif_coupe + cc.bonus_defensif_coupe

def joues_coupe(cc):
    return cc.gagnes_coupe + cc.nuls_coupe + cc.perdus_coupe

def print_classement_championat(noms_clubs_championat):
    ll = classement_championat(noms_clubs_championat)
    print 'nom', 'J', 'G', 'N', 'P', 'BO', 'BD', 'pts'
    for cc in ll:
        print cc.nom, cc.joues_championat, cc.gagnes_championat, \
              cc.perdus_championat, cc.bonus_offensif_championat, \
              cc.bonus_defensif_championat, points_championat(cc)

class ClassementWidget(QtGui.QWidget):
    def __init__(self, clubs_tournoi=[], type_tournoi=None, parent=None):
        super(ClassementWidget, self).__init__(parent)
        self.clubs_tournoi = clubs_tournoi
        self.type_tournoi = type_tournoi
        
        self.charger_classement()

        for cc in self.clubs_tournoi:
            setattr(self, "dict_"+cc.nom, dict())

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.init_classement()

        self.setup_ui()

    def setup_ui(self):
        self.hlabels = ['nom', 'J', 'G', 'N', 'P', 'BO', 'BD', 'Pour', 'Contre',
                        'Diff', 'Pts']
        self.table = QtGui.QTableWidget(len(self.clubs_tournoi),
                                        len(self.hlabels))

        for ii, cc in enumerate(self.classement):

            for jj, key in enumerate(('nom', 'joues', 'gagnes', 'nuls', 'perdus',
                                      'bonus_offensif', 'bonus_defensif',
                                      'pour', 'contre', 'difference',
                                      'points')):
                st = getattr(self, "dict_"+cc.nom)[key]
                it = QtGui.QTableWidgetItem(st)
                self.table.setItem(ii, jj, it)

        for ii in range(len(self.hlabels)):
            self.table.setColumnWidth(ii, 53)

        self.table.setHorizontalHeaderLabels(self.hlabels)
        self.lay.addWidget(self.table)

        """
        Empecher d'editer les cases
        """
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def charger_classement(self):
        if self.type_tournoi == "championat":
            self.points = points_championat
        elif self.type_tournoi == "coupe":
            self.points = points_coupe
        else:
            raise ValueError("mauvais type_tournoi")
        
        self.classement = sorted(self.clubs_tournoi,
                                 key=lambda cc: (self.points(cc), getattr(cc, 'difference_'+self.type_tournoi)))
    """
    def maj(self):
        #On supprime la table d'abord
        self.table.deleteLater()

        #On charge le classement
        self.charger_classement()

        #On re initie le classement
        self.init_classement()

        #On refait l'ui
        self.setup_ui()
    """
    def init_classement(self):
        for cc in self.classement:
            getattr(self, "dict_"+cc.nom)["nom"] = cc.nom

            for at in ('joues', 'gagnes', 'nuls', 'perdus', 'bonus_offensif',
                       'bonus_defensif', 'pour', 'contre', 'difference'):
                at_club = at + '_' + self.type_tournoi
                getattr(self, "dict_"+cc.nom)[at] = str(getattr(cc, at_club))

            if self.type_tournoi == "championat":
                points = points_championat
            elif self.type_tournoi == "coupe":
                points = points_coupe
            else:
                raise ValueError("Mauvais type_tournoi !")
                     
            getattr(self, "dict_"+cc.nom)["points"] = str(points(cc))
        self.classement.reverse()

