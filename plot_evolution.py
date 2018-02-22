import selection as s
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from ui import couleurs
from date import *
from joueur import *
from numpy import *
from matplotlib.pyplot import *

def plot_evolution(jj, dat=None):
    if dat is None:
        dat = lire_date()
    dats = []
    evs = []
    cts = []
    crs = []
    sts = []
    srs = []
    cols = []
    cols2 = []
    ll = jj.jj_passe.items() + [('s'+str(dat), jj)]
    ll.sort(key=lambda tu: int(tu[0].split('s')[1]))
    for st_dat, jjj in ll:
        da = int(st_dat.replace('s', ''))
        dats.append(da)
        evs.append(jjj.EV)
        ct = jjj.MJ1['CT'] + jjj.MJ2['CT'] + jjj.MJ3['CT']
        cr = jjj.MJ1['CR'] + jjj.MJ2['CR'] + jjj.MJ3['CR']
        st = jjj.MJ1['ST'] + jjj.MJ2['ST'] + jjj.MJ3['ST']
        sr = jjj.MJ1['SR'] + jjj.MJ2['SR'] + jjj.MJ3['SR']
        cts.append(ct)
        crs.append(cr)
        sts.append(st)
        srs.append(sr)
        c_club = couleurs.couleurs_equipes[jjj.club].getRgbF()
        c_club2 = (c_club[0], c_club[1], c_club[2], .7)
        cols.append(c_club)
        cols2.append(c_club2)

    cts, crs, sts, srs = array(cts), array(crs), array(sts), array(srs)
    
    dats = array(dats)
    width = .2
    bar(dats - width/2, cts, width,
        label='Club, titulaire',
        color=cols)
    bar(dats - width/2, crs/2., width, bottom=cts,
        label=u'Club, remplaçant',
        color=cols2)

    c_arm = couleurs.couleurs_equipes[jj.ARM].getRgbF()
    c_arm2 = (c_arm[0], c_arm[1], c_arm[2], .7)
    ax = subplot(111)
    bar(dats - width/2, sts, width, bottom=cts+crs/2.,
        label=jj.ARM+u', titulaire',
        color=c_arm)
    bar(dats - width/2, srs/2., width, bottom=cts+crs/2.+sts,
        label=jj.ARM+u', remplaçant',
        color=c_arm2)
    ax2 = ax.twinx()
    plot(dats, evs, 'o-',
         label='Evaluation',
         color='k')#couleurs.couleurs_equipes[jj.club].getRgbF())

    if not jj.anciens_clubs == '':
        for ii, st in enumerate(jj.anciens_clubs.split(';')):
            nom_club, da = st.split(' ')
            if ii == len(jj.anciens_clubs.split(';'))-1:
                trans = da + ' : ' + nom_club + ' -> ' + jj.club
            else:
                nom_club2 = jj.anciens_clubs.split(';')[ii+1].split(' ')[0]
                trans = da + ' : ' + nom_club + ' -> ' + nom_club2
            axvline(int(da)-.5, linestyle='--', color='k', linewidth=2, label=trans)

    if jj.D <= dat:
        axvline(jj.D-.5,linestyle='--', color='r', linewidth=2, label=u'Déclin : '+str(jj.D))

    xlim(min(dats)-1, max(dats)+1)
    #ax.legend()
    #ax2.legend()
    #lns = ax.lines+ax2.lines
    #ax.legend(lns, [ln.get_label() for ln in lns])
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2)
    title(jj.nom)
    xlabel('Date')
    ax.set_ylabel(u'Matches joués')
    ax2.set_ylabel(u'Evaluation')
