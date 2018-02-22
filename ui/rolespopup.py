from PyQt4 import QtCore, QtGui
import selection as s

class RolePopupWidget(QtGui.QWidget):
    def __init__(self, parent=None, joueurs=None, main=None):
        super(RolePopupWidget, self).__init__(parent)
        self.joueurs = joueurs
        self.main = main

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()
        
    def setup_ui(self):
        self.joueurs_widgets = []
        for i, jj in enumerate(self.joueurs):
            self.joueurs_widgets.append(JRolesWidget(joueur=jj))
            self.lay.addWidget(self.joueurs_widgets[i])

        #Boutons valider et annuler
        self.valider_but = QtGui.QPushButton("Valider")
        self.annuler_but = QtGui.QPushButton("Annuler")
        self.but_lay = QtGui.QHBoxLayout()
        self.but_lay.addWidget(self.valider_but)
        self.but_lay.addWidget(self.annuler_but)
        self.lay.addLayout(self.but_lay)

        #Connection des boutons
        self.valider_but.clicked.connect(self.valider)
        self.annuler_but.clicked.connect(self.close)

    def valider(self):
        self.couples = []
        for i, w in enumerate(self.joueurs_widgets):
            for line in w.lines:
                role = str(line.text())
                if role != "":
                    self.couples.append((role, self.joueurs[i]))
        self.main.maj_roles(self.couples)
        self.close()

class JRolesWidget(QtGui.QWidget):
    def __init__(self, parent=None, joueur=None):
        super(JRolesWidget, self).__init__(parent)
        self.joueur = joueur

        self.lay = QtGui.QFormLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.r = 0
        self.lines = [QtGui.QLineEdit()]
        
        self.lay.addRow("Role " + str(self.r) + " pour " + self.joueur.nom, self.lines[self.r])
        self.connect_line(self.r)

    def connect_line(self, r):
        self.lines[r].editingFinished.connect(self.add_line_aux)

    def add_line_aux(self):
        if str(self.lines[self.r].text()) != "":
            self.lines.append(QtGui.QLineEdit())
            self.r += 1
            self.connect_line(self.r)
            self.lay.addRow("Role " + str(self.r) + " pour " + self.joueur.nom, self.lines[self.r])
        
        
