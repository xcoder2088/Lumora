# Lumora

Minuteur visuel et relaxant pour les moments de calme et de sieste, pensé pour les éducateurs et les éducatrices en milieu de garde.

Au lieu d'un compte à rebours qui sonne, des créatures montent doucement à travers l'écran : des méduses dans l'eau profonde, ou des papillons dans une prairie au crépuscule. La dernière sort de l'écran au moment exact où le temps tombe à zéro. Aucune alarme : la scène s'éclaircit lentement et un message doux apparaît.

C'est une page web unique, sans bibliothèque externe ni compte, qui fonctionne dans un navigateur sur ordinateur, tablette ou téléphone.

> État : prototype (version 1, dessinée par le code), en cours de validation auprès d'éducateurs. Des illustrations plus réalistes sont en préparation (voir `assets/`).

## Fonctionnement

L'éducateur n'a que quatre choses à faire : choisir le **décor** (méduses ou papillons), la **durée** (5, 10, 15, 20, 30 ou 45 minutes, plus un essai de 30 secondes), activer ou non le **son**, puis appuyer sur « Commencer ». Tout le reste est automatique et change au fil du temps.

- **Quantité aléatoire :** le nombre de créatures à l'écran monte et descend par vagues lentes, tirées au hasard à chaque lancement. Les créatures arrivent en continu jusqu'à la fin du temps.
- **Méduses :** il y en a autant que de minutes choisies (5 minutes : 5 ; 30 minutes : 30), avec un maximum de 30. Elles montent sans cesse, sortent par le haut de l'écran et reviennent par le bas. Chaque minute, l'une d'elles ne revient pas : il y en a une de moins, et la dernière sort à zéro. Deux autres modes existent dans le code (`JELLY_MODE` : `'aquarium'` ou `'stream'`).
- **Profondeur :** au fond de l'eau, des algues illustrées sur trois plans (lointaines et pâles, intermédiaires, sombres au premier plan) ondulent doucement ; dans la prairie, de grands arbres, des bosquets lointains et des marguerites ondulent dans la brise (version 4). Les versions précédentes utilisent des algues dessinées par le code.
- **Papillons :** inspirés d'espèces réelles (monarque, morpho bleu, azuré commun, machaon, papillon de lune). Quelques lucioles discrètes s'allument de temps en temps, en vert, jaune-vert ou jaune.
- **Son (désactivé par défaut) :** ambiance enregistrée du décor, en boucle. Le bouton « Tester le son » joue un aperçu de l'ambiance, puis du carillon de fin.
- **Pendant le minuteur :** les contrôles (pause, recommencer, temps restant, son, plein écran, réglages) s'effacent après 3,5 secondes sans toucher. Un toucher ou un mouvement de souris les ramène. La barre d'espace met en pause. L'écran reste allumé.
- **Méduses :** elles traversent l'écran du bas vers le haut, de plus en plus rares au fil du temps (une douzaine au début, plus aucune à zéro). Un mode « aquarium » (elles restent dans l'écran et ne sortent qu'à la fin, une par minute) existe aussi dans le code : il suffit de mettre `JELLY_AQUARIUM = true`.
- **Papillons :** ils traversent l'écran de côté, s'éloignent au loin ou montent vers le ciel. De temps en temps, une étoile filante passe dans le ciel.
- **Fin du temps :** la dernière créature sort de l'écran à l'instant où le temps tombe à zéro. La scène s'éclaircit lentement, sans alarme. Un carillon très doux, une nappe de quelques notes graves, est joué si le son est activé.

Dans la version 1, les créatures et les décors sont dessinés par le code (canvas 2D), donc la page est légère et rien ne se répète exactement. Les choix de décor et de durée sont mémorisés dans le navigateur.

## Lancer le projet

Le son est chargé depuis le dossier `audio/` : la page doit donc être servie par un serveur web. Ouvrir `index.html` directement par double-clic montre les images, mais le navigateur bloque la lecture du son.

**Sur un ordinateur, avec Python :**

```bash
python3 -m http.server 8000
```

Puis ouvrir <http://localhost:8000>.

**En ligne, avec GitHub Pages (gratuit) :** dans le dépôt, aller dans *Settings*, puis *Pages*, choisir la branche `main` et le dossier `/ (root)`. La page est alors publiée à l'adresse `https://<compte>.github.io/Lumora/`.

