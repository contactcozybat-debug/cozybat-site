# Cozybat — site cozybat.fr

- La racine du dépôt est le site tel qu'il est en ligne (généré, ne pas modifier à la main).
  Hostinger (hPanel > Git) déploie automatiquement la branche `main` dans `domains/cozybat.fr/public_html`.
- `_build/` : générateur. `cd _build && python3 build.py` régénère le site à la racine.
  - `build.py` : gabarits des pages, villes, prix, SEO, .htaccess, sitemap.
  - `donnees.py` : couches du système 3D, chantiers, avis, FAQ.
  - `guides.py` : contenu des guides (`/guides/...`).
  - `style.css` : feuille de style source (minifiée vers `assets/css/site.min.css`).
- `_build/`, `.git/`, `README.md` sont bloqués par le `.htaccess` (jamais servis).

Dépendance du générateur : Python 3 et Pillow (`pip install pillow`).

## Ajouter un guide
Ajouter un `dict(...)` dans `GUIDES` (fichier `_build/guides.py`) : slug, titre ≤ 60 caractères,
description ≤ 155 caractères, h1, intro, sections, faq, related. Puis `python3 build.py`.
Les prix et les règles d'aides doivent être vérifiés à la date de publication.
