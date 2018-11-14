# -*- coding: cp1252 -*-
from PyQt4 import QtCore, QtGui
from plot_evolution import *

class PlotEvolutionIndividuelWidget(QtGui.QWidget):
    def __init__(self, joueur, parent=None, dat=None):
        super(PlotEvolutionIndividuelWidget, self).__init__(parent)
        self.joueur = joueur
        self.dat = dat

        self.plotables = [u'Matches joués', 'Evolution']
        for car, v in sorted(s.ordre_caracs_joueurs.items(), key=lambda tu:tu[1]):
            self.plotables.append(car)

        """ Ajouter points, essais, drops, etc """
        """ Ajouter dates (transferts, D, changements_poste, retraite """

        self.setWindowTitle(jj.nom)

        self.setup_ui()

    def setup_ui(self):
        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.lay_checks = QtGui.QGridLayout()
        for ii, item in enumerate(self.plotables):
            c = ii % 2
            r = ii / 2
            check = QtGui.QCheckBox(item)
            if item in ('Matches joues', 'Evolution'):
                check.setChecked(True)
            check.clicked.connect(partial(self.aux_plot, check))
            self.lay_checks.addWidget(check, r, c)
        self.lay.addLayout(self.lay_checks)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.lay.addWidget(self.canvas)

    def aux_plot(self, check):
        if check.isChecked():
            text = str(check.text())
            if text == u'Matches joués':
                self.plot_matches_joues()
            elif text == 'Evolution':
                self.plot_evolution()
            elif text in s.ordre_caracs_joueurs.values():
                self.plot_carac()
            else:
                raise ValueError("Texte de la checkbox non reconnu")

        else:
            text = str(check.text())
            if text == u'Matches joués':
                self.unplot_matches_joues()
            elif text == 'Evolution':
                self.unplot_evolution()
            elif text in s.ordre_caracs_joueurs.values():
                self.unplot_carac(text, car)
            else:
                raise ValueError("Texte de la checkbox non reconnu")

    def plot_matches_joues(self):
        pass

    def plot_evolution(self):
        pass

    def plot_carac(self, car):
        pass

    def unplot_matches_joues(self):
        pass

    def unplot_evolution(self):
        pass

    def unplot_carac(self, car):
        pass

    def mix_legends(self):
        pass
