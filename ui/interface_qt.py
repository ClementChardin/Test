# -*- coding: cp1252 -*-
from PyQt4 import QtCore, QtGui
import selection as s
import sip
import biopopup as b
import rolespopup as rp
import choix_joueurs as cj
from miscellaneous_jouer_match import malus_tab, tab_rate
from couleurs import *
from diagramme_compo_widget import *
from ui.calendrier_equipe_widget import CalendrierEquipeWidget
#import time

N_caracs = len(s.ordre_caracs_joueurs.items())

class InterfaceWidget(QtGui.QWidget):
    def __init__(self,
                 ecran_precedant=None,
                 parent=None,
                 match=None,
                 saison=None,
                 fatigue=True,
                 nom_compo=None,
                 c_ou_s='c',
                 dat=None):
        super(InterfaceWidget, self).__init__(parent)
        self.ecran_precedant = ecran_precedant
        self.setWindowTitle("Interface Club")
        self.setGeometry(80, 100, 1200, 600)
        self.dat = s.lire_date() if dat is None else dat
        self.club = s.charger("vide", 'c', self.dat)
        self.comp = self.club.compo_defaut
        self.compo_sauvee = True
        self.match = match
        self.saison = self.parent().saison if saison is None else saison
        self.fatigue = fatigue
        self.nom_compo = self.club.nom+'_defaut' if nom_compo is None \
                         else nom_compo
        self.c_ou_s = c_ou_s

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

        #self.show()

    def closeEvent(self):
        if not self.match is None:
            self.close()
            self.match.show()

    def setup_ui(self):
        """
        self.splitter = QtGui.QSplitter(parent=self,
                     objectName='splitter',
                     frameShape=QtGui.QFrame.StyledPanel,
                     frameShadow=QtGui.QFrame.Plain)
        self.lay.addWidget(self.splitter)
        """
        self.col1 = Col1Widget(parent=self,
                               club=self.club,
                               comp=self.comp,
                               nom_compo=self.nom_compo,
                               c_ou_s=self.c_ou_s,
                               dat=self.dat)
        self.lay.addWidget(self.col1)
        #self.splitter.addWidget(self.col1)

        self.col2 = Col2Widget(parent=self,
                               club=self.club,
                               comp=self.comp,
                               nom_compo=self.nom_compo,
                               saison=self.saison,
                               buttons=True,
                               fatigue=self.fatigue,
                               dat=self.dat)
        self.lay.addWidget(self.col2)
        #self.splitter.addWidget(self.col2)

        #self.col3 = Col3Widget(club=self.club)
        poste_filtre = self.col3.poste_filtre if "col3" in dir(self) else "all"
        self.col3 = cj.ChoixJoueursWidget(parent=self,
                                          club=self.club,
                                          poste_filtre=poste_filtre,
                                          fatigue=self.fatigue,
                                          dat=self.dat)
        self.col3_lay = QtGui.QVBoxLayout()
        self.col3_lay.addWidget(self.col3)
        self.lay.addLayout(self.col3_lay)
        #self.splitter.addWidget(self.col3)

        #pour SelectionCompoWidget
        self.update_ui()
    
    def clean_ui(self):
        """
        self.lay.removeWidget(self.splitter)
        sip.delete(self.splitter)
        """
        self.lay.removeWidget(self.col1)
        sip.delete(self.col1)
        
        self.lay.removeWidget(self.col2)
        sip.delete(self.col2)

        self.lay.removeWidget(self.col3)
        self.col3.deleteLater()
    
    def set_club(self, nom):
        if not self.compo_sauvee:
            mb = QtGui.QMessageBox()
            if mb.question(None, "Question", "Sauvegarder compo avant de changer de club ?", "Non", "Oui") == 1:
                self.comp.sauvegarder(self.col2.nom.text(), self.club.nom, self.c_ou_s)
            self.compo_sauvee = True
        self.club = self.charger(nom)
        self.comp = self.club.compo_defaut_fatigue
        self.nom_compo = None
        self.set_fatigue(True)
        self.maj()

    def charger(self, nom):
        """
        Charge un club ou une selection
        la fonction est re ecrite pour la classe SelectionCompoWidget
        """
        return s.charger(nom, self.c_ou_s, self.dat)

    def update_ui(self):
        """
        Utile uniquement pour SelectionCompoWidget
        """
        pass

    def maj(self):#, fatigue=True):
        #pas besoin de modifier la valeur de self.fatigue
        self.clean_ui()
        self.setup_ui()
        #self.fatigue = fatigue

    def maj_compo(self, joueur, num):
        """ Mise à jour de la compo après changement d'un joueur"""
        self.comp = s.changer_un_joueur(joueur, self.comp, num, self.club)
        self.compo_sauvee = False
        print 'comp changed'
        
        self.maj()

    def maj_compo_2(self, nom_compo):
        """ Mise à jour de la compo après sélection d'une nouvelle compo de départ"""
        self.nom_compo = nom_compo
        self.comp = s.charger_compo(self.nom_compo, self.club.nom, self.c_ou_s, self.dat)
        self.maj()

    def maj_roles(self, couples):
        for role, joueur in couples:
            if not role in s.roles:
                raise ValueError("Mauvais role saisi : "+str(role))
            self.comp.roles[role] = joueur
        self.compo_sauvee = False
        s.set_caracs_old_compo(self.comp, self.club, fatigue=self.fatigue)
        self.comp.calc_totaux_old()
        print 'roles changes'

        self.maj()

    def set_fatigue(self, val):
        self.fatigue = val
        self.col3.fatigue = val
        self.col2.fatigue = val
        s.set_caracs_old_compo(self.comp, self.club, fatigue=self.fatigue)

