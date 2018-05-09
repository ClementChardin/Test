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
                 saison,
                 ecran_precedant=None,
                 parent=None,
                 c_ou_s='c'):
        super(MatchWidget, self).__init__(parent)
        self.ecran_precedant = ecran_precedant
        self.c_ou_s = c_ou_s
        self.saison = saison
        self.calendriers = self.saison.calendriers
        
        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
        self.col_eq1 = EquipeWidget(parent=self, c_ou_s=self.c_ou_s)
        self.lay.addWidget(self.col_eq1)

        self.col_eq2 = EquipeWidget(parent=self, c_ou_s=self.c_ou_s)
        self.lay.addWidget(self.col_eq2)

        self.col_match = ColMatchWidget(saison=self.saison,
                                        parent=self,
                                        c_ou_s=self.c_ou_s)
        self.lay.insertWidget(1, self.col_match)

        self.show()

    def update_ui(self):
        """
        Pour la classe fille MacthSelectionWidget
        """
        pass

class EquipeWidget(QtGui.QWidget):
    def __init__(self, parent=None, c_ou_s='c', saison=None):
        super(EquipeWidget, self).__init__(parent)
        self.c_ou_s = c_ou_s
        self.saison = self.parent().saison if saison is None else saison
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
                 saison,
                 parent=None,
                 c_ou_s='c'):
        super(ColMatchWidget, self).__init__(parent)
        self.c_ou_s = c_ou_s
        self.saison = saison
        self.calendriers = self.saison.calendriers
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
        self.but_prochain_match = QtGui.QPushButton("Jouer prochain match")
        self.but_prochain_match.clicked.connect(self.set_prochain_match)
        self.lay.addWidget(self.but_prochain_match)

        #Set compos prochain match
        self.but_set_compos_prochain_match = QtGui.QPushButton("Set compos")
        self.but_set_compos_prochain_match.clicked.connect(self.set_compos_prochain_match)
        self.lay.addWidget(self.but_set_compos_prochain_match)

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
        nom_compo1 = str(self.parent().col_eq1.col1.combo2.currentText())
        nom_compo2 = str(self.parent().col_eq2.col1.combo2.currentText())
        nom = self.parent().col_eq1.equipe.nom + '_' + self.parent().col_eq2.equipe.nom
        if not (nom in nom_compo1 and nom in nom_compo2):
            dial = QtGui.QDialog()
            lay = QtGui.QVBoxLayout()
            dial.setLayout(lay)
            lay.addWidget(QtGui.QLabel(u"Les compositions d'équipes ne correspondent pas !"))
            lay.addWidget(QtGui.QLabel(u"Nom détecté : "+nom))
            lay.addWidget(QtGui.QLabel(u"Nom compo 1 : "+nom_compo1))
            lay.addWidget(QtGui.QLabel(u"Nom compo 2 : "+nom_compo2))
            but = QtGui.QPushButton('OK')
            lay.addWidget(but)
            but.clicked.connect(dial.close)
            dial.exec_()
            raise ValueError()
        else:
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

                cal = self.identifier_calendrier()
                if cal is None and sauver:
                    self.dial = MyDialog(u"Le match ne correspond à aucun calendrier, il n'a pas été joué")
                    self.dial.exec_()
                else:
                    #print "commencer"
                    self.match.jouer(sauver=sauver,
                                     phase_finale=phase_finale)
                    #self.print_res_match()
                    self.R = r.ResultatWidget(self.match)
                    self.R.show()

                    ii, jj = cal.enregistrer_resultats(self.match)
                    if sauver:
                        cal.sauvegarder()
                        if jj == len(cal.scores[ii])-1:
                            if cal.nom_championnat in self.saison.dict_indice_journees.keys():
                                self.saison.dict_indice_journees[cal.nom_championnat] += 1
                            else:
                                self.saison.dict_indice_journees[cal.nom_championnat] = 1
                        self.saison.sauvegarder()

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
        pm = self.saison.prochain_match()
        noms_equipes = pm.split(' v ')
        if pm == 'repos':
            mb = QtGui.QMessageBox()
            if mb.question(None, "Question", """"Le prochain match est un jour de repos\n
                                                 Avez-vous exempté les équipes concernées ?""", "Non", "Oui") == 1:
                idx = self.saison.repos_effectues.index(False)
                self.saison.repos_effectues[idx] = True
                self.set_prochain_match(nom_championnat)
            else:
                pass
        else:
            if not self.parent().col_eq1.equipe.nom == noms_equipes[0]:
                self.parent().col_eq1.set_club(noms_equipes[0])
            if not self.parent().col_eq2.equipe.nom == noms_equipes[1]:
                self.parent().col_eq2.set_club(noms_equipes[1])

    def set_compos_prochain_match(self):
        #pm = self.saison.prochain_match()
        #noms_compos = pm.replace(' v ', '_')
        nom1 = self.parent().col_eq1.equipe.nom
        nom2 = self.parent().col_eq2.equipe.nom
        noms_compos = nom1 + '_' + nom2

        compos1 = []
        for nom in self.parent().col_eq1.equipe.compos_sauvees():
            if noms_compos in nom:
                compos1.append(nom)
        compos2 = []
        for nom in self.parent().col_eq2.equipe.compos_sauvees():
            if noms_compos in nom:
                compos2.append(nom)
        if len(compos1) > 0 and len(compos2) > 0:
            """
            Cas len différente -> message
            Cas len == 1 -> auto
            cas len égale et > 1 -> dialog
            """
            if not compos1 == compos2:
                dial = MyDialog("Il manque une compo !")
                dial.exec_()
            elif len(compos1) == 1:
                nom = compos1[0]
                self.parent().col_eq1.col1.set_comp(nom)
                self.parent().col_eq2.col1.set_comp(nom)
            else:
                ccd = ChoixCompoDialog(compos1)
                res = ccd.exec_()
                if res == 1:
                    nom = str(ccd.group.checkedButton().text())
                    self.parent().col_eq1.col1.set_comp(nom)
                    self.parent().col_eq2.col1.set_comp(nom)
                else:
                    pass
        else:
            dial = MyDialog(u"Aucune compo correspondante détectée !")
            dial.exec_()

    def identifier_calendrier(self):#, match, nom_championnat):
        cal, ii, jj = self.saison.cal_indices_prochain_match()
        nom = cal.nom_championnat
        return cal

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

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Enter):
            self.close()
            event.accept()
        else:
            super(Dialog, self).keyPressEvent(event)

class ChoixCompoDialog(QtGui.QDialog):
    def __init__(self, compos, parent=None):
        super(ChoixCompoDialog, self).__init__(parent)
        self.compos = compos

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.group = QtGui.QButtonGroup()
        for nom in self.compos:
            rad = QtGui.QRadioButton(nom)
            self.lay.addWidget(rad)
            self.group.addButton(rad)

        self.lay_but = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_but)

        self.but_no = QtGui.QPushButton('Annuler')
        self.lay_but.addWidget(self.but_no)
        self.but_no.clicked.connect(self.reject)

        self.but_yes = QtGui.QPushButton('Valider')
        self.lay_but.addWidget(self.but_yes)
        self.but_yes.clicked.connect(self.accept)
