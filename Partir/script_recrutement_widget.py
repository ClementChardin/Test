# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
from ui.recrutements_widget_new import *
import sys
from savefiles import *
import pickle

with open(TRANSFERTS_DIR_NAME(dat=None) + '/choix' + str(0) + '.prop', 'r') as ff:
    classements = pickle.load(ff)
print u"Classement chargé"
clubs = []
joueurs = []

for nom in s.noms_clubs():
    cc = s.charger(nom, 'c')
    clubs.append(cc)
    for jj in cc.get_all_joueurs():
        if jj.nom in classements.keys():
            joueurs.append(jj)
print u"Clubs et joueurs chargés"

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    R = RecrutementsWidgetNew(dat=None,
                              clubs=clubs,
                              all_joueurs=joueurs,
                              classements=classements)
    R.showMaximized()
    sys.exit(app.exec_())
