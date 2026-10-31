# Mettre Lumora en ligne sur lumora.pixeldrop.ca

Principe : Lumora est un site statique (une page, des images, des sons). Il tourne sur **le même serveur que PixelDrop**, derrière **le même tunnel Cloudflare** : un petit serveur local sur le port **8791** (jamais exposé directement), et le tunnel le rend public en HTTPS sous `lumora.pixeldrop.ca`. Aucun nouveau tunnel.

> **À vérifier d'abord :** toutes les commandes ci-dessous se lancent **sur la machine où tourne le tunnel de pixeldrop.ca** (celle où tourne le service `pixeldrop`). D'après le dépôt PixelDrop, on s'y connecte avec `ssh ubuntu@148.116.71.199` (c'est l'adresse écrite dans `deploy.sh`). Si ce n'est pas la bonne machine, utilise celle où `cloudflared` tourne pour pixeldrop.ca (commande de vérification : `ps aux | grep [c]loudflared`).
> Ports déjà pris sur cette machine : 8123 (PixelDrop). Si `ss -ltn | grep 8791` montre quelque chose, choisis un autre port (à changer dans les trois fichiers `deploy/`).

## Ce qui est prêt dans le dépôt
- `tools/build_site.py` : prépare le dossier `dist` (la page, les sons, les images .webp : ≈ 18,5 Mo).
- `deploy/installer-sur-serveur.sh` : prépare le site, le copie dans `/var/www/lumora` (garde l'ancienne version dans `/var/www/lumora.old`), installe et démarre le service.
- `deploy/lumora-web.service` : le petit serveur local (127.0.0.1:8791, jamais exposé directement).
- `deploy/cloudflared-ingress.example.yml` : la ligne à ajouter au tunnel.

## 1. Sur le serveur : installer le site
```bash
git clone https://github.com/xcoder2088/lumora ~/lumora      # la première fois seulement
cd ~/lumora && git pull
bash deploy/installer-sur-serveur.sh
```
Le script affiche `Test local : HTTP 200` quand tout va bien. (Python 3 doit être installé : c'est le cas sur la plupart des Linux.)

## 2. Ajouter Lumora au tunnel existant (une seule fois)
1. Trouve le fichier de configuration du tunnel : `ps aux | grep [c]loudflared` (le chemin du fichier .yml apparaît après `--config`) ou `sudo systemctl cat 'cloudflared*'`. Si le tunnel est géré depuis le tableau de bord Cloudflare (Zero Trust → Networks → Tunnels → ton tunnel → **Published application routes**), ajoute simplement une route : sous-domaine `lumora`, domaine `pixeldrop.ca`, service `HTTP`, URL `127.0.0.1:8791`, et saute le point 2 et 3 (le DNS est créé automatiquement).
2. Sinon, ouvre ce fichier. Dans la liste `ingress:`, ajoute ce bloc **avant** la dernière ligne (celle qui ressemble à `- service: http_status:404`), sans rien supprimer d'autre :
```yaml
  - hostname: lumora.pixeldrop.ca
    service: http://127.0.0.1:8791
```
3. Relance le tunnel : `sudo systemctl restart <nom-du-service-cloudflared>` (le nom vu à l'étape 1).

## 3. DNS (une seule fois)
Seulement si tu as édité le fichier de configuration à la main (pas besoin avec le tableau de bord). Le domaine `pixeldrop.ca` est dans ton compte Cloudflare.
1. Cloudflare → **pixeldrop.ca** → **DNS** → **Records** → **Add record**.
2. Type **CNAME**, nom **lumora**, cible **`<UUID-du-tunnel>.cfargotunnel.com`**, **Proxied** (nuage orange), TTL Auto.
3. L'UUID est la ligne `tunnel:` du même fichier de configuration (ce n'est pas un secret). Ou, à la place des points 1 et 2 : `cloudflared tunnel route dns <UUID> lumora.pixeldrop.ca`.
4. Ouvre https://lumora.pixeldrop.ca (parfois quelques minutes d'attente).

## Mettre à jour plus tard
```bash
cd ~/lumora && git pull && bash deploy/installer-sur-serveur.sh
```
Cloudflare garde l'ancienne page en cache : si besoin, **Caching → Purge Everything**.
Retour arrière : `sudo rm -rf /var/www/lumora && sudo mv /var/www/lumora.old /var/www/lumora`.

## Bon à savoir
- Le site est visible tant que le serveur est allumé et connecté (comme PixelDrop). Alternative toujours en ligne, indépendante du serveur : Cloudflare Pages (gratuit, branché sur GitHub). Dis-le-moi si tu veux cette procédure.
- Les polices viennent de Google Fonts (connexion Internet nécessaire à l'ouverture ; sinon police de secours).
- Le son ne démarre qu'après un clic (règle des navigateurs) : déjà prévu.
- `_headers` ne sert que pour Cloudflare Pages ; il est ignoré par ce serveur local.
