# -*- coding: cp1252 -*-
import selection as s
from ui import couleurs
from date import *
from joueur import *
from numpy import *
from matplotlib.pyplot import *
import matplotlib.patches as mpatches
from plot_evolution import MyHandler

def plot_matches_joues(jj, dat=None, ax=None):
    width = .2
    if dat is None:
        dat = lire_date()
    if ax is None:
        ax = subplot(111)
    d = 100
    D = 11 #date début des datas
    I = 0 #indice pour les légendes
    dd = {} #dict pour les légendes
    dats = [] #dates

    ct1s =  [] #club titu, poste 1
    ct2s =  [] #club titu, poste 2
    ct3s =  [] #club titu, poste 3
    cts = [] #club titu, total

    cr1s =  [] #club remp, poste 1
    cr2s =  [] #club remp, poste 2
    cr3s =  [] #club remp, poste 3
    crs = [] #club remp, total

    st1s =  [] #selection titu, poste 1
    st2s =  [] #selection titu, poste 2
    st3s =  [] #selection titu, poste 3
    sts = [] #selection titu, total

    sr1s =  [] #selection remp, poste 1
    sr2s =  [] #selection remp, poste 2
    sr3s =  [] #selection remp, poste 3
    srs = [] #selection remp, total

    cols = [] #couleurs 1 club
    cols2 = [] #couleurs 2 club
    ll = jj.jj_passe.items() + [('s'+str(dat), jj)]
    ll.sort(key=lambda tu: int(tu[0].split('s')[1]))
    for st_dat, jjj in ll:
        da = int(st_dat.replace('s', ''))
        dats.append(da)

        ct1s.append(jjj.MJ1['CT'])
        ct2s.append(jjj.MJ2['CT'])
        ct3s.append(jjj.MJ3['CT'])
        ct = jjj.MJ1['CT'] + jjj.MJ2['CT'] + jjj.MJ3['CT']
        cts.append(ct)

        cr1s.append(jjj.MJ1['CR'])
        cr2s.append(jjj.MJ2['CR'])
        cr3s.append(jjj.MJ3['CR'])
        cr = jjj.MJ1['CR'] + jjj.MJ2['CR'] + jjj.MJ3['CR']
        crs.append(cr)


        st1s.append(jjj.MJ1['ST'])
        st2s.append(jjj.MJ2['ST'])
        st3s.append(jjj.MJ3['ST'])
        st = jjj.MJ1['ST'] + jjj.MJ2['ST'] + jjj.MJ3['ST']
        sts.append(st)

        sr1s.append(jjj.MJ1['SR'])
        sr2s.append(jjj.MJ2['SR'])
        sr3s.append(jjj.MJ3['SR'])
        sr = jjj.MJ1['SR'] + jjj.MJ2['SR'] + jjj.MJ3['SR']
        srs.append(sr)

        c_club = couleurs.couleurs_equipes[jjj.club].getRgbF()
        c_club2 = couleurs.couleurs_equipes[jjj.club+'2'].getRgbF()

        cols.append(c_club)
        cols2.append(c_club2)

    ct1s, ct2s, ct3s, cts = array(ct1s), array(ct2s), array(ct3s), array(cts)
    cr1s, cr2s, cr3s, crs = array(cr1s), array(cr2s), array(cr3s), array(crs)
    st1s, st2s, st3s, sts = array(st1s), array(st2s), array(st3s), array(sts)
    sr1s, sr2s, sr3s, srs = array(sr1s), array(sr2s), array(sr3s), array(srs)
    
    dats = array(dats)

    boo_poste2 = not jj.postes[2] == ''
    boo_poste3 = not jj.postes[3] == ''

    lab_postes = jj.postes[1]
    if boo_poste2:
        lab_postes += ', '+jj.postes[2]
    if boo_poste3:
        lab_postes += ', '+jj.postes[3]

    decalage_totaux = 1
    if boo_poste2:
        decalage_totaux += 1
    if boo_poste3:
        decalage_totaux += 1

    """ Barres club titulaire """
    ax.bar(dats, ct1s, width,
           color='b')#cols)
    if boo_poste2:
        ax.bar(dats + width, ct2s, width,
               color='g')#cols)
    if boo_poste3:
        ax.bar(dats + width*2, ct3s, width,
               color='r')#cols)
    lab_ct = jj.nom + ' Club, titulaire ('+lab_postes+')'
    dd[lab_ct] = I
    I += 1
    ax.bar(dats + width*decalage_totaux, cts, width,
           label=lab_ct,
           color=cols)

    """ Barres club remplaçant """
    ax.bar(dats, cr1s/2., width, bottom=ct1s,
           hatch='\\',
           color='b')#cols2)
    if boo_poste2:
        ax.bar(dats + width, cr2s/2., width, bottom=ct2s,
               hatch='\\',
               color='g')#cols2)
    if boo_poste3:
        ax.bar(dats + width*2, cr3s/2., width, bottom=ct3s,
               hatch='\\',
               color='r')#cols2)
    lab_cr = jj.nom + u' Club, remplaçant ('+lab_postes+')'
    dd[lab_cr] = I
    I += 1
    ax.bar(dats + width*decalage_totaux, crs/2., width, bottom=cts,
           label=lab_cr,
           color=cols2)

    c_arm = couleurs.couleurs_equipes[jj.ARM].getRgbF()
    c_arm2 = couleurs.couleurs_equipes[jj.ARM+'2'].getRgbF()

    """ Barres sélection titulaire """
    ax.bar(dats, st1s, width, bottom=ct1s+cr1s/2.,
           color='c')#c_arm)
    if boo_poste2:
        ax.bar(dats + width, st2s, width, bottom=ct2s+cr2s/2., 
               color='m')#c_arm)
    if boo_poste3:
        ax.bar(dats + width*2, st3s, width, bottom=ct3s+cr3s/2.,
               color='y')#c_arm)
    lab_at = jj.nom + ' ' + jj.ARM + u', titulaire ('+lab_postes+')'
    dd[lab_at] = I
    I += 1
    ax.bar(dats + width*decalage_totaux, sts, width, bottom=cts+crs/2.,
        label=lab_at,
        color=c_arm)

    """ Barres sélection remplaçant """
    ax.bar(dats, sr1s/2., width, bottom=ct1s+cr1s/2.+st1s,
           hatch='\\',
           color='c')#c_arm2)
    if boo_poste2:
        ax.bar(dats + width, sr2s/2., width, bottom=ct2s+cr2s/2.+st2s,
               hatch='\\',
               color='m')#c_arm2)
    if boo_poste3:
        ax.bar(dats + width*2, sr3s/2., width, bottom=ct3s+cr3s/2.+st3s,
               hatch='\\',
               color='y')#c_arm2)
    lab_ar = jj.nom + ' ' + jj.ARM + u', remplaçant ('+lab_postes+')'
    dd[lab_ar] = I
    I += 1
    ax.bar(dats + width*decalage_totaux, srs/2., width, bottom=cts+crs/2.+sts,
           label=lab_ar,
           color=c_arm2)

    if dats.min() < d:
        d = dats.min()
    if dats.max() > D:
        D = dats.max()
    ax.set_xlim(d-1, D+1)
    xlabel('Date')
    ax.set_ylabel(u'Matches joués')

def mix_legends(ax, ax2):
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    hh = sorted(zip(h1+h2, l1+l2), key=lambda tu: dd[tu[1]])
    handles, labels = zip(*hh)

    handler_map = {}
    for ii, lab in enumerate(labels):
        if lab == lab_ct:
            handler_map[handles[ii]] = MyHandler(cols)
        elif lab == lab_cr:
            handler_map[handles[ii]] = MyHandler(cols2)
    ax.legend(handles,
              labels,
              ncol=len(joueurs),
              handler_map=handler_map,
              fontsize='x-large')
