# Lumora, version 3 (mouvement de la version 1, illustrations de la version 2)

Cette version garde **le mouvement et le rendu de la version 1**, qui paraissaient plus fluides et plus apaisants, et utilise **les illustrations** du dossier `assets/` à la place du dessin par le code.

Ce qui reprend la version 1 :
- l'ombrelle des méduses se resserre et s'allonge en continu à chaque pulsation (une seule illustration déformée, sans fondu entre images) ;
- les bras ondulent, les filaments lumineux sont accrochés au bord réel de l'ombrelle ;
- des méduses plus grandes et plus lumineuses, sur une eau plus profonde ;
- les mêmes comportements : quantité aléatoire, nage / sur-place / plané / rafale, courant partagé, couleurs qui changent, méduse géante, lucioles, sons, fin du temps.

Ce qui vient de la version 2 : les illustrations des méduses (trois types), des papillons (cinq espèces) et des décors (eau profonde, prairie en trois calques).

Cette page charge les images de `../../assets/` et les sons de `../../audio/` : il faut donc la servir depuis la racine du dépôt, par exemple :

```bash
python3 -m http.server 8000
```

puis ouvrir <http://localhost:8000/versions/v3-fluide/>.
