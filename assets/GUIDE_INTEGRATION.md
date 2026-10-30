# Lumora — illustrations séparées, validation v1

Illustrations produites avec l'aide d'un outil d'intelligence artificielle, sans photographie, personnage ou œuvre de référence importée. Les demandes exactes sont conservées dans `prompts.json`. Les générations brutes sont conservées dans la livraison de travail hors dépôt et ne sont pas dupliquées ici; les exports ci-dessous sont redimensionnés, alignés et convertis pour la livraison. Aucune intégration dans une application n'a été effectuée.

## Contenu

- **22 éléments de méduses** : trois types, chacun avec quatre ombrelles de pulsation, un groupe de bras oraux et une lueur interne; un filament et trois grappes de tentacules partagés entre les types.
- **15 éléments de papillons** : monarque, morpho bleu, azuré commun, machaon et Actias luna; pour chaque espèce, aile avant gauche, aile arrière gauche, corps avec antennes. Les côtés droits se construisent par symétrie.
- **4 calques de décor** : eau profonde, ciel de prairie, collines transparentes et herbes transparentes. Tous sont exportés en 2560 × 1440. Eau et ciel sont volontairement opaques, avec un canal alpha à 255.

Les fichiers `.png` de `meduses/`, `papillons/` et `decors/` : PNG truecolor **RGBA 8 bits par canal**, soit 32 bits, avec indication sRGB. Les sprites de créatures ont un canevas de 1024 × 1024 avec marges; leur partie visible ne remplit pas nécessairement toute la largeur.

Les fichiers `.webp`, à côté des PNG : mêmes dimensions et alpha. Méduses en WebP sans perte pour conserver des canaux R=V=B strictement égaux; autres éléments compressés avec pertes et alpha conservé. Le poids des fichiers de chaque format est mesuré dans `manifest.json`.

Poids mesurés (Mo décimaux) : **5,46 Mo pour les 41 WebP** — univers méduses complet **2,87 Mo**, univers prairie complet **2,59 Mo**. Les 41 PNG de référence totalisent **26,76 Mo**; leur fidélité a été conservée et ils dépassent donc le budget léger. Les aperçus et les fichiers de documentation ne font pas partie du budget des images à charger. Les variantes PNG et WebP sont deux jeux alternatifs, à ne pas charger ensemble.

Les décors ont été générés en 1672 × 941 puis rééchantillonnés en 2560 × 1440; il ne s'agit pas de générations natives à cette dernière définition. Les créatures ont été générées sur des canevas d'environ 1254 × 1254 puis normalisées pour la livraison.

`planche-contact.png` : tous les éléments, sur un fond bleu-gris de lecture qui n'est pas incorporé aux sprites. `apercus/apercu-ambiances.jpg` : décors assemblés pour contrôler les calques. Ces aperçus et les originaux ne font pas partie du poids des images à charger dans l'application.

## Animation et assemblage

Les quatre états d'une ombrelle ont exactement le même canevas et le même pivot **(512, 760)** en pixels, origine en haut à gauche. Ordre de boucle proposé : **01 → 02 → 03 → 04 → 03 → 02 → 01**. Les états sont des illustrations distinctes : un fondu croisé est recommandé; un morphing de géométrie exact entre pixels n'est pas fourni. Les largeurs diminuent progressivement et les hauteurs augmentent sans déplacer le point d'attache.

Les méduses sont exportées en gris strict avec un alpha partiel. Le canal alpha des ombrelles est plafonné pour préserver la sensation translucide. Pour les teinter, multiplier leur RGB par la couleur choisie et conserver l'alpha; ne pas employer un fond noir comme masque. L'alpha est **non prémultiplié**. Les organes peuvent être superposés avec une opacité modérée; le mode additif est facultatif et à doser doucement.

Le filament est une texture **à étirer ou à déformer**. Son dessin n'est pas garanti raccordable bout à bout : une répétition sans raccord demanderait une variante dédiée. Les grappes sont prêtes à être déplacées et légèrement déformées par le code.

Pour les papillons, placer les ailes arrière derrière les ailes avant, puis le corps au-dessus. Les pivots d'ailes dans le manifeste sont des repères estimés sur le contour, **à ajuster à l'assemblage**. Les motifs sont des interprétations inspirées des espèces; ce ne sont pas des planches d'identification scientifique. Actias luna est un papillon nocturne avec des antennes plumeuses.

Les collines et les herbes partagent le canevas 2560 × 1440 du ciel : les superposer sans recadrage individuel. Ordre : ciel → collines → créatures → herbes.

## Contrôles et limites

Contrôles de livraison : présence des 41 éléments, dimensions, PNG RGBA truecolor, sRGB, transparence réelle des sprites et des deux calques de paysage, alpha partiel et neutralité exacte des méduses, conservation des pointes d'ailes et des queues à l'export. Les pixels totalement transparents des PNG sont mis à RGB zéro pour éviter un matte blanc.

La validation visuelle par le créateur de Lumora reste nécessaire avant intégration. Les textures animées n'ont pas été testées dans son moteur de rendu; la fluidité des fondus et le réglage des pivots des papillons restent à vérifier dans ce contexte. Les PNG sont les exports de référence; le budget léger vise le chargement des WebP, pas le cumul des deux jeux de fichiers ni les archives et aperçus.

`verification.json` consigne les contrôles des fichiers décodés et des archives, dont la conservation exacte de l'alpha dans les WebP et l'identité des pixels des méduses dans les deux formats. Un aperçu animé séparé `apercus/controle-pulsation.webp` montre les trois méduses assemblées et teintées; ce fichier de contrôle est hors du lot à charger dans l'application.

## Usage

Voir `LICENCE.md`.


## Intégration dans l'application

Les fichiers sont livrés uniquement sous `assets/`. La page courante, les sons, les outils audio et la référence `versions/v1-canvas/` ne sont pas modifiés par cette livraison.

Charger `assets/manifest.json`. Ses chemins `png` et `webp` sont relatifs au dossier `assets/`; depuis `index.html`, préfixer les chemins par `assets/`. Le WebP est le jeu léger conseillé; ne pas charger systématiquement les deux variantes.

Les pivots sont exprimés dans les pixels du canevas, origine en haut à gauche. Pour dessiner une pièce à l'échelle `s` autour d'une attache `(x, y)`, son coin supérieur gauche se place à `(x - pivotX*s, y - pivotY*s)`. Le pivot commun des ombrelles est `(512, 760)`. Les pivots des bras sont en haut de leur propre canevas. Les lueurs se positionnent dans la cloche; leurs repères ne sont pas ceux du centre anatomique. Les pivots des ailes sont des estimations, particulièrement à vérifier sur les ailes arrière à longue queue.

Lire les états d'ombrelle `01, 02, 03, 04, 03, 02`, avec un fondu croisé entre états. Conserver le canal alpha pendant la teinte des méduses. Pour les papillons, symétriser les deux ailes gauches autour de leur pivot et placer le corps au-dessus. Préserver les motifs naturels; ces images ne sont pas des références scientifiques exactes.

Cette livraison reste une version de validation visuelle. L'aperçu animé est un contrôle d'assemblage, pas une preuve de fonctionnement dans l'application. L'intégration et les essais sur les navigateurs cibles restent à effectuer après validation.
