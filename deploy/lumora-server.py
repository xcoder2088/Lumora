#!/usr/bin/env python3
"""Petit serveur web local de Lumora : sert un dossier, comme « python3 -m http.server », mais avec des en-têtes de cache.

La page, le service worker et le manifeste ne sont jamais gardés par Cloudflare ni par le navigateur sans vérification,
pour que chaque nouvelle version arrive seule. Les images, sons et icônes sont gardés une journée.

Usage : lumora-server.py PORT DOSSIER      (n'écoute que sur 127.0.0.1 ; le tunnel Cloudflare le rend public)
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

SANS_CACHE = ('/', '/index.html', '/sw.js', '/manifest.webmanifest')
UNE_JOURNEE = ('/assets/', '/audio/', '/icons/')


class Gestionnaire(SimpleHTTPRequestHandler):
    def end_headers(self):
        chemin = self.path.split('?', 1)[0]
        if chemin in SANS_CACHE:
            self.send_header('Cache-Control', 'public, max-age=0, must-revalidate')
        elif chemin.startswith(UNE_JOURNEE):
            self.send_header('Cache-Control', 'public, max-age=86400')
        super().end_headers()


if __name__ == '__main__':
    port, dossier = int(sys.argv[1]), sys.argv[2]
    ThreadingHTTPServer(('127.0.0.1', port), partial(Gestionnaire, directory=dossier)).serve_forever()