class Col1Widget(QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 club=None,
                 comp=None,
                 nom_compo=None,
                 nom_comp_ref=None,
                 c_ou_s='c',
                 bool_diag=True,
                 dat=None):
        super(Col1Widget, self).__init__(parent)
        self.dat = s.lire_date() if dat is None else dat
        self.col1_lay = QtGui.QVBoxLayout()
        self.setLayout(self.col1_lay)
        self.club = club
        self.comp = comp
        self.c_ou_s = c_ou_s
        self.nom_compo = self.club.nom+'_defaut' if nom_compo is None \
                         else nom_compo
        self.comp_reference = s.charger_compo(self.nom_compo, self.club.nom, self.c_ou_s, self.dat) if nom_comp_ref is None \
                              else self.club.compo_defaut_fatigue
        self.bool_diag = bool_diag
        self.setMaximumWidth(200)
        
        #Choix equipe
        self.combo = QtGui.QComboBox()
        self.combo.setObjectName("Choix equipe")
        self.combo.addItem(self.club.nom)
        noms = s.noms_clubs() if self.c_ou_s == 'c' else s.noms_armees
        for nom in sorted(noms):
            if nom != self.club.nom:
                self.combo.addItem(nom)
        self.col1_lay.addWidget(self.combo)
        
        self.split = QtGui.QSplitter()
        #self.col1_lay.addWidget(self.split)

        #Choix compo
        self.combo2 = QtGui.QComboBox()
        self.combo2.setObjectName("Choix compo")
        for nom in self.club.compos_sauvees(self.dat):
            if nom == self.nom_compo:
                self.combo2.insertItem(0,nom)
                self.combo2.setCurrentIndex(0)
            else:
                self.combo2.addItem(nom)
        self.col1_lay.addWidget(self.combo2)

        self.combo2.activated['QString'].connect(self.set_comp)

        #Caracs
        self.caracs = CarWidget(comp=self.comp, comp_def=self.comp_reference)#s.charger_compo(self.club.nom+'_defaut', self.club.nom, self.c_ou_s))
        self.col1_lay.addWidget(self.caracs)
        self.col1_lay.addWidget(self.split)

        #Totaux
        self.tot = TotWidget(self.comp, comp_def=self.comp_reference)#s.charger_compo(self.club.nom+'_defaut', self.club.nom, self.c_ou_s))
        self.col1_lay.addWidget(self.tot)

        #Diagramme étoile
        if self.bool_diag:
            self.diag = DiagrammeCompoWidget(self.comp, nom_1=self.club.nom)
            self.diag.setGeometry(0, 0, 300, 300)
            self.col1_lay.addWidget(self.diag)

        #Choix club
        self.combo.activated['QString'].connect(self.parent().set_club)

    def set_comp(self, nom):
        self.nom_compo = nom
        self.comp = self.club.compo_defaut_fatigue \
                    if nom == self.club.nom + "_defaut" \
                    else s.charger_compo(nom, self.club.nom, self.c_ou_s, self.dat)
        self.parent().col2.nom.setText(self.club.nom + "_defaut")
        self.parent().maj_compo_2(self.nom_compo)

    def mettre_a_jour(self, club):
        self.caracs.mettre_a_jour(self.comp)
        self.tot.mettre_a_jour(self.comp)

