# -*- coding: cp1252 -*-
from PyQt4 import QtCore, QtGui
import selection as s
import sip

N_caracs = len(s.ordre_caracs_joueurs.items())

class InterfaceWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(InterfaceWidget, self).__init__(parent)
        self.setWindowTitle("Interface Club")
        self.setGeometry(100, 100, 1100, 600)
        self.club = s.club(nom="")

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

        self.show()

    def setup_ui(self):
        self.col1 = Col1Widget(parent=self, club=self.club)
        self.col1_lay = QtGui.QVBoxLayout()
        self.col1_lay.addWidget(self.col1)
        self.lay.addLayout(self.col1_lay)

        self.col2 = Col2Widget(club=self.club)
        self.col2_lay = QtGui.QVBoxLayout()
        self.col2_lay.addWidget(self.col2)
        self.lay.addLayout(self.col2_lay)

        self.col3 = Col3Widget(club=self.club)
        self.col3_lay = QtGui.QVBoxLayout()
        self.col3_lay.addWidget(self.col3)
        self.lay.addLayout(self.col3_lay)

    def clean_ui(self):
        self.lay.removeWidget(self.col1)
        sip.delete(self.col1)

        self.lay.removeWidget(self.col2)
        sip.delete(self.col2)

        self.lay.removeWidget(self.col3)
        sip.delete(self.col3)
        
    def set_club(self, nom):
        self.club = s.charger(nom, 'c')
        self.clean_ui()
        self.setup_ui()
        
class Col1Widget(QtGui.QWidget):
    def __init__(self, parent=None, club=None):
        super(Col1Widget, self).__init__(parent)
        self.col1_lay = QtGui.QVBoxLayout()
        self.setLayout(self.col1_lay)
        self.club = club
        self.comp = self.club.compo_defaut()
        self.setMaximumWidth(200)
        
        #Choix equipe
        self.combo = QtGui.QComboBox()
        self.combo.setObjectName("Choix equipe")
        self.combo.addItem(self.club.nom)
        for nom in sorted(s.noms_clubs):
            if nom != self.club.nom:
                self.combo.addItem(nom)
        self.col1_lay.addWidget(self.combo)
        self.split = QtGui.QSplitter()
        self.col1_lay.addWidget(self.split)

        #Caracs
        self.caracs = CarWidget(self.comp)
        self.col1_lay.addWidget(self.caracs)
        self.split = QtGui.QSplitter()
        self.col1_lay.addWidget(self.split)

        #Totaux
        self.tot = TotWidget(self.comp)
        self.col1_lay.addWidget(self.tot)

        #Choix club
        self.combo.activated['QString'].connect(self.parent().set_club)

    def mettre_a_jour(self, club):
        self.caracs.mettre_a_jour(club.compo_defaut)
        self.tot.mettre_a_jour(club.compo_defaut)

class CarWidget(QtGui.QWidget):
    def __init__(self, comp, parent=None):
        super(CarWidget, self).__init__(parent)
        self.comp = comp
        self.car_lay = QtGui.QGridLayout()
        self.setLayout(self.car_lay)
        self.car_noms = []
        self.car_values = []
        
        self.setup_ui(self.comp)

    def setup_ui(self, comp):
        self.comp = comp
        self.caracs = comp.caracs_old

        for w in self.car_noms:
            self.car_lay.removeWidget(w)
        for w in self.car_values:
            self.car_lay.removeWidget(w)
        for i, (k,v) in enumerate(sorted(self.caracs.items(), key = lambda (k,v): s.ordres_caracs_compo[k])):
            self.car_noms.append(QtGui.QLabel())
            self.car_noms[i].setText(k)
            self.car_lay.addWidget(self.car_noms[i], i, 0)

            self.car_values.append(QtGui.QLabel())
            self.car_values[i].setText(str(v))
            self.car_lay.addWidget(self.car_values[i], i, 1)

    def mettre_a_jour(self, comp):
        self.setup_ui(comp)
         
