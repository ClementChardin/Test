import selection as s
from ui import couleurs
from date import *
from joueur import *
from numpy import *
from matplotlib.pyplot import *
import matplotlib.patches as mpatches

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
            c_club2 = couleurs.couleurs_equipes[jjj.club+'2'].getRgbF()
            #c_club2 = (c_club[0], c_club[1], c_club[2], .7)
            cols.append(c_club)
            cols2.append(c_club2)

        cts, crs, sts, srs = array(cts), array(crs), array(sts), array(srs)
        
        dats = array(dats)

        lab_ct = jj.nom + ' Club, titulaire'
        dd[lab_ct] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, cts, width,
            label=lab_ct,
            color=cols)
        
        lab_cr = jj.nom + u' Club, remplaçant'
        dd[lab_cr] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, crs/2., width, bottom=cts,
            label=lab_cr,
            color=cols2)

        c_arm = couleurs.couleurs_equipes[jj.ARM].getRgbF()
        c_arm2 = couleurs.couleurs_equipes[jj.ARM+'2'].getRgbF()
        #c_arm2 = (c_arm[0], c_arm[1], c_arm[2], .7)
        
        lab_at = jj.nom + ' ' + jj.ARM + u', titulaire'
        dd[lab_at] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, sts, width, bottom=cts+crs/2.,
            label=lab_at,
            color=c_arm)
        
        lab_ar = jj.nom + ' ' + jj.ARM + u', remplaçant'
        dd[lab_ar] = I
        I += 1
        ax.bar(dats - width/2 + width*ii, srs/2., width, bottom=cts+crs/2.+sts,
            label=lab_ar,
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
    xlabel('Date')
    ax.set_ylabel(u'Matches joués')
    ax2.set_ylabel(u'Evaluation')

class MyHandler(object):
    def __init__(self, colors):
        super(MyHandler, self).__init__()
        self.N = len(colors)
        self.colors = colors
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patches = []
        contour = mpatches.Rectangle([x0, y0],
                                     width,
                                     height,
                                     facecolor='none',
                                     edgecolor='black',
                                     lw=1.,
                                     transform=handlebox.get_transform())
        handlebox.add_artist(contour)
        patches.append(contour)
        for ii, col in enumerate(self.colors):
            #edge = 'black' if col == (1., 1., 1., 1.) else col
            patch = mpatches.Rectangle([x0+1+ii*width/self.N, y0],
                                       (width-2)/self.N,
                                       height-1,
                                       facecolor=col,
                                       edgecolor='none',
                                       lw=0,
                                       transform=handlebox.get_transform())
            handlebox.add_artist(patch)
            patches.append(patch)
        return patches
