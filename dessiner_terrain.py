from matplotlib.pyplot import *
import matplotlib.patches as mp
from matplotlib.collections import PatchCollection

def dessiner_terrain(ax=None):
    if ax is None:
        ax = subplot(111)

    r = mp.Rectangle((0, -50), 60, 60, fill=True, facecolor='g')
    pc = PatchCollection([r], facecolor='g')
    ax.add_collection(pc)

    axhline(-50, color='w', linewidth=2)
    axhline(-40, color='w', linestyle='--', linewidth=2)
    axhline(-28, color='w', linewidth=2)
    axhline(-5, color='w', linestyle='--', linewidth=2)
    axhline(0, color='w', linewidth=2)
    axhline(10, color='w', linewidth=2)

    axvline(0, color='w', linewidth=2)
    axvline(5, color='w', linestyle='--',linewidth=2)
    axvline(15, color='w', linestyle='--',linewidth=2)
    axvline(45, color='w', linestyle='--',linewidth=2)
    axvline(55, color='w', linestyle='--',linewidth=2)
    axvline(60, color='w', linewidth=2)

    plot([27.35, 26], [0, 6], 'w', linewidth=2)
    plot([32.65, 34], [0, 6], 'w', linewidth=2
    plot([27.65-2.5*tan(1.65/6), 32.65+2.5*tan(1.65/6)], [2.5, 2.5], 'w', linewidth=2)

    axis('equal')
    axis('off')
    tight_layout()
    

