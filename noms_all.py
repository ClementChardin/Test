# -*- coding: cp1252 -*-
from os import listdir, getcwd
from date import *
from savefiles import *

noms_clubs_vieux_monde = ['AL', 'ALT', 'BSK', 'DKF', 'DKW', 'KAK', 'MRB', 'MSL', 'PRG', 'QNL', 'TA', 'TLB']
noms_clubs_nouveaux_mondes = ['APA', 'BRB', 'CAT', 'ED', 'FS', 'GP', 'HTH', 'KH', 'KHR', 'MDL', 'SN', 'TO']
def noms_clubs(dat=None):
    dat = lire_date() if dat is None else dat
    return listdir(CLUBS_DIR_NAME(dat))
noms_clubs_coupe_poule_1 = ['SN', 'HTH', 'QNL']
noms_clubs_coupe_poule_2 = ['KHR', 'ALT', 'TO']
noms_clubs_coupe_poule_3 = ['TA', 'MRB', 'DKW']
noms_clubs_coupe_poule_4 = ['KAK', 'MDL', 'KH']
noms_clubs_challenge_poule_1 = ['MSL', 'PRG', 'BSK']
noms_clubs_challenge_poule_2 = ['FS', 'DKF', 'GP']
noms_clubs_challenge_poule_3 = ['AL', 'APA', 'TLB']
noms_clubs_challenge_poule_4 = ['ED', 'BRB', 'CAT']

#noms_armees = sorted(['EMP', 'CHS', 'O', 'HE', 'B', 'N', 'ES', 'S', 'EN', 'CV', 'HL', 'HB', 'OG'])
noms_armees = listdir(getcwd() + "\data\saison 12\selections")

noms_complets = {'AES':'Aeslings',
                  'AHK':'Al Haikk',
                  'AL':'Athel Loren',
                  'ALT':'Altdorf',
                  'APA':'Alliance des Peuples Anciens',
                  'BIL':'Bilbali',
                  'BRB':'Barbares',
                  'BSK':'Bersekers',
                  'CAT':'Cathay',
                  'CPH':'Copher',
                  'DKF':'Drakenhof',
                  'DKW':'Drakwald',
                  'ED':'Epine Dorsale',
                  'EKR':'Ekrund',
                  'ERE':'Erengrad',
                  'FS':'Foret Sauvage',
                  'FST':'Fort Straghov',
                  'GP':'Gardiens de la Pointe',
                  'HTH':'Hoeth',
                  'KAK':'Karaz A Karak',
                  'KH':'Karakyn Havag',
                  'KHR':'Khorne',
                  'KIS':'Kislev',
                  'KKR':'Karak Kadrin',
                  'MAG':'Magritta',
                  'MDH':'Middenheim',
                  'MDL':'Montagnes des Larmes',
                  'MRB':'Marienburg',
                  'MRT':'Martek',
                  'MSL':'Moussillon',
                  'PRG':'Praag',
                  'QNL':'Quenelles',
                  'SN':'Skarogne-Nagorond',
                  'TA':'Terres Arides',
                  'TLB':'Talabheim',
                  'TO':"Temple d'Or",
                  'vide':'vide',

                  'ARA':'Arabia',
                  'B':'Bretonnie',
                  'CHS':'Chaos',
                  'CV':'Comtes Vampires',
                  'EMP':'Empire',
                  'EN':'Elfes Noirs',
                  'ES':'Elfes Sylvains',
                  'EST':'Estalie',
                  'HB':u'Hommes Bêtes',
                  'HE':'Hauts Elfes',
                  'HL':u'Hommes Lézards',
                  'K':'Kislev',
                  'N':'Nains',
                  'O':'Orks',
                  'OG':'Ogres',
                  'S':'Skavens',
                  'ULT':'Ultime',
                  'ULTB':'Ultime B',
                  'Vide':'Vide'}

