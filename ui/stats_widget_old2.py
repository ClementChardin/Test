from PyQt4 import QtGui, QtCore

class StatsWidget(QtGui.QWidget):
    def __init__(self, calendiers, parent=None):
        super(StatsWidget, self).__init__(parent)

        self.calendiers = calendiers

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.tabs = QtGui.QTabWidget()
        self.lay.addWidget(self.tabs)

        self.stats_joueurs = StatsJoueursWidget(self.calendiers)
        self.tabs.addTab(self.stats_joueurs, "Stats Joueurs")

        self.stats_equipes = StatsEquipesWidget(self.calendiers)
        self.tabs.addTab(self.stats_equipes, "Stats Equipes")

        self.setGeometry(QtCore.QRect(492, 162, 374, 418))

class StatsJoueursWidget(QtGui.QWidget):
    def __init__(self, calendiers, parent=None):
        super(StatsJoueursWidget, self).__init__(parent)

        self.calendriers = calendiers
        self.noms_cals = []
        for cal in self.calendriers:
            self.noms_cals.append(cal.nom_championnat)
        self.idx_cal_actif = 0

        self.attrs = ['Essais', 'Transformations', 'Penalites', 'Drops', 'Points']
        #, 'Points']
        self.idx_attr_actif = 0

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.lay_combos = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_combos)

        self.combo_cal = QtGui.QComboBox()
        for nom in self.noms_cals:
            self.combo_cal.addItem(nom)
        self.combo_cal.activated['QString'].connect(self.maj_cal)
        self.lay_combos.addWidget(self.combo_cal)

        self.combo_attr = QtGui.QComboBox()
        for attr in self.attrs:
            self.combo_attr.addItem(attr)
        self.combo_attr.activated['QString'].connect(self.maj_attr)
        self.lay_combos.addWidget(self.combo_attr)

        self.tables = []
        for ii in range(len(self.calendriers)):
            tables = []
            for jj in range(len(self.attrs)):
                ll = self.get_classement(ii, jj)

                table = QtGui.QTableWidget(10, 3)
                hlabels = ['Nom', 'Club', self.attrs[jj]]
                table.setHorizontalHeaderLabels(hlabels)

                for kk, tu in enumerate(ll):
                    nom = tu[0]
                    club = '' #Pas implémenté dans calendrier.get_classement_joueur
                    val = str(tu[1]) #Sera tu[2] à la fin

                    table.setItem(kk, 0, QtGui.QTableWidgetItem(nom))
                    table.setItem(kk, 1, QtGui.QTableWidgetItem(club))
                    table.setItem(kk, 2, QtGui.QTableWidgetItem(val))

                self.lay.addWidget(table)
                if not (ii == self.idx_cal_actif and jj == self.idx_attr_actif):
                    table.hide()
                tables.append(table)
            self.tables.append(tables)

    @property
    def cal_actif(self):
        return self.calendriers[self.idx_cal_actif]

    @property
    def nom_cal_actif(self):
        return self.noms_cals[self.idx_cal_actif]

    @property
    def attr_actif(self):
        return self.attrs[self.idx_attr_actif]

    def get_classement(self, idx_cal, idx_attr):
        cal = self.calendriers[idx_cal]
        attr = self.attrs[idx_attr]

        maj = attr[0]
        min = chr(ord(maj)+32)

        attr = min + attr[1:]
        ll = cal.get_classement_joueurs(attr)[:10]
        return ll

    def cacher_table(self):
        ii, jj = self.idx_cal_actif, self.idx_attr_actif
        self.tables[ii][jj].hide()

    def montrer_table(self):
        ii, jj = self.idx_cal_actif, self.idx_attr_actif
        self.tables[ii][jj].show()

    def maj_cal(self, nom_cal):
        self.cacher_table()
        self.idx_cal_actif = self.noms_cals.index(nom_cal)
        self.montrer_table()

    def maj_attr(self, attr):
        self.cacher_table()
        self.idx_attr_actif = self.attrs.index(attr)
        self.montrer_table()

class StatsEquipesWidget(QtGui.QWidget):
    def __init__(self, calendiers, parent=None):
        super(StatsEquipesWidget, self).__init__(parent)
        pass