class CarWidget(QtGui.QWidget):
    def __init__(self, comp, parent=None, comp_def=None):
        super(CarWidget, self).__init__(parent)
        self.comp_def = comp_def
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

            v_def = self.comp_def.caracs_old[k]
            self.car_values.append(QtGui.QLabel())
            if v < v_def:
                self.car_values[i].setStyleSheet("QLabel { color: rgba("+values_rouge+"); }")
            if v > v_def:
                self.car_values[i].setStyleSheet("QLabel { color: rgba("+values_vert+"); }")
            self.car_values[i].setText(str(v) + ' (' + str(v-v_def) + ')')
            self.car_lay.addWidget(self.car_values[i], i, 1)

    def mettre_a_jour(self, comp):
        self.setup_ui(comp)
         
class TotWidget(QtGui.QWidget):
    def __init__(self, comp, parent=None, comp_def=None):
        super(TotWidget, self).__init__(parent)
        self.comp = comp
        self.comp_def=comp_def
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

            v_def = self.comp_def.totaux_old[k]
            self.tot_values.append(QtGui.QLabel())
            if v < v_def:
                self.tot_values[i].setStyleSheet("QLabel { color: rgba("+values_rouge+"); }")
            if v > v_def:
                self.tot_values[i].setStyleSheet("QLabel { color: rgba("+values_vert+"); }")
            self.tot_values[i].setText(str(v) + ' (' + str(v-v_def) + ')')
            self.tot_lay.addWidget(self.tot_values[i], i, 1)

