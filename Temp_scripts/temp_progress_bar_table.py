from PyQt4 import QtGui, QtCore
import selection as s
from miscellaneous_jouer_match_new import *
from jouer_match import *
from miscellaneous import *

AL = s.charger('AL', 'c')
comp = s.charger_compo("AL_defaut", "AL", "c")
comp.get_joueurs_noms()
eq1 = EquipeMatch('AL', comp)

ll = comp.get_joueurs_compo() 
nn = len(ll)

def ajouter_fatigue():
    for jj in ll:
        jj.fatigue += 1
    lay.removeWidget(w.Table)
    add_table(w, lay)

def add_table(w, lay):
    w.Table = QtGui.QTableWidget(nn,5)
    w.Table.setHorizontalHeaderLabels(['Nom', 'EV', 'fatigue', "Pourcentage d'EV"])

    for ii, jj in enumerate(ll):
        nom = QtGui.QLabel(jj.nom)
        w.Table.setCellWidget(ii,0,nom)

        end = 10#5 + ii%7
        ev1 = s.calc_EV(jj, jj.postes[1])

        lab = QtGui.QLabel(str(round(ev1, 2)))
        w.Table.setCellWidget(ii,1,lab)

        fat = QtGui.QLabel(str(jj.fatigue))
        w.Table.setCellWidget(ii,2,fat)

        pourcent = max(50, 100 - (jj.fatigue * 5))
        pr = QtGui.QProgressBar()
        pr.setStyle(QtGui.QStyleFactory.create("Plastique"))
        pr.setRange(0, 100)
        pr.setValue(min(100, pourcent))
        w.Table.setCellWidget(ii,3,pr)

        #print jj.nom, ev1, pourcent
    lay.addWidget(w.Table)

w = QtGui.QWidget()
lay = QtGui.QVBoxLayout()
w.setLayout(lay)
but = QtGui.QPushButton("Ajouter fatigue")
but.clicked.connect(ajouter_fatigue)
lay.addWidget(but)

add_table(w, lay)
w.show()
