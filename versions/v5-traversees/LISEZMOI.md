# Lumora, version 5 (traversées dans toutes les directions)

Cette version part de la **version 4** (conservée telle quelle dans `versions/v4-concept-1/`, c'est la sauvegarde) et change la façon dont les créatures arrivent et se déplacent.

**Méduses**
- Il y en a autant que de minutes choisies (au plus 30). Elles arrivent peu à peu pendant les 30 premières secondes, la première dans la seconde qui suit le départ.
- Elles ne viennent plus seulement du bas : chaque traversée a une direction au hasard (vers le haut, de gauche à droite, de droite à gauche, en diagonale). Elles entrent par un bord de l'écran, le traversent, sortent par un autre bord puis reviennent par un autre côté, avec une nouvelle direction.
- Chaque minute, une seule s'en va pour de bon, et la dernière sort à zéro.

**Papillons**
- Même principe : autant que de minutes (au plus 30), arrivée étalée sur les 30 premières secondes.
- Chaque passage entre par un bord au hasard (gauche, droite, bas ou haut) et sort par un autre : de côté, en diagonale, vers le haut ou vers le bas. Un papillon sur dix environ s'éloigne au loin, vers l'horizon.
- Ils se posent toujours sur les marguerites (deux au plus à la fois), sans jamais se chevaucher.

Cette page charge les images de `../../assets/` et les sons de `../../audio/` : il faut la servir depuis la racine du dépôt (`python3 -m http.server 8000`).

**Grands écrans (tableau blanc interactif)**
- Les boutons et les textes s'agrandissent avec l'écran (jusqu'à 2,6 fois) pour rester lisibles de loin et faciles à toucher.
- Sur un écran très grand (4K), le dessin est limité à environ 4 millions de points pour rester fluide, puis étiré à l'écran.
- Vérifié à 1280×1024 (format 5:4), 1600×1200, 1920×1080 et 3840×2160, avec des appuis tactiles : choix des réglages, démarrage, barre de commandes.
