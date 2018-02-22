from PyQt4 import QtGui, QtCore
import selection as s
import os.path as osp
import sip
import pickle
from date import *
from savefiles import *
from couleurs import *
from biopopup import BioPopup
from choix_joueurs import MyTableWidgetItem
from choix_joueurs_selection import *
from match import MyDialog

class ChoixJoueursFinSaisonWidget(QtGui.QWidget):
    def __init__(self, parent=None, noms_clubs=s.noms_clubs, dat=None, vagues=0):
        super(ChoixJoueursFinSaisonWidget, self).__init__(parent)

        self.dat = lire_date() if dat is None else dat
        self.vagues = vagues

        self.noms_clubs = noms_clubs
        self.clubs = []
        self.recrutements = {}
        for nom in self.noms_clubs:
            self.clubs.append(s.charger(nom, 'c'))
            self.recrutements[nom] = {}

        self.clubs_saison_suivante = []
        for nom in self.noms_clubs:
            self.clubs_saison_suivante.append(s.charger(nom, 'c', self.dat+1))
        self.club = self.clubs_saison_suivante[0]

        if osp.isfile(TRANSFERTS_DIR_NAME(self.dat)+'/recrutements' + str(self.vagues) + '.prop'):
            self.recrutements = self.charger_recrutements()

        self.non_renouveles = []

        self.partants = []
        self.joueurs_partants = []
        for cc in self.clubs:
            for jj in cc.get_all_joueurs():
                if jj.veut_partir:
                    self.partants.append(jj.nom)
                    self.joueurs_partants.append(jj)

        self.en_attente = self.get_joueurs_en_attente()
        self.effectif = self.get_effectif()

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()
        self.wid_en_attente.filtrer_joueurs()

    def setup_ui(self):
        self.wid_en_attente = ChoixJoueursSelectionWidget(autre=None,
                                                          parent=None,
                                                          joueurs=self.en_attente,
                                                          poste_filtre='Tous',
                                                          ev_filtre='Tous',
                                                          fatigue=False,
                                                          dat=self.dat+1,
                                                          changement_poste_joueur_possible=True)
        #Retirer le choix "compo"
        self.wid_en_attente.combo.removeItem(1)
        self.lay.addWidget(self.wid_en_attente)

        self.milieu = MilieuWidget(parent=self)
        self.milieu.combo_clubs.setCurrentIndex(self.noms_clubs.index(self.club.nom))
        self.lay.addWidget(self.milieu)

        self.wid_effectif = ChoixJoueursSelectionWidget(autre=None,
                                                   parent=None,
                                                   joueurs=self.effectif,
                                                   poste_filtre='Tous',
                                                   ev_filtre='Tous',
                                                   fatigue=False)
        #Retirer le choix "compo"
        self.wid_effectif.combo.removeItem(1)
        self.lay.addWidget(self.wid_effectif)
        self.wid_en_attente.autre = self.wid_effectif
        self.wid_effectif.autre = self.wid_en_attente

    def clean_ui(self):
        
        self.lay.removeWidget(self.wid_en_attente)
        self.wid_en_attente.deleteLater()

        self.lay.removeWidget(self.wid_effectif)
        self.wid_effectif.deleteLater()

        self.lay.removeWidget(self.milieu)
        self.milieu.deleteLater()
        """
        sip.delete(self.wid_en_attente)
        sip.delete(self.wid_effectif)
        sip.delete(self.milieu)
        """

    def maj(self):
        self.clean_ui()
        self.setup_ui()
        self.wid_en_attente.filtrer_joueurs()

    def get_joueurs_en_attente(self):
        ll = []
        noms = []
        for dd in self.recrutements:
            ddd = dd[self.club.nom]
            noms += [nom for nom in ddd.keys()]
        for cc in self.clubs_saison_suivante:
            for jj in cc.get_all_joueurs():
                if jj.nom in noms and jj.nom in self.partants \
                   or jj in self.non_renouveles:
                    ll.append(jj)
        return ll

    def get_effectif(self):
        ll = []
        for jj in self.club.get_all_joueurs():
            if not jj.nom in self.partants \
               and not jj in self.non_renouveles:
                ll.append(jj)
        return ll

    def charger_recrutements(self):
        ll = []
        for vag in range(self.vagues+1):
            with open(TRANSFERTS_DIR_NAME(dat=self.dat) + '/recrutements' + str(vag) + '.prop', 'r') as ff:
                recrutements = pickle.load(ff)
            ll.append(recrutements)
        return ll

    def choix_club(self, nom):
        self.enlever_non_renouveles()
        self.club = self.clubs_saison_suivante[self.noms_clubs.index(nom)]
        self.en_attente = self.get_joueurs_en_attente()
        self.effectif = self.get_effectif()
        self.maj()

    def transferer_joueur(self, jj, source, cible):
        if jj in self.en_attente:
            poste = 'CE' if jj.postes[1] in ('C1', 'C2') else jj.postes[1]
            lim = s.limite_poste[poste]
            nb = len(self.club.joueurs['N8']) + len(self.club.joueurs['TL']) if poste in ('N8', 'TL') \
                 else len(self.club.joueurs[poste])
            if nb >= lim and not jj in self.club.joueurs[poste]:
                #print "Probleme"
                self.dial = MyDialog("Poste plein")
            else:
                if jj in self.non_renouveles:
                    self.non_renouveles.remove(jj)
                else:
                    print "Transfert", jj.nom
                    for dd in self.recrutements:
                        if jj.nom in dd[self.club.nom].keys():
                            tu = dd[self.club.nom][jj.nom]
                            #tu = (val, ms, (poste_besoin, ev_besoin))
                    idx_old = self.noms_clubs.index(jj.club)
                    club_old = self.clubs_saison_suivante[idx_old]
                    idx_new = self.noms_clubs.index(self.club.nom)
                    club_new = self.clubs_saison_suivante[idx_new]
                    if club_new.nom == club_old.nom:
                        club_new.masse_salariale += tu[1] - jj.MS
                        jj.MS = tu[1]
                        jj.veut_partir = False
                        jj.MS_probleme = False
                    else:
                        s.transfert(jj.nom, club_old, club_new, tu[0], tu[1])
                    self.partants.remove(jj.nom)
                #self.club = club_new
                self.en_attente = self.get_joueurs_en_attente()
                self.effectif = self.get_effectif()
                self.maj()
        elif jj in self.effectif:
            #s.supprimer_joueur(jj, self.clubs_saison_suivante[self.noms_clubs.index(self.club.nom)])
            self.non_renouveles.append(jj)
            self.en_attente = self.get_joueurs_en_attente()
            self.effectif = self.get_effectif()
            self.maj()

    def enlever(self):
        noms_recrutes = []
        for dd in self.recrutements:
            for ddd in dd.values():
                noms_recrutes += ddd.keys()
        vide = self.clubs_saison_suivante[self.noms_clubs.index('vide')]
        for jj in self.joueurs_partants:
            if not jj.nom in noms_recrutes:
                club_old = self.clubs_saison_suivante[self.noms_clubs.index(jj.club)]
                s.transfert(jj.nom, club_old, vide, 0, 0, transfert_argent=False)

    def enlever_non_renouveles(self):
        if len(self.non_renouveles) == 0:
            pass
        else:
            mb = QtGui.QMessageBox()
            quest = u"""Enever les joueurs non renouvelés ?
                        Il ne sera plus possible de récupérer
                        les joueurs suivants : """
            for jj in self.non_renouveles:
                quest += jj.nom + ' '
            if mb.question(None,
                           "Question",
                           quest,
                           "Non", "Oui") == 1:
                vide = self.clubs_saison_suivante[self.noms_clubs.index('vide')]
                for jj in self.non_renouveles:
                    club_old = self.clubs_saison_suivante[self.noms_clubs.index(jj.club)]
                    s.transfert(jj.nom, club_old, vide, 0, 0, transfert_argent=False)
                self.non_renouveles = []
    def sauvegarder(self):
        for cc in self.clubs_saison_suivante:
            cc.sauvegarder(dat=self.dat+1)
        self.dial = MyDialog(u"Sauvegarde effectuée")

class MilieuWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MilieuWidget, self).__init__(parent)
        self.noms_clubs = self.parent().noms_clubs

        self.lay_milieu = QtGui.QVBoxLayout()
        self.setLayout(self.lay_milieu)

        """
        Combo pour choix du club
        """
        self.combo_clubs = QtGui.QComboBox()
        for nom in self.noms_clubs:
            self.combo_clubs.addItem(nom)
        self.combo_clubs.activated['QString'].connect(self.parent().choix_club)
        self.lay_milieu.addWidget(self.combo_clubs)

        """
        Boutton pour enlever les joueurs partants non recrutés
        """
        self.but_enlever = QtGui.QPushButton(u"Enlever les partants non recrutés")
        self.but_enlever.clicked.connect(self.parent().enlever)
        self.lay_milieu.addWidget(self.but_enlever)

        """
        Boutton pour enlever les joueurs non renouvelés
        """
        self.but_enlever_non_renouveles = QtGui.QPushButton(u"Enlever les joueurs non renouvelés")
        self.but_enlever_non_renouveles.clicked.connect(self.parent().enlever_non_renouveles)
        self.lay_milieu.addWidget(self.but_enlever_non_renouveles)

        """
        Boutton pour sauvegarder
        """
        self.but_sauver = QtGui.QPushButton("Sauvegarder")
        self.but_sauver.clicked.connect(self.parent().sauvegarder)
        self.lay_milieu.addWidget(self.but_sauver)
