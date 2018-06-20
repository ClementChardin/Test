# -*- coding: cp1252 -*-
from PyQt4 import QtGui, QtCore
from numpy.random import shuffle
from transferts_widget import MyTableWidgetItem
from plot_evolution_widget import PlotEvolutionWidget
from match import MyDialog
from couleurs import *
import selection as s
import biopopup as b
import os.path as osp
import pickle

class RecrutementsWidgetNew(QtGui.QWidget):
    def __init__(self,
                 parent=None,
                 dat=None,
                 clubs=[],
                 all_joueurs=[],
                 classements=None,
                 classements_depart=None):
        """
        classements est un dict qui contient en keys les noms des joueurs et
        en values le classement des propositions qui ont été faites au joueur

        Ces classements sont sous la forme de list
        Chaque item de la liste est un tuple
        (nom_club, val, ms, besoin, tps_laisse)
        """
        super(RecrutementsWidgetNew, self).__init__(parent)
        self.dat = s.lire_date() if dat is None else dat
        self.clubs = clubs
        self.all_joueurs = all_joueurs

        if not classements is None:
            self.classements = classements
            self.classements_depart = classements_depart
            print u'Classements et classements départ initiés avec la valeur fournie'
        else:
            self.charger_classements()

        self.charger_ordre_clubs()

        self.dd_joueurs_recrutes = {}
        self.dd_valides_definitivement = {}
        self.dd_temps_passe = {}
        self.dd_besoins_recrutes = {}
        self.dd_tours_passes = {}
        self.dd_ventes = {}
        self.dd_joueurs_interesses_precedant = {}
        """
        dd_valides_definitivement[nom_club] = bool
        dd_temps_passe[nom_club][nom_joueur] = temps passé par le joueur sur une offre (int)
        dd_joueurs_recrutes[nom_club] = (nom_joueur, offre acceptée)
        dd_besoins_recrutes[nom_club] = (nom_joueur, tuple_besoin)
        dd_tours_passes[nom_club] = nb de tours passés pour ce club (int)
        dd_ventes[nom_club] = revenus de la vente des joueurs recrutés par les autres clubs (in)
        dd_joueurs_interesses_precedant[nom_club] = [joueurs intéressés au tour précédant]
        """
        for nom in self.noms_clubs:
            self.dd_valides_definitivement[nom] = False
            self.dd_temps_passe[nom] = {}
            self.dd_joueurs_recrutes[nom] = []
            self.dd_besoins_recrutes[nom] = []
            self.dd_tours_passes[nom] = 0
            self.dd_ventes[nom] = 0
            self.dd_joueurs_interesses_precedant[nom] = []

        for nom_joueur, classement in self.classements.items():
            nom_club = classement[0][0]
            self.dd_temps_passe[nom_club][nom_joueur] = 0

        #Charger dd_joueurs_recrutes si il a été sauvegardé auparavant
        self.charger_recrutements()
        joueurs_recrutes = []
        for ll in self.dd_joueurs_recrutes.values():
            joueurs_recrutes += ll
        for nom_joueur, offre in joueurs_recrutes:
            jj = self.get_joueur_from_nom(nom_joueur)
            self.dd_ventes[jj.club] += offre[1]

        ll_tours_passes = [self.dd_tours_passes[nom] for nom in self.noms_clubs]
        self.idx_club = min([ll_tours_passes.index(min(ll_tours_passes))])
        self.club = self.clubs[self.idx_club]
        self.joueurs = self.get_joueurs_interesses(self.club.nom)
        self.joueur_recrute_temp = None
        self.besoin_temp = None
        self.refuses = []

        self.setup_ui()

    def setup_ui(self):
        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        """
        Nom club, budget, prévision et avertissement
        """
        self.lay_club = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_club)

        self.lab_nom = QtGui.QLabel(self.club.nom)
        self.lay_club.addWidget(self.lab_nom)

        bud = self.budget_temps_reel(self.club.nom)
        self.lab_budget = QtGui.QLabel("Budget : "+str(bud))
        couleur = rouge if self.club.budget < 0 else noir
        colorer_qlabel(self.lab_budget, couleur)
        self.lay_club.addWidget(self.lab_budget)

        self.lab_prevision = QtGui.QLabel(u"Prévisions : "+str(self.prevision()))
        self.lay_club.addWidget(self.lab_prevision)

        self.lab_avertissement = QtGui.QLabel("Avertissement : "+\
                                              str(self.club.avertissement))
        couleur = rouge if self.club.avertissement > 1 else noir
        colorer_qlabel(self.lab_avertissement, couleur)
        self.lay_club.addWidget(self.lab_avertissement)

        """
        Nombre de joueurs par poste
        """
        self.lay_nb_joueurs = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_nb_joueurs)

        for poste in sorted(s.limite_poste.keys(), key=lambda pp: s.ordre_postes[pp]):
            if not poste == 'N8':
                st, couleur = self.st_lab_nb_joueurs(poste)
                lab = QtGui.QLabel(st)
                colorer_qlabel(lab, couleur)
                self.lay_nb_joueurs.addWidget(lab)
                setattr(self, 'lab_' + poste, lab)

        """
        Besoins
        """
        self.set_table_besoins()

        #self.lay.addStretch()

        """
        Table des joueurs intéressés
        """
        self.setup_table()
        self.colorer_table()

        """
        Bouttons club suivant et valider définitivement
        """
        self.lay_but = QtGui.QHBoxLayout()
        self.lay.addLayout(self.lay_but)

        self.but_club_suivant = QtGui.QPushButton("Club suivant")
        self.but_club_suivant.clicked.connect(self.club_suivant)
        self.lay_but.addWidget(self.but_club_suivant)

        self.but_valider_definitivement = QtGui.QPushButton(u"Valider définitivement")
        self.but_valider_definitivement.clicked.connect(self.valider_definitivement)
        self.lay_but.addWidget(self.but_valider_definitivement)

        self.but_sauvegarder_recrutements = QtGui.QPushButton("Sauvegarder transferts")
        self.but_sauvegarder_recrutements.clicked.connect(self.sauvegarder_recrutements)
        self.lay_but.addWidget(self.but_sauvegarder_recrutements)

        self.but_faire_transferts = QtGui.QPushButton("Faire transferts")
        self.but_faire_transferts.clicked.connect(self.faire_transferts)
        self.lay_but.addWidget(self.but_faire_transferts)

    def setup_table(self):
        self.hlabels = ['Nom', 'EV', 'Poste 1', 'Poste 2', 'Poste 3', 'club',
                        u'Création', u'Déclin', 'Besoin', 'VAL', 'MS',
                        'Temps restant', 'Nb propositions']
        self.table = QtGui.QTableWidget(len(self.joueurs),
                                        len(self.hlabels))
        #self.lay.addWidget(self.table)
        self.lay.insertWidget(3, self.table)
        self.table.setHorizontalHeaderLabels(self.hlabels)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        for ii, jj in enumerate(self.joueurs):
            st_ev = '%0.2f' % jj.EV
            kk = 0
            
            lab = QtGui.QTableWidgetItem(jj.nom)
            self.table.setItem(ii, kk, lab)
            kk += 1
            
            lab = QtGui.QTableWidgetItem(st_ev)
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.postes[1])
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.postes[2])
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.postes[3])
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(jj.club)
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(jj.C))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(jj.D))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1

            offre = self.classements[jj.nom][0]
            nom_club, val, ms, besoin, tps_laisse = offre
            
            lab = QtGui.QTableWidgetItem(str(besoin))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1

            lab = QtGui.QTableWidgetItem(str(val))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(ms))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(tps_laisse - \
                                             self.dd_temps_passe[nom_club][jj.nom]))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1
            
            lab = QtGui.QTableWidgetItem(str(len(self.classements[jj.nom])))
            self.table.setItem(ii, kk, MyTableWidgetItem(lab))
            kk += 1

        """
        Connections
        """
        self.table.doubleClicked.connect(self.recruter)

        """
        Empecher d'editer les cases
        """
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        """
        Possibilite de trier
        Trier par poste 1 -> le 0 est la pour mettre dans le bon ordre
        """
        self.table.setSortingEnabled(True)
        self.table.sortByColumn(2, 0)

        """
        Cacher les verticalHeaders
        """
        #self.table.verticalHeader().setVisible(False)

        """
        Resize
        """
        #self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        """
        geometry_besoins = self.table_besoins.geometry()
        geometry = self.table.geometry()
        rect_besoins = geometry_besoins.getRect()
        rect = geometry.getRect()
        self.table.setGeometry(rect_besoins[0]+50, rect[1], rect[2], rect[0])
        #self.table.verticalHeader()setStretchLastSection(True)

        p = QtGui.QSizePolicy()
        #p.setHorizontalPolicy(QtGui.QSizePolicy.Maximum)
        p.setVerticalPolicy(QtGui.QSizePolicy.Maximum)
        p.setHorizontalStretch(3)
        self.table.setSizePolicy(p)
        """

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        compAction = QtGui.QAction(u'Recruter', self)
        compAction.triggered.connect(self.recruter)
        self.menu.addAction(compAction)

        diagAction = QtGui.QAction('Diagramme etoile', self)
        diagAction.triggered.connect(self.diagramme_etoile)
        self.menu.addAction(diagAction)

        plotevAction = QtGui.QAction(u'Plot évoltution', self)
        plotevAction.triggered.connect(self.plot_evolution)
        self.menu.addAction(plotevAction)

        classementAction = QtGui.QAction(u'Voir classement', self)
        classementAction.triggered.connect(self.voir_classement)
        self.menu.addAction(classementAction)

        refuserAction = QtGui.QAction(u'Refuser', self)
        refuserAction.triggered.connect(self.refuser)
        self.menu.addAction(refuserAction)

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
            jj = self.get_joueur_from_nom(nom)
            joueurs.append(jj)
        
        self.pop = b.BioPopup(joueurs=joueurs, col3=self, fatigue=False)
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
            joueur = self.get_joueur_from_nom(nom)
            joueurs.append(joueur)
            TO.append(joueur.caracs_sans_fatigue['TO'])
            TB.append(joueur.caracs_sans_fatigue['TB'])
            TA = TA or 'TA' in joueur.postes
            AV = AV or est_un_avant(joueur)
        label_TO = True if max(TO) >= 8 and AV \
                   else False
        label_TA = True if TA \
                   else False
        label_TB = True if max(TB) >= 8 \
                   else False
        self.djw = DiagrammeJoueursWidget(joueurs,
                                     label_TO=label_TO,
                                     label_TA=label_TA,
                                     label_TB=label_TB)

    def plot_evolution(self):
        rows = []
        joueurs = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.get_joueur_from_nom(nom)
            joueurs.append(jj)
        self.pew = PlotEvolutionWidget(joueurs)

    def refuser(self):
        rows = []
        joueurs = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.get_joueur_from_nom(nom)
            if jj in self.refuses:
                self.refuses.remove(jj)
            else:
                self.refuses.append(jj)
        self.colorer_table()

    def club_suivant(self):
        if not self.joueur_recrute_temp is None:
            self.dd_joueurs_recrutes[self.club.nom].append((self.joueur_recrute_temp.nom,
                                                            self.classements[self.joueur_recrute_temp.nom][0]))
            self.dd_besoins_recrutes[self.club.nom].append((self.joueur_recrute_temp.nom,
                                                            self.besoin_temp))
            if not self.joueur_recrute_temp.club == self.club.nom:
                self.dd_ventes[self.joueur_recrute_temp.club] += self.classements[self.joueur_recrute_temp.nom][0][1]

        for jj in self.get_joueurs_interesses(self.club.nom):
            self.dd_temps_passe[self.club.nom][jj.nom] += 1

        for jj in self.refuses:
            self.passer_offre(jj.nom)

        self.dd_joueurs_interesses_precedant[self.club.nom] = self.get_joueurs_interesses(self.club.nom)

        self.idx_club += 1
        self.dd_tours_passes[self.club.nom] += 1

        if self.idx_club % len(self.clubs) == 0:
            for jj in self.all_joueurs:
                nom_club, val, ms, besoin, tps_laisse = self.classements[jj.nom][0]
                if not jj in self.get_joueurs_recrutes(nom_club):
                    if tps_laisse - self.dd_temps_passe[nom_club][jj.nom] < 1:
                        self.passer_offre(jj.nom)

        self.club = self.clubs[self.idx_club%len(self.clubs)]
        self.joueurs = self.get_joueurs_interesses(self.club.nom)
        self.joueur_recrute_temp = None
        self.besoin_temp = None
        self.refuses = []
        self.maj_labs_club()
        self.maj_table_besoins()
        self.maj_st_nb_joueurs()

        self.maj_table()

    def maj_table(self):
        self.lay.removeWidget(self.table)
        self.setup_table()
        self.colorer_table()

    def get_joueur_from_nom(self, nom):
        for jj in self.all_joueurs:
            if jj.nom == nom:
                break
        return jj

    def recruter(self):
        rows = []
        joueurs = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        if len(rows) > 1:
            raise ValueError(u"Trop de joueurs sélectionnés")
        rr = rows[0]
        nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
        jj = self.get_joueur_from_nom(nom)

        if jj in self.get_joueurs_recrutes(self.club.nom):
            dial = MyDialog(u"Joueur déjà recruté")
            dial.exec_()

        else:
            offre = self.classements[jj.nom][0]
            boo = self.recrutement_possible(offre, jj)

            if boo:
                ll = []
                for bes in self.club.besoins:
                    poste = bes[0]
                    if poste in jj.postes or (poste in ('C1', 'C2', 'CE') and \
                                              jj.joue_centre()):
                                              #('C1' in jj.postes or 'C2' in jj.postes \
                                               #or 'CE' in jj.postes
                        ll.append(bes)
                print '\nListe des besoins possibles', ll
                if len(ll) == 0:
                    dial = MyDialog(u"Aucun besoin ne correspond aux postes de ce joueur")
                    dial.exec_()
                elif len(ll) == 1:
                    besoin = ll[0]
                    dial = MyDialog(u"Recruté automatiquement en tant que "+self.get_st_besoin(besoin))
                    dial.exec_()
                else:
                    self.cbd = ChoixBesoinDialog(ll, jj, parent=self)
                    res = self.cbd.exec_()
                    if res == 1:
                        besoin = self.st_besoin_to_besoin(self.cbd.group.checkedButton().text())
                    else:
                        besoin = None
                print besoin
                self.joueur_recrute_temp = jj
                self.besoin_temp = besoin
                self.colorer_table()
                val = self.classements[jj.nom][0][1]
                self.maj_labs_club()
            else:
                dial = MyDialog(u"Recrutement impossible")
                dial.exec_()

    def get_bool_avertissement(self, val):
        """
        True si le recrutement est permis
        """
        bool_avertissement = True
        avertissement = self.club.avertissement
        bud = self.budget_temps_reel(self.club.nom)
        if avertissement >= 2:
            if bud - val < 0:
                bool_avertissement = False
            else:
                bool_avertissement = True
        elif avertissement == 1:
            if bud + self.prevision() - val < 0:
                bool_avertissement = False
            else:
                bool_avertissement = True
        else:
            bool_avertissement = True
        return bool_avertissement

    def recrutement_possible(self, offre, joueur):
        nom_club, val, ms, besoin, tps_laisse = offre

        valide_definitivement = self.dd_valides_definitivement[self.club.nom]

        bool_avertissement = self.get_bool_avertissement(val) or \
                             joueur.club == self.club.nom

        meme_club = joueur.club == self.club.nom and not joueur.MS_probleme

        print 'valide_definitivement', valide_definitivement
        print 'bool_avertissement', bool_avertissement

        return (not valide_definitivement) and bool_avertissement \
               and (not meme_club)

    def prevision(self):
        nom_club = self.club.nom
        p = 0
        for jj in self.all_joueurs:
            if jj.club == nom_club and \
               not jj in self.get_joueurs_recrutes(nom_club):
                p += jj.VAL
        return p

    def colorer_table(self):
        dd = {}
        for jj in self.joueurs:
            couleur = blanc

            if jj in self.get_joueurs_recrutes(self.club.nom):
                couleur = bleu_clair
            elif jj in self.refuses:
                couleur = rouge
            elif not jj.nom in [jjj.nom for jjj in self.get_joueurs_interesses_precedant(self.club.nom)]:
                couleur = orange

            if jj.retraite:
                couleur = gris

            if not self.joueur_recrute_temp is None:
                if jj.nom == self.joueur_recrute_temp.nom:
                    couleur = vert

            dd[jj.nom] = couleur

        for rr in range(self.table.rowCount()):
            for cc in range(self.table.columnCount()):
                nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
                self.table.item(rr, cc).setBackgroundColor(dd[nom])

    def valider_definitivement(self):
        pass

    def maj_labs_club(self):
        self.lab_nom.setText(self.club.nom)
        bud = self.budget_temps_reel(self.club.nom)
        if not self.joueur_recrute_temp is None:
            if not self.joueur_recrute_temp.club == self.club.nom:
                bud -= self.classements[self.joueur_recrute_temp.nom][0][1]
        self.lab_budget.setText("Budget : "+str(bud))
        couleur = rouge if bud < 0 else noir
        colorer_qlabel(self.lab_budget, couleur)
        self.lab_avertissement.setText("Avertissement : "+\
                                       str(self.club.avertissement))
        couleur = rouge if self.club.avertissement > 1 else noir
        colorer_qlabel(self.lab_avertissement, couleur)
        self.lab_prevision.setText(u"Prévisions : "+str(self.prevision()))

    def budget_temps_reel(self, nom_club):
        club = self.clubs[self.noms_clubs.index(nom_club)]
        bud = club.budget + self.dd_ventes[club.nom]*.75
        for jj, offre in self.dd_joueurs_recrutes[club.nom]:
            bud -= offre[1]
        return int(bud)

    def set_table_besoins(self):
        self.hlabels_besoins = [bes for bes in self.club.besoins]
        for bes in self.hlabels_besoins:
            while self.hlabels_besoins.count(bes) > 1:
                self.hlabels_besoins.remove(bes)
        self.hlabels_besoins.sort(key=lambda tu: s.ordre_postes[tu[0]])                
        self.table_besoins = QtGui.QTableWidget(1, len(self.hlabels_besoins))
        self.table_besoins.setHorizontalHeaderLabels([self.get_st_besoin(hlab) for hlab in self.hlabels_besoins])
        for kk in range(len(self.hlabels_besoins)):
            val = 0
            N = self.club.besoins.count(self.hlabels_besoins[kk])
            for nom, besoin in self.dd_besoins_recrutes[self.club.nom]:
                #nom = jj.nom
                #offre = self.get_offre(self.club.nom, nom)
                if besoin == self.hlabels_besoins[kk]:
                    val += 1
            lab = QtGui.QTableWidgetItem(str(val))
            it = MyTableWidgetItem(lab)
            if val > N:
                couleur = orange
            elif val == N:
                couleur = vert
            elif val > 0:
                couleur = bleu_clair
            else:
                couleur = blanc
            it.setBackgroundColor(couleur)
            self.table_besoins.setItem(0, kk, it)

        p = QtGui.QSizePolicy()
        #p.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
        p.setHorizontalPolicy(QtGui.QSizePolicy.Minimum)
        #p.setHorizontalStretch(10)
        self.table_besoins.setSizePolicy(p)

        self.lay.insertWidget(2, self.table_besoins)

        """
        geometry = self.table_besoins.geometry()
        rect = geometry.getRect()
        self.table_besoins.setGeometry(rect[0], rect[1], rect[2], rect[0]+34)
        self.table_besoins.verticalHeader().setStretchLastSection(True)
        """

    def maj_table_besoins(self):
        self.lay.removeWidget(self.table_besoins)
        self.set_table_besoins()

    def maj_st_nb_joueurs(self):
        for poste in sorted(s.limite_poste.keys(), key=lambda pp: s.ordre_postes[pp]):
            if not poste == 'N8':
                st, couleur = self.st_lab_nb_joueurs(poste)
                lab = getattr(self, 'lab_' + poste)
                lab.setText(st)
                colorer_qlabel(lab, couleur)

    def st_lab_nb_joueurs(self, poste):
        st = poste
        nb = len(self.club.joueurs[poste])
        if poste == 'TL':
            st = 'TL / N8'
            nb += len(self.club.joueurs['N8'])
        st += ' : ' + str(nb) + ' / ' + str(s.limite_poste[poste])
        couleur = rouge if nb > s.limite_poste[poste] else noir
        return st, couleur

    def get_joueurs_interesses(self, nom_club, classements_depart=False):
        ll = []
        noms_recrutes = [jj.nom for jj in self.get_joueurs_recrutes(nom_club)]
        for jj in self.all_joueurs:
            classement = self.classements_depart[jj.nom] if classements_depart else self.classements[jj.nom]
            offre_preferee = classement[0]
            if offre_preferee[0] == nom_club:# and not jj.nom in noms_recrutes:
                ll.append(jj)
        return ll

    def get_joueurs_interesses_precedant(self, nom_club):
        if self.dd_joueurs_interesses_precedant[nom_club] == []:
            return self.get_joueurs_interesses(nom_club, True)
        else:
            return self.dd_joueurs_interesses_precedant[nom_club]

    def get_joueurs_recrutes(self, nom_club):
        ll = []
        for nom, offre in self.dd_joueurs_recrutes[nom_club]:
            jj = self.get_joueur_from_nom(nom)
            #classement = self.classements[nom]
            #offre_preferee = classement[0]
            #if offre_preferee[0] == nom_club:
            ll.append(jj)
        return ll

    def get_offre(self, nom_club, nom_joueur):
        found = False
        for offre in self.classements[nom_joueur]:
            if offre[0] == nom_club:
                found = True
                break
        if found:
            return offre
        else:
            raise ValueError("Offre de "+nom_club+" pour "+nom_joueur+u" non trouvée")

    def get_st_besoin(self, besoin):
        poste, ev = besoin
        return poste + ' : ' + str(ev)

    def st_besoin_to_besoin(self, st):
        poste, ev = st.split(' : ')
        return str(poste), float(ev)

    def passer_offre(self, nom_joueur):
        ll = self.classements[nom_joueur]
        offre = ll[0]
        nom_club, val, ms, besoin, tps_laisse = offre

        ll.remove(offre)
        ll.append(offre)

        del(self.dd_temps_passe[nom_club][nom_joueur])
        nouvelle_offre = ll[0]
        nom_club, val, ms, besoin, tps_laisse = nouvelle_offre
        self.dd_temps_passe[nom_club][nom_joueur] = 0

    def sauver_ordre_clubs(self):
        with open(s.TRANSFERTS_DIR_NAME(self.dat)+'/ordre_clubs.oc', 'w') as ff:
            pickle.dump(self.noms_clubs, ff)
        print u"Ordre clubs sauvegardé\n"

    def charger_ordre_clubs(self):
        filename = s.TRANSFERTS_DIR_NAME(self.dat)+'/ordre_clubs.oc'
        if osp.isfile(filename):
            with open(filename, 'r') as ff:
                self.noms_clubs = pickle.load(ff)
            self.clubs.sort(key=lambda cc: self.noms_clubs.index(cc.nom))
            print u"Ordre clubs chargé\n"
        else:
            #On tire au hasard l'ordre de passage des clubs
            shuffle(self.clubs)
            self.noms_clubs = [cc.nom for cc in self.clubs]
            print u"Ordre clubs créé\n"
            self.sauver_ordre_clubs()

    def sauvegarder_recrutements(self):
        filename = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_joueurs_recrutes.dict'
        with open(filename, 'w') as ff:
            pickle.dump(self.dd_joueurs_recrutes, ff)
        print u"dd_joueurs_recrutes sauvegardé"

        filename_besoins = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_besoins_recrutes.dict'
        with open(filename_besoins, 'w') as ff:
            pickle.dump(self.dd_besoins_recrutes, ff)
        print u"dd_besoins_recrutes sauvegardé"

        filename_tours_passes = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_tours_passes.dict'
        with open(filename_tours_passes, 'w') as ff:
            pickle.dump(self.dd_tours_passes, ff)
        print u"dd_tours_passes sauvegardé"
        
        filename_classements = s.TRANSFERTS_DIR_NAME(self.dat)+'/classements.dict'
        with open(filename_classements, 'w') as ff:
            pickle.dump(self.classements, ff)
        print u"classements sauvegardé"

        filename_temps_passes = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_temps_passe.dict'
        with open(filename_temps_passes, 'w') as ff:
            pickle.dump(self.dd_temps_passe, ff)
        print u"dd_temps_passe sauvegardé"

        filename_dd_joueurs_interesses_precedant = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_joueurs_interesses_precedant.dict'
        with open(filename_dd_joueurs_interesses_precedant, 'w') as ff:
            pickle.dump(self.dd_joueurs_interesses_precedant, ff)
        print u"dd_joueurs_interesses_precedant sauvegardé"

        dial = MyDialog(u"Joueurs recrutés et besoins correspondant sauvegardés")
        dial.exec_()

    def charger_recrutements(self):
        filename = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_joueurs_recrutes.dict'
        if osp.isfile(filename):
            with open(filename, 'r') as ff:
                dd = pickle.load(ff)
            self.dd_joueurs_recrutes = dd
            print u"\ndd_joueurs_recrutes chargé"
        else:
            print u"\ndd_joueurs_recrutes initié vide"
            pass

        filename_besoins = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_besoins_recrutes.dict'
        if osp.isfile(filename_besoins):
            with open(filename_besoins, 'r') as ff:
                dd = pickle.load(ff)
            self.dd_besoins_recrutes = dd
            print u"dd_besoins_recrutes chargé"
        else:
            print u"dd_besoins_recrutes initié vide"
            pass

        filename_tours_passes = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_tours_passes.dict'
        if osp.isfile(filename_tours_passes):
            with open(filename_tours_passes, 'r') as ff:
                dd = pickle.load(ff)
            self.dd_tours_passes = dd
            print u"dd_tours_passes chargé"
        else:
            print u"dd_tours_passes initié à 0"
            pass

        filename_temps_passes = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_temps_passe.dict'
        if osp.isfile(filename_temps_passes):
            with open(filename_temps_passes, 'r') as ff:
                dd = pickle.load(ff)
            self.dd_temps_passe = dd
            print u"dd_temps_passe chargé"
        else:
            print u"dd_temps_passe initié à 0"
            pass

        filename_dd_joueurs_interesses_precedant = s.TRANSFERTS_DIR_NAME(self.dat)+'/dd_joueurs_interesses_precedant.dict'
        if osp.isfile(filename_dd_joueurs_interesses_precedant):
            with open(filename_dd_joueurs_interesses_precedant, 'r') as ff:
                dd = pickle.load(ff)
            self.dd_joueurs_interesses_precedant = dd
            print u"dd_joueurs_interesses_precedant chargé"
        else:
            print u"dd_joueurs_interesses_precedant initié vide"
            pass

    def voir_classement(self):
        rows = []
        joueurs = []
        classements = {}
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.get_joueur_from_nom(nom)
            joueurs.append(jj)
            classements[nom] = self.classements[nom]
        C = ClassementOffresDialog(joueurs, classements)
        C.exec_()

    def charger_classements(self):
        filename = s.TRANSFERTS_DIR_NAME(self.dat)+'/classements.dict'
        filename_choix_depart = s.TRANSFERTS_DIR_NAME(self.dat) + '/choix' + str(0) + '.prop'
        if osp.isfile(filename_choix_depart):
            with open(filename_choix_depart, 'r') as ff:
                dd = pickle.load(ff)
            self.classements_depart = dd
            print u"classements_depart chargés"
        else:
            self.classements_depart = {}
            print u"classements_depart initiés vides"

        if osp.isfile(filename):
            with open(filename, 'r') as ff:
                dd = pickle.load(ff)
            self.classements = dd
            print u"\nclassements chargés"
        else:
            self.classements = self.classements_depart
            print u"classements chargés à partir des choix de départ"

    def faire_transferts(self):
        mb = QtGui.QMessageBox()
        if mb.question(None,
                       "Question",
                       u"Effectuer définitivement les transferts ?",
                       "Non",
                       "Oui") == 1:
            self.en_attente = []
            self.noms_recrutes = []
            for nom_club in self.noms_clubs:
                ll = self.dd_joueurs_recrutes[nom_club]
                recrutes = [tu[0] for tu in ll]
                offres = [tu[1] for tu in ll]
                for ii, nom_jj in enumerate(recrutes):
                    self.noms_recrutes.append(nom_jj)
                    jj = self.get_joueur_from_nom(nom_jj)
                    espoir = self.dat - jj.C <= 2
                    nom_club_new, val, ms, poste, tps_laisse = offres[ii]
                    if not nom_club == nom_club_new:
                        raise ValueError("nom_club et nom_club_new ne correspondent pas : "+nom_club+" et "+nom_club_new)
                    cc_old = self.clubs[self.noms_clubs.index(jj.club)]
                    if jj.club == nom_club:
                        cc_old.masse_salariale -= jj.MS
                        cc_old.masse_salariale += ms
                        jj.MS = ms
                    else:
                        cc_new = self.clubs[self.noms_clubs.index(nom_club)]
                        try:
                            s.transfert(jj.nom, cc_old, cc_new, val, ms, espoir=espoir, forcer_ajout=True)
                        except ValueError:
                            self.en_attente.append((jj, offres[ii]))
                print nom_club, u" : transferts faits"

            vide = self.clubs[self.noms_clubs.index('vide')]
            for cc in self.clubs:
                for jj in cc.get_all_joueurs():
                    if (jj.veut_partir or jj.retraite) and not jj.nom in self.noms_recrutes:
                        s.transfert(jj.nom, cc, vide, jj.VAL, jj.MS, transfert_argent=False)
                cc.sauvegarder()

class ClassementOffresDialog(QtGui.QDialog):
    def __init__(self, joueurs, classements, parent=None):
        super(ClassementOffresDialog, self).__init__(parent)
        self.joueurs = joueurs
        self.classements = classements

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.lay_joueurs = QtGui.QGridLayout()
        self.lay.addLayout(self.lay_joueurs)

        for nn, jj in enumerate(self.joueurs):
            self.lay_joueurs.addWidget(QtGui.QLabel(jj.nom), 0, 2*nn)

            grid = QtGui.QGridLayout()
            self.lay_joueurs.addLayout(grid, 1, 2*nn)

            for ii, offre in enumerate(self.classements[jj.nom]):
                for kk, it in enumerate(offre):
                    st = str(it)
                    lab = QtGui.QLabel(st)
                    grid.addWidget(lab, ii, kk)

            if not jj == self.joueurs[-1]:
                #self.lay_joueurs.addSpacing(50)
                self.lay_joueurs.addWidget(QtGui.QLabel('\t'), 0, 2*nn+1)

        self.but = QtGui.QPushButton("OK")
        self.but.clicked.connect(self.close)
        self.lay.addWidget(self.but)

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Escape, QtCore.Qt.Key_Enter):
            self.close()
            event.accept()
        else:
            super(Dialog, self).keyPressEvent(event)

class ChoixBesoinDialog(QtGui.QDialog):
    def __init__(self, besoins, joueur, parent=None):
        super(ChoixBesoinDialog, self).__init__(parent)
        self.besoins = besoins
        self.joueur = joueur

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.group = QtGui.QButtonGroup()
        for besoin in self.besoins:
            rad = QtGui.QRadioButton(self.parent().get_st_besoin(besoin))
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
