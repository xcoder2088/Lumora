# assets/ : illustrations de Lumora

Ce dossier reçoit les illustrations produites pour remplacer le dessin par le code. **Déposer les fichiers ici uniquement.**

## Règles

- **Ne rien modifier en dehors de `assets/`.** En particulier, ne pas toucher à `index.html`, `audio/`, `tools/` ni à `versions/v1-canvas/` (copie figée de la version 1, gardée comme référence).
- Un sous-dossier par thème : `meduses/`, `papillons/`, `decors/`.
- Une planche-contact `planche-contact.png` à la racine de `assets/` avec tous les éléments, pour validation d'un coup d'œil.
- Petits commits clairs, par exemple « Ajout des méduses : ombrelles et tentacules ». Faire un `git pull` avant d'envoyer.

## Format

- PNG 32 bits (RVB + alpha), sRGB, fond **vraiment transparent**, sans halo blanc ni frange sur les bords. Une version WebP en plus est un bonus.
- Ombrelles et ailes : environ 1024 px de large. Décors : 2560 x 1440 px.
- Poids visé : moins de 3 Mo par décor, 6 Mo au total pour tout.
- Noms clairs, en minuscules, sans accents ni espaces : `meduse-lune-ombrelle-01.png`, `papillon-monarque-aile-avant.png`, `decor-eau-profonde.png`.

## Ce qui est attendu

- **Méduses** (vue de côté, 3 types) : ombrelle seule en 4 à 6 états d'un cycle de pulsation, bras oraux, filament de tentacule étirable, calque de lueur interne. À fournir en **blanc ou gris neutre translucide, sans teinte**, car l'application change la couleur des méduses en temps réel.
- **Papillons** (vue de dessus, ailes ouvertes, 5 espèces : monarque, morpho bleu, azuré commun, machaon, papillon de lune) : aile avant gauche, aile arrière gauche (symétrisées par le code) et corps avec antennes, en fichiers séparés, aux couleurs naturelles de l'espèce.
- **Décors**, sans créatures : eau profonde avec rayons de lumière ; prairie au crépuscule en calques séparés (ciel, collines lointaines transparentes, herbes d'avant-plan transparentes).

## Style

Réaliste doux, translucide, lumineux. Pas de dessin animé, pas de contours noirs, pas de visages, pas de couleurs saturées ni de contrastes durs. Le but est d'apaiser.

## Licence

Créations originales, sans personnage ni œuvre protégée, utilisables dans un projet public sous licence GPL-3.0 (usage commercial permis). Idéal : CC0.
