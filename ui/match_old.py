# -*- coding: cp1252 -*-
import sip
import interface_qt as iqt
import selection as s
import resultat as r
import calendrier as cal
from PyQt4 import QtGui, QtCore
from tournoi import Match
from diagramme_compo_widget import *

class MatchWidget(QtGui.QWidget):
    def __init__(self,
                 ecran_precedant=None,
                 parent=None,
                 c_ou_s='c',
                 calendriers=[]):
        super(MatchWidget, self).__init__(parent)
        self.ecran_precedant = ecran_precedant
        self.c_ou_s = c_ou_s
        self.calendriers = calendriers
        
        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        self.col_eq1 = EquipeWidget(parent=self, c_ou_s=self.c_ou_s)
        self.lay.addWidget(self.col_eq1)

        self.col_eq2 = EquipeWidget(parent=self, c_ou_s=self.c_ou_s)
        self.lay.addWidget(self.col_eq2)

        self.col_match = ColMatchWidget(parent=self,
                                        c_ou_s=self.c_ou_s,
                                        calendriers=self.calendriers)
        self.lay.insertWidget(1, self.col_match)

        self.show()

    def update_ui(self):
        """
        Pour la classe fille MacthSelectionWidget
        """
        pass

class EquipeWidget(QtGui.QWidget):
    def __init__(self, parent=None, c_ou_s='c'):
        super(EquipeWidget, self).__init__(parent)
        self.c_ou_s = c_ou_s
        self.equipe = s.club(nom="Vide")
        self.comp = s.compo()
        self.nom_compo = ""
        self.fatigue = True

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        self.col1 = iqt.Col1Widget(parent=self,
                                   club=self.equipe,
                                   comp=self.comp,
                                   nom_compo=self.nom_compo,
                                   nom_comp_ref='defaut',
                                   c_ou_s=self.c_ou_s,
                                   bool_diag=False)
        self.lay.addWidget(self.col1)
        self.setup_col1()

        self.col2 = iqt.Col2Widget(parent=self,
                                   club=self.equipe,
                                   comp=self.comp,
                                   buttons=False)
        self.lay.addWidget(self.col2)
        self.setup_col2()

    def setup_col1(self):
        #Bouton 'creer compo'
        self.col1.creer = QtGui.QPushButton("Creer compo")
        self.col1.col1_lay.insertWidget(2, self.col1.creer)

        self.col1.creer.clicked.connect(self.creer_compo)

    def setup_col2(self):
        self.col2.nom_wid.hide()

    def maj_compo_2(self, nom_compo):
        self.nom_compo = nom_compo
        self.comp = s.charger_compo(nom_compo, self.equipe.nom, self.c_ou_s)
        self.maj()
        
    def clean_ui(self):
        self.lay.removeWidget(self.col1)
        sip.delete(self.col1)
        self.lay.removeWidget(self.col2)
        sip.delete(self.col2)

    def maj(self):
        self.clean_ui()
        self.setup_ui()
        self.parent().col_match.faire_diagramme()
        
    def set_club(self, nom):
        self.equipe = s.charger(nom, self.c_ou_s)
        self.comp = self.equipe.compo_defaut_fatigue
        self.maj()

    def creer_compo(self):
        #self.I = iqt.InterfaceWidget(match=self.parent())
        if not self.parent().parent() is None:
            I = self.parent().parent().interface_widget if self.c_ou_s == 'c' \
                else self.parent().parent().selection_compo_widget
            I.set_club(self.equipe.nom)
            I.ecran_precedant = self.parent()
            I.show()
            self.parent().hide()
        else:
            M = QtGQMessageBox()
            M.setText("Pas de MasterUI definie !")
            M.show()

