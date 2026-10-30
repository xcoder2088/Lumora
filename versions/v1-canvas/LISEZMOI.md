# Lumora, version 1 (dessinée par le code)

Copie **figée** de la première version complète de Lumora, faite le 30 octobre 2026. Les méduses et les papillons sont dessinés par le code (canvas 2D), sans images.

**Ne pas modifier ce dossier.** Il sert de sauvegarde et de point de comparaison quand une nouvelle version (avec des illustrations) sera prête. Pour revenir exactement à cet état du dépôt : `git checkout reference-v1` (branche qui ne doit plus recevoir de changement).

Il fonctionne seul : `index.html` et le dossier `audio/` de ce dossier suffisent. Comme la page charge du son, il faut la servir par un serveur web, par exemple, depuis ce dossier :

```bash
python3 -m http.server 8000
```

puis ouvrir <http://localhost:8000>.

Licence : GNU GPL v3 (voir le fichier `LICENSE` à la racine du dépôt). Sons : CC0, crédits dans le `README.md` à la racine.
