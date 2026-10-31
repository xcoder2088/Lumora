# Mettre Lumora en ligne sur lumora.pixeldrop.ca

Même méthode que PhoenixWire (wire.phoenixmail.ca) : le site tourne sur le portable, et le **tunnel Cloudflare déjà en place** le rend public, avec le HTTPS. Aucun nouveau tunnel. Lumora n'est qu'un site statique (une page, des images, des sons) : un tout petit serveur local suffit.

Ports déjà pris sur le portable : 8788 (phoenixmail-web), 8790 (PhoenixWire), 8099 (claim). Lumora utilise **8791**.

## Ce qui est prêt dans le dépôt
- `tools/build_site.py` : prépare le dossier `dist` (la page, les sons, les images .webp : ≈ 18,5 Mo).
- `deploy/installer-sur-portable.sh` : prépare le site, le copie dans `/var/www/lumora` (garde l'ancienne version dans `/var/www/lumora.old`), installe et démarre le service.
- `deploy/lumora-web.service` : le petit serveur local (127.0.0.1:8791, jamais exposé directement).
- `deploy/cloudflared-ingress.example.yml` : la ligne à ajouter au tunnel.

## 1. Sur le portable : installer le site
```bash
git clone https://github.com/xcoder2088/lumora ~/lumora      # la première fois seulement
cd ~/lumora && git pull
bash deploy/installer-sur-portable.sh
```
Le script affiche `Test local : HTTP 200` quand tout va bien. (Python 3 doit être installé : c'est le cas sur la plupart des Linux.)

## 2. Ajouter Lumora au tunnel existant (une seule fois)
1. Trouve le fichier de configuration du tunnel : `sudo systemctl cat cloudflared-phoenixmail` (cherche la ligne avec `--config` ou le chemin du fichier .yml).
2. Ouvre ce fichier. Dans la liste `ingress:`, ajoute ce bloc **avant** la dernière ligne (celle qui ressemble à `- service: http_status:404`), sans rien supprimer d'autre :
```yaml
  - hostname: lumora.pixeldrop.ca
    service: http://127.0.0.1:8791
```
3. Relance le tunnel : `sudo systemctl restart cloudflared-phoenixmail`.

## 3. DNS (une seule fois)
Le domaine `pixeldrop.ca` est dans le même compte Cloudflare que `phoenixmail.ca` : tout se fait au même endroit.
1. Cloudflare → **pixeldrop.ca** → **DNS** → **Records** → **Add record**.
2. Type **CNAME**, nom **lumora**, cible **`<UUID-du-tunnel>.cfargotunnel.com`**, **Proxied** (nuage orange), TTL Auto.
3. L'UUID est la ligne `tunnel:` du même fichier de configuration (ce n'est pas un secret). Ou, à la place des points 1 et 2 : `cloudflared tunnel route dns <UUID> lumora.pixeldrop.ca`.
4. Ouvre https://lumora.pixeldrop.ca (parfois quelques minutes d'attente).

## Mettre à jour plus tard
```bash
cd ~/lumora && git pull && bash deploy/installer-sur-portable.sh
```
Cloudflare garde l'ancienne page en cache : si besoin, **Caching → Purge Everything**.
Retour arrière : `sudo rm -rf /var/www/lumora && sudo mv /var/www/lumora.old /var/www/lumora`.

## Bon à savoir
- Le site n'est visible que si le **portable est allumé** et connecté (comme PhoenixWire). Pour un site toujours en ligne, même portable éteint, il existe l'hébergement Cloudflare Pages (gratuit, branché sur GitHub). Dis-le-moi si tu veux que j'écrive cette procédure.
- Les polices viennent de Google Fonts (connexion Internet nécessaire à l'ouverture ; sinon police de secours).
- Le son ne démarre qu'après un clic (règle des navigateurs) : déjà prévu.
- `_headers` ne sert que pour Cloudflare Pages ; il est ignoré par ce serveur local.
