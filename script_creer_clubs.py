import selection as s
from generer_joueur.generer_joueur import *
from miscellaneous import *
from numpy.random import choice, random_integers
import os.path as osp

"""
/!\ Il faut ajouter une couleur pour chaque club !
"""

besoins = dict(PI=5,
               TA=3,
               DL=4,
               TL=3,
               N8=2,
               DM=2,
               DO=2,
               CE=5,
               AI=3,
               AR=2)
"""
armees = dict(FST='K',
              KKR='N',
              MDH='EMP',
              AES='CHS')
"""
armees = dict(AHK='ARA',
              CPH='ARA',
              MRT='ARA',
              MAG='EST',
              BIL='EST',
              EKR='O')

noms_armees = s.noms_armees[:-3]

for nom, arm in armees.items():
    if osp.isfile(s.CLUBS_DIR_NAME() + '/' + nom + '/' + nom + '.clb'):
        cc = s.charger(nom, 'c')
        print '\n'
        print nom, u'chargé'
    else:
        cc = s.club(nom)
    nb = d6_plus()
    print nom, ':', nb, u'étrangers'
    etrangers = choice(sum(besoins.values()), nb, False)
    N = 0
    for poste, vv in besoins.items():
        N += len(cc.joueurs[poste])
        print poste, len(cc.joueurs[poste]), u'joueurs déjà créés'
        for ii in range(vv - len(cc.joueurs[poste])):
            armee = noms_armees[random_integers(len(noms_armees))-1] if N in etrangers \
                    else arm
            generer_ajouter_joueur_complet(poste,
                                           armee,
                                           saison_en_cours=False,
                                           club=cc,
                                           nom_club=nom,
                                           payer=False,
                                           espoir=False)
            N += 1
    cc.sauvegarder()
    comp = s.compo()
    comp.sauvegarder(nom+'_defaut', nom, 'c')

