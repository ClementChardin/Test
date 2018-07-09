# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
import selection as s

class AjoutPosteDialog(QtGui.QDialog):
    def __init__(self, joueur, parent=None):
        super(AjoutPosteDialog, self).__init__(parent)
        self.joueur = joueur

        self.lay = QtGui.QGridLayout()
        self.setLayout(self.lay)

        self.group = QtGui.QButtonGroup()

        for jj, st in enumerate(('Poste', 'EV actuelle', 'EV finale',
                                 'Remarques')):
            lab = QtGui.QLabel(st)
            self.lay.addWidget(lab, 0, jj)

        for ii, poste in enumerate(s.postes):
            rad = QtGui.QRadioButton(poste)
            self.lay.addWidget(rad, ii+1, 0)
            self.group.addButton(rad)

            joue = poste in self.joueur.postes or \
                   (s.est_poste_centre(poste) and self.joueur.joue_centre())
            print poste, joue
            if joue:
                if poste in ('C1', 'C2') and \
                   not poste in self.joueur.postes:
                    if 'C1' in self.joueur.postes:
                        idx = self.joueur.postes.index('C1')
                    elif 'C2' in self.joueur.postes:
                        idx = self.joueur.postes.index('C2')
                    elif 'CE' in self.joueur.postes:
                        idx = self.joueur.postes.index('CE')
                else:
                    idx = self.joueur.postes.index(poste)
                maitrise = self.joueur.postes_maitrises[idx]
            else:
                maitrise = False

            ev = s.calc_EV(self.joueur, poste, fatigue=False)

            eva = round(ev, 2)
            if not joue:
                eva += 1
            lab_EVa = QtGui.QLabel(str(eva))
            self.lay.addWidget(lab_EVa, ii+1, 1)

            evf = round(ev, 2)
            if not joue:
                evf += 2
            elif not maitrise:
                evf += 1
            lab_EVf = QtGui.QLabel(str(evf))
            self.lay.addWidget(lab_EVf, ii+1, 2)

            rq = ''
            if joue:
                rq = u"Joué"
                if maitrise:
                    rq += u" et maitrisé"
            lab_rq = QtGui.QLabel(rq)
            self.lay.addWidget(lab_rq, ii+1, 3)

        self.but_no = QtGui.QPushButton('Annuler')
        self.but_no.clicked.connect(self.reject)
        self.lay.addWidget(self.but_no, len(s.postes)+1, 0)

        self.but_yes = QtGui.QPushButton('Valider')
        self.but_yes.clicked.connect(self.accept)
        self.lay.addWidget(self.but_yes, len(s.postes)+1, 2)

    def poste_choisi(self):
        return str(self.group.checkedButton().text())

    def EV_choisie(self):
        but = self.group.checkedButton()
        idx = self.lay.indexOf(but)
        pos = self.lay.getItemPosition(idx+1)
        ev = str(self.lay.itemAtPosition(pos[0], pos[1]).widget().text())
        return ev
