from PyQt4 import QtGui, QtCore
import selection as s

class RemplacementWidget(QtGui.QWidget):
    def __init__(self, equipe, parent=None):
        super(RemplacementWidget, self).__init__(parent)
        self.equipe = equipe
        self.selection = None
        self.joueurs = []
        for key in sorted(self.equipe.comp.joueurs.keys(),
                          key=lambda kk: int(kk.split('n')[1])):
            self.joueurs.append(self.equipe.comp.joueurs[key])

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.table = QtGui.QTableWidget(22,5)
        self.table.setHorizontalHeaderLabels(['Nom', 'EV', 'fatigue', "Pourcentage d'EV"])
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        for ii, jj in enumerate(self.joueurs):
            nom = QtGui.QLabel(jj.nom)
            self.table.setCellWidget(ii,0,nom)

            end = 10#5 + ii%7
            ev1 = s.calc_EV(jj, jj.postes[1])

            lab = QtGui.QLabel(str(round(ev1, 2)))
            self.table.setCellWidget(ii,1,lab)

            fat = QtGui.QLabel(str(jj.fatigue))
            self.table.setCellWidget(ii,2,fat)

            pourcent = max(50, 100 - (jj.fatigue * 5))
            pr = QtGui.QProgressBar()
            pr.setStyle(QtGui.QStyleFactory.create("Plastique"))
            pr.setRange(0, 100)
            pr.setValue(min(100, pourcent))
            self.table.setCellWidget(ii,3,pr)
        self.table.doubleClicked.connect(self.remplacement)
        self.lay.addWidget(self.table)

    def remplacement(self):
        rr = self.table.currentIndex().row()
        temp = [self.table.cellWidget(rr, jj) \
                for jj in range(self.table.columnCount())]
        temp.append(rr)
        if self.selection is None:
            self.selection = temp
        else:
            if self.selection[-1] < temp[-1]:
                self.table.insertRow(temp[-1])
                for jj in range(self.table.columnCount()):
                    self.table.setCellWidget(temp[-1], jj, self.selection[jj])
                self.table.insertRow(self.selection[-1])
                for jj in range(self.table.columnCount()):
                    self.table.setCellWidget(self.selection[-1], jj, temp[jj])
                self.table.removeRow(self.selection[-1]+1)
                self.table.removeRow(temp[-1]+1)
            else:
                self.table.insertRow(self.selection[-1])
                for jj in range(self.table.columnCount()):
                    self.table.setCellWidget(self.selection[-1], jj, temp[jj])
                self.table.insertRow(temp[-1])
                for jj in range(self.table.columnCount()):
                    self.table.setCellWidget(temp[-1], jj, self.selection[jj])
                self.table.removeRow(temp[-1]+1)
                self.table.removeRow(self.selection[-1]+1)
            self.selection = None
