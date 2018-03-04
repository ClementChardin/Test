from PyQt4 import QtGui, QtCore
from ui.master import MasterWidget
import sys

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    master = MasterWidget()
    master.show()
    sys.exit(app.exec_())