class TotWidget(QtGui.QWidget):
    def __init__(self, comp, parent=None):
        super(TotWidget, self).__init__(parent)
        self.comp = comp
        self.tot_lay = QtGui.QGridLayout()
        self.setLayout(self.tot_lay)

        self.tot_noms = []
        self.tot_values = []

        self.mettre_a_jour(self.comp)

    def mettre_a_jour(self, comp):
        self.comp = comp
        self.tot = comp.totaux_old
        for w in self.tot_noms:
            self.tot_lay.removeWidget(w)
        for w in self.tot_values:
            self.tot_lay.removeWidget(w)
        for i, (k, v) in enumerate(sorted(self.tot.items(), key = lambda (k,v): k.split('T')[1])):
            self.tot_noms.append(QtGui.QLabel())
            self.tot_noms[i].setText(k)
            self.tot_lay.addWidget(self.tot_noms[i], i, 0)

            self.tot_values.append(QtGui.QLabel())
            self.tot_values[i].setText(str(v))
            self.tot_lay.addWidget(self.tot_values[i], i, 1)

class Col2Widget(QtGui.QWidget):
    def __init__(self, club=None, parent=None):
        super(Col2Widget, self).__init__(parent)
        self.club = club
        self.comp = club.compo_defaut
        self.col2_lay = QtGui.QVBoxLayout()
        self.setLayout(self.col2_lay)
        self.setMaximumWidth(200)

        self.setup_ui()

    def setup_ui(self):
        #Nom compo
        self.nom_lay = QtGui.QFormLayout()
        self.nom = QtGui.QLineEdit()
        self.nom.setText(self.club.nom + "_defaut")
        self.nom_lay.addRow("Nom compo", self.nom)
        self.col2_lay.addLayout(self.nom_lay)

        #Affichage compo
        self.comp_lay = QtGui.QVBoxLayout()
        self.a_afficher = []
        self.font = QtGui.QFont("courrier", 8, italic=True)
        self.remp = QtGui.QLabel("Remplacants : ")
        self.remp.setFont(self.font)

        self.tit = QtGui.QLabel("Titulaires : ")
        self.tit.setFont(self.font)
        self.col2_lay.addWidget(self.tit)
        for i, (k, v) in enumerate(sorted(self.comp.joueurs.items(), key=lambda (k,v): int(k.split("n")[1]))):
            self.a_afficher.append(QtGui.QLabel(str(i+1) + " - " + v.nom))

        for i, l in enumerate(self.a_afficher):
            if i == 15:
                self.split = QtGui.QSplitter()
                self.comp_lay.addWidget(self.split)
                self.comp_lay.addWidget(self.remp)
            self.comp_lay.addWidget(l)

        self.col2_lay.addLayout(self.comp_lay)

        #sauvegarder compo
        self.sauv = QtGui.QPushButton("Sauver compo")
        self.sauv.clicked.connect(self.sauvegarder_compo)
        self.col2_lay.addWidget(self.sauv)
    
    def sauvegarder_compo(self):
        mb = QtGui.QMessageBox()
        if mb.question(None, "Confirmation", "Sauvegarder sous nom " + self.nom.text(), "Non", "Oui") == 1:
            self.comp.sauvegarder(self.nom.text(), self.club.nom, 'c')