class ColMatchWidget(QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 c_ou_s='c',
                 calendriers=[]):
        super(ColMatchWidget, self).__init__(parent)
        self.c_ou_s = c_ou_s
        self.calendriers = calendriers
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.championat_prochain_match = None

        self.setup_ui()
        
    def setup_ui(self):
        #Commencer le match
        self.commencer_but = QtGui.QPushButton("Commencer le match")
        self.lay.addWidget(self.commencer_but)
        self.commencer_but.clicked.connect(self.commencer)

        #Type de match
        self.rad_championat = QtGui.QRadioButton("Championat")
        self.rad_championat.setChecked(True)
        self.lay.addWidget(self.rad_championat)
        
        self.rad_coupe = QtGui.QRadioButton("Coupe")
        self.lay.addWidget(self.rad_coupe)

        #Sauvegarder les résultats
        self.sauv_check = QtGui.QCheckBox("Conserver resultats")
        self.lay.addWidget(self.sauv_check)

        #Terrain neutre
        self.neutre_check = QtGui.QCheckBox("Terrain neutre")
        self.lay.addWidget(self.neutre_check)

        #Coupe du monde
        self.check_coupe_monde = QtGui.QCheckBox("Coupe du monde")
        self.lay.addWidget(self.check_coupe_monde)
        self.check_coupe_monde.setChecked(False)
        self.check_coupe_monde.hide()

        #Phase finale
        self.finale_check = QtGui.QCheckBox("Phase finale")
        self.lay.addWidget(self.finale_check)

        #Retour ecran precedant
        self.retour_but = QtGui.QPushButton("Retour a l'ecran precedant")
        self.lay.addWidget(self.retour_but)
        self.retour_but.clicked.connect(self.retour_ecran_precedant)

        #Prochains matches
        self.lay_prochains_matches = QtGui.QGridLayout()
        self.list_but_prochains_match = []
        for ii, cal in enumerate(self.calendriers):
            nom = cal.nom_championnat
            but = QtGui.QPushButton("Prochain match " + nom.replace('_', ' '))
            but.clicked.connect(getattr(self, 'set_prochain_match_'+nom))
            self.list_but_prochains_match.append(but)
            self.lay_prochains_matches.addWidget(but, ii/2, ii%2)
        self.lay.addLayout(self.lay_prochains_matches)
        """
        self.prochain_match_vm_but = QtGui.QPushButton("Prochain match Vieux Monde")
        self.lay.addWidget(self.prochain_match_vm_but)
        self.prochain_match_vm_but.clicked.connect(self.set_prochain_match_vm)

        #Prochain match Nouveaux mondes
        self.prochain_match_nm_but = QtGui.QPushButton("Prochain match Nouveaux Mondes")
        self.lay.addWidget(self.prochain_match_nm_but)
        self.prochain_match_nm_but.clicked.connect(self.set_prochain_match_nm)
        """

        #Diagramme étoile
        self.diag = None
        self.faire_diagramme()

    def faire_diagramme(self):
        if not self.diag is None:
            self.lay.removeWidget(self.diag)
            sip.delete(self.diag)
        self.diag = DiagrammeCompoWidget(compo=self.parent().col_eq1.comp,
                                         compo2=self.parent().col_eq2.comp,
                                         nom_1=self.parent().col_eq1.equipe.nom,
                                         nom_2=self.parent().col_eq2.equipe.nom,
                                         fatigue=True)
        self.lay.addWidget(self.diag)

    def definir_match(self):
        nom1 = self.parent().col_eq1.equipe.nom
        nom2 = self.parent().col_eq2.equipe.nom
        comp1 = self.parent().col_eq1.comp
        comp2 = self.parent().col_eq2.comp
        if self.check_coupe_monde.isChecked():
            type_tournoi = "coupe_monde"
        elif self.rad_championat.isChecked():
            type_tournoi = "championat"
        elif self.rad_coupe.isChecked():
            type_tournoi = "coupe"
        else:
            type_tournoi = None
        journee = 1
        num = 1
        terrain_neutre = self.neutre_check.isChecked()

        self.match = Match(nom1,
                           nom2,
                           comp1,
                           comp2,
                           type_tournoi,
                           terrain_neutre,
                           journee,
                           num,
                           self.c_ou_s)
        
    def commencer(self):
        self.mb = QtGui.QMessageBox()
        st = "Avez-vous clique sur la compo voulue ?"
        sauver = self.sauv_check.isChecked()
        if sauver:
            st += "\nSauver active"
        terrain_neutre = self.neutre_check.isChecked()
        if terrain_neutre:
            st += "\nTerrain neutre active"
        phase_finale = self.finale_check.isChecked()
        if phase_finale:
            st += "\nPhase finale activee"
        if self.mb.question(None,
                         "Question",
                         st,
                         "Non",
                         "Oui") == 1:
            self.definir_match()

            cal = self.identifier_calendrier(self.match,
                                             self.championat_prochain_match)
            if cal is None and sauver and not phase_finale:
                self.dial = MyDialog(u"Le match ne correspond à aucun calendrier, il n'a pas été joué")
            else:
                #print "commencer"
                self.match.jouer(sauver=sauver,
                                 phase_finale=phase_finale)
                #self.print_res_match()
                self.R = r.ResultatWidget(self.match)
                self.R.show()

                cal.enregistrer_resultats(self.match)
                if sauver and not phase_finale:
                    cal.sauvegarder()

    def print_res_match(self):
        eq1 = self.match.eq1
        eq2 = self.match.eq2
        print ""
        print eq1.nom, eq1.score, "-", eq2.score, eq2.nom

    def retour_ecran_precedant(self):
        self.parent().hide()
        if self.c_ou_s == 'c':
            self.parent().parent().maj()
        self.parent().ecran_precedant.show()

    def set_prochain_match(self, nom_championnat):
        self.championat_prochain_match = nom_championnat
        for cal in self.calendriers:
            if cal.nom_championnat == nom_championnat:
                break
        noms_equipes = cal.prochain_match().split(' v ')
        self.parent().col_eq1.set_club(noms_equipes[0])
        self.parent().col_eq2.set_club(noms_equipes[1])

    def set_prochain_match_vieux_monde(self):
        self.set_prochain_match('vieux_monde')

    def set_prochain_match_nouveaux_mondes(self):
        self.set_prochain_match('nouveaux_mondes')

    def set_prochain_match_coupe_poule_1(self):
        self.set_prochain_match('coupe_poule_1')

    def set_prochain_match_coupe_poule_2(self):
        self.set_prochain_match('coupe_poule_2')

    def set_prochain_match_coupe_poule_3(self):
        self.set_prochain_match('coupe_poule_3')

    def set_prochain_match_coupe_poule_4(self):
        self.set_prochain_match('coupe_poule_4')

    def set_prochain_match_challenge_poule_1(self):
        self.set_prochain_match('challenge_poule_1')

    def set_prochain_match_challenge_poule_2(self):
        self.set_prochain_match('challenge_poule_2')

    def set_prochain_match_challenge_poule_3(self):
        self.set_prochain_match('challenge_poule_3')

    def set_prochain_match_challenge_poule_4(self):
        self.set_prochain_match('challenge_poule_4')

    def identifier_calendrier(self, match, nom_championnat):
        calendrier = None
        for cal in self.parent().calendriers:
            if cal.nom_championnat == nom_championnat:
                calendrier = cal
        return calendrier

class MyDialog(QtGui.QDialog):
    def __init__(self, st, parent=None):
        super(MyDialog, self).__init__(parent)
        self.st = st

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.lab = QtGui.QLabel(self.st)
        self.lay.addWidget(self.lab)

        self.but = QtGui.QPushButton("OK")
        self.but.clicked.connect(self.close)
        self.lay.addWidget(self.but)

        self.show()

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Enter):
            self.close()
            event.accept()
        else:
            super(Dialog, self).keyPressEvent(event)

