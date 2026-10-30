# Lumora, version 2 (avec illustrations)

Même fonctionnement que la version 1 : quantité de créatures aléatoire, mouvements variés, couleurs des méduses qui changent pendant leur trajet, lucioles, sons, fin du temps. La différence : les méduses, les papillons et les décors sont des **illustrations** (dossier `assets/`) au lieu d'être dessinés par le code.

- Méduses : trois types d'ombrelle (lune, haute, fantomatique) en gris translucide, teintées par le code, avec leurs bras oraux et leur lueur interne.
- Papillons : cinq espèces (monarque, morpho bleu, azuré commun, machaon, papillon de lune), ailes séparées pour le battement.
- Décors : eau profonde ; prairie en trois calques (ciel, collines, herbes).

Cette page charge les images de `../../assets/` et les sons de `../../audio/` : il faut donc la servir depuis la racine du dépôt, par exemple :

```bash
python3 -m http.server 8000
```

puis ouvrir <http://localhost:8000/versions/v2-illustrations/>.
