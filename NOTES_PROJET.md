# Lumora — notes de reprise du projet

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

## À FAIRE EN PRIORITÉ (session avec accès SSH à l'ordinateur du propriétaire)
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
