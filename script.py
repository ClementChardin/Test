from ui.master import MasterWidget
import sys
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)
M = MasterWidget()
app.exec_()
