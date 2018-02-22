import selection as s
from generer_joueur.generer_joueur import *
from miscellaneous import *
from numpy import random

"""
dd_jeunes contient les postes des jeunes voulus par le club,
il suffit de  remplacer par [] ceux déjà faits si une erreur a lieu.
"""
"""
dd_jeunes=dict(AL=[],
               ALT=[],
               APA=[],
        BRB=[],
        BSK=[],
        CAT=[],
        DKF=[],
        DKW=[],
        ED=[],
        FS=[],
        GP=[],
        HTH=[],
        KAK=[],
        KH=[],
        KHR=[],
        MDL=[],
        MRB=[],
        MSL=[],
        PRG=[],
        QNL='DL TL CE AI N8'.split(' '),
        SN='AR DL TA DM DO'.split(' '),
        TA='DL DO DM N8 TL DL TA'.split(' '),
        TLB='TL AI AR'.split(' '),
        TO='AR TL TA'.split(' '),
        vide=[])
"""

N = len(s.postes)
dd_jeunes = {}
for nom in s.noms_clubs:
    dd_jeunes[nom] = []
    if not nom == 'vide':
        nb = d6_plus()
        for ii in range(nb):
            rand = random.random_integers(N)
            dd_jeunes[nom].append(s.postes[rand-1])
    print nom, dd_jeunes[nom]

dd_armees=dict(AL='ES'.split(' '),
              ALT='EMP'.split(' '),
              APA='HL HE'.split(' '),
              BRB='O HB'.split(' '),
              BSK='O'.split(' '),
              CAT='EN'.split(' '),
              DKF='CV'.split(' '),
              DKW='HB'.split(' '),
              ED='S OG'.split(' '),
               ERE='K'.split(' '),
              FS='O ES'.split(' '),
              GP='N HL'.split(' '),
              HTH='HE'.split(' '),
              KAK='N'.split(' '),
              KH='N'.split(' '),
              KHR='CHS'.split(' '),
               KIS='K'.split(' '),
              MDL='OG'.split(' '),
              MRB='EMP EN'.split(' '),
              MSL='B CV'.split(' '),
              PRG='CHS EMP'.split(' '),
              QNL='B'.split(' '),
              SN='S EN'.split(' '),
              TA='S O'.split(' '),
              TLB='EMP HB'.split(' '),
              TO='HL'.split(' '),
              vide=[])

"""
Liste à mettre à la place de s.noms_clubs en cas de bug
"""
#ll =  ['ERE', 'FS',  'GP', 'HTH', 'KAK', 'KH', 'KHR', 'KIS', 'MDL', 'MRB', 'MSL', 'PRG', 'QNL', 'SN', 'TA', 'TLB', 'TO', 'vide']
ll = s.noms_clubs

for nom in ll:
    print nom
    cc = s.charger(nom, 'c')
    for poste in dd_jeunes[nom]:
        idx = random.random_integers(len(dd_armees[nom])) - 1
        armee = dd_armees[nom][idx]
        generer_ajouter_joueur_complet(poste,
                                       armee,
                                       saison_en_cours=True,
                                       club=cc,
                                       nom_club=nom,
                                       payer=True,
                                       espoir=True)

for armee in ('K', 'EST', 'ARA'):
    nn = random.random_integers(4, 8)
    jeunes = []
    for ii in range(nn):
        jeunes.append(s.postes[random.random_integers(nn) - 1])
    for poste in jeunes:
        if poste in ('C1', 'C2'):
            poste = 'CE'
        generer_ajouter_joueur_complet(poste,
                                       armee,
                                       saison_en_cours=True,
                                       club=None,
                                       nom_club='vide',
                                       payer=True)
