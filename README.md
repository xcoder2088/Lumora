# Lumora

Minuteur visuel et relaxant pour les moments de calme et de sieste, pensé pour les éducateurs et les éducatrices en milieu de garde.

Au lieu d'un compte à rebours qui sonne, des créatures montent doucement à travers l'écran : des méduses dans l'eau profonde, ou des papillons dans une prairie au crépuscule. La dernière sort de l'écran au moment exact où le temps tombe à zéro. Aucune alarme : la scène s'éclaircit lentement et un message doux apparaît.

C'est une page web unique, sans bibliothèque externe ni compte, qui fonctionne dans un navigateur sur ordinateur, tablette ou téléphone.

> État : premier prototype, en cours de validation auprès d'éducateurs.

## Fonctionnement

- **Décor :** méduses (mer) ou papillons (nuit à la campagne).
- **Durée :** 5, 10, 15, 20, 30 ou 45 minutes, plus un essai de 30 secondes.
- **Rythme :** vitesse à laquelle les créatures traversent l'écran (très calme, calme, vif).
- **Créatures à l'écran :** combien sont visibles en même temps. Elles arrivent en continu jusqu'à la fin du temps.
- **Son (désactivé par défaut) :** ambiance enregistrée du décor, en boucle, et un carillon final. Le bouton « Tester le son » joue un aperçu.
- **Pendant le minuteur :** les contrôles (pause, recommencer, temps restant, son, plein écran, réglages) s'effacent après 3,5 secondes sans toucher. Un toucher ou un mouvement de souris les ramène. La barre d'espace met en pause. L'écran reste allumé.
- **Décors :**
  - Méduses : petites, moyennes et grandes, et de temps en temps une méduse géante qui traverse l'écran d'un côté à l'autre.
  - Papillons inspirés d'espèces réelles : monarque, morpho bleu, azuré commun, machaon, papillon de lune. Quelques lucioles discrètes s'allument de temps en temps, en vert, jaune-vert ou jaune.
- **Fin du temps :** la scène s'éclaircit lentement, sans alarme. Un carillon doux est joué si le son est activé.

Les créatures et les décors sont dessinés par le code (canvas 2D), donc la page est légère et rien ne se répète exactement. Les réglages sont mémorisés dans le navigateur.

## Lancer le projet

Le son est chargé depuis le dossier `audio/` : la page doit donc être servie par un serveur web. Ouvrir `index.html` directement par double-clic montre les images, mais le navigateur bloque la lecture du son.

**Sur un ordinateur, avec Python :**

```bash
python3 -m http.server 8000
```

Puis ouvrir <http://localhost:8000>.

**En ligne, avec GitHub Pages (gratuit) :** dans le dépôt, aller dans *Settings*, puis *Pages*, choisir la branche `main` et le dossier `/ (root)`. La page est alors publiée à l'adresse `https://<compte>.github.io/Lumora/`.

## Structure

```
index.html         l'application complète (HTML, CSS et JavaScript)
audio/             les trois boucles sonores (MP3)
tools/             scripts utilisés pour préparer les sons (voir ci-dessous)
LICENSE            texte de la licence GNU GPL v3
```

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

## Licence

Le code est publié sous la licence **GNU General Public License v3.0** (voir `LICENSE`). Les sons sont dans le domaine public (CC0), voir ci-dessus.
