#!/usr/bin/env bash
# À lancer SUR LE SERVEUR, depuis une copie à jour du dépôt Lumora :  bash deploy/installer-sur-serveur.sh
# Prépare le site, le copie dans /var/www/lumora (en gardant l'ancienne version), installe et démarre le petit serveur.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build_site.py
sudo rm -rf /var/www/lumora.new
sudo mkdir -p /var/www
sudo cp -r dist /var/www/lumora.new
sudo chown -R root:root /var/www/lumora.new
sudo chmod -R a+rX /var/www/lumora.new
sudo rm -rf /var/www/lumora.old
[ -d /var/www/lumora ] && sudo mv /var/www/lumora /var/www/lumora.old
sudo mv /var/www/lumora.new /var/www/lumora
sudo install -d -o root -g root -m 755 /usr/local/share/lumora
sudo install -o root -g root -m 644 deploy/lumora-server.py /usr/local/share/lumora/lumora-server.py
sudo install -o root -g root -m 644 deploy/lumora-web.service /etc/systemd/system/lumora-web.service
sudo systemctl daemon-reload
sudo systemctl enable --now lumora-web
sudo systemctl restart lumora-web
sleep 1
curl -fsS -o /dev/null -w "Test local : HTTP %{http_code}\n" http://127.0.0.1:8791/
echo "Site installé. Il reste, une seule fois : ajouter l'entrée au tunnel et le DNS (voir DEPLOIEMENT.md, étapes 2 et 3)."
