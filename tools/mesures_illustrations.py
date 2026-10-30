"""Calcule les mesures des illustrations de assets/ et écrit la constante GEOM utilisée par les pages
des versions 2 à 4 (versions/v2-illustrations, v3-fluide, v4-concept-1).

Pourquoi : la page ne doit JAMAIS lire les pixels des images dans le navigateur (Safari sur iPhone peut
les brouiller ou les bloquer, ce qui décale les filaments et les lueurs des méduses). Les mesures sont donc
calculées ici, une fois, puis collées dans la page.

Pour chaque image : emprise visible (alpha > 10, marge de 2 px) ; pour les ombrelles : contour du bord
inférieur sur 41 colonnes (point le plus bas dont l'alpha dépasse 40, fenêtre de +-4 px), en pixels
d'origine, relatif au pivot du manifeste.

Usage, depuis la racine du dépôt (Pillow et numpy requis) :  python3 tools/mesures_illustrations.py > geom.js
Coller ensuite le résultat à la place de la ligne « const GEOM = {...}; » des pages.
"""
import json
import numpy as np
from PIL import Image

N = 41
manifeste = {a['name']: a for a in json.load(open('assets/manifest.json', encoding='utf-8'))['assets']}
geom = {}
for nom in sorted(n for n, a in manifeste.items() if not a.get('fullFrame') and not n.startswith('meduse-tentacule')):
    a = np.array(Image.open('assets/' + manifeste[nom]['png']).convert('RGBA').getchannel('A'))
    H, W = a.shape
    py = manifeste[nom]['pivot'][1]
    ys, xs = np.where(a > 10)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1
    g = {'bb': [max(0, x0 - 2), max(0, y0 - 2), min(W, x1 + 2), min(H, y1 + 2)]}
    if '-ombrelle-0' in nom:
        rim = []
        for i in range(N):
            xc = int(round(x0 + (x1 - 1 - x0) * i / (N - 1)))
            col = a[:, max(0, xc - 4):xc + 5]
            bas = -1
            for y in range(H - 1, -1, -1):
                if (col[y] > 40).any():
                    bas = y
                    break
            rim.append(int(bas + 1 - py))
        g['rim'] = rim
        g['rx0'] = x0
        g['rw'] = x1 - x0
    geom[nom] = g
print('const GEOM = ' + json.dumps(geom, separators=(',', ':')) + ';')