class Col3Widget(QtGui.QWidget):
    def __init__(self, parent=None, club=None):
        super(Col3Widget, self).__init__(parent)
        self.club = club
        self.joueurs = []
        for l in self.club.joueurs.values():
            for jj in l:
                self.joueurs.append(jj)

        self.mod = QtGui.QStandardItemModel(10, 10)
        self.setup_model()

        self.setup_ui()

    def setup_model(self):
        r = 0
        """
        c = 0
        r_lab = []
        for (p,l) in sorted(self.club.joueurs.items(), key=lambda (p,l):s.ordre_postes[p]):
            for i, jj in enumerate(l):
                c = 0
                self.mod.setItem(r, c, QtGui.QStandardItem(jj.nom))
                c +=1
                for car in jj.caracs.keys():
                    if car != 'RP_tot':
                        self.mod.setItem(r, c, QtGui.QStandardItem(str(jj.caracs[car])))
                        c += 1
                for key in sorted(jj.postes.keys(), key = lambda k: k.split('poste')[1]):
                    poste = jj.postes[key]
                    if poste != '':
                        if poste in ['C1', 'CE']:
                            self.mod.setItem(r, c, QtGui.QStandardItem("C1 : " + ('%0.2f' % s.calc_EV(jj, 'C1'))
                                                                       + "C2 : " + ('%0.2f' % s.calc_EV(jj, 'C2'))))
                        elif poste == 'C2':
                            self.mod.setItem(r, c, QtGui.QStandardItem("C2 : " + ('%0.2f' % s.calc_EV(jj, 'C2'))
                                                                       + "\nC1 : " + ('%0.2f' % s.calc_EV(jj, 'C1'))))

                        else:
                            self.mod.setItem(r, c, QtGui.QStandardItem(poste + " : " + ('%0.2f' % s.calc_EV(jj, poste))))
                    else:
                        self.mod.setItem(r, c, QtGui.QStandardItem(""))
                    c += 1
                r_lab.append(jj.postes['poste1'])
                r += 1
        #self.mod.setVerticalHeaderLabels(r_lab)
        """

        for p in sorted(self.club.joueurs.keys(), key=lambda p:s.ordre_postes[p]):
            for jj in self.club.joueurs[p]:
                self.mod.setItem(r, 0, QtGui.QStandardItem(jj.nom))
                for poste in sorted(s.ordre_postes.keys(), key=lambda p:s.ordre_postes[p]):
                    if poste in jj.postes.values() and poste != 'CE':
                        st = get_first_key_from_value(jj.postes, poste)
                        if poste in ['C1', 'C2'] and st == None:
                            st = get_first_key_from_value(jj.postes, 'CE')
                        if st == None:
                            num = ''
                        else:
                            num = ' (' + st.split('poste')[1] + ')'
                        self.mod.setItem(r, s.ordre_postes[poste]+1, QtGui.QStandardItem(('%0.2f' % s.calc_EV(jj, poste)) ))# + num))
                r += 1

        c_lab = ["Nom"]
        for p in sorted(s.ordre_postes.keys(), key=lambda p:s.ordre_postes[p]):
            if p != 'CE':
                c_lab.append(p)
                    
        self.mod.setHorizontalHeaderLabels(c_lab)
    

    def setup_ui(self):
        self.vue = QtGui.QTableView()
        self.vue.setModel(self.mod)

        #Cacher l'en-tete de lignes
        self.vue.verticalHeader().hide()

        #Selection par lignes
        self.vue.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #Valeurs non editables
        self.vue.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        #Classement
        self.vue.setSortingEnabled(True)

        #Largeur des colones
        self.vue.resizeColumnsToContents()

        self.col4_lay = QtGui.QVBoxLayout()
        self.col4_lay.addWidget(self.vue)

        self.setLayout(self.col4_lay)

        #Connect double clic
        self.vue.doubleClicked.connect(self.func)

    def func(self):
        r = self.vue.currentIndex().row()
        print self.mod.item(r,0).text()

def get_first_key_from_value(dic, val):
    res = None
    for k in dic.keys():
        if dic[k] == val:
            return k
    return None

        
        
"""
class MyTableWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self, text):
        #call custom constructor with UserType item type
        QtGui.QTableWidgetItem.__init__(self, text, QtGui.QTableWidgetItem.UserType)
        try:
            self.sortKey = float(str(self.text()).split(' ')[0])
        except ValueError:
            self.sortKey = str(self.text())

    #Qt uses a simple < check for sorting items, override this to use the sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey
"""


