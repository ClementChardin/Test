# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
from ui.recrutements_widget_new import *
import sys
from savefiles import *
import pickle

filename = TRANSFERTS_DIR_NAME(dat=None)+'/classements.dict'
filename_choix_depart = TRANSFERTS_DIR_NAME(dat=None) + '/choix' + str(0) + '.prop'
if osp.isfile(filename_choix_depart):
    with open(filename_choix_depart, 'r') as ff:
        dd = pickle.load(ff)
    classements_depart = dd
    print u"Classements départ chargés"
else:
    classements_depart = {}

if osp.isfile(filename):
    with open(filename, 'r') as ff:
        dd = pickle.load(ff)
    classements = dd
    print u"Classements chargés"
else:
    classements = classements_depart
    print u"Classements chargés à partir des choix de départ"

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
                              classements=classements,
                              classements_depart=classements_depart)
    R.showMaximized()
    sys.exit(app.exec_())
