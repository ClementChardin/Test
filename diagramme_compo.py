import selection as s
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from ui import couleurs

def diagramme_etoile_compo(compo,
                           N_points_cercles=100,
                           fatigue=True,
                           texte=True,
                           ax=None,
                           compo2=None,
                           nom_1=None,
                           nom_2=None,
                           qcolor_1=None):

    caracs_a_ploter = 'M OplusAV OplusAR OmoinsAV OmoinsAR ME R TO_def PA A JP E'.split(' ')
    labels = 'M O+AV O+AR O-AV O-AR ME R TO_def PA A JP E'.split(' ')

    dd = dict()
    for car in caracs_a_ploter:
        dd[car] = 0
        somme_coeffs = 0
        for num, jj in compo.joueurs.items():
            if num in s.coeffs_compo_old[car].keys():
                caracs_jj = s.get_caracs(jj, fatigue)
                dd[car] = dd[car] + s.coeffs_compo_old[car][num] * caracs_jj[s.correspondance[car]]
                somme_coeffs += s.coeffs_compo_old[car][num]
        if not somme_coeffs == 0:
            dd[car] = dd[car]*1. / somme_coeffs

    for rol in ('SA_pcp1', 'SA_pcp2', 'SA_scd', 'SA_remp1', 'SA_remp2'):
        SA_pcp1 = compo.roles['SA_pcp1']
        SA_pcp2 = compo.roles['SA_pcp2']
        SA_scd = compo.roles['SA_scd']
        SA_remp1 = compo.roles['SA_remp1']
        SA_remp2 = compo.roles['SA_remp2']
        dd['TO_def'] = 4* s.get_caracs(SA_pcp1, fatigue)['TO'] + \
                       4* s.get_caracs(SA_pcp2, fatigue)['TO'] + \
                       3.5* s.get_caracs(SA_scd, fatigue)['TO'] + \
                       2* s.get_caracs(SA_remp1, fatigue)['TO'] + \
                       2* s.get_caracs(SA_remp2, fatigue)['TO']
        dd['TO_def'] = dd['TO_def'] / (4 + 4 + 3.5 + 2 + 2)

    car_max = max(dd.values())
    xx = []
    yy = []
    for ii, car in enumerate(caracs_a_ploter):
        angle = 2*ii*np.pi/len(caracs_a_ploter)
        x = dd[car]*np.cos(angle)
        xx.append(x)
        y = dd[car]*np.sin(angle)
        yy.append(y)
        ax.plot([0, (car_max+1)*np.cos(angle)],
                 [0, (car_max+1)*np.sin(angle)],
                 linestyle='--',
                 color='k')
        if texte:
            ax.text(15*np.cos(angle),
                     15*np.sin(angle),
                     labels[ii])

    xx.append(dd[caracs_a_ploter[0]])
    yy.append(0)

    points = [(xx[ii], yy[ii]) for ii in range(len(xx))]

    codes = [Path.MOVETO] + [Path.LINETO]*(len(points)-2) + [Path.CLOSEPOLY]

    qcolor = couleurs.couleurs_equipes[nom_1]
    if qcolor == qcolor_1:
        qcolor = couleurs.couleurs_equipes[nom_1+'2']
    RGB = qcolor.getRgb()
    rgb = (RGB[0]/255., RGB[1]/255., RGB[2]/255., .5)

    path = Path(points, codes)
    patch = patches.PathPatch(path, facecolor=rgb)#, lw=2)

    if ax is None:
        ax = plt.gca()
    ax.add_patch(patch)
    #ax.plot(xx, yy)#, label=self.nom) 
    ax.legend()

    for i in range(1, 15):
        cercle_x = []
        cercle_y = []
        for k in range(N_points_cercles+1):
            cercle_x.append(i*np.cos(2*k*np.pi/N_points_cercles))
            cercle_y.append(i*np.sin(2*k*np.pi/N_points_cercles))
        if i%5 ==0:
            ax.plot(cercle_x, cercle_y, color='k')
        else:
            ax.plot(cercle_x, cercle_y, color='k', linestyle='--')

    if not compo2 is None:
        diagramme_etoile_compo(compo2,
                               N_points_cercles=N_points_cercles,
                               fatigue=fatigue,
                               texte=False,
                               ax=ax,
                               compo2=None,
                               nom_1=nom_2,
                               nom_2=None,
                               qcolor_1=qcolor)

    #ax.setxlim(-18, 18)
    #ax.setylim(-18, 18)
