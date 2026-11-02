# Lumora — notes de reprise du projet

## REPRISE RAPIDE (état au 2 novembre 2026 : version 5.19 en ligne ; voir aussi les sections 5.17 et 5.18 plus bas)
**À lire en premier.** Les sections plus bas sont l'historique ; si elles se contredisent, ce qui est ici et dans les sections « Version 5.x » les plus récentes fait foi.

**Où c'est** : https://lumora.pixeldrop.ca (même serveur Oracle que PixelDrop, tunnel Cloudflare existant, petit serveur local `deploy/lumora-server.py` sur 127.0.0.1:8791, service `lumora-web`). Dépôt : github.com/xcoder2088/Lumora (branche `main`). Dossier local : `~/Desktop/lumora`.

**Façon de travailler (demandée par le propriétaire, à garder)**
1. Une branche par version (`version-5.17`…), commits signés `Xcoder <103386958+xcoder2088@users.noreply.github.com>`, sans co-auteur, sans aucun nom d'outil ou d'assistant dans le dépôt.
2. Numéro de version à changer à DEUX endroits à chaque révision : `ver x.y` (élément `#ver` de `index.html`) et `VERSION` dans `sw.js`. Après modification : recopier `index.html` vers `versions/v5-traversees/index.html` en remplaçant `./assets/` et `./audio/` par `../../assets/` et `../../audio/`.
3. Toujours donner d'abord un LIEN D'ESSAI, sans toucher à la vraie page : copie de `index.html` déposée dans `/var/www/lumora/essai/index.html` du serveur (chemins `../assets/`, `../audio/`, liens d'icônes en `../`, enregistrement du service worker retiré, `noindex`, version affichée « · essai »). Lien : https://lumora.pixeldrop.ca/essai/ . Il disparaît au prochain déploiement.
4. Publier seulement sur demande explicite : fusionner la branche dans `main` (`git fetch` avant : un autre outil d'illustration pousse parfois sur le dépôt), `git push origin HEAD:refs/heads/main`, puis sur le serveur `cd ~/lumora && git pull && bash deploy/installer-sur-serveur.sh`, puis vérifier la page, `sw.js`, le manifeste, une icône, un son et que https://pixeldrop.ca répond (ne jamais toucher au service PixelDrop).
5. Accès serveur : par SSH, avec la clé du serveur de PixelDrop (la commande habituelle est dans `deploy.sh` du dépôt PixelDrop et dans `~/.ssh/config` de l'ordinateur du propriétaire). Les adresses et chemins de clés ne sont volontairement pas écrits ici (dépôt public). On a décidé de garder Lumora sur le serveur de PixelDrop plutôt que sur celui de QuickQuoteTool/QuickProof.
6. Réponses au propriétaire : français simple, sans jargon, honnête sur ce qui est mesuré et ce qui ne l'est pas (jamais testé sur un vrai téléphone, un vrai tableau blanc, ni avec un vrai paiement).
7. Les vidéos du propriétaire (`~/Videos/Screencasts/*.mp4`) se lisent avec GStreamer : `gst-launch-1.0 filesrc location=… ! decodebin ! videoconvert ! videorate ! video/x-raw,framerate=1/1 ! pngenc ! multifilesink location=f%03d.png`, puis une planche de vignettes avec Pillow.

**Comment tester sans téléphone** : serveur `python3 -m http.server 8771` depuis la racine du dépôt, copie de test de `index.html` avec des crochets (exposer `live`, `S`, `build`, `resetStream`, `streamUpdate`, `updateJelly`, `updateButterfly`, `frame`, `W`, `H`, `T` juste avant `requestAnimationFrame(frame);` suivi de `})();`, à la fin du premier grand script), simulations accélérées dans le navigateur de l'outil (pas de temps 0,0167 à 0,1), mesures : collisions entre paires, répartition, orientation de la tête, départs, comptes par minute ; fin de minuteur de bout en bout avec `performance.now` simulé et `requestAnimationFrame` neutralisé. Pièges : la fenêtre de l'outil tombe à 3 images/s si elle n'est pas au premier plan (rien à faire en temps réel dans ce cas) ; les cloches ne se dessinent pas si on démarre avant la fin du chargement des images ; ne pas nommer une fonction `t` (conflit : la fonction de traduction s'appelle `txt`) ; `pkill -f` peut tuer le shell lui-même.

**Ce que fait la 5.16 (la 5.17 corrige les fleurs et l'espacement des papillons, la 5.18 ajoute le mode hors ligne complet : voir plus bas)** : minuteur de sieste à méduses ou papillons, une créature de moins à chaque minute (max 30), toutes à l'écran dès le départ et toujours les mêmes ; chaque minute la créature désignée vient près de la vitre (bien plus grande), puis sort en un ou deux battements ; la tête mène et les filaments traînent ; quatre à six plans de profondeur pour éviter les collisions ; pause qui fige tout ; temps personnalisé (1 à 180 min) ; langue et devise de l'appareil (fr, en, es, de, zh) ; application installable (manifeste, service worker, icônes papillon) ; « Pourquoi Lumora ? » ; soutien par lien PayPal.me `QuickquoteSupport` (montants 5/10/20 ou autre montant). Détail dans les sections « Version 5.x » ci-dessous.

**Reste à faire / ouvert**
- **Google Pay** : affiché « Bientôt ». Il ne fonctionne pas via PayPal (même constat dans QuickProof) ; il faut une autre technique (non choisie).
- **Dons PayPal** : jamais testés avec un vrai paiement ; confirmer que `QuickquoteSupport` est bien le compte voulu pour Lumora ; Lumora ne voit plus si le paiement a été fait (pas de message de remerciement). Si la page PayPal pose encore problème dans l'application installée sur iPhone, demander ce qui s'affiche.
- **Non vérifié sur de vrais appareils** : mouvement en temps réel (toutes les mesures viennent de simulations), iPhone, Android, tableau blanc 5 pi × 4 pi, service worker hors ligne.
- **Cas rares connus** : une grosse méduse coincée entre ses voisines peut avoir la tête mal orientée un moment ; avec 30 méduses il reste quelques cloches qui se touchent (à des profondeurs différentes) ; sur un petit écran vertical une méduse déjà au bord peut rester partiellement hors cadre pendant son approche.
- **Papillons** : encore un peu concentrés vers le centre (répartition par cinquième de largeur 9/22/32/26/11 %).

## Icônes — 31 octobre 2026

Le propriétaire a choisi le **papillon bleu seul**, sans le mot miniature, pour l'onglet du navigateur et les raccourcis. Les fichiers `icons/icon-192.png`, `icon-512.png`, `icon-maskable-512.png` et `apple-touch-icon.png` sont remplacés par ce dessin. Ajouts : `icons/icon.svg`, `favicon-16.png`, `favicon-32.png` et `favicon.ico` à la racine.

[Aperçu des icônes aux différentes tailles](assets/apercus/icones-papillon.png). Vérifié : build réel du site, liens et types des fichiers, manifeste lu par Chromium, tailles PNG 180/192/512, quatre tailles dans le ICO, marge de sécurité de l'icône adaptative, chargement des icônes hors ligne et conservation des caches étrangers à Lumora. Aucun essai sur un écran d'accueil iOS physique n'est revendiqué.

Le manifeste garde l'identifiant et le démarrage de l'application existante; les URL d'icônes portent `?v=2` pour éviter l'ancien dessin en cache. Le service worker est passé à `5.5-papillon-2`; il conserve les nouvelles icônes hors ligne et ne nettoie que les anciens caches de Lumora. Les métadonnées sont à jour dans la page racine et la v5. Le générateur `tools/make_icons.py` reproduit tous les formats avec Pillow, et `tools/build_site.py` copie aussi le favicon dans `dist`.

Après récupération de cette mise à jour, republier `dist` par la procédure habituelle du site. Un raccourci déjà présent sur un écran d'accueil peut garder son ancien dessin jusqu'à sa recréation. Ne pas remplacer toute la page par une copie plus ancienne : seuls les liens d'icônes ont été modifiés.

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
- `index.html` (racine) : la version courante (copie de la v5 avec chemins adaptés). Si on modifie la v5, refaire la copie.
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

## Ajouts du 31 octobre 2026
- Méduses : **3 plans de profondeur** (devant / milieu / fond). Quand deux méduses vont se croiser, celle qui n'a pas la priorité passe lentement (≈ 1,7 s par plan) dans un plan plus profond : un peu plus petite et plus pâle, dessinée derrière. Elle revient devant quand la voie est libre. Si tous les plans sont occupés, elle attend comme avant. Mesure (téléphone, 170 s, simulation) : chevauchements à 14 % et 33 % des instants avant, 3 % et 4 % après.
- Accueil : après l'écriture et le halo, un papillon bleu arrive de la droite, ralentit, se pose sur le haut du L et bat des ailes très doucement ; l'accueil se ferme ≈ 3,8 s plus tard (durée totale ≈ 11 s ; « Passer l'animation » reste disponible).
- Mise en ligne : voir `DEPLOIEMENT.md` (Cloudflare Pages, lumora.pixeldrop.ca, commande `python3 tools/build_site.py`, dossier `dist`).
- Important : ces changements ont été faits directement dans `versions/v5-traversees/index.html`. Le script `outils/makev5.py` ne les contient pas : il ne reproduit plus la v5 exacte. Modifier la v5 directement, puis refaire la copie racine.

## Reconstruire la v5 (ancienne méthode, avant les ajouts ci-dessus)
`makev5.py` lit une copie de la v4 (identique à `versions/v4-concept-1/index.html`) et applique des remplacements de texte précis ; chaque remplacement vérifie qu'il trouve exactement le texte attendu. Les chemins en tête du script pointent vers un dossier temporaire : les adapter. Plus simple en général : modifier directement `versions/v5-traversees/index.html`.

## Tests (Playwright, Node)
Serveur local : `python3 -m http.server 8771` depuis la racine du dépôt. Copie de test exposant l'état des créatures, à supprimer ensuite. La simulation sans carte graphique tourne à ≈ 0,5× : les images/seconde mesurées ne reflètent pas un vrai appareil.

## Pas encore vérifié
Vrai iPhone, vrai tableau blanc, son à l'oreille, fluidité réelle.

## Décisions déjà prises (31 octobre 2026)
- La v5 est devenue la page principale (`index.html` racine, chemins `./assets/` et `./audio/`).
- Texte d'introduction du panneau de départ mis à jour.
- Historique nettoyé : aucun nom d'outil dans les messages, fichiers ou contenus (poussé en mode forcé avec l'accord du propriétaire). Si l'autre outil d'illustration avait une copie locale ancienne, il doit refaire `git fetch` puis `git reset --hard origin/main` avant de pousser.

## État au 31 octobre 2026 (fin de la session dans le nuage)
Déjà dans le dépôt (main) :
- Méduses sur 3 plans de profondeur (se croisent sans se toucher).
- Accueil : papillon qui se pose sur le L.
- Texte de crédits retiré du panneau de départ (les crédits restent dans le README).
- Fichiers de mise en ligne : `tools/build_site.py` (prépare `dist`), `deploy/installer-sur-serveur.sh`, `deploy/lumora-web.service` (serveur local 127.0.0.1:8791), `deploy/cloudflared-ingress.example.yml`, `_headers` (utile seulement pour Cloudflare Pages), procédure dans `DEPLOIEMENT.md`.

## (FAIT le 31 octobre 2026 : le site est en ligne) À FAIRE EN PRIORITÉ (session avec accès SSH à l'ordinateur du propriétaire)
**1. Mettre Lumora en ligne sur lumora.pixeldrop.ca, sur le même serveur que PixelDrop.** Le propriétaire veut que l'assistant le fasse lui-même, comme pour ses autres sites (le dépôt PixelDrop contient `deploy.sh` : la commande SSH habituelle vise `ubuntu@148.116.71.199`, le service PixelDrop tourne sur le port 8123). La session dans le nuage n'avait ni SSH ni clés : rien n'a été déployé ni testé sur le serveur.
Marche à suivre :
- Se connecter au serveur de PixelDrop (Oracle, selon le propriétaire), vérifier que le port 8791 est libre (`ss -ltn | grep 8791`), puis : `git clone https://github.com/xcoder2088/lumora ~/lumora` (ou `git pull`) et `bash deploy/installer-sur-serveur.sh` (attendu : « Test local : HTTP 200 »).
- Ajouter la route du tunnel Cloudflare existant : `lumora.pixeldrop.ca` vers `http://127.0.0.1:8791` (fichier de configuration du tunnel ou tableau de bord Zero Trust → Tunnels → Published application routes), et le DNS (CNAME `lumora` vers `<UUID-du-tunnel>.cfargotunnel.com`, proxy activé) si le fichier est édité à la main. Relancer le tunnel.
- Vérifier https://lumora.pixeldrop.ca (méduses ET papillons, son après un clic) ET que PixelDrop fonctionne toujours. Les deux doivent tourner. Ne pas modifier le service PixelDrop, son `.env`, ses données.
- Si le propriétaire préfère un hébergement indépendant du serveur : Cloudflare Pages (commande de build `python3 tools/build_site.py`, dossier `dist`).

**2. Défaut signalé par le propriétaire, non résolu : les méduses se retrouvent en « paquet » dans la zone du bas / milieu de l'écran (téléphone).** Les essais de correction (choisir les trajets dans les zones vides ; écarter doucement les méduses proches) ont donné des mesures contradictoires et n'ont pas été gardés. Demander à quel moment le paquet apparaît (début ou plus tard) et obtenir une vidéo ou des captures espacées de 30 s. Piste : dans `updateJelly`, en vol libre, l'évitement « doux » n'a aucun effet (`kx = 0`) ; seule la priorité (attente ou changement de plan) agit.

## Pièges techniques (pour les tests)
- La page est une fonction auto-appelée : pour tester, copier `index.html` et ajouter `window.__live=()=>live;` juste avant `requestAnimationFrame(frame);\n})();`, puis supprimer la copie.
- Serveur de test : `python3 -m http.server 8771` depuis la racine du dépôt, lancé en arrière-plan avec une longue durée ; il s'arrête tout seul au bout de sa durée.
- Sans carte graphique, la simulation tourne à ≈ 0,5× et les mesures varient beaucoup d'une exécution à l'autre : toujours répéter.
- Les scripts de mesure étaient dans un dossier temporaire du nuage (perdus) : mesurer les chevauchements par paires (distance < 0,75 × somme des rayons, même plan), les plans occupés et les plus gros paquets.

## Page de démonstration privée
Version 5 : la page de démonstration privée est dans la liste des pages publiées du propriétaire (titre « Lumora »).

## Version 5.3 (31 octobre 2026)
**Règle : à chaque version ou révision, changer le numéro à deux endroits : le texte `ver x.y` (élément `#ver` de `index.html`, sous le bouton Commencer) et `VERSION` dans `sw.js` (sinon les appareils gardent l'ancienne copie).**
- Titre du panneau : le tracé écrit à la main de l'accueil, avec le papillon posé sur le L (plus de texte « Lumora » en police simple). Sous le titre, la phrase du sens du nom : l'éveil de la lumière, un nouveau départ, une lueur douce qui naît de l'intérieur (aussi dans la description et le manifeste).
- Version déplacée sous le bouton Commencer (« ver 5.3 »), avec le bouton « Soutenir le développement » (petite tasse).
- Fin du minuteur : le message apparaît (et le carillon joue) dès que la dernière créature a quitté l'écran, dans les 8 dernières secondes, au lieu d'attendre zéro puis 1,5 s. L'horloge passe alors à 0:00. Mesuré en essai de 30 s : la dernière méduse sort jusqu'à ~5 s avant zéro selon son trajet, le dernier papillon environ 2 s avant.
- Langue : celle de l'appareil, comme QuickProof (français, anglais, espagnol, allemand, chinois ; sinon anglais ; `?lang=fr` force une langue). Textes dans `I18N` (premier script de `index.html`), fonction `txt('clé')`. Ne pas la nommer `t` : conflit avec des variables locales.
- Soutien : PayPal, dans la devise de l'appareil (région de la langue, sinon fuseau : US→USD, CA→CAD, zone euro→EUR, etc. ; montants 5 / 10 / 20 ou équivalents). Pas de serveur : la commande PayPal est créée et validée par le navigateur avec l'identifiant public du compte (le même que QuickProof, aucun secret dans la page). **Google Pay : affiché « Bientôt »**. Il ne fonctionne pas via PayPal (même constat dans QuickProof) : une autre technique est à choisir.
- Application installable : `manifest.webmanifest` (mode standalone), `sw.js` (copie hors ligne), icônes dans `icons/` (refaites avec `python3 tools/make_icons.py`), bouton « Installer l'app » quand le navigateur le propose. Une page web ne peut pas s'ouvrir sans barre d'adresse sans être installée : Android/Chrome « Installer », iPhone Partager > Sur l'écran d'accueil. Pour une ouverture sans barre garantie sur Android, il faut une application TWA comme QuickProof (non faite).
- Non vérifié : service worker (le navigateur intégré de l'outil de test ne l'accepte pas), paiement PayPal réel, installation sur un vrai téléphone, fin du minuteur pour 5 min et plus (testé en essai de 30 s seulement).

## Version 5.4 (31 octobre 2026)
Corrections d'affichage : boutons PayPal sur un fond clair (plus de bande blanche dans la fenêtre sombre) ; pied du panneau (version, Installer, Soutenir) aligné sur le bouton Commencer, barre de défilement fine. Numéro changé dans `#ver` et dans `VERSION` de `sw.js`.

## Version 5.5 (31 octobre 2026)
Le panneau de départ ne défile plus : il est un peu plus compact, le bouton « Installer l'app » est dans la ligne du pied, et un petit script (`fitSetup`) réduit le panneau (variable CSS `--fit`, au plus à 50 %) quand l'écran est trop court. Testé à 640×420 et 375×667 : aucun défilement.

## Serveur (31 octobre 2026)
Le service `lumora-web` lance maintenant `deploy/lumora-server.py` (copié dans `/usr/local/share/lumora/` par `installer-sur-serveur.sh`) au lieu de `python3 -m http.server`. Il envoie `Cache-Control: public, max-age=0, must-revalidate` pour la page, `sw.js` et le manifeste, et `max-age=86400` pour `assets/`, `audio/` et `icons/`. Cloudflare avait gardé l'ancien `sw.js` : une purge unique (Caching > Purge Everything) est nécessaire après ce changement.

## Version 5.6 (31 octobre 2026)
Nouvelles icônes : le papillon bleu seul (favicon, raccourcis, écran d'accueil), voir « Icônes » en haut de ce document. Numéro changé dans `#ver` et dans `VERSION` de `sw.js`.

## Version 5.7 (31 octobre 2026)
Écran de fin : la ligne sous « Doucement, c'est l'heure. » devient « Une lueur douce se lève. » (clé `endText`, cinq langues) : à la fin la scène s'éclaircit vraiment, c'est l'éveil de la lumière. Numéro changé dans `#ver` et dans `VERSION` de `sw.js`.

## Version 5.8 (31 octobre 2026)
Sens du nom : une ligne sous le mot sur la page d'ouverture (apparaît quand le papillon ralentit pour se poser, clé `welcomeLine`) et un lien « Pourquoi Lumora ? » dans le pied du panneau qui ouvre la citation complète (clés `aboutTitle`, `aboutP1`, `aboutP2`). Cinq langues. Panneau toujours sans défilement (testé 375×667). Numéro changé dans `#ver` et dans `VERSION` de `sw.js`.

## Version 5.9 (1er novembre 2026, branche `version-5.9`, pas encore publiée)
Demandes des éducatrices :
1. Toutes les créatures sont déjà à l'écran au départ (plus d'arrivée progressive) : autant que de minutes choisies (au plus 30, donc 30 jusqu'à la 30e minute restante pour 45 min), une de moins à chaque minute, la dernière à zéro. Une minute = 60 s fixes (`P = 60`). Méduses : le premier passage commence dans l'écran, loin des autres (`newJellyPass`, option `first`). Papillons : chacun démarre au milieu d'un passage (`ph`, durée de passage `T = e / (m - ph)`). `arrivalTime()` renvoie `-1000`.
2. La pause fige tout : décompte, créatures, herbes, lucioles (`dt = 0` et plus de mise à jour des créatures quand `S.phase === 'paused'`). Le son d'ambiance continue.
3. « Essai 30 s » retiré ; « Temps personnalisé » à la place (ligne avec un champ en minutes, de 1 à 180, mémorisée). Un ancien réglage à 30 s est ignoré.
Mesuré (essai local, durée 5 min) : méduses et papillons 5 au départ, puis 4, 3, 2, 1 à chaque minute ; pause : positions et horloge figées. Numéro `ver 5.9` dans `#ver` et `VERSION` de `sw.js`.
4. (précision des éducatrices) Ce sont toujours les mêmes créatures qui restent affichées : aucune ne sort puis revient, aucune nouvelle n'arrive pour combler le nombre. Méduses : demi-tour doux avant le bord (`turnJelly`, `jellyAheadOut`) et paroi douce autour de l'écran tant qu'elles ne sont pas dans leur dernier passage (`c.finalPass`). Papillons : `BFLY_STAY` (de repère en repère dans l'écran, le dernier passage seul mène hors de l'écran). Vérifié par simulation (durées de 5 à 45 min, plusieurs essais) : aucune sortie avant le dernier passage, et 5, 4, 3, 2, 1 à chaque minute ; pour 45 min, 30 créatures jusqu'à la 30e minute restante.
5. (collisions, vidéo du 1er novembre) Profondeur de champ pour les méduses : 4 plans (`JELLY_LANES`, 0 = devant, 3 = au fond) répartis dès le départ (`k % 4`). Une méduse qui chevauche une autre du même plan (distance < 1,3 × la somme des rayons) et qui a la priorité la plus faible passe lentement dans un plan libre (≈ 1,7 s par plan) ; deux plans d'écart = elles se croisent sans se gêner. Espace personnel plus large (1,45 × dans le même plan, 1,1 × entre plans voisins). Plus on est au fond, plus la méduse est petite (jusqu'à −30 %), pâle (jusqu'à −45 %) et bleutée. Mesure en simulation (10 méduses, cloches qui se touchent, même plan ou plan voisin) : 11 à 14 % du temps de paires avant, 2 % après ; aucune méduse qui se recouvre dans le même plan. Les papillons n'ont presque aucune collision (0 à 0,1 %).
6. (collisions, 2e vidéo : 45 min, 30 méduses, fenêtre 1834×868) La profondeur est maintenant décidée d'après la trajectoire : chaque créature regarde les 8 prochaines secondes (méduses) ou 5 s (papillons) avec la vitesse réelle des autres ; si elle va croiser ou touche une créature PLUS ANCIENNE dans le même plan ou un plan voisin, elle change de plan (le moins peuplé et sans conflit) ; deux plans d'écart suffisent. Nombre de plans selon le nombre de créatures : méduses 4 (jusqu'à 10), 5 (jusqu'à 20), 6 (plus) ; papillons 3, ou 4 au-delà de 12. Une créature revient d'un plan vers l'avant quand la voie est libre. Un papillon posé sur une fleur est toujours au premier plan. Plus on est au fond : plus petit (méduses −38 %, papillons −28 %), plus pâle (méduses −50 %, papillons −40 %), plus bleuté (méduses). Les méduses sont plus petites quand elles sont plus de 24 (×0,65).
Mesure en simulation (cloches qui se touchent, même plan ou plan voisin ; 30 méduses sur 1834×868) : 0,89 % du temps de paires avant cette étape, 0,2 % après ; 10 méduses : environ 1 % après (11 à 14 % avant la 1re étape de profondeur). Papillons : 0 chevauchement mesuré avant et après. Non reproduit en simulation : le gros groupe au centre haut de la vidéo ; si il revient, demander l'heure exacte (horloge) et la taille de la fenêtre.

## Version 5.10 (1er novembre 2026, branche `version-5.10`)
Comportements « erratiques » et filaments (3e vidéo, 20 min) : mesure de la 5.9 en simulation : cloche à l'envers (inclinée de plus de 83°) 45 à 52 % du temps, rotation jusqu'à 40°/s, 30 % des filaments à l'horizontale, bout des filaments à 48° de la verticale en moyenne. Cause : les demi-tours ajoutés en 5.9 (`turnJelly`) changeaient le cap d'un coup et la cloche suivait le cap dans tous les sens.
Corrections : la cloche reste en haut, inclinaison `TILT_MAX * sin(cap)` (au plus 35°, droite quand elle monte ou descend) ; le cap tourne doucement vers le cap voulu (`TURN_RATE`, 9°/s), la rotation du corps est limitée à 8°/s ; pas de demi-tour ; les battements poussent selon le cap (fort vers le haut, à peine vers le bas) ; le but suivant est dans l'autre moitié de l'écran en hauteur et la méduse coule un peu plus (`sink`), pour qu'elles occupent tout l'écran. Filaments : la traîne est proportionnelle à la vitesse (0,006 au lieu de 0,02) et propre à chaque filament (`kd`), ils pendent plus vite (`gk`, exposant 0,7), ondulation plus douce avec une 2e composante lente.
Mesure après : cloche à l'envers 0 %, rotation médiane 1°/s (95e centile 5°/s), bout des filaments à 10° en moyenne et 0 % à l'horizontale, collisions inchangées (30 méduses : 0,12 % du temps de paires), aucune sortie de l'écran, répartition verticale uniforme (moyenne 0,44 à 0,46).

## Nouvelle stratégie de sortie (1er novembre 2026, branche `version-5.10`, 4e vidéo)
Avant : une méduse qui devait partir dérivait pendant jusqu'à 55 s vers le bord (dernier passage guidé), donc elle était presque sortie de l'écran bien avant sa minute, et un papillon traversait l'écran pendant 34 à 52 s. Maintenant (demande des éducatrices) : toutes les créatures se déplacent librement dans l'écran, et à chaque minute UNE seule part vite, en ligne droite, par le bord le plus proche, puis les autres continuent.
- Méduses : libres jusqu'à `JELLY_EXIT_T` = 8 s avant leur instant de sortie `e`, puis départ rapide par le bord le plus proche (côtés ou haut ; le bas seulement s'il est 2,2 fois plus proche), guidage ferme (`guide = smooth(u / 0.12)`). Sécurité : une méduse dont le centre reste plus de 2 s hors de l'écran avant son départ est ramenée vers le centre.
- Papillons : libres (repères dans l'écran) jusqu'à `BFLY_EXIT_T` = 6,5 s avant `e`, puis envol droit vers le bord le plus proche (même s'ils sont posés sur une fleur). Le dernier passage n'est plus guidé vers un bord.
- L'ordre de départ est celui des indices k (positions et tailles aléatoires), donc aléatoire pour l'œil. Un départ se termine à l'instant `e` (60 s, 120 s, ... et zéro pour la dernière).
Mesure (simulation) : aucune créature sortie de l'écran avant ses 9 dernières secondes (0 s sur tous les essais) ; comptes exacts à chaque minute (5, 4, 3, 2, 1) ; la créature est « surtout sortie » 1 à 6 s avant son instant de sortie (jamais moins de 0,5 s) ; mêmes mesures de collision et de naturel qu'avant (aucune méduse à l'envers, filaments pendants).

## Version 5.11 (1er novembre 2026, branche `version-5.11`, 5e vidéo : site en ligne, 30 min)
Deux défauts vus sur la 5.10 :
1. « Elles semblent toutes se diriger du même côté » : le courant marin partagé (fonction du temps seulement) emportait tout le groupe dans le même sens. Mesure : le centre du groupe (30 méduses) allait de 0,57 à 0,66 de la largeur en 30 s puis revenait à 0,37, identique dans 4 essais. Le courant est maintenant petit (0,012 × la taille d'écran au lieu de 0,03) et propre à chaque méduse et à chaque endroit ; un nouveau but est choisi après 40 s au plus (avant 90 s). Mesure après : centre à 0,5 ± 0,05 dans tous les essais, vitesse moyenne nulle.
2. « La première quitte 6 s trop tôt » : le départ se TERMINAIT à la minute, donc il commençait 8 s avant. Maintenant il COMMENCE à la minute (`e = D - k × 60 + EXIT_T`, `EXIT_T` = 8 s pour les méduses, 6,5 s pour les papillons) : à 29:00 pour 30 min la première créature part, et elle est partie quelques secondes plus tard. La dernière commence à partir à zéro : le décompte reste à 00:00 pendant son départ, puis le message de fin arrive dès qu'elle est sortie (environ 5 à 8 s après zéro). Filet de sécurité : fin forcée à D + 12 s.
Test de bout en bout (boucle d'animation réelle avec horloge simulée, 3 min méduses et 2 min papillons) : compte exact à chaque minute (3, 2, 1), fin à 188 s pour 180 s (méduses) et 124,9 s pour 120 s (papillons). Numéro changé dans `#ver` et dans `VERSION` de `sw.js`.

## Version 5.12 (1er novembre 2026, branche `version-5.12`, 6e vidéo : site en ligne, 30 min)
Retour : « méduses et papillons semblent tous se diriger vers le haut sans arrêt ; ils devraient aussi aller vers le fond et de gauche à droite ; **c'est la tête de la méduse qui dirige** et les filaments suivent de façon fluide et naturelle ; et en quittant l'écran la créature devrait passer près de nous ».
- Cap de départ : une direction quelconque (avant : 6 méduses sur 10 partaient vers le haut, 1 sur 10 vers le bas, donc tout le groupe montait pendant la première minute).
- **La tête mène (retour au modèle « tête en avant » avec une rotation douce)** : la cloche pointe dans le sens du mouvement, dans toutes les directions (elle peut donc être inclinée ou à l'envers quand elle descend, c'est voulu), chaque battement pousse dans le sens où pointe la tête, le cap tourne à 9°/s au plus, la rotation du corps à 12°/s au plus (26°/s pendant un départ) ; l'eau freine les glissements de côté (`kperp`). La direction visée suit peu à peu le mouvement réel (`tdx`, `tdy` vers la vitesse, 0,5/s), si bien que même une méduse poussée par ses voisines tourne la tête vers là où elle va. L'inclinaison maximale de 35° de la 5.10 est supprimée.
- **Filaments** : ils traînent dans le sens opposé au mouvement (proportionnel à la vitesse, propre à chaque filament), avec une faible pesanteur et un suivi plus souple (`lerp(7, 2.8)`).
- Poussées plafonnées et ordonnées : voisines (au plus 120), parois (140, toujours plus fortes que les voisines, marges d'au moins 45 px même pour une petite méduse) ; apparition à l'intérieur des marges ; demi-tour immédiat dans la zone des parois ; plus de dérive vers le bas (`sink` presque nul).
- **Départ** : la créature qui part passe au premier plan et grossit (méduse jusqu'à ×1,7, papillon jusqu'à ×1,9) : elle passe près de nous et on voit qui part ; elle choisit le bord le plus proche parmi ceux vers lesquels sa tête est déjà tournée ; plus poussée par ses voisines ; elle s'estompe à la toute fin si elle traînait. Papillons : restent dans l'écran jusqu'à leur départ.
Mesure (simulation) : directions de déplacement de la méduse : 14 % haut, 18 % bas, 49 % côtés, 19 % presque immobile (avant : 60 % de têtes vers le haut au départ) ; papillons 17 / 24 / 40 / 19 ; répartition verticale moyenne 0,45 à 0,55. Tête dans le sens du mouvement : 13 à 24° d'écart en moyenne dans 4 essais sur 5 (un essai à 36°, avec une grosse méduse coincée entre ses voisines) ; traîne des filaments à 14 à 21° du sens opposé au mouvement ; vitesse de rotation du bout d'un filament : 0,3 à 0,6 rad/s (95e centile). Collisions inchangées (10 méduses : 0,4 à 1 % du temps de paires ; 30 : 0,17 %). Aucune sortie anticipée sur les durées testées ; fin du minuteur à D + 7,5 s (méduses) et D + 5,9 s (papillons).

## Version 5.13 (1er novembre 2026, branche `version-5.13`, 7e et 8e vidéos : méduses, puis papillons, site en ligne 30 min)
Retour : « la sortie est encore beaucoup trop subtile : celle désignée pour sortir doit passer au premier plan près de la vitre de façon évidente, puis sortir en un ou deux battements, calé sur la fin de la minute ». Même chose pour les papillons.
Nouveau départ (constantes `JELLY_APPROACH/DASH/TAIL` = 3,5 / 3,5 / 1 s, `BFLY_APPROACH/DASH/TAIL` = 3 / 2,5 / 1 s) :
1. Approche, de 3,5 s (méduse) ou 3 s (papillon) AVANT la minute : la créature désignée vient au premier plan, se rapproche du centre (70 % du chemin), grossit jusqu'à 3,4 fois (au plus environ 44 % de la hauteur de l'écran), s'éclaircit (40 % vers le blanc) et tourne déjà la tête vers sa sortie. Elle reste entière à l'écran.
2. À la minute : elle sort en un ou deux grands battements (`thrustK` 1,7, `perK` 0,62 pour les méduses), par le bord le plus proche parmi ceux vers lesquels sa tête est tournée ; elle est sortie environ 1 à 2 s après la minute (mesuré : « surtout sortie » 2,5 à 3 s avant sa disparition `e` = minute + 4,5 s pour les méduses, +3,5 s pour les papillons), puis elle s'estompe et disparaît.
La fin du minuteur arrive donc environ 2 à 4 s après zéro (avant 5 à 8 s).
Défaut corrigé au passage (présent en 5.11 et 5.12) : après le déclenchement de la fin, le temps de la scène revenait à D pile, donc la dernière créature, encore en train de partir, aurait pu revenir à l'écran ; maintenant `S.doneEl` garde le temps réel (mesuré : aucune créature à l'écran 10 s après la fin).
Papillons : zone de vol élargie (4 à 96 % de la largeur) et ils s'attardent près de leurs repères, pour occuper tout l'écran (répartition horizontale 9/22/32/26/11 % au lieu de 6/28/40/23/3 %).
Mesure (simulation) : aucune sortie avant l'approche (0 s sur méduses 5, 10, 30 et papillons 10, 30) ; comptes exacts à chaque minute ; collisions et orientation de la tête inchangées.
Remarque pour les tests : dans le navigateur de l'outil de test, les cloches n'apparaissent pas si on démarre avant la fin du chargement des images ; attendre quelques secondes.

## Version 5.14 (1er novembre 2026, branche `version-5.14`)
Retour sur PayPal (iPhone) : « petit bug : une fois PayPal ouvert, on ne peut pas revenir en arrière » ; et « montant personnalisé à ajouter ».
- Le script PayPal est chargé avec `disable-funding=paylater,venmo` : plus de « Payer plus tard » (sa fenêtre de connexion n'avait aucun bouton pour revenir). Restent « PayPal » et « Carte de débit ou de crédit ».
- Si on annule dans la fenêtre PayPal (`onCancel`), on revient au choix du montant avec le message « Paiement annulé. Vous pouvez choisir un autre montant. » ; le bouton « Retour » de la fenêtre reste disponible.
- Montant personnalisé : champ « Autre montant » + devise + bouton « Continuer » sous les trois montants. Accepte la virgule ou le point (au plus 2 décimales ; entier pour JPY, HUF, TWD) ; minimum = 1 / 5 du premier montant proposé (1 USD, 100 JPY…), maximum = 50 fois le troisième (1 000 USD). Message d'erreur dans la langue de l'appareil. Cinq langues (`customAmount`, `continueBtn`, `amountInvalid`, `cancelled`).
Non vérifié : paiement réel (aucun test avec de l'argent), comportement exact de la fenêtre PayPal sur iPhone après ce changement.

## Version 5.15 (1er novembre 2026, branche `version-5.15`)
Retour sur la 5.14 (iPhone) : le formulaire de carte de crédit intégré de PayPal (« Adresse de facturation ») prend tout l'écran et on ne peut ni en sortir ni revenir en arrière. Ce formulaire est dessiné par PayPal dans la page, on ne peut pas y ajouter de bouton. Correction : le script PayPal est chargé avec `disable-funding=card,paylater,venmo` : il ne reste que le bouton « PayPal », qui s'ouvre dans sa propre fenêtre (fermable). Le don par carte reste possible via la page de connexion PayPal (paiement sans compte, selon l'éligibilité de PayPal). Non vérifié sur l'iPhone ; si la fenêtre PayPal pose encore problème, l'alternative est un lien `paypal.me` (pas de montant imposé par la page, tout se passe sur le site de PayPal, avec le bouton retour du navigateur).

## Version 5.16 (1er novembre 2026, branche `version-5.16`)
Retour sur la 5.15 (iPhone, application installée sur l'écran d'accueil) : la fenêtre des boutons PayPal (connexion, carte de crédit) s'ouvre sans aucun bouton de fermeture et on ne peut pas revenir à l'application. C'est PayPal qui ouvre cette fenêtre, on ne peut pas y ajouter de bouton. Correction : plus aucun script PayPal dans la page (suppression de `paypal.com/sdk`, de `PAYPAL_CLIENT_ID`, des boutons) ; le choix du montant (trois montants ou « Autre montant », dans la devise de l'appareil) mène à un bouton « Continuer vers PayPal » qui est un simple lien `https://www.paypal.me/QuickquoteSupport/<montant><DEVISE>` (`target="_blank"`), ouvert comme une page web normale avec le retour du système. Compte PayPal.me utilisé : `QuickquoteSupport` (trouvé dans le code de QuickQuoteTool et QuickProof ; à vérifier avec le propriétaire). Limites : Lumora ne voit plus si le paiement a été fait (pas de message de remerciement) ; PayPal.me peut ne pas accepter toutes les devises listées.
Non vérifié : ouverture du lien sur l'iPhone dans l'application installée, paiement réel.

## Version 5.17 (1er novembre 2026, en ligne, commit `633565d`)
Retour (iPhone, scène des papillons) : des fleurs sans pétales et des papillons trop collés. 1) L'image `fleur-marguerite-04` est un bouton fermé : elle n'est plus utilisée (ni décor, ni atterrissage ; seules 01, 02, 03 et 05 restent). 2) Écartement des papillons : un décalage lent propre à chacun (`c.ox`, `c.oy`) les éloigne des autres quand la distance passe sous 3,4 × la somme de leurs tailles, quel que soit le plan ; pas pour un papillon posé ni en départ. Mesure (simulation 430×900, 25 papillons) : paires à moins de 2 × la taille : 4,1 % du temps avant, 0,14 % après ; à moins de 3 × : 8,9 % avant, 3,3 % après. Le propriétaire a confirmé : « Beaucoup mieux ».

## Version 5.18 (1er novembre 2026, branche `version-5.18`) : utilisation sans internet
Besoin : que les éducatrices puissent continuer d'utiliser l'application sans connexion (iPhone et Android). Avant : seuls la page et les icônes étaient gardés ; les images et sons ne l'étaient qu'une fois utilisés (une scène jamais ouverte restait vide hors ligne) et les polices venaient de Google.
- Polices en local (`fonts/`, Cormorant Garamond 300/400/500 et Jost 400/500, licence SIL OFL) : plus aucun appel à Google Fonts.
- `tools/build_site.py` écrit `dist/precache.json` (73 fichiers : images, sons, polices) ; `sw.js` garde tout au premier lancement (par lots de 6), puis pose un témoin ; la page affiche « Prêt hors ligne ✓ » (cinq langues, clés `offReady` et `offLoading`) à côté du numéro de version.
- `deploy/lumora-server.py` : `/precache.json` sans cache, `/fonts/` gardé un jour.
Mesuré (Chromium réel, serveur local sur `dist`) : 84 entrées gardées, témoin posé, message affiché ; serveur éteint puis page rechargée : la page s'ouvre, les polices se chargent, les 73 fichiers répondent. Non mesuré : vrai iPhone/Android, mode avion réel, effacement des données par Safari après longue inactivité (l'application doit être rouverte avec internet de temps en temps). Le navigateur intégré à l'outil de test n'accepte pas les service workers : tester avec un vrai Chromium (`/snap/bin/chromium --headless=new --remote-debugging-port=…`, piloté par le protocole de débogage avec le `WebSocket` de Node).

## Version 5.19 (2 novembre 2026, branche `version-5.19`) : son beaucoup plus fort
Retour d'utilisateurs Android : « même avec le volume de l'appareil au maximum, le son reste plutôt faible dans un environnement bruyant ».
Mesure (rendu hors ligne dans le navigateur) : les enregistrements sont très faibles. Niveau moyen (RMS, en dB sous le maximum) : baleines1 −39,5 ; baleines2 −38,5 ; profondeurs −23,4 ; nuit −58,4 (crêtes à −35) ; musique-nuit −33,6 ; brise −51 (non utilisée). Une musique ordinaire est vers −14. Le mélange de la scène des méduses sortait à −38 dB, celui des papillons à −53 dB (presque inaudible). Le carillon de fin était à −44 dB et très grave (220 à 554 Hz, sans harmoniques, filtre à 900 Hz) donc inaudible sur un petit haut-parleur.
Correction (`index.html`, section « Niveau sonore ») :
- `SCENE_BOOST = { jelly: 5, butterfly: 28 }` multiplie les gains des calques de chaque scène (les proportions entre calques sont conservées) ;
- `buildOutputChain(ctx, dest)` : filtre passe-haut 110 Hz (les petits haut-parleurs ne reproduisent pas les graves), un peu de présence (+4 dB à 1,2 kHz), compresseur doux (seuil −28 dB, rapport 3) puis limiteur (seuil −4 dB, rapport 20) : plus régulier donc plus audible dans le bruit, aucune saturation ;
- carillon : amplitudes ×8, chaque note accompagnée de son octave et de sa quinte à l'octave (×2 et ×3), filtre à 2,4 kHz, et il passe par la même chaîne (`master`) ;
- le volume de l'appareil reste le seul réglage de l'utilisateur (pas de curseur).
Mesure après (rendu hors ligne, mêmes fichiers) : méduses −38,3 → −16,7 dB (crête −5,2) ; papillons −53,3 → −17,3 dB (crête −3,5) ; avec un filtre qui imite un petit haut-parleur (coupure à 350 Hz) c'est pareil (−16,8 et −17,5) ; carillon −44 → environ −17 dB (crête sous −4 dB). Les crêtes restent sous 0 dB : pas de saturation.
Non vérifié : l'écoute réelle (je ne peux pas entendre), sur un vrai téléphone Android, dans un vrai local bruyant, ni le confort d'écoute dans une pièce calme (le niveau est maintenant celui d'une musique ordinaire quand le volume est au maximum ; l'éducatrice règle le volume de l'appareil). Si c'est trop fort dans une pièce calme, baisser `SCENE_BOOST` (par exemple 3,5 et 20 pour environ −3 dB).
