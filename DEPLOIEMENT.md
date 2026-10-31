# Mettre Lumora en ligne sur lumora.pixeldrop.ca (Cloudflare Pages)

Lumora est un site tout simple : une page, des images et des sons. Aucun serveur à gérer.
Cloudflare Pages va lire le dépôt GitHub, préparer le site, puis le publier à l'adresse voulue.
Chaque fois que le dépôt change (branche `main`), le site se met à jour tout seul.

## Ce qui est déjà prêt dans le dépôt
- `tools/build_site.py` : prépare un dossier `dist` qui contient seulement l'utile (la page, les sons, les images `.webp`). Résultat : environ 18 Mo au lieu de 80 Mo. Les notes, les anciennes versions et les images en double ne sont pas publiées.
- `_headers` : réglages envoyés avec chaque fichier (sécurité de base, et la page se rafraîchit toujours quand on la rouvre).

## Étapes (une seule fois)

### A. Créer le projet
1. Va sur https://dash.cloudflare.com et connecte-toi.
2. Dans le menu de gauche : **Workers & Pages** (ou « Compute (Workers) » selon l'affichage).
3. Clique **Create** (ou « Créer une application »), puis choisis l'onglet **Pages**, puis **Import an existing Git repository** (« Se connecter à Git »).
4. Choisis **GitHub**. Cloudflare demande l'autorisation d'accéder à ton compte GitHub : accepte, et donne accès au dépôt **xcoder2088/lumora** seulement.
5. Sélectionne le dépôt `lumora`, puis **Begin setup**.

### B. Réglages du projet
Remplis exactement ceci :

| Champ | Valeur |
|---|---|
| Project name | `lumora` |
| Production branch | `main` |
| Framework preset | `None` |
| Build command | `python3 tools/build_site.py` |
| Build output directory | `dist` |

Laisse le reste vide, puis clique **Save and Deploy**. Après une ou deux minutes, Cloudflare te donne une adresse de test du genre `lumora.pages.dev`. Ouvre-la et vérifie que Lumora fonctionne.

### C. Brancher lumora.pixeldrop.ca
1. Dans le projet `lumora` : onglet **Custom domains**, puis **Set up a custom domain**.
2. Écris : `lumora.pixeldrop.ca`, puis continue.
3. Deux cas :
   - **pixeldrop.ca est déjà dans ton compte Cloudflare** (son DNS est géré par Cloudflare) : Cloudflare ajoute tout seul la ligne DNS. Clique pour confirmer.
   - **pixeldrop.ca est ailleurs** : Cloudflare te donne une ligne à ajouter chez ton fournisseur de domaine : type **CNAME**, nom `lumora`, valeur `lumora.pages.dev`.
4. Attends quelques minutes (parfois jusqu'à une heure). Le statut passe à **Active**. Le certificat HTTPS (le cadenas) est créé automatiquement.

## Au quotidien
- Pour mettre à jour le site : modifier `index.html` (ou les images, les sons), enregistrer dans GitHub sur `main`. Cloudflare republie en environ une minute.
- Les anciennes versions restent consultables dans l'onglet **Deployments** du projet, avec un bouton pour revenir en arrière.
- Pour tester le site préparé sur ton ordinateur : `python3 tools/build_site.py`, puis `cd dist` et `python3 -m http.server 8000`, puis ouvrir http://localhost:8000.

## Bon à savoir
- Les polices de caractères viennent de Google Fonts : il faut une connexion Internet à l'ouverture. Si la connexion manque, une police de secours s'affiche et tout fonctionne.
- Le son ne démarre qu'après un clic de l'éducatrice (règle des navigateurs). C'est déjà prévu.
- Sur iPhone et tableau blanc, ouvrir l'adresse en **https** (Cloudflare le fait automatiquement).
- Le dossier `dist` est recréé à chaque publication : ne jamais le modifier à la main (il est ignoré par Git).
- Les limites gratuites de Cloudflare Pages (500 publications par mois, 20 000 fichiers, 25 Mo par fichier) sont très au-dessus des besoins de Lumora (70 fichiers, le plus gros fait moins de 5 Mo).
