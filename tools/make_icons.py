#!/usr/bin/env python3
"""Papillon seul, lisible en onglet et sur l'écran d'accueil.
Usage : python3 tools/make_icons.py (Pillow).
Même silhouette et palette que le papillon bleu de l'accueil, sans texte miniature.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, PngImagePlugin

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'icons'
OUT.mkdir(exist_ok=True)
BG = (4, 16, 26)
TOP = [((0,-.08),(.3,-.8),(1,-.95),(1.1,-.5)), ((1.1,-.5),(1.15,-.12),(.6,.04),(0,.04))]
BOTTOM = [((0,.04),(.6,.04),(.95,.2),(.82,.6)), ((.82,.6),(.7,.9),(.25,.72),(0,.26))]

def curve(a,b,c,d,n=48):
    return [((1-t)**3*a[0]+3*(1-t)**2*t*b[0]+3*(1-t)*t*t*c[0]+t**3*d[0],
             (1-t)**3*a[1]+3*(1-t)**2*t*b[1]+3*(1-t)*t*t*c[1]+t**3*d[1]) for t in (i/n for i in range(n+1))]

def render(size, maskable=False):
    n = size*4
    im = Image.new('RGB', (n,n), BG)
    halo = Image.new('RGBA', (n,n))
    ImageDraw.Draw(halo).ellipse((n*.19,n*.22,n*.81,n*.83), fill=(169,205,238,20))
    halo = halo.filter(ImageFilter.GaussianBlur(n*.10))
    im.paste(halo,(0,0),halo)
    draw = ImageDraw.Draw(im)
    scale = n*(148 if maskable else 180)/512
    cx,cy = n*.5,n*270/512
    def point(p,side=1): return (cx+side*p[0]*scale,cy+p[1]*scale)
    for side in (-1,1):
        for segments,color in ((TOP,(143,187,230)),(BOTTOM,(121,162,207))):
            draw.polygon([point(p,side) for s in segments for p in curve(*s)], fill=color)
        for a,b in (((.05,-.03),(.95,-.55)),((.05,0),(1,-.3)),((.05,.08),(.7,.5))):
            draw.line((point(a,side),point(b,side)),fill=(76,112,152),width=max(1,round(.012*scale)))
    draw.ellipse((cx-.06*scale,cy-.37*scale,cx+.06*scale,cy+.47*scale),fill=(39,50,77))
    for side in (-1,1):
        antenna=curve((.01,-.36),(.1,-.62),(.22,-.7),(.3,-.66))
        draw.line([point(p,side) for p in antenna],fill=(116,142,174),width=max(1,round(.022*scale)))
    return im.resize((size,size),Image.Resampling.LANCZOS)

metadata=PngImagePlugin.PngInfo()
metadata.add(b'sRGB',b'\x00')
for name,size,maskable in (('favicon-16.png',16,False),('favicon-32.png',32,False),('icon-192.png',192,False),('icon-512.png',512,False),('icon-maskable-512.png',512,True),('apple-touch-icon.png',180,False)):
    render(size,maskable).save(OUT/name,pnginfo=metadata,optimize=True)
render(512).save(ROOT/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64)])

svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-labelledby="title">
<title id="title">Papillon bleu — Lumora</title>
<defs><radialGradient id="halo"><stop stop-color="#a9cdee" stop-opacity=".10"/><stop offset="1" stop-color="#a9cdee" stop-opacity="0"/></radialGradient>
<g id="wings"><path d="M0 -.08 C.3 -.8 1 -.95 1.1 -.5 C1.15 -.12 .6 .04 0 .04 Z" fill="#8fbbe6"/>
<path d="M0 .04 C.6 .04 .95 .2 .82 .6 C.7 .9 .25 .72 0 .26 Z" fill="#79a2cf"/>
<path d="M.05 -.03 L.95 -.55 M.05 0 L1 -.3 M.05 .08 L.7 .5" fill="none" stroke="#4c7098" stroke-width=".012"/></g></defs>
<path d="M0 0h512v512H0z" fill="#04101a"/>
<g transform="translate(256 270) scale(180)"><circle r="1.4" fill="url(#halo)"/><use href="#wings"/><use href="#wings" transform="scale(-1 1)"/>
<ellipse cy=".05" rx=".06" ry=".42" fill="#27324d"/>
<path d="M-.01 -.36 C-.1 -.62 -.22 -.7 -.3 -.66 M.01 -.36 C.1 -.62 .22 -.7 .3 -.66" fill="none" stroke="#748eae" stroke-width=".022" stroke-linecap="round"/></g></svg>
'''
(OUT/'icon.svg').write_text(svg,encoding='utf-8')
print('Icônes papillon : SVG, ICO et six tailles PNG générés.')

