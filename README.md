# Cozybat — site cozybat.fr

- `public/` : le site tel qu'il est en ligne (généré, ne pas modifier à la main).
- `_build/` : générateur. `cd _build && python3 build.py` régénère `public/`.
  - `build.py` : gabarits des pages, villes, prix, SEO, .htaccess, sitemap.
  - `donnees.py` : couches du système 3D, chantiers, avis, FAQ.
  - `guides.py` : contenu des guides (`/guides/...`).
  - `style.css` : feuille de style source (minifiée vers `public/assets/css/site.min.css`).
- `.github/workflows/deploy.yml` : mise en ligne automatique sur Hostinger (FTP) à chaque modification de `public/` sur `main`.
- `archive-ancien-site/` : ancienne version du site, conservée pour mémoire (non publiée).

Dépendance du générateur : Python 3 et Pillow (`pip install pillow`).

## Ajouter un guide
Ajouter un `dict(...)` dans `GUIDES` (fichier `_build/guides.py`) : slug, titre ≤ 60 caractères,
description ≤ 155 caractères, h1, intro, sections, faq, related. Puis `python3 build.py`.
Les prix et les règles d'aides doivent être vérifiés à la date de publication.
