# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
import selection as s

class RecrutementsWidgetNew(QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 dat=None,
                 clubs=[],
                 joueurs=[]
                 classements={}):
        """
        classements est un dict qui contient en keys les noms des joueurs et
        en values le classement des propositions qui ont été faites au joueur

        Ces classements sont sous la forme de list
        Chaque item de la liste est un tuple (nom_club, val, ms, besoin)
        """
        super(RecrutementWidgetNew, self).__init__(parent)
        self.dat = s.lire_date() if dat is None else dat
        self.clubs = clubs
        self.noms_clubs = [cc.nom for cc in self.clubs]
        self.joueurs = joueurs
        self.classements = classements

        #On tire au hasard l'ordre de passage des clubs
        shuffle(self.noms_clubs)

    def setup_ui(self):
        

    def get_joueurs_interresse(nom_club):
        ll = []
        for jj in self.joueurs:
            classement = self.classements[jj.nom]
            offre_preferee = classement[0]
            if offre_preferee[0] == nom_club:
                ll.append(jj)
        return ll
