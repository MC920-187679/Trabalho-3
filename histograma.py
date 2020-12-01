import sys, cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator

import seaborn as sns
sns.set_theme(context='paper', style='darkgrid', palette='muted', rc={
    # 'axes.spines.right': False,
    # 'axes.spines.top':   False,
    # 'axes.edgecolor':  '.4',
    # 'axes.labelcolor': '.0',
    # 'axes.titlesize': 'large',
    # 'axes.labelsize': 'medium',
    'figure.autolayout': True,
    'figure.figsize': (4, 2.5),
    'font.family': ['serif'],
    # 'font.size': 10.0,
    # 'grid.linestyle': '--',
    # 'legend.facecolor': '.9',
    # 'legend.frameon': True,
    # 'savefig.transparent': True,
    # 'text.color': '.0',
    # 'xtick.labelsize': 'small',
    # 'ytick.labelsize': 'small',
    'text.usetex': True,
    'pgf.preamble': r"""
        \usepackage[portuguese]{babel}
        \usepackage[T1]{fontenc}
        \usepackage[utf8]{inputenc}
    """,
    'pgf.rcfonts': False
})

try:
    [_, filename, output] = sys.argv
except ValueError:
    [_, filename] = sys.argv
    output = None

img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

sns.histplot(x=img.flat, bins=np.arange(256), fill=False, color='k')
plt.xlabel('Valor do Pixel')
plt.ylabel('Número de Pixels')
plt.gca().xaxis.set_major_locator(MultipleLocator(64))

if output is None:
    plt.show()
else:
    plt.savefig(output, bbox_inches='tight', pad_inches=0)
