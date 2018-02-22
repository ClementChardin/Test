import selection as s
from PyQt4 import QtCore, QtGui

class ChangementPostePopup(QtGui.QWidget):
    def __init__(self, jj, dat=None, parent=None, choix_joueurs_selection = None):
        super(ChangementPostePopup, self).__init__(parent)
        self.jj = jj
        self.dat = dat
        self.choix_joueurs_selection = choix_joueurs_selection

        self.lay = QtGui.QGridLayout()
        self.setLayout(self.lay)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.lab_nom = QtGui.QLabel(self.jj.nom)
        self.lay.addWidget(self.lab_nom, 0, 2)

        for ii, st in enumerate(('EV', u'Matches joués club',
                                 u'Matches joués sélection')):
            lab = QtGui.QLabel(st)
            self.lay.addWidget(lab, ii+2, 0)

        for ii in range(1, 4):
            dd = getattr(self.jj, 'MJ'+str(ii)+'_total')
            club_tit = dd['CT']
            club_remp = dd['CR']
            sel_tit = dd['ST']
            sel_remp = dd['SR']

            if self.jj.postes[ii] == 'CE':
                ev1 = s.calc_EV(self.jj, 'C1', fatigue=False)
                ev2 = s.calc_EV(self.jj, 'C2', fatigue=False)
                st_ev = 'C1 : ' + str(round(ev1, 2)) + \
                        '\nC2 : ' + str(round(ev2, 2))
            else:
                st_ev = str(round(s.calc_EV(self.jj, self.jj.postes[ii]), 2))
            lab_ev = QtGui.QLabel(st_ev)
            self.lay.addWidget(lab_ev, 2, ii)

            st_club = str(club_tit+club_remp) + ' (' + str(club_tit) + ')'
            lab_club = QtGui.QLabel(st_club)
            self.lay.addWidget(lab_club, 3, ii)

            st_sel = str(sel_tit+sel_remp) + ' (' + str(sel_tit) + ')'
            lab_sel = QtGui.QLabel(st_sel)
            self.lay.addWidget(lab_sel, 4, ii)

            rad = QtGui.QRadioButton(self.jj.postes[ii])
            setattr(self, 'rad_'+str(ii), rad)
            self.lay.addWidget(rad, 1, ii)

        self.but_annuler = QtGui.QPushButton("Annuler")
        self.but_annuler.clicked.connect(self.close)
        self.lay.addWidget(self.but_annuler, 5, 1)

        self.but_valider = QtGui.QPushButton("OK")
        self.but_valider.clicked.connect(self.valider)
        self.lay.addWidget(self.but_valider)

    def valider(self):
        if self.rad_1.isChecked():
            poste = self.jj.postes[1]
        elif self.rad_2.isChecked():
            poste = self.jj.postes[2]
        elif self.rad_3.isChecked():
            poste = self.jj.postes[3]

        if poste == 'CE':
            mb = QtGui.QMessageBox()
            if mb.question(None,
                           "Question",
                           u"""Choisir poste""",
                           "C1", "C2") == 1:
                poste = 'C2'
            else:
                poste = 'C1'

        s.changer_poste_joueur(self.jj, poste, self.dat)

        self.choix_joueurs_selection.parent().maj()
        self.close()
            
            
