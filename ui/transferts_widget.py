from PyQt4 import QtGui, QtCore
import sip
import pickle
import selection as s
import os.path as osp
from date import *
from savefiles import *
from changement_saison import *
from couleurs import *
from biopopup import BioPopup
from choix_joueurs import MyTableWidgetItem


class TransfertsWidget(QtGui.QWidget):
    def __init__(self, parent=None, noms_clubs=s.noms_clubs, dat=None, vague=0):
        super(TransfertsWidget, self).__init__(parent)

        self.dat = dat
        self.vague = vague

        self.noms_clubs = noms_clubs
        self.clubs = []
        self.propositions = {}
        self.recrutements = {}
        self.val_propositions = {}
        self.val_recrutements = {}
        for nom in self.noms_clubs:
            self.clubs.append(s.charger(nom, 'c'))
            self.propositions[nom] = {}
            self.recrutements[nom] = {}
            self.val_propositions[nom] = 0
            self.val_recrutements[nom] = 0
        self.club = self.clubs[0]

        if osp.isfile(TRANSFERTS_DIR_NAME(self.dat)+'/propositions' + str(self.vague) + '.prop'):
            self.propositions, self.val_propositions = self.charger_propositions_et_val()
        if self.vague > 0:
            if osp.isfile(TRANSFERTS_DIR_NAME(self.dat)+ '/recrutements' + str(self.vague - 1) + '.prop'):
                self.recrutements, self.val_recrutements = self.charger_recrutements_et_val()

        #self.liste = self.get_liste_departs(liste)

        self.recrutes = []
        for dd in self.recrutements.values():
            for nom in dd.keys():
                self.recrutes.append(nom)
        self.all_joueurs = []
        for cc in self.clubs:
            for jj in cc.get_all_joueurs():
                if jj.veut_partir and not jj.nom in self.recrutes:
                    self.all_joueurs.append(jj)
        self.selected_joueurs = self.all_joueurs
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()
        self.setup_table(tous_clubs=True)
        self.filtrer_joueurs()

    def setup_ui(self):
        """
        Choix club + infos budget
        """
        self.lay_club = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_club)

        self.combo_club = QtGui.QComboBox()
        self.combo_club.addItem('Tous')
        for nom in self.noms_clubs:
            self.combo_club.addItem(nom)
        self.combo_club.setCurrentIndex(0)
        self.combo_club.activated['QString'].connect(self.choix_club)
        self.lay_club.addWidget(self.combo_club)

        self.lab_budget = QtGui.QLabel("Budget disponnible :")
        self.lay_club.addWidget(self.lab_budget)

        self.lab_val_budget = QtGui.QLabel(str(self.club.budget))
        self.lay_club.addWidget(self.lab_val_budget)

        self.lab_previsions = QtGui.QLabel(u'Prévisions')
        self.lay_club.addWidget(self.lab_previsions)

        self.lab_val_previsions = QtGui.QLabel(str(self.previsions_club()))
        self.lay_club.addWidget(self.lab_val_previsions)

        self.lab_temps_reel = QtGui.QLabel(u"Temps réel")
        self.lay_club.addWidget(self.lab_temps_reel)

        tps_reel = self.club.budget - self.valeurs_propositions_club()
        self.lab_val_temps_reel = QtGui.QLabel(str(tps_reel))
        self.lay_club.addWidget(self.lab_val_temps_reel)

        self.lab_avertissement = QtGui.QLabel("Avertissement")
        self.lay_club.addWidget(self.lab_avertissement)

        self.lab_val_avertissement = QtGui.QLabel(str(self.club.avertissement))
        self.lay_club.addWidget(self.lab_val_avertissement)

        """
        Options de tri des joueurs + sauver propositions + Faire propositions
        """
        self.lay_option = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_option)

        self.label = QtGui.QLabel(u"Filtrer par évalutation")
        self.lay_option.addWidget(self.label)

        self.combo_EV = QtGui.QComboBox()
        self.combo_EV.addItem('Tous')
        for ii in range(8, 13):
            self.combo_EV.addItem(str(ii))
        self.combo_EV.setCurrentIndex(0)
        self.combo_EV.activated['QString'].connect(self.filtrer_joueurs)
        self.lay_option.addWidget(self.combo_EV)

        self.rad_egal = QtGui.QRadioButton("Egale")
        self.rad_egal.clicked.connect(self.filtrer_joueurs)
        self.lay_option.addWidget(self.rad_egal)

        self.rad_superieur = QtGui.QRadioButton(u"Supérieure")
        self.rad_superieur.setChecked(True)
        self.rad_superieur.clicked.connect(self.filtrer_joueurs)
        self.lay_option.addWidget(self.rad_superieur)

        self.combo_poste = QtGui.QComboBox()
        self.combo_poste.addItem('Tous')
        for poste in s.postes:
            self.combo_poste.addItem(poste)
        self.combo_poste.setCurrentIndex(0)
        self.combo_poste.activated['QString'].connect(self.filtrer_joueurs)
        self.lay_option.addWidget(self.combo_poste)

        self.but_sauver = QtGui.QPushButton("Sauvegarder propositions")
        self.but_sauver.clicked.connect(self.sauvegarder_propositions)
        self.lay_option.addWidget(self.but_sauver)

        self.but_choisir = QtGui.QPushButton("Choisir propositions")
        self.but_choisir.clicked.connect(self.choisir_propositions)
        self.lay_option.addWidget(self.but_choisir)

    def setup_table(self, tous_clubs=False):
        self.labs = ['nom', 'Club', u'MS problème', 'EV', 'Poste 1', 'Poste 2',
                     'Poste 3']
        numlin = len(self.selected_joueurs)
        numcol = len(self.labs) + len(self.clubs) if tous_clubs \
                 else len(self.labs) + 1
        self.table = QtGui.QTableWidget(numlin, numcol)
        print "set_table ; tous_clubs =", tous_clubs, "; numlin =", numlin, "; numcol =", numcol
        if tous_clubs:
            for kk, nom in enumerate(self.noms_clubs):
                if not nom in self.labs:
                    self.labs.append(nom)
        else:
            self.labs.append(self.club.nom)
        self.table.setHorizontalHeaderLabels(self.labs)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        for ii, jj in enumerate(self.selected_joueurs):
            it = QtGui.QTableWidgetItem(jj.nom)
            self.table.setItem(ii, 0, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(jj.club)
            self.table.setItem(ii, 1, MyTableWidgetItem(it))

            it = QtGui.QTableWidgetItem(str(jj.MS_probleme))
            self.table.setItem(ii, 2, MyTableWidgetItem(it))
            
            filtre_poste = str(self.combo_poste.currentText())
            st_ev = '%0.2f' % jj.EV if filtre_poste == 'Tous' \
                    else '%0.2f' % s.calc_EV(jj, filtre_poste,
                                           fatigue=False)
            it = QtGui.QTableWidgetItem(st_ev)
            self.table.setItem(ii, 3, MyTableWidgetItem(it))
            
            it = QtGui.QTableWidgetItem(jj.postes[1])
            self.table.setItem(ii, 4, MyTableWidgetItem(it))
            
            it = QtGui.QTableWidgetItem(jj.postes[2])
            self.table.setItem(ii, 5, MyTableWidgetItem(it))
            
            it = QtGui.QTableWidgetItem(jj.postes[3])
            self.table.setItem(ii, 6, MyTableWidgetItem(it))

            if tous_clubs:
                for kk, nom in enumerate(self.noms_clubs):
                    if jj.nom in self.propositions[nom].keys():
                        tu = self.propositions[nom][jj.nom]
                        self.ajouter_proposition_table(tu, ii, kk+7)
            else:
                if jj.nom in self.propositions[self.club.nom].keys():
                    tu = self.propositions[self.club.nom][jj.nom]
                    self.ajouter_proposition_table(tu, ii)

        self.lay.addWidget(self.table)

        """
        Connection
        """
        self.table.doubleClicked.connect(self.faire_proposition)

        """
        Empecher d'editer les cases
        """
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        """
        Possibilite de trier
        Trier par poste 1 -> le 0 est la pour mettre dans le bon ordre
        """
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(4, 0)

        """
        Colorer table
        """
        self.colorer_table()

    def ajouter_proposition_table(self, tu, num_ligne, num_col=7):
        st = str(tu[0]) + ' ; ' + str(tu[1]) + ' ; ' + tu[2][0] + ' (' \
             + str(tu[2][1]) + ')'
        it = QtGui.QTableWidgetItem(st)
        self.table.setItem(num_ligne, num_col, MyTableWidgetItem(it))

    def colorer_table(self):
        dd = dict()
        for ii, jj in enumerate(self.selected_joueurs):
            if not jj.blessure == 0:
                couleur = indian_red
            else:
                couleur = noir
                if jj.est_jeune():
                    couleur = vert
                elif jj.D <= s.date:
                    couleur = rouge
                elif jj.D == s.date + 1:
                    couleur = bleu

            dd[jj.nom] = couleur

        numcol = self.table.columnCount()
        for rr in range(self.table.rowCount()):
            nom = str(self.table.item(rr, 0).text())
            for cc in range(numcol):
                if not self.table.item(rr, cc) is None:
                    self.table.item(rr, cc).setTextColor(dd[nom])

    def choix_club(self, nom):
        nom = str(self.combo_club.currentText())
        if nom == 'Tous':
            self.lab_val_budget.setText('0')
            self.lab_val_temps_reel.setText('0')
            self.lab_val_previsions.setText('0')
        else:
            cc = self.clubs[self.noms_clubs.index(nom)]
            self.club = cc
            self.lab_val_budget.setText(str(cc.budget))
            if cc.budget < 0:
                self.lab_val_budget.setStyleSheet('color: red')
            else:
                self.lab_val_budget.setStyleSheet('color: black')

            tps_reel = self.club.budget - self.valeurs_propositions_club()
            self.lab_val_temps_reel.setText(str(tps_reel))
            if tps_reel < 0:
                self.lab_val_temps_reel.setStyleSheet('color: red')
            else:
                self.lab_val_temps_reel.setStyleSheet('color: black')

            self.lab_val_previsions.setText(str(self.previsions_club()))

        self.maj()

    def filtrer_joueurs(self):
        filtre_poste = str(self.combo_poste.currentText())
        filtre_EV = str(self.combo_EV.currentText())
        egal = self.rad_egal.isChecked()

        ll = self.all_joueurs
        self.selected_joueurs = []
        for jj in ll:
            if filtre_poste == 'Tous' or filtre_poste in jj.postes \
               or (filtre_poste in ('C1', 'C2') and ('C1' in jj.postes or \
                                                     'C2' in jj.postes or \
                                                     'CE' in jj.postes)):
                poste = jj.postes[1] if filtre_poste == 'Tous' else filtre_poste
                if filtre_EV == 'Tous':
                    self.selected_joueurs.append(jj)
                else:
                    filtre_EV = int(filtre_EV)
                    if egal:
                        if int(s.calc_EV(jj, poste, fatigue=False)) == filtre_EV:
                            self.selected_joueurs.append(jj)
                    else:
                        if s.calc_EV(jj, poste, fatigue=False) >= filtre_EV:
                            self.selected_joueurs.append(jj)

        self.maj()

    def maj(self):
        self.lay.removeWidget(self.table)
        sip.delete(self.table)
        tous_clubs = (str(self.combo_club.currentText()) == 'Tous')
        self.setup_table(tous_clubs)

    def faire_proposition(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            nom_club = str(self.table.item(rr, 1).text()).split(" - ")[0]
            cc = self.clubs[self.noms_clubs.index(nom_club)]
            jj = cc.get_joueur_from_nom(nom)
            joueurs.append(jj)

        for ii, jj in enumerate(joueurs):
            nom_club = str(self.combo_club.currentText())
            cc = self.clubs[self.noms_clubs.index(nom_club)]
            dial = PropositionDialog(jj, parent=self, nom_club=cc.nom,
                                     besoins=cc.besoins)
            dial.exec_()
            if dial.ok:
                tu = dial.proposition
                print self.club.nom, jj.nom, tu
                self.ajouter_proposition_table(tu, rows[ii])

                self.propositions[self.club.nom][jj.nom] = tu
                self.val_propositions[self.club.nom] += tu[0]

                tps_reel = self.club.budget - self.valeurs_propositions_club()
                self.lab_val_temps_reel.setText(str(tps_reel))
                if int(self.lab_val_temps_reel.text()) < 0:
                    self.lab_val_temps_reel.setStyleSheet('color: red')

    def previsions_club(self):
        res = 0
        for jj in self.all_joueurs:
            if jj.club == self.club.nom:
                res += jj.VAL
        return res

    def valeurs_propositions_club(self):
        res = 0
        dd = self.propositions[self.club.nom]
        for besoin in self.club.besoins:
            vals = []
            for tu in dd.values():
                if tu[2] == besoin:
                    vals.append(tu[0])
            if len(vals) > 0:
                res += max(vals)
        return res

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        diagAction = QtGui.QAction('Diagramme etoile', self)
        diagAction.triggered.connect(self.diagramme_etoile)
        self.menu.addAction(diagAction)

        propAction = QtGui.QAction('Faire proposition', self)
        propAction.triggered.connect(self.faire_proposition)
        self.menu.addAction(propAction)

        self.menu.popup(QtGui.QCursor.pos())

    def afficher_bio(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            nom_club = str(self.table.item(rr, 1).text()).split(" - ")[0]
            cc = self.clubs[self.noms_clubs.index(nom_club)]
            jj = cc.get_joueur_from_nom(nom)
            joueurs.append(jj)

        self.pop = BioPopup(joueurs=joueurs, col3=self, fatigue=False, dat=self.dat)
        self.pop.show()
        
    def diagramme_etoile(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)

        TA = False
        TB = []
        TO = []
        AV = False
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            nom_club = str(self.table.item(rr, 1).text()).split(" - ")[0]
            cc = self.clubs[self.noms_clubs.index(nom_club)]
            joueur = cc.get_joueur_from_nom(nom)
            joueurs.append(joueur)
            TO.append(joueur.caracs_sans_fatigue['TO'])
            TB.append(joueur.caracs_sans_fatigue['TB'])
            TA = TA or 'TA' in joueur.postes
            AV = AV or s.est_un_avant(joueur)
        label_TO = True if max(TO) >= 8 and AV \
                   else False
        label_TA = True if TA \
                   else False
        label_TB = True if max(TB) >= 8 \
                   else False
        
        for nn, jj in enumerate(joueurs):
            texte = True if nn == 0 else False
            jj.diagramme_etoile(texte=texte,
                                label_TO=label_TO,
                                label_TA=label_TA,
                                label_TB=label_TB)

    def sauvegarder_propositions(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/propositions' + str(self.vague) + '.prop', 'w') as ff:
            pickle.dump(self.propositions, ff)
        print u"Propositions sauvegardées"
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/val_propositions' + str(self.vague) + '.prop', 'w') as ff:
            pickle.dump(self.val_propositions, ff)
        print u"Valeurs propositions sauvegardées"

    def charger_recrutements_et_val(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/recrutements' + str(self.vague - 1) + '.prop', 'r') as ff:
            recrutements = pickle.load(ff)
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/val_recrutements' + str(self.vague - 1) + '.prop', 'r') as ff:
            val = pickle.load(ff)
        return recrutements, val

    def charger_propositions_et_val(self):
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/propositions' + str(self.vague) + '.prop', 'r') as ff:
            prop = pickle.load(ff)
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/val_propositions' + str(self.vague) + '.prop', 'r') as ff:
            val = pickle.load(ff)
        return prop, val

    def choisir_propositions(self):
        mb = QtGui.QMessageBox()
        if mb.question(None,
                       "Question",
                       u"Avez-vous bien effectué toutes les propostitions ?"
                       , "Non", "Oui") == 1:
            self.choix = {}
            for jj in self.all_joueurs:
                offres = []
                for nom, dd in self.propositions.items():
                    if jj.nom in dd.keys():
                        tu = dd[jj.nom]
                        offres.append((self.clubs[self.noms_clubs.index(nom)],
                                       tu[0],
                                       tu[1],
                                       tu[2][0]))
                if offres == []:
                    pass
                else:
                    ch = choisir_offre(jj, offres)
                    self.choix[jj.nom] = ch
                    print jj.nom, ch[0].nom, ch[1], ch[2], ch[3]
        with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/choix' + str(self.vague) + '.prop', 'w') as ff:
            pickle.dump(self.choix, ff)
        print u"Choix sauvegardés"

class PropositionDialog(QtGui.QDialog):
    def __init__(self, joueur, parent=None, nom_club="", besoins=[]):
        super(PropositionDialog, self).__init__(parent)
        self.joueur = joueur
        self.nom_club = nom_club
        self.besoins = besoins
        self.ok = False
        
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle("Proposition de "+self.nom_club)

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

    def setup_ui(self):
        """
        Priorité et besoin
        """
        self.rad_normal = QtGui.QRadioButton(u"Priorité normale")
        self.rad_normal.setChecked(True)
        self.lay.addWidget(self.rad_normal)

        self.rad_eleve = QtGui.QRadioButton(u"Priorité élevée")
        self.lay.addWidget(self.rad_eleve)

        self.rad_tres_eleve = QtGui.QRadioButton(u"Priorité très élevée")
        self.lay.addWidget(self.rad_tres_eleve)

        self.combo_besoin = QtGui.QComboBox()
        for tu in self.besoins:
            st = tu[0] + ' : ' + str(tu[1])
            self.combo_besoin.addItem(st)
        self.lay.addWidget(self.combo_besoin)

        """
        Bouttons pour valider ou annuler
        """
        self.lay_but = QtGui.QHBoxLayout()
        self.but_annuler = QtGui.QPushButton("Annuler")
        self.but_annuler.clicked.connect(self.annuler)
        self.lay_but.addWidget(self.but_annuler)

        self.but_ok = QtGui.QPushButton("OK")
        self.but_ok.clicked.connect(self.valider)
        self.lay_but.addWidget(self.but_ok)

        self.lay.addLayout(self.lay_but)

    def annuler(self):
        self.close()

    def valider(self):
        if self.rad_normal.isChecked():
            priorite = 2
        elif self.rad_eleve.isChecked():
            priorite = 3
        elif self.rad_tres_eleve.isChecked():
            priorite = 4
        tu = (str(self.combo_besoin.currentText()).split(' : ')[0],
              float(str(self.combo_besoin.currentText()).split(' : ')[1]))
        poste = self.joueur.postes[1] if tu[0] == 'tous' else tu[0]

        val, ms = faire_offre(self.joueur, priorite, poste)
        self.proposition = (val, ms, tu)
        self.ok = True
        self.accept()
        
