from PyQt4 import QtGui, QtCore

class InfoDialog(QtGui.QDialog):
    def __init__(self, st, parent=None):
        super(InfoDialog, self).__init__(parent)
        self.st = st

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.lab = QtGui.QLabel(self.st)
        self.lay.addWidget(self.lab)

        self.but = QtGui.QPushButton("OK")
        self.but.clicked.connect(self.close)
        self.lay.addWidget(self.but)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Enter):
            self.close()
            event.accept()
        else:
            super(Dialog, self).keyPressEvent(event)

