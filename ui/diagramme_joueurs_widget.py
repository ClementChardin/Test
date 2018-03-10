from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class DiagrammeJoueursWidget(QtGui.QDialog):
    def __init__(self,
                 joueurs,
                 N_points_cercles=100,
                 label_TO=None,
                 label_TA=None,
                 label_TB=None,
                 force_av_ar=None,
                 parent=None):
        super(DiagrammeJoueursWidget, self).__init__(parent)
        self.joueurs = joueurs

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.lay.addWidget(self.canvas)

        for ii, jj in enumerate(self.joueurs):
            texte = ii == 0
            jj.diagramme_etoile(texte=texte,
                                label_TO=label_TO,
                                label_TA=label_TA,
                                label_TB=label_TB,
                                force_av_ar=force_av_ar,
                                ax=self.axis)
        self.canvas.draw()

        self.show()
