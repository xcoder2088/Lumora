# Lumora

Minuteur visuel et relaxant pour les moments de calme et de sieste, pensé pour les éducateurs et les éducatrices en milieu de garde.

Au lieu d'un compte à rebours qui sonne, des créatures montent doucement à travers l'écran : des méduses dans l'eau profonde, ou des papillons dans une prairie au crépuscule. La dernière sort de l'écran au moment exact où le temps tombe à zéro. Aucune alarme : la scène s'éclaircit lentement et un message doux apparaît.

C'est une page web unique, sans bibliothèque externe ni compte, qui fonctionne dans un navigateur sur ordinateur, tablette ou téléphone.

> État : prototype (version 1, dessinée par le code), en cours de validation auprès d'éducateurs. Des illustrations plus réalistes sont en préparation (voir `assets/`).

## Fonctionnement

L'éducateur n'a que quatre choses à faire : choisir le **décor** (méduses ou papillons), la **durée** (5, 10, 15, 20, 30 ou 45 minutes, plus un essai de 30 secondes), activer ou non le **son**, puis appuyer sur « Commencer ». Tout le reste est automatique et change au fil du temps.

- **Quantité aléatoire :** le nombre de créatures à l'écran monte et descend par vagues lentes, tirées au hasard à chaque lancement. Les créatures arrivent en continu jusqu'à la fin du temps.
- **Méduses :** petites, moyennes et grandes, plus de temps en temps une méduse géante qui traverse l'écran d'un côté à l'autre. Chacune change d'allure (nage régulière, sur place, plané, rafale), s'incline, suit un courant partagé et change de couleur pendant son trajet (bleu, puis mauve, parfois blanc). Le fond de l'eau dérive aussi lentement d'une teinte à l'autre.
- **Papillons :** inspirés d'espèces réelles (monarque, morpho bleu, azuré commun, machaon, papillon de lune). Quelques lucioles discrètes s'allument de temps en temps, en vert, jaune-vert ou jaune.
- **Son (désactivé par défaut) :** ambiance enregistrée du décor, en boucle. Le bouton « Tester le son » joue un aperçu de l'ambiance, puis du carillon de fin.
- **Pendant le minuteur :** les contrôles (pause, recommencer, temps restant, son, plein écran, réglages) s'effacent après 3,5 secondes sans toucher. Un toucher ou un mouvement de souris les ramène. La barre d'espace met en pause. L'écran reste allumé.
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
tools/               scripts utilisés pour préparer les sons (voir ci-dessous)
LICENSE              licence : utilisation libre, modification sur autorisation
```

**La version 1 est conservée comme référence** dans le dossier `versions/v1-canvas/`. C'est une copie figée et autonome (elle a sa propre copie des sons) : on peut l'ouvrir et la comparer à tout moment avec les autres versions.

**La version 2** (`versions/v2-illustrations/`) a exactement le même fonctionnement que la version 1 (quantité aléatoire, mouvements, couleurs qui changent, lucioles, sons, fin du temps). Seul le dessin change : les méduses, les papillons et les décors sont les illustrations du dossier `assets/` au lieu d'être dessinés par le code. Elle utilise les images en WebP (environ 5 Mo) et les sons du dossier `audio/`.

Pour comparer, servir le dépôt par un serveur web (voir « Lancer le projet »), puis ouvrir :

- `/versions/v1-canvas/` : version 1, dessinée par le code ;
- `/versions/v2-illustrations/` : version 2, avec les illustrations.

## Sons et crédits

Les trois sons sont des enregistrements libres de droits (CC0, domaine public). Ils ont été rognés, filtrés, ajustés en volume et rendus bouclables sans coupure par les scripts du dossier `tools/`.

| Fichier | Utilisé pour | Source originale | Auteur |
|---|---|---|---|
| `audio/mer.mp3` | Méduses : vagues douces (très adoucies : aigus retirés, pics lissés) | [Small Waves Facing the Ocean](https://bigsoundbank.com/small-waves-facing-the-ocean-s1046.html), BigSoundBank | Joseph Sardin |
| `audio/profondeurs.mp3` | Méduses : ambiance sous-marine, mélangée aux vagues | [Aquaria](https://opengameart.org/content/aquaria), OpenGameArt | cynicmusic |
| `audio/nuit.mp3` | Papillons : grillons de nuit (volume bas, aigus retirés) | [Campaign at Night #4](https://bigsoundbank.com/campagne-la-nuit-4-s1880.html), BigSoundBank | Joseph Sardin |

La licence CC0 n'exige aucune mention, elles sont citées par courtoisie. Le carillon final est généré par le code (aucun fichier).

### Refaire les boucles sonores

Les enregistrements d'origine ne sont pas dans le dépôt (plusieurs dizaines de Mo). Pour refaire les boucles :

1. Installer `ffmpeg`, Python 3 et `numpy`.
2. Télécharger les trois fichiers MP3 d'origine dans un dossier `snd_raw/` en les nommant `crickets4.mp3`, `waves.mp3` et `aquaria.mp3`.
3. Lancer dans cet ordre (le dossier `audio/` existe déjà, ses fichiers sont remplacés) : `python3 tools/mkloops.py`, `python3 tools/soften.py` (remplace `mer.mp3` par la version adoucie), `python3 tools/softcrickets.py` (remplace `nuit.mp3` par la version sobre).
4. `python3 tools/seam.py` vérifie que le raccord de chaque boucle est continu, et `python3 tools/analyze.py` mesure le volume et le contenu en fréquences des enregistrements d'origine.

Les scripts doivent être lancés depuis la racine du dépôt.

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
