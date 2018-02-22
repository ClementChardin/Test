import match as m
from PyQt4 import QtCore, QtGui

class ResultatWidget(QtGui.QWidget):
    def __init__(self, match, parent=None):
        super(ResultatWidget, self).__init__(parent)
        self.match = match

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.tabs = QtGui.QTabWidget()
        self.lay.addWidget(self.tabs)

        self.tab_score = ScoreWidget(match=self.match, parent=self)
        self.tabs.addTab(self.tab_score, "Score")

        self.tab_physionomie = PhysionomieWidget(match=self.match, parent=self)
        self.tabs.addTab(self.tab_physionomie, "Physionomie du match")

class ScoreWidget(QtGui.QWidget):
    def __init__(self, match, parent=None):
        super(ScoreWidget, self).__init__(parent)
        self.match = match

        self.setup_ui()

        self.show()

    def setup_ui(self):
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        #Score
        self.score_wid = QtGui.QWidget()
        self.score_lay = QtGui.QHBoxLayout()
        self.score_wid.setLayout(self.score_lay)
        self.lay.addWidget(self.score_wid)
        
        self.lab_nom1 = QtGui.QLabel(self.match.eq1.nom)
        self.score_lay.addWidget(self.lab_nom1)

        self.lab_score1 = QtGui.QLabel(str(self.match.eq1.score))
        self.score_lay.addWidget(self.lab_score1)

        self.lab_score2 = QtGui.QLabel(str(self.match.eq2.score))
        self.score_lay.addWidget(self.lab_score2)
        
        self.lab_nom2 = QtGui.QLabel(self.match.eq2.nom)
        self.score_lay.addWidget(self.lab_nom2)

        #Essais
        self.essais_lab = QtGui.QLabel("Essais")
        self.lay.addWidget(self.essais_lab)

        self.essais_wid = QtGui.QWidget()
        self.essais_lay = QtGui.QGridLayout()
        self.essais_wid.setLayout(self.essais_lay)
        self.lay.addWidget(self.essais_wid)

        for n_eq, eq in enumerate([self.match.eq1, self.match.eq2]):
            ll = eq.dict_essais.items()
            if ll == []:
                lab = QtGui.QLabel("")
                self.essais_lay.addWidget(lab, 0, n_eq)
            else:
                for i, (nom, es) in enumerate(ll):
                    lab = QtGui.QLabel(nom + " (" + str(es) + ")")
                    self.essais_lay.addWidget(lab, i, n_eq)

        #Transformations, Penalites et Drops

        for nom_attr in ("transformation", "penalite", "drop"):
            setattr(self, nom_attr + "_lab", QtGui.QLabel(nom_attr))
            self.lay.addWidget(getattr(self, nom_attr + "_lab"))

            setattr(self, nom_attr + "_wid", QtGui.QWidget())
            setattr(self, nom_attr + "_lay", QtGui.QGridLayout())
            getattr(self, nom_attr + "_wid").setLayout(getattr(self, nom_attr + "_lay"))
            self.lay.addWidget(getattr(self, nom_attr + "_wid"))

            for n_eq, eq in enumerate([self.match.eq1, self.match.eq2]):
                noms = []
                dic = getattr(eq, "dict_" + nom_attr + "s")
                rate = "_rates" if nom_attr == "drop" else "_ratees"
                dic_rate = getattr(eq, "dict_" + nom_attr + rate)
                if dic == {} and dic_rate == {}:
                    lab = QtGui.QLabel("")
                    getattr(self, nom_attr + "_lay").addWidget(lab, 0, n_eq)
                else:
                    for i, (nom, val) in enumerate(dic.items()):
                        try:
                            tot = val + dic_rate[nom]
                        except KeyError:
                            tot = val
                        lab = QtGui.QLabel(nom + " (" + str(val) + "/" + str(tot) + ")")
                        getattr(self, nom_attr + "_lay").addWidget(lab, i, n_eq)
                        noms.append(nom)
                    for k, (nom, val) in enumerate(dic_rate.items()):
                        if not nom in noms:
                            lab = QtGui.QLabel(nom + " (0/" + str(val) + ")")
                            getattr(self, nom_attr + "_lay").addWidget(lab, i+k+1, n_eq)
                            noms.append(nom)

        #Cartons
        for nom_attr in ("jaune", "rouge"):
            setattr(self, nom_attr + "_lab", QtGui.QLabel(nom_attr))
            self.lay.addWidget(getattr(self, nom_attr + "_lab"))

            setattr(self, nom_attr + "_wid", QtGui.QWidget())
            setattr(self, nom_attr + "_lay", QtGui.QGridLayout())
            getattr(self, nom_attr + "_wid").setLayout(getattr(self, nom_attr + "_lay"))
            self.lay.addWidget(getattr(self, nom_attr + "_wid"))

            for n_eq, eq in enumerate([self.match.eq1, self.match.eq2]):
                noms = []
                dic = getattr(eq, "dict_" + nom_attr + "s")
                ll = dic.items()
                if ll == []:
                    lab = QtGui.QLabel("")
                    getattr(self, nom_attr + "_lay").addWidget(lab, 0, n_eq)
                else:
                    for i, (nom, ca) in enumerate(ll):
                        lab = QtGui.QLabel(nom + " (" + str(ca) + ")")
                        getattr(self, nom_attr + "_lay").addWidget(lab, i, n_eq)

        #Blessures
        self.blessures_lab = QtGui.QLabel("Blessures")
        self.lay.addWidget(self.blessures_lab)

        self.blessures_wid = QtGui.QWidget()
        self.blessures_lay = QtGui.QGridLayout()
        self.blessures_wid.setLayout(self.blessures_lay)
        self.lay.addWidget(self.blessures_wid)

        for n_eq, eq in enumerate([self.match.eq1, self.match.eq2]):
            ll = eq.dict_blessures.items()
            if ll == []:
                lab = QtGui.QLabel("")
                self.blessures_lay.addWidget(lab, 0, n_eq)
            else:
                for i, (nom, es) in enumerate(ll):
                    lab = QtGui.QLabel(nom + " (" + str(es) + ")")
                    self.blessures_lay.addWidget(lab, i, n_eq)

class PhysionomieWidget(QtGui.QWidget):
    def __init__(self, match, parent=None):
        super(PhysionomieWidget, self).__init__(parent)
        self.match = match

        self.lay = QtGui.QGridLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        for ii, attr in enumerate(['essai', 'melee', 'touche', 'penalite']):
            lab = QtGui.QLabel("Occasions de " + attr )
            self.lay.addWidget(lab, 2*ii, 0)

            st = str(getattr(self.match.eq1, "occase_" + attr))
            lab1 = QtGui.QLabel(st)
            self.lay.addWidget(lab1, 2*ii +1, 0)

            st = str(getattr(self.match.eq2, "occase_" + attr))
            lab2 = QtGui.QLabel(st)
            self.lay.addWidget(lab2, 2*ii +1, 1)