## Structure et versions

```
index.html           la version courante de l'application (HTML, CSS et JavaScript)
audio/               les trois boucles sonores (MP3)
assets/              illustrations (méduses, papillons, décors), voir assets/LISEZMOI.md
versions/v1-canvas/  COPIE FIGÉE de la version 1, dessinée par le code. Ne pas modifier.
versions/v2-illustrations/  version 2 : le même fonctionnement, avec les illustrations de assets/
versions/v3-fluide/  version 3 : le mouvement de la version 1, avec les illustrations de assets/
versions/v4-concept-1/  version 4 : le concept de la version 1 (décor, couleurs, ambiance), avec les illustrations de assets/
tools/               scripts utilisés pour préparer les sons (voir ci-dessous)
LICENSE              licence : utilisation libre, modification sur autorisation
```

**La version 1 est conservée comme référence** dans le dossier `versions/v1-canvas/`. C'est une copie figée et autonome (elle a sa propre copie des sons) : on peut l'ouvrir et la comparer à tout moment avec les autres versions.

**La version 2** (`versions/v2-illustrations/`) a exactement le même fonctionnement que la version 1 (quantité aléatoire, mouvements, couleurs qui changent, lucioles, sons, fin du temps). Seul le dessin change : les méduses, les papillons et les décors sont les illustrations du dossier `assets/` au lieu d'être dessinés par le code. Elle utilise les images en WebP (environ 5 Mo) et les sons du dossier `audio/`.

**La version 3** (`versions/v3-fluide/`) reprend le mouvement et le rendu de la version 1, jugés plus fluides et plus apaisants, avec les illustrations : l'ombrelle des méduses est déformée en continu au lieu de passer d'une image à l'autre.

