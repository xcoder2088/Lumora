# Lumora — notes de reprise du projet

Document pour reprendre le travail dans une nouvelle conversation sans rien perdre.

## But
Minuteur de sieste visuel et calme pour éducatrices en garderie. Autant de créatures que de minutes choisies (max 30). Une part à chaque minute, la dernière exactement à zéro. Pas d'alarme : la scène s'éclaircit et affiche « Doucement, c'est l'heure. ». Tout doit rester doux, naturel, sans mouvement brusque.
Deux scènes : méduses (eau profonde) ou papillons (prairie au crépuscule).

## Règles données par le propriétaire du projet
- Répondre en français simple, précis et complet, sans jargon, en supposant qu'il ne connaît rien. Recommander plutôt que multiplier les options.
- Aucun nom d'outil ou d'assistant d'IA dans le dépôt (fichiers, noms, commits, historique). Seule mention permise : « illustrations produites avec l'aide d'une intelligence artificielle ».
- Auteur des commits : Xcoder <103386958+xcoder2088@users.noreply.github.com>, sans co-auteur ni ligne de session.
- Ne jamais réécrire l'historique ni forcer un push sans accord explicite.
- Être honnête : on ne peut pas écouter le son ni tester sur un vrai iPhone / tableau blanc. Distinguer ce qui est mesuré de ce qui ne l'est pas.
- Licence personnalisée (usage libre ; modifier, copier ou redistribuer seulement avec autorisation écrite). Sons en CC0.
- Les illustrations sont produites par un autre outil d'IA qui pousse aussi sur le dépôt : toujours faire `git fetch origin main` avant de travailler et attendre qu'il ait fini.
- Publication : `git push origin HEAD:refs/heads/main`.

## Structure
- `versions/v5-traversees/index.html` : version actuelle (la plus à jour). Fichier unique, sans dépendance.
- `versions/v5-traversees/outils/makev5.py` : script qui a produit la v5 à partir de la v4 (voir « Reconstruire »).
- `versions/v4-concept-1/` : sauvegarde figée de la v4. Ne pas modifier.
- `versions/v1-canvas`, `v2-illustrations`, `v3-fluide` : anciennes versions, plus reconstruites.
- `index.html` (racine) : ancienne page de base, avec l'accueil animé et un seul halo. À remplacer par la v5 quand le propriétaire le décide.
- `assets/` : illustrations, décors, plantes, fleurs, sons.

## État actuel (commit 96e7458)
Méduses :
- Vol libre en boucle ; arrivée progressive sur 30 s, la première en moins de 5 s ; entrées par les côtés ou le bas, jamais par le haut.
- Types de passages tirés d'un sac mélangé : verticaux, obliques, horizontaux, légères descentes.
- La tête pointe dans le sens du mouvement ; rotation par ressort amorti (≈ 2°/s typique).
- Elles s'attendent au lieu de se cogner (priorité à celle qui sort).
Papillons :
- Ailes rigides en 3D, plusieurs espèces (peu de bleus, petits), arrivées par les côtés et le bas, sorties à des bords aléatoires.
- Ne se chevauchent jamais ; maximum 2 posés en même temps sur des marguerites ; ailes lentes posés, battements rapides au décollage.
Décor : plantes animées, arbres lointains seulement, petites marguerites proportionnelles.
Accueil : une luciole écrit « Lumora », un seul halo ensuite.
Grands écrans (tableau blanc 5 pi × 4 pi) : interface agrandie jusqu'à 2,6×, image limitée à ≈ 4,2 M de points. Testé en simulation (1280×1024, 1600×1200, 1920×1080, 3840×2160) : fonctionne, tactile OK.

## Reconstruire la v5
`makev5.py` lit une copie de la v4 (identique à `versions/v4-concept-1/index.html`) et applique des remplacements de texte précis ; chaque remplacement vérifie qu'il trouve exactement le texte attendu. Les chemins en tête du script pointent vers un dossier temporaire : les adapter. Plus simple en général : modifier directement `versions/v5-traversees/index.html`.

## Tests (Playwright, Node)
Serveur local : `python3 -m http.server 8771` depuis la racine du dépôt. Copie de test exposant l'état des créatures, à supprimer ensuite. La simulation sans carte graphique tourne à ≈ 0,5× : les images/seconde mesurées ne reflètent pas un vrai appareil.

## Pas encore vérifié
Vrai iPhone, vrai tableau blanc, son à l'oreille, fluidité réelle.

## Décisions en attente du propriétaire
1. Faire de la v5 la page principale (`index.html` racine) ?
2. Mettre à jour le texte d'introduction du panneau de départ (« Les créatures montent doucement… » n'est plus exact) ?
3. Retirer le nom d'outil d'un ancien message de commit de l'outil d'illustration (réécriture d'historique : seulement avec accord et si l'autre outil est inactif) ?
4. Retours attendus après essai sur le tableau blanc.

## Page de démonstration privée
Version 5 : la page de démonstration privée est dans la liste des pages publiées du propriétaire.
