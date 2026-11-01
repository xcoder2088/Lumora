#!/usr/bin/env python3
"""Prépare le dossier « dist » : uniquement les fichiers nécessaires au site publié.

Usage (depuis la racine du dépôt) :  python3 tools/build_site.py
Cloudflare Pages l'exécute automatiquement (commande de build), puis publie le dossier dist.
Le dossier dist est recréé à chaque fois ; il ne faut jamais le modifier à la main.
"""
import json, shutil, sys
from pathlib import Path

racine = Path(__file__).resolve().parent.parent
dist = racine / "dist"
if dist.exists():
    shutil.rmtree(dist)
dist.mkdir()

# page, en-têtes HTTP et sons
shutil.copy2(racine / "index.html", dist / "index.html")
shutil.copy2(racine / "_headers", dist / "_headers")
# application installable : manifeste, service worker et icônes
for f in ("manifest.webmanifest", "sw.js", "favicon.ico"):
    shutil.copy2(racine / f, dist / f)
shutil.copytree(racine / "icons", dist / "icons")
shutil.copytree(racine / "audio", dist / "audio")
shutil.copytree(racine / "fonts", dist / "fonts")

# images : seulement le manifeste et les fichiers .webp qu'il cite (pas les .png, pas les aperçus)
manifeste = racine / "assets" / "manifest.json"
(dist / "assets").mkdir()
shutil.copy2(manifeste, dist / "assets" / "manifest.json")
donnees = json.loads(manifeste.read_text(encoding="utf-8"))

def webp_cites(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from webp_cites(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from webp_cites(v)
    elif isinstance(obj, str) and obj.lower().endswith(".webp"):
        yield obj

manquants = []
for chemin in sorted(set(webp_cites(donnees))):
    source = racine / "assets" / chemin
    if not source.is_file():
        manquants.append(chemin)
        continue
    cible = dist / "assets" / chemin
    cible.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, cible)

if manquants:
    print("ERREUR : fichiers cités dans le manifeste mais absents :", *manquants, sep="\n  ")
    sys.exit(1)

# liste des fichiers que l'application garde pour fonctionner sans réseau (lue par sw.js)
exclus = {"_headers", "sw.js", "precache.json", "index.html", "manifest.webmanifest", "favicon.ico"}
liste = sorted("./" + f.relative_to(dist).as_posix() for f in dist.rglob("*") if f.is_file() and f.relative_to(dist).as_posix() not in exclus and not f.relative_to(dist).as_posix().startswith("icons/"))
(dist / "precache.json").write_text(json.dumps(liste), encoding="utf-8")

octets = sum(f.stat().st_size for f in dist.rglob("*") if f.is_file())
nb = sum(1 for f in dist.rglob("*") if f.is_file())
print(f"Site prêt dans dist/ : {nb} fichiers, {octets/1e6:.1f} Mo")