class Col2Widget(QtGui.QWidget):
    def __init__(self,
                 club=None,
                 parent=None,
                 comp=None,
                 nom_compo=None,
                 saison=None,
                 buttons=True,
                 fatigue=True,
                 dat=None):
        super(Col2Widget, self).__init__(parent)
        self.dat = s.lire_date() if dat is None else dat
        self.club = club
        self.comp = comp
        self.nom_compo = self.club.nom+'_defaut' if nom_compo is None \
                         else nom_compo
        self.saison = self.parent().saison if saison is None else saison
        self.buttons = buttons
        self.fatigue = fatigue
        
        self.col2_lay = QtGui.QVBoxLayout()
        self.setLayout(self.col2_lay)
        self.setMaximumWidth(200)

        self.setup_ui()

    def setup_ui(self):
        #Nom club et compo
        self.nom_club_lab = QtGui.QLabel(s.noms_complets[self.club.nom])
        font = self.nom_club_lab.font()
        font.setBold(True)
        self.nom_club_lab.setFont(font)
        self.col2_lay.addWidget(self.nom_club_lab)

        self.nom_lay = QtGui.QFormLayout()
        self.nom = QtGui.QLineEdit()
        self.nom.setText(self.nom_compo)
        self.nom_lay.addRow("Nom compo", self.nom)
        self.nom_wid = QtGui.QWidget()
        self.nom_wid.setLayout(self.nom_lay)
        self.col2_lay.addWidget(self.nom_wid)

        #Affichage compo
        self.comp_roles_lay = QtGui.QHBoxLayout()
        
        self.comp_lay = QtGui.QVBoxLayout()
        self.a_afficher = []
        self.font = QtGui.QFont("courrier", 8, italic=True)
        self.remp = QtGui.QLabel("Remplacants : ")
        self.remp.setFont(self.font)

        self.tit = QtGui.QLabel("Titulaires : ")
        self.tit.setFont(self.font)
        for i, (k, v) in enumerate(sorted(self.comp.joueurs.items(),
                                          key=lambda (k,v): int(k.split("n")[1]))):
            self.a_afficher.append(QtGui.QLabel(str(i+1) + " - " + v.nom))

        for ii, lab in enumerate(self.a_afficher):
            if ii == 0:
                self.comp_lay.addWidget(self.tit)
            elif ii == 15:
                self.split = QtGui.QSplitter()
                self.comp_lay.addWidget(self.split)
                self.comp_lay.addWidget(self.remp)
            self.comp_lay.addWidget(lab)

            if self.fatigue:
                #joueur blesse
                if self.comp.joueurs["n"+str(ii+1)].blessure > 0:
                    lab.setStyleSheet("QLabel { color: rgba("+values_indian_red+"); }")
                #joueur fatigue niveau 2
                elif self.comp.joueurs["n"+str(ii+1)].fatigue > 14:
                    lab.setStyleSheet("QLabel { color: rgba("+values_orange+"); }")
                #joueur fatigue niveau 1
                elif self.comp.joueurs["n"+str(ii+1)].fatigue > 7:
                    lab.setStyleSheet("QLabel { color: rgba("+values_jaune+"); }")

            #joueur deux fois dans la compo
            if self.comp.get_joueurs_noms().values().count(str(lab.text()).split(' - ')[1]) >1:
                lab.setStyleSheet("QLabel { color: rgba("+values_rouge+"); }")

        self.comp_roles_lay.addLayout(self.comp_lay)

        #Roles compo
        self.split = QtGui.QSplitter()
        self.comp_roles_lay.addWidget(self.split)
        self.roles = RolesWidget(comp=self.comp)
        self.comp_roles_lay.addWidget(self.roles)

        self.col2_lay.addLayout(self.comp_roles_lay)

        if self.buttons:
            #sauvegarder compo
            self.but_wid = QtGui.QWidget()
            self.but_lay = QtGui.QGridLayout()
            self.but_wid.setLayout(self.but_lay)
            
            self.sauv = QtGui.QPushButton("Sauver compo")
            self.sauv.clicked.connect(self.sauvegarder_compo)
            self.but_lay.addWidget(self.sauv, 0, 0)

            """
            #restaurer defaut
            self.reset = QtGui.QPushButton("Restaurer defaut")
            self.reset.clicked.connect(self.restaurer_defaut)
            self.but_lay.addWidget(self.reset, 1, 0)
            """

            #enlever fatigue
            self.enlever_fat = QtGui.QPushButton ("Enlever fatigue")
            self.enlever_fat.clicked.connect(self.enlever_fatigue)
            self.but_lay.addWidget(self.enlever_fat, 1, 0)
            if self.parent().fatigue:
                self.enlever_fat.setEnabled(True)
            else:
                self.enlever_fat.setEnabled(False)

            #remettre fatigue
            self.remettre_fat = QtGui.QPushButton ("Remettre fatigue")
            self.remettre_fat.clicked.connect(self.remettre_fatigue)
            self.but_lay.addWidget(self.remettre_fat, 2, 0)
            if self.parent().fatigue:
                self.remettre_fat.setEnabled(False)
            else:
                self.remettre_fat.setEnabled(True)

            """
            #restaurer defaut fatigue
            self.reset_fatigue = QtGui.QPushButton("Restaurer defaut fatigue")
            self.reset_fatigue.clicked.connect(self.restaurer_defaut_fatigue)
            self.but_lay.addWidget(self.reset_fatigue, 1, 1)
            """

            #Afficher calendrier
            self.afficher_cal = QtGui.QPushButton("Afficher calendrier")
            self.afficher_cal.clicked.connect(self.afficher_calendrier)
            self.but_lay.addWidget(self.afficher_cal, 1, 1)

            #retour à l'écran precedant
            if not self.parent().ecran_precedant is None:
                self.retour = QtGui.QPushButton("Retour a l'ecran precedant")
                self.retour.clicked.connect(self.retour_ecran_precedant)
                self.but_lay.addWidget(self.retour, 0, 1)

            #aide TAB
            self.aide_tab = QtGui.QPushButton("Aide TAB")
            self.aide_tab.clicked.connect(self.show_aide_tab)
            self.but_lay.addWidget(self.aide_tab, 2, 1)

            self.col2_lay.addWidget(self.but_wid)

        #Fixe la largeur
        self.setFixedWidth(350)

    def sauvegarder_compo(self):
        if self.nom.text() in self.parent().club.compos_sauvees() \
           and not self.comp.nom == self.nom.text():
            dial = QtGui.QDialog()
            lay = QtGui.QVBoxLayout()
            dial.setLayout(lay)
            lab = QtGui.QLabel(u"Ce nom de compo est déjà utilisé !")
            lay.addWidget(lab)
            but = QtGui.QPushButton('OK')
            lay.addWidget(but)
            but.clicked.connect(dial.close)
            dial.exec_()
        else:
            mb = QtGui.QMessageBox()
            if mb.question(None, "Confirmation", "Sauvegarder sous nom " + self.nom.text(), "Non", "Oui") == 1:
                self.comp.sauvegarder(self.nom.text(), self.club.nom, self.parent().c_ou_s)
                self.parent().compo_sauvee = True

    def restaurer_defaut(self):
        self.parent().comp = s.charger_compo(self.club.nom+'_defaut', self.club.nom, self.c_ou_s, self.dat)
        s.set_caracs_old_compo(self.parent().comp, self.club, sans_fatigue=True)
        self.parent().comp.calc_totaux_old()
        self.compo_sauvee = True
        self.parent().maj()

    """
    def restaurer_defaut_fatigue(self):
        self.parent().comp = self.club.compo_defaut_fatigue
        s.set_caracs_old_compo(self.parent().comp, self.club, fatigue=True)
        self.parent().comp.calc_totaux_old()
        self.compo_sauvee = True
        self.parent().maj()
    """

    def afficher_calendrier(self):
        self.calendrier_widget = CalendrierEquipeWidget(self.saison,
                                                        self.club.nom)
        self.calendrier_widget.show()

    def enlever_fatigue(self):
        self.parent().set_fatigue(False)

        self.comp.calc_totaux_old()

        self.compo_sauvee = False
        self.parent().maj()

    def remettre_fatigue(self):
        self.parent().set_fatigue(True)

        self.comp.calc_totaux_old()

        self.compo_sauvee = False
        self.parent().maj()

    def retour_ecran_precedant(self):
        if not self.parent().compo_sauvee:
            mb = QtGui.QMessageBox()
            if mb.question(None,
                           "Question",
                           "Sauvegarder compo avant de changer de club ?",
                           "Non",
                           "Oui") == 1:
                self.comp.sauvegarder(self.nom.text(),
                                      self.club.nom,
                                      self.c_ou_s)
            self.parent().compo_sauvee = True
        self.parent().col3.poste_filtre = 'all'
        self.parent().hide()
        self.parent().ecran_precedant.show()

    def show_aide_tab(self):
        self.aide_wid = AideWidget()
        self.aide_wid.show()

class AideWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AideWidget, self).__init__(parent)

        self.setGeometry(80, 100, 320, 400)


        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.lab1 = QtGui.QLabel("Valeur de base d'echec de tir au but")
        self.lay.addWidget(self.lab1)
        
        self.table_TB_vs_rate = QtGui.QTableWidget(2, 8)
        for TB in range(7, 15):
            self.table_TB_vs_rate.setCellWidget(0, TB-7, QtGui.QLabel(str(TB)))
            lab = QtGui.QLabel(str(tab_rate(TB)))
            self.table_TB_vs_rate.setCellWidget(1, TB-7, lab)
        self.table_TB_vs_rate.setVerticalHeaderLabels(['TB', 'rate'])
        self.table_TB_vs_rate.horizontalHeader().hide()
        self.table_TB_vs_rate.resizeColumnsToContents()
        self.lay.addWidget(self.table_TB_vs_rate)

        self.split = QtGui.QSplitter()
        self.lay.addWidget(self.split)

        self.lab2 = QtGui.QLabel("Malus en fonction de la puissance et de la zone")
        self.lay.addWidget(self.lab2)

        self.table_P_vs_zone = QtGui.QTableWidget(4, 8)
        for zone in range(1, 5):
            for P in range(6,14):
                val = malus_tab(P, zone)
                lab = QtGui.QLabel(str(val))
                self.table_P_vs_zone.setCellWidget(zone-1, P-6, lab)
        self.table_P_vs_zone.setHorizontalHeaderLabels([str(ii) for ii in range(6, 14)])
        self.table_P_vs_zone.setVerticalHeaderLabels([str(ii) for ii in range(1, 5)])
        self.table_P_vs_zone.resizeColumnsToContents()
        self.lay.addWidget(self.table_P_vs_zone)

