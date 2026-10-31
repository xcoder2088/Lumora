# Ouverture animée de Lumora

L'introduction est intégrée directement à `index.html` : sur un fond uni bleu nuit, une petite luciole trace le nom « Lumora » en écriture cursive lumineuse. Elle s'écarte doucement, puis l'écran se fond vers les options du minuteur. L'éducateur choisit ensuite son décor, sa durée et son son, et démarre lui-même l'activité.

## Comportement

- Environ **5,6 secondes**, transition comprise, à chaque ouverture complète de la page.
- **Passer l’animation** ou **Échap** donne directement accès aux options. La tabulation reste dans l'accueil tant qu'il est visible, puis le focus revient au titre des réglages.
- Si la réduction des mouvements est activée, les options apparaissent directement. L'activer pendant l'introduction interrompt aussi l'animation.
- Aucun son ni minuteur n'est lancé par l'introduction. Le retour aux réglages après une activité ne rejoue pas l'accueil.
- Un délai de sécurité rend l'application accessible même si l'animation ne se termine pas normalement. Une erreur de géométrie SVG permet également de passer directement aux réglages.

## Réalisation

Un tracé SVG original sert à la fois à l'écriture et au parcours de la luciole : la lumière reste à la pointe du trait. Les ailes sont animées par CSS. L'introduction n'ajoute aucune police, bibliothèque, vidéo ni image à télécharger. Les éléments du minuteur sont temporairement `inert` et masqués; sa boucle de dessin attend la fin de l'accueil.

Les durées se règlent dans le script de l'accueil (`delay`, `duration`, puis le départ de la luciole); le fondu est défini par `#welcome` en CSS. Le dessin des lettres est dans le chemin SVG `#welcomeWriting`.

Les versions archivées dans `versions/`, les sons et les illustrations existantes ne sont pas modifiés.

## Aperçus et vérification

- [Accueil sur ordinateur](apercu.png)
- [Accueil au format téléphone](apercu-mobile.png)
- [Compte rendu des contrôles](verification.json)

Vérifié dans Chromium, sur un affichage de 1440 × 900 et un viewport tactile de 390 × 844 : fin automatique, déplacement de la luciole, bouton Passer, Échap, gestion du focus, réduction des mouvements (y compris activée en cours d'animation), repli si la géométrie SVG est indisponible. Après l'accueil, un essai de 30 secondes peut démarrer, être mis en pause puis revenir aux réglages. Aucune erreur JavaScript non interceptée pendant ces contrôles. Aucun essai sur un appareil iOS physique n'est revendiqué.
