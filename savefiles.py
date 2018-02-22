import os.path as osp
from date import *

CURRENT_DIR_NAME = osp.dirname(osp.abspath(__file__))
IMAGES_DIR = CURRENT_DIR_NAME + "/images"

def SAISON_DIR_NAME(dat=None):
    date = lire_date() if dat is None else dat
    return CURRENT_DIR_NAME + '/data/saison ' + str(date)

def SELECTIONS_DIR_NAME(dat=None):
    return SAISON_DIR_NAME(dat=dat) + '/selections'

def CLUBS_DIR_NAME(dat=None):
    return SAISON_DIR_NAME(dat=dat) + '/clubs'

def TRANSFERTS_DIR_NAME(dat=None):
    return SAISON_DIR_NAME(dat=dat) + '/transferts'

def CALENDRIERS_DIR_NAME(dat=None):
    return SAISON_DIR_NAME(dat=dat) + '/calendriers'
