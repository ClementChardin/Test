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

def plot_evolution(joueurs, dat=None, ax=None):
    width = .2 if len(joueurs) < 5 else 1./len(joueurs)
    if dat is None:
        dat = lire_date()
    if ax is None:
        ax = subplot(111)
    ax2 = ax.twinx()
    d = 100
    D = 11
    I = 0 #indice pour les légendes
    dd = {} #dict pour les légendes
    for ii, jj in enumerate(joueurs):
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

        lab = jj.nom + ' Club, titulaire'
        dd[lab] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, cts, width,
            label=lab,
            color=cols)
        
        lab = jj.nom + u' Club, remplaçant'
        dd[lab] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, crs/2., width, bottom=cts,
            label=lab,
            color=cols2)

        c_arm = couleurs.couleurs_equipes[jj.ARM].getRgbF()
        c_arm2 = (c_arm[0], c_arm[1], c_arm[2], .7)
        
        lab = jj.nom + ' ' + jj.ARM + u', titulaire'
        dd[lab] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, sts, width, bottom=cts+crs/2.,
            label=lab,
            color=c_arm)
        
        lab = jj.nom + ' ' + jj.ARM + u', remplaçant'
        dd[lab] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, srs/2., width, bottom=cts+crs/2.+sts,
            label=lab,
            color=c_arm2)
        
        lab = jj.nom+' Evaluation'
        dd[lab] = I
        I += 1
        ax2.plot(dats, evs, 'o-',
             label=lab)
             #color='k')#couleurs.couleurs_equipes[jj.club].getRgbF())

        if not jj.anciens_clubs == '':
            for ii, st in enumerate(jj.anciens_clubs.split(';')):
                nom_club, da = st.split(' ')
                if ii == len(jj.anciens_clubs.split(';'))-1:
                    trans = da + ' : ' + nom_club + ' -> ' + jj.club
                else:
                    nom_club2 = jj.anciens_clubs.split(';')[ii+1].split(' ')[0]
                    trans = da + ' : ' + nom_club + ' -> ' + nom_club2
                
                lab = jj.nom + ' ' + trans
                dd[lab] = I
                I += 1
                x = int(da) - width/2. - (1 - width*len(joueurs))/2.
                ax.axvline(x, linestyle='--', color='k', linewidth=2, label=lab)

        if jj.D <= dat:
            lab = jj.nom + u' Déclin : ' + str(jj.D)
            dd[lab] = I
            I += 1
            ax.axvline(jj.D-.5,linestyle='--', color='r', linewidth=2, label=lab)

        if dats.min() < d:
            d = dats.min()
        if dats.max() > D:
            D = dats.max()

    ax.set_xlim(d-1, D+1)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    hh = sorted(zip(h1+h2, l1+l2), key=lambda tu: dd[tu[1]])
    handles, labels = zip(*hh)
    ax.legend(handles, labels, ncol=len(joueurs))
              #bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
              #mode="expand", borderaxespad=0)
    #ax.set_title(jj.nom)
    xlabel('Date')
    ax.set_ylabel(u'Matches joués')
    ax2.set_ylabel(u'Evaluation')
