import biopopup as b
import rolespopup as rp
from selection import *
from PyQt4 import QtCore, QtGui
from couleurs import *
from plot_evolution_widget import PlotEvolutionWidget
from diagramme_joueurs_widget import DiagrammeJoueursWidget

class ChoixJoueursWidget(QtGui.QWidget):
    def __init__(self, parent=None,
                 club=charger('Vide', 'c'),
                 poste_filtre='all',
                 dat=None,
                 fatigue=True):
        super(ChoixJoueursWidget, self).__init__(parent)
        self.club = club
        self.dat = s.lire_date() if dat is None else dat
        self.all_joueurs = self.club.get_all_joueurs()
        self.poste_filtre = poste_filtre
        self.fatigue = fatigue
        #self.selected_joueurs = self.all_joueurs

        self.lay = QtGui.QVBoxLayout()
        self.setLayout(self.lay)

        self.setup_ui()

        #click droit
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def setup_ui(self):
        self.lay_options = QtGui.QHBoxLayout()
        """
        ComboBox pour les filtrages par postes
        """
        self.combo = QtGui.QComboBox()
        self.combo.setObjectName("Filtrer par poste")
        for poste in ["Tous", "Compo"]+postes:
            if poste == self.poste_filtre or \
               (poste == "Tous" and self.poste_filtre == "all") or \
               (poste == "Compo" and self.poste_filtre == "compo"):
                   self.combo.insertItem(0, poste)
                   self.combo.setCurrentIndex(0)
            else:
                self.combo.addItem(poste)
        self.combo.activated['QString'].connect(self.filtrer_joueurs)

        self.lay_options.addWidget(self.combo)
        """
        Option couleur pour la fatigue ou sur la compo
        """
        #self.split_options = QtGui.QSplitter()
        #self.lay_options.addWidget(self.split_options)
        
        self.lab_options = QtGui.QLabel("Options d'affichage : ")
        self.lay_options.addWidget(self.lab_options)

        self.rad_fatigue = QtGui.QRadioButton("Fatigue")
        self.rad_fatigue.clicked.connect(self.colorer_table)
        self.lay_options.addWidget(self.rad_fatigue)

        self.rad_age = QtGui.QRadioButton("Age")
        self.rad_age.clicked.connect(self.colorer_table)
        self.lay_options.addWidget(self.rad_age)

        if not self.parent() is None:
            self.rad_compo = QtGui.QRadioButton("Sur la compo")
            self.rad_compo.setChecked(True)
            self.rad_compo.clicked.connect(self.colorer_table)
            self.lay_options.addWidget(self.rad_compo)

        self.lay.addLayout(self.lay_options)
        
        """
        Tableau Ev, postes, fatigue
        """
        self.setup_table()
        self.colorer_table()

    def setup_table(self):
        self.hlabels = ['Nom', 'EV', 'Poste 1', 'Poste 2', 'Poste 3', 'Fatigue',
                        u'Création']
        self.table = QtGui.QTableWidget(len(self.selected_joueurs),
                                        len(self.hlabels))
        self.table.setHorizontalHeaderLabels(self.hlabels)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        #self.table.setSortingEnabled(True)

        for ii, jj in enumerate(self.selected_joueurs):

            st_ev = '%0.2f' % jj.EV if self.poste_filtre in ('all', 'compo') \
                    else '%0.2f' % calc_EV(jj, self.poste_filtre,
                                           fatigue=self.fatigue)
            
            if jj.blessure == 0:
                lab = QtGui.QTableWidgetItem(jj.nom)
            else: #jj.blessure > 0
                lab = QtGui.QTableWidgetItem(jj.nom + " - " + str(jj.blessure))
            self.table.setItem(ii, 0, lab)
            
            lab = QtGui.QTableWidgetItem(st_ev)
            self.table.setItem(ii, 1, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(jj.postes[1])
            self.table.setItem(ii, 2, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(jj.postes[2])
            self.table.setItem(ii, 3, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(jj.postes[3])
            self.table.setItem(ii, 4, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(str(jj.fatigue))
            self.table.setItem(ii, 5, MyTableWidgetItem(lab))
            
            lab = QtGui.QTableWidgetItem(str(jj.C))
            self.table.setItem(ii, 6, MyTableWidgetItem(lab))

        self.lay.addWidget(self.table)

        """
        Connections
        """
        self.table.doubleClicked.connect(self.maj_compo_aux_1)

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
        self.table.verticalHeader().setVisible(False)

    @property
    def selected_joueurs(self):
        if self.poste_filtre == 'all':
            return self.all_joueurs

        elif self.poste_filtre == 'compo':
            ll = []
            for jj in self.all_joueurs:
                comp = self.parent().comp
                if jj.nom in comp.noms_titulaires or \
                   jj.nom in comp.noms_remplacants:
                    ll.append(jj)
            return ll

        else:
            ll = []
            for jj in self.all_joueurs:
                vals = jj.postes
                if self.poste_filtre in vals or (self.poste_filtre in \
                                                 ("C1", "C2") and \
                                                 ("CE" in vals or \
                                                  "C1" in vals or \
                                                  "C2" in vals)):
                    ll.append(jj)
            return ll

    @property
    def filtre_couleur(self):
        if self.rad_fatigue.isChecked():
            return "fatigue"
        elif self.rad_age.isChecked():
            return "age"
        else:
            return "compo"

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)
        
        bioAction = QtGui.QAction('Afficher bio', self)
        bioAction.triggered.connect(self.afficher_bio)
        self.menu.addAction(bioAction)

        compAction = QtGui.QAction('Ajouter a la compo', self)
        compAction.triggered.connect(self.ajouter_compo_mult)
        self.menu.addAction(compAction)

        roleAction = QtGui.QAction('Assigner un role', self)
        roleAction.triggered.connect(self.assigner_role_mult)
        self.menu.addAction(roleAction)

        diagAction = QtGui.QAction('Diagramme etoile', self)
        diagAction.triggered.connect(self.diagramme_etoile)
        self.menu.addAction(diagAction)

        plotevAction = QtGui.QAction(u'Plot évoltution', self)
        plotevAction.triggered.connect(self.plot_evolution)
        self.menu.addAction(plotevAction)

        self.menu.popup(QtGui.QCursor.pos())

    def filtrer_joueurs(self, poste='Tous'):
        self.lay.removeWidget(self.table)
        if poste == 'Tous':
            self.poste_filtre = 'all'
        elif poste == 'Compo':
            self.poste_filtre = 'compo'
        else:
            self.poste_filtre = poste
        self.setup_table()
        self.colorer_table()

    def colorer_table(self):
        dd = dict()
        dd_fond = {}
        for ii, jj in enumerate(self.selected_joueurs):
            if jj.blessure == 0:
                couleur = noir
                if self.filtre_couleur == "fatigue":
                    if jj.fatigue > 14:
                        couleur = orange
                    elif jj.fatigue > 7:
                        couleur = jaune
                elif self.filtre_couleur == "compo":
                    if jj.nom in [jjj.nom for jjj in self.parent().comp.joueurs.values()]:
                        couleur = bleu
                elif self.filtre_couleur == "age":
                    if jj.est_jeune():
                        couleur = vert
                    elif jj.D == s.date + 1:
                        couleur = bleu
                    elif jj.D <= s.date:
                        couleur = rouge
            else: #jj.blessure > 0
                couleur = indian_red

            dd[jj.nom] = couleur

            if jj.veut_partir:
                fond = orange if jj.MS_probleme else rouge
            else:
                fond = blanc
            if jj.retraite:
                fond = gris
            dd_fond[jj.nom] = fond

        for rr in range(self.table.rowCount()):
            for cc in range(self.table.columnCount()):
                nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
                self.table.item(rr, cc).setTextColor(dd[nom])
                self.table.item(rr, cc).setBackgroundColor(dd_fond[nom])

    def maj_compo_aux_1(self):
        rr = self.table.currentIndex().row()
        nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
        self.maj_compo_aux_2(nom)
        
    def maj_compo_aux_2(self, nom):
        joueur = self.club.get_joueur_from_nom(nom)

        self.num, ok = QtGui.QInputDialog.getText(QtGui.QWidget(),
                                                  'Input Dialog',
                                                  'Nouveau numero pour ' \
                                                  + joueur.nom + ' :')
        self.num = 'n'+str(self.num)
        if ok:
            self.table.clearSelection()
            self.parent().maj_compo(joueur, self.num)
            self.colorer_table()

    def afficher_bio(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            jj = self.club.get_joueur_from_nom(nom)
            joueurs.append(jj)
        
        self.pop = b.BioPopup(joueurs=joueurs,
                              col3=self, 
                              fatigue=self.fatigue,
                              dat=self.dat)
        self.pop.show()

    def assigner_role_mult(self):
        joueurs = []
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            joueur = self.club.get_joueur_from_nom(nom)
            joueurs.append(joueur)
        self.role_pop = rp.RolePopupWidget(joueurs=joueurs, main=self.parent())
        self.role_pop.show()
        
    def ajouter_compo_mult(self):
        rows = []
        for idx in self.table.selectedIndexes():
            rr = idx.row()
            if not rr in rows:
                rows.append(rr)
        for rr in rows:
            nom = str(self.table.item(rr, 0).text()).split(" - ")[0]
            self.maj_compo_aux_2(nom) 
        
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
            joueur = self.club.get_joueur_from_nom(nom)
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
            jj = self.club.get_joueur_from_nom(nom)
            joueurs.append(jj)
        self.pew = PlotEvolutionWidget(joueurs)

class MyTableWidgetItem(QtGui.QTableWidgetItem):
    def __lt__(self, other):
        if isfloat(self.text()) and isfloat(other.text()):
            return True if float(self.text()) < float(other.text()) else False
        elif self.text() in ordre_postes.keys() and \
             other.text() in ordre_postes.keys():
            return ordre_postes[str(self.text())] < ordre_postes[str(other.text())]
        else:
            self_new = QtGui.QTableWidgetItem(self.text())
            other_new = QtGui.QTableWidgetItem(other.text())
            return self_new < other_new

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
