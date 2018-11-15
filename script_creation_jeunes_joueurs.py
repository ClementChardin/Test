import selection as s
from generer_joueur.generer_joueur import *
from miscellaneous import *
from numpy import random
import pickle
import os.path as osp

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
filename = s.TRANSFERTS_DIR_NAME()+'/jeunes_joueurs.dict'
if osp.isfile(filename):
    with open(filename, 'r') as ff:
        dd_jeunes = pickle.load(ff)
    print u"dd_jeunes chargé"
else:
    N = len(s.postes)
    dd_jeunes = {}
    for nom in s.noms_clubs():
        dd_jeunes[nom] = []
        if not nom == 'vide':
            nb = d6_plus()
            for ii in range(nb):
                rand = random.random_integers(N)
                dd_jeunes[nom].append(s.postes[rand-1])
        print nom, dd_jeunes[nom]
    with open(filename, 'w') as ff:
        pickle.dump(dd_jeunes, ff)
    print u"dd_jeunes créé et sauvegardé"

with open('data/noms_joueurs.list', 'r') as ff:
    noms_joueurs = pickle.load(ff)
print u"noms joueurs chargés"

dd_armees=dict(AL='ES'.split(' '),
              ALT='EMP'.split(' '),
              APA='HL HE'.split(' '),
              BRB='O HB'.split(' '),
              BSK='O'.split(' '),
              CAT='EN'.split(' '),
              DKF='CV'.split(' '),
              DKW='HB'.split(' '),
              ED='S OG'.split(' '),
              FS='O ES'.split(' '),
              GP='N HL'.split(' '),
              HTH='HE'.split(' '),
              KAK='N'.split(' '),
              KH='N'.split(' '),
              KHR='CHS'.split(' '),
              MDL='OG'.split(' '),
              MRB='EMP EN'.split(' '),
              MSL='B CV'.split(' '),
              PRG='CHS EMP'.split(' '),
              QNL='B'.split(' '),
              SN='S EN'.split(' '),
              TA='S O'.split(' '),
              TLB='EMP HB'.split(' '),
              TO='HL'.split(' '),
              vide=[],
               AES='CHS'.split(' '),
               KKR='N'.split(' '),
               ERE='K'.split(' '),
               FST='K'.split(' '),
               KIS='K'.split(' '),
               MDH='EMP'.split(' '),
               MRT='ARA'.split(' '),
               BIL='EST'.split(' '),
               AHK='ARA'.split(' '),
               MAG='EST'.split(' '),
               CPH='ARA'.split(' '),
               EKR='O'.split(' '))

"""
Liste à mettre à la place de s.noms_clubs en cas de bug
"""
ll = [nom for nom in s.noms_clubs()]
deja_faits = ['AES', 'AHK']
"""
['AES', 'AHK', 'AL', 'APA', 'BIL', 'BRB', 'BSK', 'CAT', 'CPH',
'DKF', 'DKW', 'ED', 'EKR', 'ERE', 'FS', 'FST', 'GP', 'HTH',
'KAK', 'KH', 'KHR', 'KIS', 'KKR', 'MAG', 'MDH', 'MDL', 'MRB',
'MRT', 'MSL', 'PRG', 'QNL', 'SN', 'TA', 'TLB', 'TO']
"""
for nom in deja_faits:
    ll.remove(nom)

for nom in ll:
    print '\n', nom
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

for armee in s.noms_armees:
    nn = d3_plus()
    print '\n', armee, nn
    jeunes = []
    for ii in range(nn):
        jeunes.append(s.postes[random.random_integers(len(s.postes)) - 1])
    for poste in jeunes:
        if poste in ('C1', 'C2'):
            poste = 'CE'
        generer_ajouter_joueur_complet(poste,
                                       armee,
                                       saison_en_cours=True,
                                       club=None,
                                       nom_club='vide',
                                       payer=True,
                                       noms_joueurs=noms_joueurs)

noms_joueurs = []
for nom in s.noms_clubs(14):
    cc = s.charger(nom, 'c', 14)
    for jj in cc.get_all_joueurs():
        noms_joueurs.append(jj.nom)
with open('data/noms_joueurs.list', 'w') as ff:
    pickle.dump(noms_joueurs, ff)