class RolesWidget(QtGui.QWidget):
    def __init__(self, parent=None, comp=None):
        super(RolesWidget, self).__init__(parent)
        self.comp = comp
        self.roles = self.comp.roles

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.a_afficher = []
        noms = [jj.nom for jj in self.comp.joueurs.values()]

        for (k, v) in sorted(self.roles.items(), key=lambda (k,v):s.ordre_roles[k]):
            lab = QtGui.QLabel(k + " - " + v.nom + " : " + s.carac_roles[k] + " = " + str(v.caracs[s.carac_roles[k]]))
            if not v.nom in self.comp.noms_remplacants + self.comp.noms_titulaires:
                lab.setStyleSheet("color: red")
            elif not v.nom in self.comp.noms_titulaires:
                lab.setStyleSheet("color: orange")
            self.a_afficher.append(lab)

        for lab in self.a_afficher:
            self.lay.addWidget(lab)

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
        for p in sorted(self.club.joueurs.keys(),
                        key=lambda p:s.ordre_postes[p]):
            for jj in self.club.joueurs[p]:
                c = 0
                self.mod.setItem(r, c, MyItem(jj.nom, club=self.club))
                c = 1
                for poste in sorted(s.ordre_postes.keys(),
                                    key=lambda p:s.ordre_postes[p]):
                    if (poste in jj.postes or \
                        (jj.joue_centre() and s.est_poste_centre(poste))) and \
                        poste != 'CE':
                        st = jj.postes.index(poste)
                        if poste in ['C1', 'C2'] and st == '':
                            st = jj.postes.index('CE')
                        if st == '':
                            st = jj.postes.index('C1')
                        if st == '':
                            st = jj.postes.index('C2')
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
        self.vue = QtGQTableView()
        self.vue.setModel(self.mod)

        #Cacher l'en-tete de lignes
        self.vue.verticalHeader().hide()

        #Selection par lignes
        self.vue.setSelectionBehavior(QtGQAbstractItemView.SelectRows)

        #Valeurs non editables
        self.vue.setEditTriggers(QtGQAbstractItemView.NoEditTriggers)

        #Classement
        self.vue.setSortingEnabled(True)

        #Largeur des colones
        self.vue.resizeColumnsToContents()

        self.col3_lay = QtGui.QVBoxLayout()
        self.col3_lay.addWidget(self.vue)

        self.setLayout(self.col3_lay)

        #Connect double clic
        self.vue.doubleClicked.connect(self.maj_compo_aux_1)

    def maj_compo_aux_1(self):
        r = self.vue.currentIndex().row()
        nom = self.mod.item(r,0).text()
        self.maj_compo_aux_2(nom)
        
    def maj_compo_aux_2(self, nom):
        joueur = self.club.get_joueur_from_nom(nom)

        self.num, ok = QtGQInputDialog.getText(QtGui.QWidget(), 'Input Dialog', 'Nouveau numero pour ' + joueur.nom + ' :')
        self.num = 'n'+str(self.num)
        print self.num
        if ok:
            self.vue.clearSelection()
            self.parent().maj_compo(joueur, self.num)

    def contextMenuEvent(self, event):
        self.menu = QtGQMenu(self)
        
        bioAction = QtGQAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        compAction = QtGQAction('Ajouter a la compo', self)
        compAction.triggered.connect(self.ajouter_compo_mult)
        self.menu.addAction(compAction)

        roleAction = QtGQAction('Assigner un role', self)
        roleAction.triggered.connect(self.assigner_role_mult)
        self.menu.addAction(roleAction)

        self.menu.popup(QtGQCursor.pos())

    def afficher_bio(self):
        joueurs = []
        for mi in self.vue.selectionModel().selectedRows():
            r = mi.row()
            nom = self.mod.item(r,0).text()
            jj = self.club.get_joueur_from_nom(nom)
            joueurs.append(jj)
        
        self.pop = b.BioPopup(joueurs=joueurs, col3=self, dat=s.lire_date())
        self.pop.show()

    def assigner_role_mult(self):
        joueurs = []
        for mi in self.vue.selectionModel().selectedRows():
            r = mi.row()
            nom = self.mod.item(r,0).text()
            joueur = self.club.get_joueur_from_nom(nom)
            joueurs.append(joueur)
        self.role_pop = rp.RolePopupWidget(joueurs=joueurs, main=self.parent())
        self.role_pop.show()
        
    def ajouter_compo_mult(self):
        for mi in self.vue.selectionModel().selectedRows():
            r = mi.row()
            nom = self.mod.item(r,0).text()
            self.maj_compo_aux_2(nom)
    
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
            self.sortKey = s.ordre_postes[jj.postes[1]]

    #Qt uses a simple < check for sorting items, override this to use the sortKey
    def __lt__(self, other):
        return self.sortKey < other.sortKey

