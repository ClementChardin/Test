from PyQt4 import QtCore, QtGui
from saison import *

class CalendrierEquipeWidget(QtGui.QWidget):
    def __init__(self, saison, nom_equipe, parent=None):
        super(CalendrierEquipeWidget, self).__init__(parent)
        self.saison = saison
        self.nom_equipe = nom_equipe
        self.calendrier = self.saison.get_calendrier_equipe(nom_equipe)

        self.lay = QtGui.QGridLayout()
        self.setLayout(self.lay)

        for ii, tu in enumerate(self.calendrier):
            nom_champ, match, score = tu

            if score is None or score[0] == score[1]:
                bolds = []
            elif score[0] > score[1]:
                bolds = (2, 4)
            elif score[1] > score[0]:
                bolds = (6, 8)

            st_champ = nom_champ.replace('_', ' ')
            st_eq1 = '' if match is None else match.split(' v ')[0]
            st_eq2 = '' if match is None else match.split(' v ')[1]
            st_score1 = '' if score is None else str(score[0])
            st_score2 = '' if score is None else str(score[1])

            self.labs = []
            for jj, st in enumerate((st_champ, '', st_eq1, '', st_score1, ' - ',
                                     st_score2, '', st_eq2)):
                lab = QtGui.QLabel(st)
                if jj in bolds:
                    font = lab.font()
                    font.setBold(True)
                    lab.setFont(font)
                self.labs.append(lab)
                self.lay.addWidget(lab, ii, jj)
