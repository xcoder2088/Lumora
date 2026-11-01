#!/usr/bin/env python3
"""Dessine les icônes de l'application (icons/*.png) : le mot « Lumora » écrit à la main, avec le papillon posé sur le L.

Usage (depuis la racine du dépôt) :  python3 tools/make_icons.py     (nécessite Pillow)
Le tracé est celui de l'accueil, lu directement dans index.html.
"""
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

racine = Path(__file__).resolve().parent.parent
html = (racine / "index.html").read_text(encoding="utf-8")
d = re.search(r'<path id="welcomeWriting" d="([^"]+)"', html).group(1)

def cubic(p0, p1, p2, p3, n=24):
    return [((1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t*t*p2[0] + t**3*p3[0],
             (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t*t*p2[1] + t**3*p3[1]) for t in [i/n for i in range(n+1)]]

def lire_trace(d):
    jet = d.replace(",", " ").split()
    pts, cur, i = [], None, 0
    while i < len(jet):
        c = jet[i]
        if c == "M": cur = (float(jet[i+1]), float(jet[i+2])); pts.append(cur); i += 3
        elif c == "L": cur = (float(jet[i+1]), float(jet[i+2])); pts.append(cur); i += 3
        elif c == "C":
            q = [(float(jet[i+1+2*k]), float(jet[i+2+2*k])) for k in range(3)]
            pts += cubic(cur, q[0], q[1], q[2])[1:]; cur = q[2]; i += 7
        else: raise SystemExit("commande inconnue : " + c)
    return pts

trace = lire_trace(d)
haut = min(trace[:len(trace)//2], key=lambda p: p[1])          # le point le plus haut du L

AILE_HAUT = [((0, -0.08), (0.3, -0.8), (1.0, -0.95), (1.1, -0.5)), ((1.1, -0.5), (1.15, -0.12), (0.6, 0.04), (0, 0.04))]
AILE_BAS = [((0, 0.04), (0.6, 0.04), (0.95, 0.2), (0.82, 0.6)), ((0.82, 0.6), (0.7, 0.9), (0.25, 0.72), (0, 0.26))]
def contour(segs): return [p for s in segs for p in cubic(*s)]

def dessiner(taille, marge):
    S = 4 * taille
    fond = Image.new("RGB", (S, S), (4, 16, 26))
    halo = Image.new("RGB", (S, S), (0, 0, 0)); hd = ImageDraw.Draw(halo)
    hd.ellipse([S*0.18, S*0.2, S*0.82, S*0.8], fill=(18, 44, 60))
    fond = Image.blend(fond, halo.filter(ImageFilter.GaussianBlur(S*0.12)), 0.8)
    # trace du mot : boîte 40..550 x 20..210 (mêmes unités que l'accueil), centrée dans le carré
    largeur = S * (1 - 2*marge)
    k = largeur / 510
    xs = [q[0] for q in trace]
    ox = S / 2 - (min(xs) + max(xs)) / 2 * k      # le mot est centré sur sa largeur réelle
    oy = S * 0.56 - 115*k
    P = lambda p: (ox + p[0]*k, oy + p[1]*k)
    couche = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(couche)
    pts = [P(p) for p in trace]
    cd.line(pts, fill=(230, 223, 184, 255), width=max(2, int(4.2*k)), joint="curve")
    for p in (pts[0], pts[-1]):
        r = 2.1*k; cd.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=(230, 223, 184, 255))
    lueur = couche.filter(ImageFilter.GaussianBlur(5*k)); lueur.putalpha(lueur.getchannel("A").point(lambda a: min(255, a*2)))
    fond.paste(lueur, (0, 0), lueur); fond.paste(couche, (0, 0), couche)
    # papillon posé sur le haut du L
    cx, cy = P(haut); sz = 46*k; cy -= sz*0.18
    pap = Image.new("RGBA", (S, S), (0, 0, 0, 0)); pd = ImageDraw.Draw(pap)
    def aile(segs, couleur, sens):
        pd.polygon([(cx + sens*x*sz, cy + y*sz) for x, y in contour(segs)], fill=couleur, outline=(58, 90, 138, 140))
    for sens in (-1, 1):
        aile(AILE_HAUT, (143, 187, 230, 255), sens); aile(AILE_BAS, (110, 152, 200, 255), sens)
    pd.ellipse([cx-0.055*sz, cy-0.37*sz, cx+0.055*sz, cy+0.47*sz], fill=(39, 50, 77, 255))
    fond.paste(pap, (0, 0), pap)
    return fond.resize((taille, taille), Image.LANCZOS)

sortie = racine / "icons"
sortie.mkdir(exist_ok=True)
dessiner(192, 0.10).save(sortie / "icon-192.png")
dessiner(512, 0.10).save(sortie / "icon-512.png")
dessiner(512, 0.20).save(sortie / "icon-maskable-512.png")   # marge élargie : la zone « sûre » des icônes adaptatives
dessiner(180, 0.12).save(sortie / "apple-touch-icon.png")
print("icônes écrites dans", sortie)
