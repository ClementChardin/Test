from PyQt4 import QtGui, QtCore
import selection as s
from date import *
from savefiles import *
from biopopup import BioPopup

class TransfertsWidget(QtGui.QWidget):
    def __init__(self, parent=None, noms_clubs=s.noms_clubs, liste=None,
                 dat=None):
        super(TransfertsWidget, self).__init__(parent)

        self.noms_clubs = noms_clubs
        self.clubs = []
        for nom in self.noms_clubs:
            self.clubs.append(s.charger(nom, 'c'))

        self.dat = dat
        self.liste = self.get_liste_departs(liste)

        self.labs = ['nom', 'Club', 'Poste 1', 'Poste 2', 'Poste 3', 'EV']#,
                     #'RG', 'RG_max', 'C', 'D', 'MS_probleme', 'VAL', 'MS']

        self.lay = QtGui.QHBoxLayout()
        self.setLayout(self.lay)
        self.setup_ui()

    def setup_ui(self):
        self.scroll = QtGui.QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.widget_contenu = QtGui.QWidget(self.scroll)
        self.lay_contenu = QtGui.QGridLayout()
        self.widget_contenu.setLayout(self.lay_contenu)
        #self.widget_contenu.setGeometry(QtCore.QRect(0, 0, 380, 247))
        self.scroll.setWidget(self.widget_contenu)
        self.lay.addWidget(self.scroll)

        for jj, lab in enumerate(self.labs + self.noms_clubs):
            self.lay_contenu.addWidget(QtGui.QLabel(lab), 0, jj)

        for ii, tu in enumerate(self.liste):
            for jj, it in enumerate(tu):
                self.lay_contenu.addWidget(QtGui.QLabel(str(it)), ii+1, jj)
            JJ = len(tu)
            
            for jj, cc in enumerate(self.clubs):
                self.lay_contenu.addWidget(PropositionWidget(cc.besoins, prop=None),
                                   ii+1, jj+JJ)



    def get_liste_departs(self, liste=None):
        ll = []
        if liste is None:
            for cc in self.clubs:
                for jj in cc.get_all_joueurs():
                    if jj.veut_partir:
                        tu = [jj.nom, jj.club, jj.postes[1], jj.postes[2],
                              jj.postes[3], round(jj.EV, 2)]#, jj.RG.rang,
                              #jj.RG_max.rang, jj.C, jj.D, jj.MS_probleme, jj.VAL,
                              #jj.MS]
                        ll.append(tu)
        else:
            dirname = SAISON_DIR_NAME(dat=self.dat)
            with open(dirname + '/' + liste, 'r') as ff:
                for line in ff.readlines():
                    tu = line.replace('\n', '').split('\t')
                    ll.append(tu)
        ll.sort(key=lambda tu: s.ordre_postes[tu[2]])
        return ll



class PropositionWidget(QtGui.QWidget):
    def __init__(self, besoins, prop=None, parent=None):
        """
        Une colonne, trois lignes
        L1 : VAL transfert
        L2 : MS proposée
        L3 : à quel besoin du club répond la proposition

        proposition est de la forme (VAL, MS, (Poste, EV))
        besoins est une liste de tuples : [(Poste, EV), ...]
        """
        if not prop is None and not prop[2] in besoins:
            raise ValueError(u"Le poste proposé ne correspond pas à un besoin !")
        super(PropositionWidget, self).__init__(parent)
        self.proposition = prop
        self.besoins = besoins

        val = '' if self.proposition is None else str(self.proposition[0])
        ms = '' if self.proposition is None else str(self.proposition[1])
        besoin = tuple() if self.proposition is None else self.proposition[2]

        self.lay = QtGui.QGridLayout()
        self.setLayout(self.lay)

        self.line_val = QtGui.QLineEdit(val)
        self.lay.addWidget(self.line_val)

        self.line_ms = QtGui.QLineEdit(ms)
        self.lay.addWidget(self.line_ms)

        self.combo_besoin = QtGui.QComboBox()
        for tu in self.besoins:
            if tu == besoin:
                self.combo_besoin.insertItem(0, tu[0] + ' : ' + str(tu[1]))
            else:
                self.combo_besoin.addItem(tu[0] + ' : ' + str(tu[1]))
        if self.proposition is None:
            self.combo_besoin.insertItem(0, '')
        self.combo_besoin.setCurrentIndex(0)
        self.lay.addWidget(self.combo_besoin)

    def get_proposition(self):
        return (int(self.line_val.text()),
                int(self.line_ms.text()),
                self.combo_besoin.currentText())
