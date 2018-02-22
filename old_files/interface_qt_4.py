# -*- coding: cp1252 -*-
from PyQt4 import QtCore, QtGui
import selection as s
import sip
import biopopup as b
import time

N_caracs = len(s.ordre_caracs_joueurs.items())

class InterfaceWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(InterfaceWidget, self).__init__(parent)
        self.setWindowTitle("Interface Club")
        self.setGeometry(100, 100, 1100, 600)
        self.club = s.club(nom="")
        self.comp = self.club.compo_defaut
        self.compo_sauvee = True

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

        self.show()

    def setup_ui(self):
        self.col1 = Col1Widget(parent=self, club=self.club, comp=self.comp)
        self.col1_lay = QtGui.QVBoxLayout()
        self.col1_lay.addWidget(self.col1)
        self.lay.addLayout(self.col1_lay)
       
        self.col2 = Col2Widget(club=self.club, comp=self.comp)
        self.col2_lay = QtGui.QVBoxLayout()
        self.col2_lay.addWidget(self.col2)
        self.lay.addLayout(self.col2_lay)

        self.col3 = Col3Widget(club=self.club)
        self.col3_lay = QtGui.QVBoxLayout()
        self.col3_lay.addWidget(self.col3)
        self.lay.addLayout(self.col3_lay)

    """
    def setup_ui2(self):
        self.col1 = Col1Widget(parent=self, club=self.club, comp=self.comp)
        self.col1_lay = QtGui.QVBoxLayout()
        self.col1_lay.addWidget(self.col1)
        self.lay.addLayout(self.col1_lay)
        time.sleep(2)
        print 'col1'
       
        self.col2 = Col2Widget(club=self.club, comp=self.comp)
        self.col2_lay = QtGui.QVBoxLayout()
        self.col2_lay.addWidget(self.col2)
        self.lay.addLayout(self.col2_lay)
        time.sleep(2)
        print 'col2'

        self.col3 = Col3Widget(club=self.club)
        self.col3_lay = QtGui.QVBoxLayout()
        self.col3_lay.addWidget(self.col3)
        self.lay.addLayout(self.col3_lay)
        time.sleep(2)
        print 'col3'
    """
    
    def clean_ui(self):
        self.lay.removeWidget(self.col1)
        sip.delete(self.col1)
        
        self.lay.removeWidget(self.col2)
        sip.delete(self.col2)

        self.lay.removeWidget(self.col3)
        print 'removed'
        print 'removed'
        self.col3.deleteLater()
        #sip.delete(self.col3)
        print 'deleted'
        print 'deleted'
    
    def set_club(self, nom):
        if not self.compo_sauvee:
            mb = QtGui.QMessageBox()
            if mb.question(None, "Question", "Sauvegarder compo avant de changer de club ?", "Non", "Oui") == 1:
                self.comp.sauvegarder(self.col2.nom.text(), self.club.nom, 'c')
                self.compo_sauvee = True
        self.club = s.charger(nom, 'c')
        self.comp = self.club.compo_defaut
        self.clean_ui()
        self.setup_ui()

    def maj_compo(self, joueur, num):
        self.comp = s.changer_un_joueur(joueur, self.comp, num, self.club)
        self.compo_sauvee = False
        print 'comp changed'
        
        self.clean_ui()
        print 'cleaned'
        #return
        #time.sleep(2)
        
        self.setup_ui()
        print 'finished'
        print 'finished'
        
class Col1Widget(QtGui.QWidget):
    def __init__(self, parent=None, club=None, comp=None):
        super(Col1Widget, self).__init__(parent)
        self.col1_lay = QtGui.QVBoxLayout()
        self.setLayout(self.col1_lay)
        self.club = club
        self.comp = comp
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
        self.caracs.mettre_a_jour(self.comp)
        self.tot.mettre_a_jour(self.comp)

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
    def __init__(self, club=None, parent=None, comp=None):
        super(Col2Widget, self).__init__(parent)
        self.club = club
        self.comp = comp
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
        for i, (k, v) in enumerate(sorted(self.comp.joueurs.items(), key=lambda (k,v): int(k.split("n")[1]))):
            self.a_afficher.append(QtGui.QLabel(str(i+1) + " - " + v.nom))

        for i, l in enumerate(self.a_afficher):
            if i == 0:
                self.col2_lay.addWidget(self.tit)
            elif i == 15:
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
        self.parent().compo_sauvee = True
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
        c = 0
        for p in sorted(self.club.joueurs.keys(), key=lambda p:s.ordre_postes[p]):
            for jj in self.club.joueurs[p]:
                c = 0
                self.mod.setItem(r, c, MyItem(jj.nom, club=self.club))
                c = 1
                for poste in sorted(s.ordre_postes.keys(), key=lambda p:s.ordre_postes[p]):
                    if (poste in jj.postes.values() or (jj.joue_centre() and s.est_poste_centre(poste))) and poste != 'CE':
                        st = get_first_key_from_value(jj.postes, poste)
                        if poste in ['C1', 'C2'] and st == '':
                            st = get_first_key_from_value(jj.postes, 'CE')
                        if st == '':
                            st = get_first_key_from_value(jj.postes, 'C1')
                        if st == '':
                            st = get_first_key_from_value(jj.postes, 'C2')
                        if st == '':
                            num = ''
                        else:
                            num = ' (' + st.split('poste')[1] + ')'
                        self.mod.setItem(r,
                                         c,
                                         MyItem(('%0.2f' % s.calc_EV(jj, poste) + num)
                                                , club=self.club)
                                         )
                    if poste != 'CE':
                        c += 1
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
        self.vue.doubleClicked.connect(self.maj_compo_aux)

    def maj_compo_aux(self):
        r = self.vue.currentIndex().row()
        nom = self.mod.item(r,0).text()
        joueur = self.club.get_joueur_from_nom(nom)

        self.num, ok = QtGui.QInputDialog.getText(QtGui.QWidget(), 'Input Dialog', 'Nouveau numero pour ' + joueur.nom + ' :')
        self.num = 'n'+str(self.num)
        print self.num
        if ok:
            self.vue.clearSelection()
            self.parent().maj_compo(joueur, self.num)

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        self.menu.popup(QtGui.QCursor.pos())

    def afficher_bio(self):
        joueurs = []
        for mi in self.vue.selectionModel().selectedRows():
            r = mi.row()
            nom = self.mod.item(r,0).text()
            jj = self.club.get_joueur_from_nom(nom)
            joueurs.append(jj)
        
        self.pop = b.BioPopup(joueurs=joueurs)
        self.pop.show()        
    
def get_first_key_from_value(dic, val):
    res = ''
    for k in dic.keys():
        if dic[k] == val:
            res = k
            break
    return res

class MyItem(QtGui.QStandardItem):
    def __init__(self, text, club):
        #call custom constructor with UserType item type
        QtGui.QStandardItem.__init__(self, QtGui.QStandardItem.UserType)
        self.setText(text)
        self.club = club
        if str(self.text())[0].isdigit():
            self.sortKey = float(str(self.text()).split(' ')[0])
        elif str(self.text())[0].isalpha():
            nom = str(self.text())
            jj = self.club.get_joueur_from_nom(nom)
            self.sortKey = s.ordre_postes[jj.postes['poste1']]

    #Qt uses a simple < check for sorting items, override this to use the sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey


        