**La version 4** (`versions/v4-concept-1/`) reprend tout le concept de la version 1 (décor de l'eau, couleurs, mouvement) avec les détails des illustrations ; la prairie est assombrie à la tombée de la nuit, avec des herbes qui bougent dans le vent.

Pour comparer, servir le dépôt par un serveur web (voir « Lancer le projet »), puis ouvrir :

- `/versions/v1-canvas/` : version 1, dessinée par le code ;
- `/versions/v2-illustrations/` : version 2, avec les illustrations ;
- `/versions/v3-fluide/` : version 3, le mouvement de la version 1 avec les illustrations ;
- `/versions/v4-concept-1/` : version 4, le concept de la version 1 avec les illustrations.

## Sons et crédits

Les sons sont des enregistrements libres de droits (CC0 ou domaine public). Ils ont été rognés, filtrés, ajustés en volume et rendus bouclables sans coupure par les scripts du dossier `tools/`. Le carillon final est généré par le code (aucun fichier).

| Fichier | Utilisé pour | Source originale | Auteur |
|---|---|---|---|
| `audio/baleines1.mp3` | Méduses : chant de baleine bleue, très discret (une octave plus haut pour être audible sur un petit haut-parleur) | [Blue Whale West Pacific 1x](https://commons.wikimedia.org/wiki/File:Blue_Whale_West_Pacific_1x.oga), Wikimedia Commons (CC0) | NOAA |
| `audio/baleines2.mp3` | Méduses : second chant de baleine bleue, en boucle plus courte pour que la répétition ne se remarque pas | [Blue whale atlantic3 1x](https://commons.wikimedia.org/wiki/File:Blue_whale_atlantic3_1x.oga), Wikimedia Commons (CC0) | NOAA |
| `audio/profondeurs.mp3` | Méduses : ambiance sous-marine | [Aquaria](https://opengameart.org/content/aquaria), OpenGameArt | cynicmusic |
| `audio/nuit.mp3` | Papillons : grillons de nuit, très lointains, avec de longues pauses | [Campaign at Night #4](https://bigsoundbank.com/campagne-la-nuit-4-s1880.html), BigSoundBank | Joseph Sardin |
| `audio/brise.mp3` | Papillons : brise dans les arbres (fichier gardé, mais plus utilisé pour l’instant : le vent a été retiré) | [Wind in the Trees](https://bigsoundbank.com/forest-wind-in-the-trees-s0904.html), BigSoundBank | Joseph Sardin |
| `audio/musique-nuit.mp3` | Papillons : petite musique calme (fin retirée pour la boucle) | [Another August](https://opengameart.org/content/another-august), OpenGameArt | cynicmusic |

La licence CC0 n'exige aucune mention, elles sont citées par courtoisie.

### Refaire les boucles sonores

Les enregistrements d'origine ne sont pas dans le dépôt. Pour refaire les boucles :

1. Installer `ffmpeg`, Python 3 et `numpy`.
2. Télécharger les originaux : « Campaign at Night #4 » dans `snd_raw/crickets4.mp3`, « Wind in the Trees » dans `papillons_raw/vent_arbres.mp3`, « Another August » dans `papillons_raw/musique.mp3`, « Aquaria » dans `snd_raw/aquaria.mp3`, et les deux enregistrements de baleines bleues dans `whales_raw/bleue_ouest_pacifique.oga` et `whales_raw/bleue_atlantique3.oga`.
3. Depuis la racine du dépôt : `python3 tools/mkloops.py` (musique sous-marine), `python3 tools/crickets_soft.py` (grillons, avec leurs pauses), `python3 tools/whales_make.py` (baleines), `python3 tools/wind_music_make.py` (brise et musique de nuit).
4. `python3 tools/seam.py` vérifie que le raccord de chaque boucle est continu, et `python3 tools/analyze.py` mesure le volume et le contenu en fréquences des enregistrements d'origine.

## Limites connues

- Les sons n'ont été vérifiés que par des mesures, pas à l'oreille. Leur volume et leur caractère sont à valider.
- Pas encore de mode hors ligne (application installable) : la page demande une connexion pour charger les polices et le son la première fois.
- Les polices (Cormorant Garamond et Jost) sont chargées depuis Google Fonts. Pour une version entièrement locale, il faudra les inclure dans le dépôt.
- Testé sur Chromium. Le comportement sur iPhone et iPad (son avec le mode silencieux) n'a pas été vérifié sur un vrai appareil.

## Idées pour la suite

- Retour des éducateurs : durées, vitesse, volume, besoins non couverts.
- Remplacer les dessins par des illustrations plus réalistes (images à fond transparent animées par le code).
- Autres décors (forêt de lucioles, étoiles, poissons, flocons).
- Version installable hors ligne.
- Un enregistrement de cloche douce pour le carillon final.

## Licence et droits

**Droit d'auteur :** Copyright (c) 2026 Xcoder. Le texte complet est dans le fichier `LICENSE`.

**En bref :**

- **Tout le monde peut utiliser Lumora gratuitement** (à la maison, en garderie, à l'école, au travail) et **lire le code source**.
- **Pour le modifier, en copier des parties dans un autre projet, ou le redistribuer, il faut demander l'autorisation écrite de l'auteur.** Pour demander : ouvrir une « issue » sur ce dépôt.
- Le nom « Lumora » ne peut pas être utilisé pour un autre produit.

Cette licence est volontairement simple. Ce n'est pas une licence « open source » au sens strict (qui permettrait à tous de modifier sans demander) : c'est du **code source visible**, avec les droits de modification réservés à l'auteur.

**Sons.** Les trois enregistrements du dossier `audio/` sont dans le domaine public (CC0), voir « Sons et crédits ». Ils gardent leur propre statut.

**Illustrations.** Les images du dossier `assets/` suivent les mêmes conditions que le reste du projet, voir `assets/LICENCE.md`.

**Polices.** Cormorant Garamond et Jost sont publiées sous licence SIL Open Font License. Elles ne sont pas incluses dans le dépôt : la page les charge depuis Google Fonts.

**Aucune garantie.** Lumora est fourni « tel quel », sans garantie. C'est un outil d'ambiance : il **ne remplace en aucun cas la surveillance des enfants**.

**Vie privée.** Lumora ne demande aucun compte, ne collecte aucune donnée personnelle et n'utilise aucun suivi. Les seuls réglages mémorisés (décor et durée) restent dans le navigateur de l'appareil. Seule exception : le chargement des polices depuis Google Fonts transmet l'adresse IP du visiteur à Google. Pour s'en passer, il faudra inclure les polices dans le dépôt (prévu).

**Intelligence artificielle.** Une partie du code, du traitement des sons et des illustrations a été produite avec l'aide d'outils d'intelligence artificielle générative, sous la direction de l'auteur.
