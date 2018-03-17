from PyQt4 import QtGui, QtCore
from diagramme_compo import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib

class DiagrammeCompoWidget(QtGui.QWidget):
    def __init__(self,
                 compo,
                 compo2=None,
                 fatigue=True,
                 parent=None,
                 nom_1=None,
                 nom_2=None):
        super(DiagrammeCompoWidget, self).__init__(parent)
        self.compo = compo
        self.compo2 = compo2
        self.nom_1 = nom_1
        self.nom_2 = nom_2
        self.fatigue = fatigue

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.plot()

    def plot(self):
        #self.fig = plt.figure()
        #self.ax = self.fig.add_subplot(111)
        self.fig = plt.gcf()
        self.ax = plt.gca()
        self.canvas = FigureCanvas(self.fig)
        self.lay.addWidget(self.canvas)
        plt.axis('off')
        plt.close(self.fig)

        diagramme_etoile_compo(self.compo,
                               fatigue=self.fatigue,
                               ax=self.ax,
                               compo2=self.compo2,
                               nom_1=self.nom_1,
                               nom_2=self.nom_2)
