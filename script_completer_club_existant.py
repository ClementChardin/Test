import selection as s
from generer_joueur.generer_joueur import *

besoins = ['PI', 'DL', 'TL', 'TL', 'AI']
armee = 'K'
nom_club = 'KIS'
cc = s.charger(nom_club, 'c')

for poste in besoins:
    generer_ajouter_joueur_complet(poste,
                                   armee,
                                   saison_en_cours=False,
                                   club=cc,
                                   nom_club=nom_club,
                                   payer=False,
                                   espoir=False)
