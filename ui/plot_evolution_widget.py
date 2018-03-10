from PyQt4 import QtCore, QtGui
from plot_evolution import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class PlotEvolutionWidget(QtGui.QWidget):
    def __init__(self, jj, parent=None, dat=None):
        super(PlotEvolutionWidget, self).__init__(parent)
        self.jj = jj
        self.dat = dat

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.lay.addWidget(self.canvas)

        plot_evolution(self.jj, self.dat, self.axis)
        self.canvas.draw()

        self.show()
