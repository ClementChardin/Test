# -*- coding: cp1252 -*-
import selection as s
from generer_joueur.generer_joueur import creer_joueur_legendaire

vide = s.charger('vide', 'c')
dat = s.lire_date()

st = raw_input(u"Créer un joueur ? y/[n] ")

while st in ('y', 'Y'):
    jj = creer_joueur_legendaire(dat)
    jj.veut_partir = True

    s.ajouter_joueur(jj, vide)

    st = raw_input(u"Créer un joueur ? y/[n] ")

vide.sauvegarder()
