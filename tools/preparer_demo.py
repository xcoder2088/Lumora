"""Prépare une version du dossier versions/ pour une page de démonstration à un seul dossier.

Usage : python3 tools/preparer_demo.py versions/v4-concept-1 sortie/

Copie la page (sans l'en-tête de document, que la plateforme de démonstration ajoute elle-même),
remplace les chemins ../../assets/ et ../../audio/ par assets/ et audio/, et copie les images (WebP)
et les sons utilisés à côté. Les versions 2 à 4 chargent leurs images et leurs sons depuis ../../.
"""
import os, re, shutil, sys
src, out = sys.argv[1], sys.argv[2]
html = open(os.path.join(src, 'index.html'), encoding='utf-8').read()
html = html.replace('../../assets/', 'assets/').replace('../../audio/', 'audio/')
html = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta charset="utf-8">\s*<meta name="viewport"[^>]*>\s*', '', html)
html = html.replace('</head>\n<body>\n', '').replace('\n</body>\n</html>\n', '\n')
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
for d in ('audio', 'assets'):
    if os.path.isdir(d):
        for root, _, files in os.walk(d):
            for f in files:
                if d == 'assets' and not (f.endswith('.webp') or f == 'manifest.json'):
                    continue
                dst = os.path.join(out, root); os.makedirs(dst, exist_ok=True)
                shutil.copy(os.path.join(root, f), os.path.join(dst, f))
print('page de démonstration prête dans', out)
