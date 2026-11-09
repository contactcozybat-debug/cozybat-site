#!/usr/bin/env python3
"""Génère le site Cozybat (pages HTML statiques) à la racine du dépôt — version optimisée SEO.
Données (couches, chantiers, avis, FAQ) : donnees.py. Lancer : python3 build.py
"""
import json, os, re, html, time
from datetime import date
from PIL import Image
import donnees as D
from guides import GUIDES
import maconnerie
GBY = {g['slug']: g for g in GUIDES}

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(ROOT)  # racine du dépôt = racine du site (déployée par Hostinger Git)
DOMAIN = 'https://cozybat.fr'
TEL, TEL_H = '+33619425151', '06 19 42 51 51'
MAIL = 'contact.cozybat@gmail.com'
IG = 'https://www.instagram.com/cozybat_renovation/'
GOOGLE = 'https://share.google/EaXcsYWDln5izOgJN'
ADR = dict(street='6 avenue Évariste Galois', cp='91420', city='Morangis')
ADR_TXT = '6 avenue Évariste Galois, 91420 Morangis'
SIRET, SIRET_H = '99311278800019', '993 112 788 00019'
RGE = 'E-E213612'
TODAY = date.today().isoformat()
MOIS = ['janvier','février','mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre'][date.today().month-1] + ' ' + str(date.today().year)
import hashlib
VER = hashlib.md5(b''.join(open(os.path.join(ROOT, f), 'rb').read() for f in ('style.css', '../assets/js/site.js', '../assets/js/stack.js'))).hexdigest()[:10]
e = html.escape

# ------------------------------------------------------------------ chantiers (noms de fichiers en mots-clés)
CH = {
  'isolation-exterieure-ollainville': dict(old='ite-ollainville', city='ollainville'),
  'isolation-exterieure-saint-michel-sur-orge': dict(old='ite-saint-michel-sur-orge', city='saint-michel-sur-orge'),
  'isolation-lucarnes-sainte-genevieve-des-bois': dict(old='ite-lucarnes-sainte-genevieve-des-bois', city='sainte-genevieve-des-bois'),
  'ravalement-facade-morangis': dict(old='ravalement-morangis', city='morangis'),
  'ravalement-facade-yerres': dict(old='ravalement-yerres', city='yerres'),
  'ravalement-facade-brunoy': dict(old='ravalement-brunoy', city='brunoy'),
}
OLD2NEW = {v['old']: k for k, v in CH.items()}
CHANTIERS = []
for c in D.CHANTIERS:
    c = dict(c); c['old'] = c['slug']; c['slug'] = OLD2NEW[c['slug']]; c['cityslug'] = CH[c['slug']]['city']
    c['work'] = 'Isolation par l’extérieur' if c['type'] == 'ite' else 'Ravalement de façade'
    CHANTIERS.append(c)
BYSLUG = {c['slug']: c for c in CHANTIERS}

# ------------------------------------------------------------------ pages villes (textes propres à chaque commune)
CITIES = [
  dict(slug='morangis', name='Morangis', cp='91420', own=['ravalement-facade-morangis'], near=['isolation-lucarnes-sainte-genevieve-des-bois', 'isolation-exterieure-saint-michel-sur-orge'],
       intro=['Cozybat est installée à Morangis : nos locaux du 6 avenue Évariste Galois accueillent les rendez-vous clients, et l’équipe intervient chaque semaine sur les maisons de la commune, en isolation par l’extérieur comme en ravalement de façade.',
              'Être à quelques rues de votre maison, c’est une visite technique organisée rapidement, des réponses le jour même pendant le chantier et un interlocuteur que vous pouvez venir voir. Nous connaissons aussi les démarches à faire auprès de la mairie de Morangis avant de modifier l’aspect d’une façade.'],
       tip_t='Un ravalement D3 armé à Morangis', tip=['Sur la façade de Morangis présentée ci-dessous, l’enduit d’origine était délavé et encrassé. Après lavage et préparation du support, un enduit armé d’un filet en fibre de verre a été appliqué sur toute la surface, puis une finition en deux teintes.',
              'C’est la solution adaptée quand les murs sont sains mais la façade fatiguée : sans isolant, elle traite les microfissures et redonne un aspect neuf pour longtemps.']),
  dict(slug='savigny-sur-orge', name='Savigny-sur-Orge', cp='91600', own=[], near=['ravalement-facade-morangis', 'isolation-exterieure-saint-michel-sur-orge'],
       intro=['Savigny-sur-Orge est une grande commune pavillonnaire, des quartiers proches de l’Orge jusqu’aux hauteurs. Beaucoup de maisons y ont des façades enduites qui, avec les années, ont pris des fissures, des coulures et des salissures.',
              'Nous intervenons à Savigny-sur-Orge depuis Morangis, la commune voisine, pour deux types de travaux : l’isolation thermique par l’extérieur, qui isole la maison et refait la façade en même temps, et le ravalement D3 armé, qui rénove une façade fissurée sans ajouter d’isolant.'],
       tip_t='Isoler ou seulement ravaler ?', tip=['Si la maison est froide l’hiver ou chère à chauffer, l’isolation par l’extérieur est l’investissement le plus utile : elle traite les murs en continu et peut être aidée par les primes CEE, car nous sommes qualifiés RGE.',
              'Si la maison est déjà bien isolée et que seule la façade est abîmée, un ravalement D3 armé suffit. Le questionnaire de notre page d’accueil vous oriente en trois questions, et la visite technique gratuite permet de trancher sur place.']),
  dict(slug='athis-mons', name='Athis-Mons', cp='91200', own=[], near=['ravalement-facade-morangis', 'isolation-exterieure-ollainville'],
       intro=['À Athis-Mons, une partie de la commune vit avec la proximité de l’aéroport d’Orly. Pour beaucoup de propriétaires, rénover la façade est l’occasion d’améliorer à la fois le confort thermique et le calme à l’intérieur.',
              'Cozybat intervient à Athis-Mons depuis Morangis, juste à côté, pour l’isolation par l’extérieur et le ravalement de façade : visite technique, devis détaillé couche par couche et chantier suivi par les associés eux-mêmes.'],
       tip_t='L’isolation par l’extérieur, aussi pour le confort acoustique', tip=['Le choix de l’isolant compte. Le polystyrène graphité est le plus performant thermiquement à épaisseur égale, tandis que la laine de roche et la fibre de bois apportent en plus un meilleur affaiblissement des bruits extérieurs.',
              'Lors de la visite, nous vous présentons les deux options avec leur épaisseur, leur coût et leur effet sur les aides, pour choisir en connaissance de cause.']),
  dict(slug='juvisy-sur-orge', name='Juvisy-sur-Orge', cp='91260', own=[], near=['ravalement-facade-morangis', 'ravalement-facade-brunoy'],
       intro=['Juvisy-sur-Orge compte de nombreuses maisons anciennes, avec des façades en meulière, en brique ou en enduit traditionnel. Rénover ces façades demande de respecter leur caractère tout en traitant les fissures et l’usure.',
              'Nous intervenons à Juvisy-sur-Orge pour le ravalement de façade et l’isolation par l’extérieur, en vous conseillant sur la solution qui préserve le mieux l’aspect de votre maison.'],
       tip_t='Façade ancienne : rénover sans dénaturer', tip=['Une isolation par l’extérieur recouvre la façade d’un nouvel enduit : elle change donc l’aspect d’une meulière ou d’une brique apparente. Sur ces maisons, nous proposons selon les cas une isolation des seules façades enduites, ou un ravalement qui conserve les éléments de caractère.',
              'Tout changement d’aspect de façade doit être déclaré en mairie (déclaration préalable de travaux) et respecter le PLU de Juvisy-sur-Orge. Nous vous aidons à constituer le dossier.']),
  dict(slug='sainte-genevieve-des-bois', name='Sainte-Geneviève-des-Bois', cp='91700', own=['isolation-lucarnes-sainte-genevieve-des-bois'], near=['isolation-exterieure-saint-michel-sur-orge'],
       intro=['À Sainte-Geneviève-des-Bois, nous avons notamment isolé par l’extérieur les lucarnes d’une maison dont la brique apparente était restée sans protection. Un chantier typique des maisons de la commune, avec des combles aménagés et des façades à plusieurs niveaux.',
              'Nous intervenons à Sainte-Geneviève-des-Bois pour l’isolation thermique par l’extérieur et le ravalement de façade, de la visite technique à la réception du chantier.'],
       tip_t='Isoler les lucarnes et les chiens-assis', tip=['Les lucarnes sont souvent les parties les moins bien isolées d’une maison : petites surfaces, angles nombreux, raccords avec la toiture. Elles demandent des découpes précises de l’isolant et un traitement soigné des angles et des appuis.',
              'Bien isolées, elles suppriment les pièces froides sous les toits et s’intègrent à la teinte du reste de la façade.']),
  dict(slug='saint-michel-sur-orge', name='Saint-Michel-sur-Orge', cp='91240', own=['isolation-exterieure-saint-michel-sur-orge'], near=['isolation-lucarnes-sainte-genevieve-des-bois', 'isolation-exterieure-ollainville'],
       intro=['À Saint-Michel-sur-Orge, nous avons isolé par l’extérieur une maison sur deux niveaux dont l’étage, ajouté plus tard, était resté en brique apparente. La surélévation et l’ancien enduit ont disparu sous un même enduit neuf, sans démarcation.',
              'Nous intervenons à Saint-Michel-sur-Orge pour l’isolation thermique par l’extérieur et le ravalement de façade, avec une équipe qui pose elle-même le système, du collage à la finition.'],
       tip_t='Maison agrandie ou surélevée : une seule façade', tip=['Quand une maison a été agrandie, les murs d’origine et l’extension ne sont souvent ni du même matériau ni du même aspect. L’isolation par l’extérieur unifie l’ensemble : un seul isolant, un seul enduit armé et une seule teinte sur toute la maison.',
              'C’est aussi le moment de traiter les jonctions entre ancien et nouveau, souvent à l’origine de fissures.']),
  dict(slug='epinay-sur-orge', name='Épinay-sur-Orge', cp='91360', own=[], near=['isolation-exterieure-saint-michel-sur-orge', 'isolation-lucarnes-sainte-genevieve-des-bois'],
       intro=['À Épinay-sur-Orge comme dans une grande partie de l’Essonne, les maisons sont construites sur des sols argileux qui gonflent et se rétractent selon les saisons. Résultat fréquent : des fissures en façade, plus ou moins importantes.',
              'Nous intervenons à Épinay-sur-Orge pour le ravalement de façade D3 armé et l’isolation par l’extérieur, en commençant toujours par un diagnostic des fissures lors de la visite technique gratuite.'],
       tip_t='Fissures de façade : savoir les lire', tip=['Les microfissures et les fissures fines de l’enduit sont traitées par un ravalement armé : le filet en fibre de verre noyé dans l’enduit ponte les fissures et limite leur réapparition.',
              'Les fissures larges, en escalier ou qui évoluent peuvent révéler un mouvement de la structure : elles relèvent d’un diagnostic spécifique avant tout ravalement. Nous vous le disons clairement lors de la visite.']),
  dict(slug='chilly-mazarin', name='Chilly-Mazarin', cp='91380', own=[], near=['ravalement-facade-morangis', 'isolation-exterieure-ollainville'],
       intro=['À Chilly-Mazarin, de nombreuses maisons sont mitoyennes ou construites en limite de propriété. Rénover ou isoler une façade y demande d’anticiper les raccords avec le voisin et l’emprise des travaux.',
              'Nous intervenons à Chilly-Mazarin, à quelques minutes de nos locaux de Morangis, pour l’isolation thermique par l’extérieur et le ravalement de façade.'],
       tip_t='Maison mitoyenne ou en limite de propriété', tip=['Pour une isolation par l’extérieur d’un mur en limite de propriété, la loi prévoit, sous conditions, un droit de surplomb du terrain voisin de 35 cm au plus, au-dessus de 2 m du sol. Il faut en informer le voisin avant les travaux.',
              'Sur une maison mitoyenne, nous soignons le raccord avec la façade voisine et l’arrêt de l’isolant, pour un résultat propre et étanche.']),
  dict(slug='ollainville', name='Ollainville', cp='91340', own=['isolation-exterieure-ollainville'], near=['isolation-exterieure-saint-michel-sur-orge'],
       intro=['À Ollainville, nous avons isolé par l’extérieur une maison individuelle avec 140 mm de polystyrène graphité. L’ancien crépi a disparu sous un enduit neuf, lisse et blanc : la maison a changé d’aspect et elle est isolée sur toutes ses façades.',
              'Nous intervenons à Ollainville et dans les communes voisines du secteur d’Arpajon pour l’isolation thermique par l’extérieur et le ravalement de façade, de la visite technique gratuite à la réception du chantier.'],
       tip_t='Quelle épaisseur d’isolant choisir ?', tip=['Pour être éligibles aux primes CEE, les murs isolés doivent atteindre une résistance thermique d’au moins 3,7 m².K/W. Avec un polystyrène graphité, cela correspond en général à 120 à 140 mm d’épaisseur.',
              'Aller jusqu’à 160 ou 200 mm améliore encore le confort, mais demande d’adapter davantage les appuis de fenêtre et les débords de toiture. Nous comparons les options lors de la visite.']),
  dict(slug='yerres', name='Yerres', cp='91330', own=['ravalement-facade-yerres'], near=['ravalement-facade-brunoy'],
       intro=['À Yerres, nous avons repris en ravalement D3 armé une façade grise et tachée. Après préparation du support, un enduit armé d’un filet a été appliqué sur toute la surface, avec une finition beige. Les câbles qui couraient sur la façade sont désormais dissimulés sous des moulures blanches.',
              'Nous intervenons à Yerres et dans le Val d’Yerres pour le ravalement de façade et l’isolation thermique par l’extérieur.'],
       tip_t='Câbles et éléments en façade : le bon moment pour les reprendre', tip=['Câbles électriques ou téléphoniques, boîtiers, descentes d’eau : un ravalement est l’occasion de remettre de l’ordre sur la façade. Les câbles peuvent être dissimulés sous des moulures ou des goulottes dans la teinte choisie.',
              'Le déplacement d’un câble du réseau (électricité, téléphone) relève en revanche de l’opérateur concerné : nous vous indiquons lors de la visite ce qui peut être traité pendant le chantier.']),
  dict(slug='brunoy', name='Brunoy', cp='91800', own=['ravalement-facade-brunoy'], near=['ravalement-facade-yerres'],
       intro=['À Brunoy, nous avons remplacé un ancien crépi gris par un enduit armé lisse, soubassement compris, souligné par une bande de séparation. Un ravalement complet qui donne à la maison un aspect neuf et une protection durable.',
              'Nous intervenons à Brunoy et dans le Val d’Yerres pour le ravalement de façade et l’isolation thermique par l’extérieur.'],
       tip_t='Le soubassement, la partie la plus exposée', tip=['Le bas des murs reçoit les éclaboussures de pluie et l’humidité du sol : c’est souvent là que l’enduit se dégrade en premier. Il demande un traitement adapté et, souvent, une teinte plus soutenue que le reste de la façade, séparée par une bande.',
              'Si votre maison se trouve dans le périmètre d’un monument historique, l’avis de l’Architecte des Bâtiments de France peut être requis pour la teinte et l’aspect : nous vous aidons à préparer la déclaration préalable.']),
]
CITY_BY = {c['slug']: c for c in CITIES}

PRICES = {
  'ite': dict(title='Isolation par l’extérieur', rng='180 à 210 €', unit='TTC / m² isolé',
              pts=['Isolant PSE graphité 140 à 200 mm, collé et chevillé', 'Échafaudage, préparation, enduit armé, régulateur et finition compris', 'Varie selon les volets, appuis et descentes à traiter', 'Avant déduction des primes CEE'], projet='ite'),
  'd3': dict(title='Ravalement D3 armé', rng='100 à 120 €', unit='TTC / m² de façade',
             pts=['Lavage, traitement des fissures et des parties abîmées', 'Enduit armé d’un filet sur toute la surface, régulateur et finition', 'Varie selon l’état du support', 'Échafaudage et nettoyage du chantier compris'], projet='d3'),
}

# ------------------------------------------------------------------ utilitaires
CSS = open(os.path.join(ROOT, 'style.css'), encoding='utf-8').read()
def minify_css(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*([{};:,>])\s*', r'\1', s)
    s = s.replace(';}', '}')
    return s.replace('url(../', 'url(/assets/').strip()
CSS_MIN = minify_css(CSS)
open(os.path.join(OUT, 'assets/css/site.min.css'), 'w', encoding='utf-8').write(CSS_MIN.replace('url(/assets/', 'url(../'))

IMG = {}
def img_size(rel):
    if rel not in IMG:
        IMG[rel] = Image.open(os.path.join(OUT, rel.lstrip('/'))).size
    return IMG[rel]

def url(path):  # URL propre : chaque page est un dossier /page/ (fonctionne même sans .htaccess)
    return '/' if path in ('', 'index') else '/' + path + '/'

PAGE_RE = re.compile(r'href="/((?:isolation-exterieure|ravalement-facade|nos-realisations|devis|merci|mentions-legales|confidentialite|maconnerie-facade|ravalement-isolation-[a-z-]+|chantiers/[a-z-]+|guides|guides/[a-z-]+))(?=[?#"])')

PAGES = []  # (path, priority, indexable)

def head(path, title, desc, ld=None, noindex=False, og_img='/assets/img/og-cozybat.jpg', preload=None, stack=False, preload_sizes='(max-width: 860px) 92vw, 440px'):
    assert len(title) <= 60, (title, len(title))
    assert len(desc) <= 155, (desc, len(desc))
    canon = DOMAIN + url(path)
    PAGES.append((path, noindex))
    ld = ld or []
    lds = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in ld)
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">\n'
    pre = ''
    if preload:
        sm = preload[:-5] + '-700.webp'
        extra = ''
        if os.path.exists(os.path.join(OUT, sm.lstrip('/'))):
            extra = f' imagesrcset="{sm} 700w, {preload} {img_size(preload)[0]}w" imagesizes="{preload_sizes}"'
        pre = f'<link rel="preload" as="image" href="{preload}"{extra} fetchpriority="high">\n'
    return f'''<!doctype html>
<html lang="fr" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Cozybat">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Façade rénovée par Cozybat en Essonne">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{DOMAIN}{og_img}">
<meta name="theme-color" content="#2E3A47">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/fav-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/fav-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/img/fav-180.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/poppins-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="/assets/css/site.min.css?v={VER}">
{lds}<!-- Statistiques sans cookie (Plausible) : retirez les marques de commentaire une fois le compte créé sur plausible.io
<script defer data-domain="cozybat.fr" src="https://plausible.io/js/script.js"></script>
-->
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''

ICON_TEL = D.ICON_TEL
ICON_IG = D.ICON_IG

def header(active=''):
    def cur(k): return ' aria-current="page"' if k == active else ''
    return f'''<header class="hd">
<div class="wrap hd-in">
<a class="hd-logo" href="/" aria-label="Cozybat, retour à l’accueil"><img src="/assets/img/logo-cozybat.webp" alt="Cozybat" width="600" height="300" fetchpriority="high"></a>
<nav class="hd-nav" aria-label="Navigation principale">
<a href="/isolation-exterieure"{cur('ite')}>Isolation extérieure</a>
<a href="/ravalement-facade"{cur('d3')}>Ravalement</a>
<a href="/nos-realisations"{cur('real')}>Réalisations</a>
<a href="/guides"{cur('guides')}>Guides</a>
<a href="/#avis">Avis</a>
<a class="hd-tel" href="tel:{TEL}">{TEL_H}</a>
<a class="btn btn-gold" href="/devis" data-track="Clic devis">Devis gratuit</a>
</nav>
<div class="hd-mob">
<a class="icon-btn gold" href="tel:{TEL}" aria-label="Appeler Cozybat au {TEL_H}">{ICON_TEL}</a>
<button class="icon-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="mnav" aria-label="Ouvrir le menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div>
</div>
<nav class="mnav" id="mnav" aria-label="Menu mobile">
<a href="/isolation-exterieure">Isolation par l’extérieur</a>
<a href="/ravalement-facade">Ravalement de façade</a>
<a href="/nos-realisations">Nos réalisations</a>
<a href="/#avis">Avis clients</a>
<a href="/guides">Guides prix et aides</a>
<a href="/#faq">Questions fréquentes</a>
<a class="btn btn-gold" href="/devis">Demander un devis gratuit</a>
</nav>
</header>
<main id="contenu">
'''

def footer(stack=False):
    cities = ''.join(f'<li><a href="/ravalement-isolation-{c["slug"]}">Façade à {e(c["name"])}</a></li>' for c in CITIES)
    js = '<script src="/assets/js/stack.js?v=%s" defer></script>\n' % VER if stack else ''
    return f'''</main>
<footer class="ft">
<div class="wrap ft-grid">
<div>
<img src="/assets/img/logo-cozybat-clair.webp" alt="Cozybat" width="600" height="300" loading="lazy">
<p>Isolation thermique par l’extérieur et ravalement de façade en Essonne. Un métier de façade transmis de père en fils.</p>
<p style="margin-top:10px"><a class="ig" href="{IG}" rel="noopener">{ICON_IG}<span>Instagram @cozybat_renovation</span></a></p>
</div>
<div>
<p class="ft-h">Contact</p>
<ul>
<li><a href="tel:{TEL}">{TEL_H}</a></li>
<li><a href="mailto:{MAIL}">{MAIL}</a></li>
<li>{ADR_TXT}</li>
<li><a href="/devis">Demander un devis gratuit</a></li>
</ul>
</div>
<div>
<p class="ft-h">Nos spécialités</p>
<ul>
<li><a href="/isolation-exterieure">Isolation thermique par l’extérieur</a></li>
<li><a href="/ravalement-facade">Ravalement de façade D3 armé</a></li>
<li><a href="/maconnerie-facade">Maçonnerie de façade : reprises et appuis</a></li>
<li><a href="/nos-realisations">Nos réalisations avant / après</a></li>
<li><a href="/guides/prix-isolation-exterieure">Prix de l’isolation par l’extérieur</a></li>
<li><a href="/guides/prix-ravalement-facade">Prix d’un ravalement de façade</a></li>
<li><a href="/guides/aides-isolation-exterieure">Aides à l’isolation 2026</a></li>
<li><a href="/guides">Tous nos guides</a></li>
<li>RGE Qualibat n° {RGE}</li>
<li>Assurance décennale SMABTP</li>
<li><a href="{GOOGLE}" rel="noopener">5,0/5 sur 48 avis Google</a></li>
</ul>
</div>
<div>
<p class="ft-h">Zone d’intervention</p>
<ul>{cities}</ul>
</div>
</div>
<div class="wrap ft-bot">
<p>© {date.today().year} Cozybat SAS · SIRET {SIRET_H} · Morangis (91)</p>
<p><a href="/mentions-legales">Mentions légales</a> · <a href="/confidentialite">Politique de confidentialité</a></p>
</div>
</footer>
<nav class="callbar" aria-label="Contact rapide">
<a class="c1" href="tel:{TEL}">Appeler</a>
<a class="c2" href="/devis" data-track="Clic devis">Devis gratuit</a>
</nav>
<script src="/assets/js/site.js?v={VER}" defer></script>
{js}</body>
</html>
'''

def crumbs_html(items):
    parts = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1: parts.append(f'<span aria-current="page">{e(name)}</span>')
        else: parts.append(f'<a href="{url(path)}">{e(name)}</a>')
    return '<nav class="crumbs-h" aria-label="Fil d’Ariane">' + ' › '.join(parts) + '</nav>'

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + url(p)} for i, (n, p) in enumerate(items)]}

AREA = [{"@type": "City", "name": c['name'], "address": {"@type": "PostalAddress", "postalCode": c['cp'], "addressCountry": "FR"}} for c in CITIES] + \
       [{"@type": "AdministrativeArea", "name": "Essonne (91)"}]
ORG_ID = DOMAIN + '/#entreprise'
ORG_LD = {
  "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": ORG_ID,
  "name": "Cozybat", "legalName": "Cozybat SAS", "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo-cozybat.png",
  "image": DOMAIN + "/assets/img/og-cozybat.jpg", "telephone": TEL, "email": MAIL, "foundingDate": "2025",
  "identifier": {"@type": "PropertyValue", "propertyID": "SIRET", "value": SIRET}, "vatID": "FR60993112788",
  "description": "Isolation thermique par l’extérieur (ITE) et ravalement de façade D3 armé en Essonne. Entreprise RGE Qualibat, assurance décennale SMABTP.",
  "address": {"@type": "PostalAddress", "streetAddress": ADR['street'], "postalCode": ADR['cp'], "addressLocality": ADR['city'], "addressRegion": "Île-de-France", "addressCountry": "FR"},
  "areaServed": AREA,
  "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
  "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "Qualification RGE Qualibat", "identifier": RGE},
  "sameAs": [GOOGLE, IG],
  "knowsAbout": ["Isolation thermique par l’extérieur", "Ravalement de façade", "Enduit armé D3"]
}
def provider():
    return {k: v for k, v in ORG_LD.items() if k in ('@type', '@id', 'name', 'url', 'telephone', 'email', 'image', 'logo', 'address')}

def service_ld(name, desc, path, stype):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype, "description": desc,
            "url": DOMAIN + url(path), "provider": provider(),
            "areaServed": AREA}
def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

SWOOSH = D.SWOOSH

def slogan(w1, delay=True):
    a = (lambda d: f' style="animation-delay:{d}s"') if delay else (lambda d: '')
    r = ' rise' if delay else ''
    return f'<p class="h1"><span class="ln"><span class="{r.strip()}"{a(.15)}>{w1}</span></span><span class="ln"><span class="{r.strip()}"{a(.3)}>couches.</span></span><span class="ln"><span class="{(r + " hl").strip()}"{a(.45)}>Zéro</span></span><span class="ln"><span class="{(r + " hl").strip()}"{a(.6)}>raccourci.</span></span></p>'

def ticker():
    items = ''.join(f'<span class="tk"><span class="st" aria-hidden="true">★★★★★</span><q>{e(q)}</q><b>{e(n)}</b></span>' for q, n in D.TICKER)
    return f'<div class="ticker" role="region" aria-label="Extraits d’avis clients Google"><div class="ticker-track">{items}</div></div>\n'

def trust():
    return f'''<section class="trust" aria-label="Nos garanties"><div class="wrap trust-grid">
<a class="trust-it" href="{GOOGLE}" rel="noopener"><strong>5,0 <em aria-hidden="true">★★★★★</em></strong><span>48 avis Google</span></a>
<div class="trust-it"><strong>RGE</strong><span>Qualibat {RGE}</span></div>
<div class="trust-it"><strong>De père en fils</strong><span>Un métier de façade transmis</span></div>
<div class="trust-it"><strong>Décennale</strong><span>Assurée chez SMABTP</span></div>
<div class="trust-it"><strong>48 h</strong><span>Réponse · visite et devis gratuits</span></div>
</div></section>
'''

def srcset(base, s, w):
    if w <= 700: return ''
    return f' srcset="{base}-{s}-700.webp 700w, {base}-{s}.webp {w}w" sizes="(max-width: 860px) 92vw, 440px"'

def ba_card(c, near=False, lcp=False):
    base = f'/assets/img/chantiers/{c["slug"]}'
    w, h = img_size(base + '-avant.webp')
    lazy = '' if lcp else ' loading="lazy"'
    fp = ' fetchpriority="high"' if lcp else ''
    lab = ('PRÈS DE CHEZ VOUS · ' if near else '') + c['label'].upper()
    return f'''<figure class="ba-card" data-type="{c['type']}">
<div class="ba">
<img src="{base}-avant.webp"{srcset(base, 'avant', w)} alt="{e(c['work'])} à {e(c['ville'])} : façade avant les travaux" width="{w}" height="{h}"{lazy}{fp} decoding="async">
<img class="after" src="{base}-apres.webp"{srcset(base, 'apres', w)} alt="{e(c['work'])} à {e(c['ville'])} : façade après les travaux Cozybat" width="{w}" height="{h}" loading="lazy" decoding="async">
<span class="bar" aria-hidden="true"></span><span class="knob" aria-hidden="true">↔</span>
<span class="tag l" aria-hidden="true">AVANT</span><span class="tag r" aria-hidden="true">APRÈS</span>
<input type="range" min="0" max="100" value="50" aria-label="Comparer avant et après, {e(c['work'].lower())} à {e(c['ville'])}">
</div>
<figcaption class="ba-cap"><a href="/chantiers/{c['slug']}">{e(c['work'])} à {e(c['ville'])}</a><span>{e(lab)}</span><p>{e(c['desc'])}</p></figcaption>
</figure>'''

def avis_section():
    cards = ''.join(f'''<figure class="avis"><div class="avis-top"><span class="st" aria-hidden="true">★★★★★</span><small>{t}</small></div><blockquote>« {e(x)} »</blockquote><figcaption>{e(n)} · 5 étoiles sur 5</figcaption></figure>''' for n, t, x in D.AVIS)
    return f'''<section class="sec sec-dark" id="avis"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Avis clients</p><h2 class="h2">Ils nous ont confié leur façade.</h2></div>
<a class="score" href="{GOOGLE}" rel="noopener"><strong>5,0 <em aria-hidden="true">★★★★★</em></strong><span>LIRE LES 48 AVIS SUR GOOGLE</span></a></div>
<div class="avis-cols">{cards}</div>
</div></section>
'''

def team_section():
    chips = ''.join((f'<li><a href="/ravalement-isolation-{CITY_BY[s]["slug"]}">{e(v)}</a></li>' if (s := slugify(v)) in CITY_BY else f'<li>{e(v)}</li>') for v in D.VILLES)
    return f'''<section class="sec sec-warm" id="equipe"><div class="wrap team">
<div class="team-photo" data-reveal><img src="/assets/img/equipe-cozybat-facadiers-morangis.webp" alt="David et Vincent, associés de Cozybat, devant une maison en meulière rénovée en Essonne" width="820" height="1093" loading="lazy" decoding="async"></div>
<div class="team-txt">
<div><p class="kicker">Qui sommes-nous</p><h2 class="h2" style="margin-bottom:18px">Une jeune équipe, un métier de famille.</h2>
<p>Cozybat, ce sont David et Vincent, associés et présents sur chaque chantier avec leur équipe. Un métier de façade transmis de père en fils : nous avons appris sur les chantiers bien avant de créer Cozybat en 2025, et nous sommes spécialisés en ravalement et en isolation par l’extérieur.</p>
<p style="margin-top:12px">Un seul interlocuteur de la visite à la réception, et des rendez-vous possibles dans nos locaux à Morangis.</p></div>
<div class="zone"><h3>Zone d’intervention : toute l’Essonne (91)</h3><ul class="chips">{chips}</ul>
<p>Votre commune n’apparaît pas ? <a href="tel:{TEL}">Appelez-nous au {TEL_H}</a> : nous intervenons aussi dans les départements voisins.</p></div>
</div></div></section>
'''

def slugify(v):
    t = v.lower()
    for a, b in (('é', 'e'), ('è', 'e'), ('ê', 'e'), ('à', 'a'), ('ô', 'o'), ('î', 'i'), ('ç', 'c'), (' ', '-'), ('’', '-')):
        t = t.replace(a, b)
    return 'juvisy-sur-orge' if t == 'juvisy-sur-orge' else t

def methode_section(sys=None):
    st = ''.join(f'<div class="st4"><div class="line"><i style="transition-delay:{i*.15:.2f}s"></i></div><small>{n}</small><h3>{t}</h3><p>{x}</p></div>' for i, (n, t, x) in enumerate(D.METHODE))
    perks = ''
    if sys:
        perks = '<div class="perks">' + ''.join(f'<div class="perk"><h3>{t}</h3><p>{x}</p></div>' for t, x in D.PERKS[sys]) + '</div>'
    return f'''<section class="sec sec-dark" id="methode"><div class="wrap" data-reveal>
<p class="kicker">Méthode</p><h2 class="h2" style="margin-bottom:48px">Du diagnostic à la réception.</h2>
<div class="steps4">{st}</div>{perks}
</div></section>
'''

def price_section(sys):
    p = PRICES[sys]
    pts = ''.join(f'<li>{x}</li>' for x in p['pts'])
    return f'''<section class="sec sec-warm" id="prix"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Prix indicatif</p><h2 class="h2">Quel budget prévoir ?</h2></div>
<p class="lead">Une fourchette pour vous donner un ordre d’idée. Chaque devis est ensuite détaillé couche par couche, sans surprise.</p></div>
<div class="prices"><div class="price dark"><small>FOURCHETTE INDICATIVE</small><h3>{p['title']}</h3>
<p class="amt"><b>{p['rng']}</b><i>{p['unit']}</i></p><ul>{pts}</ul>
<a class="btn btn-gold" href="/devis?projet={p['projet']}" data-track="Clic devis">Obtenir mon prix exact</a></div></div>
<p class="note">Prix indicatifs, toutes taxes comprises, pour une maison individuelle en Essonne. Ils ne constituent pas une offre : le prix exact dépend de la surface, de l’état du support et des points singuliers, et il est fixé sur devis après la visite technique gratuite. Détails et exemples chiffrés : <a href="/guides/{'prix-isolation-exterieure' if sys == 'ite' else 'prix-ravalement-facade'}">{'guide du prix de l’isolation par l’extérieur' if sys == 'ite' else 'guide du prix d’un ravalement de façade'}</a>{' et <a href="/guides/aides-isolation-exterieure">guide des aides 2026</a>' if sys == 'ite' else ' et <a href="/guides/fissures-facade">guide des fissures de façade</a>'}.</p>
</div></section>
'''

def faq_section(items, dark=True, title='Vos questions.'):
    det = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items)
    cls = 'sec sec-dark' if dark else 'sec sec-warm'
    return f'''<section class="{cls}" id="faq"><div class="wrap faq">
<div class="faq-head"><p class="kicker">Questions fréquentes</p><h2 class="h2">{title}</h2></div>
<div class="faq-list">{det}</div>
</div></section>
'''

def form_block():
    f = D.form_block('/')
    f = f.replace('action="/contact.php"', 'action="/contact.php"').replace('href="/confidentialite.html"', 'href="/confidentialite"')
    return f

def devis_section(title_tag='h2', title='Parlons de votre façade.', h1=None):
    top = f'<h1 class="kicker" style="font-size:14px">{h1}</h1>' if h1 else ''
    return f'''<section class="sec sec-gold" id="contact"><div class="wrap devis">
<div class="devis-txt">{top}<{title_tag} class="h2">{title}</{title_tag}>
<div class="devis-info"><a href="tel:{TEL}">Appeler le {TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a><span>Rendez-vous : {ADR_TXT}</span><span>Réponse sous 48 h ouvrées · visite et devis gratuits</span></div></div>
{form_block()}
</div></section>
'''

def cta_band(projet='', where=''):
    q = f'?projet={projet}' if projet else ''
    t = f'Un projet de façade{where} ?'
    return f'''<section class="sec-tight sec-gold"><div class="wrap cta-band">
<h2 class="h2">{t}</h2>
<div class="hero-cta" style="margin:0"><a class="btn btn-navy btn-lg" href="/devis{q}" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline btn-lg" href="tel:{TEL}">Appeler le {TEL_H}</a></div>
</div></section>
'''

def story_section(sys):
    L = D.layers(sys)
    steps = ''
    for l in L:
        specs = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in l['specs'])
        steps += f'''<article class="step" data-num="{l['num']}" data-name="{e(l['name'].upper())}"><span class="n" aria-hidden="true">{l['num']}</span><h3>{e(l['name'])}</h3><p class="plain">{e(l['plain'])}</p>
<details><summary>+ DÉTAIL TECHNIQUE</summary><p>{e(l['text'])}</p><dl class="specs-tbl">{specs}</dl></details></article>
'''
    title = 'Le système d’isolation, couche par couche.' if sys == 'ite' else 'Le ravalement armé, couche par couche.'
    return f'''<section class="sec-dark" id="systeme"><div class="wrap" style="padding-top:104px">
<p class="kicker">Le système</p><h2 class="h2">{title}</h2>
<p class="lead">Faites défiler : chaque couche se pose sur la précédente, dans l’ordre du chantier.</p>
</div>
<div class="wrap story">
<div class="story-stage"><div class="story-3d" data-stack="story" data-system="{sys}"></div>
<div class="story-bar"><div class="story-meta"><span data-story-num>COUCHE 00</span><span data-story-name></span></div><div class="prog"><i data-story-prog></i></div></div></div>
<div class="story-steps">
{steps}</div>
</div></section>
'''

def write(path, content):
    if path.endswith('.html') and path not in ('index.html', '404.html'):
        path = path[:-5] + '/index.html'
    if path.endswith('.html'):
        content = PAGE_RE.sub(r'href="/\1/', content)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)

# ------------------------------------------------------------------ pages
def page_index():
    hero = f'''<section class="hero" id="top">{SWOOSH}
<div class="wrap hero-grid">
<div class="hero-txt">
<div class="tabs" role="group" aria-label="Voir la coupe du système">
<button class="tab" type="button" data-sys-tab="ite" aria-pressed="true"><small>01</small><span>Isolation par l’extérieur</span></button>
<button class="tab" type="button" data-sys-tab="d3" aria-pressed="false"><small>02</small><span>Ravalement D3 armé</span></button>
</div>
<h1 class="eyebrow eyebrow-h1 fade" style="animation-delay:.1s">Isolation par l’extérieur et ravalement de façade en Essonne</h1>
<div data-sys-copy="ite">{slogan('Huit')}
<p class="hero-sub fade" style="animation-delay:.9s">Cozybat isole et rénove les façades des maisons de l’Essonne, autour de Morangis. Un métier de façade transmis de père en fils, posé dans les règles du système, du collage à la dernière passe d’enduit.</p></div>
<div data-sys-copy="d3" hidden>{slogan('Cinq', delay=False)}
<p class="hero-sub">Ravalement armé pour façades fissurées : préparation du support, enduit armé d’un filet en fibre de verre et finition, posés dans les règles du système.</p></div>
<div class="hero-cta fade" style="animation-delay:1.05s"><a class="btn btn-gold btn-lg" href="/devis" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline btn-lg" href="#solutions">Voir nos deux spécialités</a></div>
</div>
<div class="hero-stage"><div data-stack="hero" data-system="ite" style="position:absolute;inset:0"></div><p class="hero-count" data-hero-count aria-hidden="true"></p></div>
</div>
{ticker()}</section>
'''
    quiz = f'''<section class="sec sec-dark" id="orientation"><div class="wrap quiz">
<div class="quiz-intro"><p class="kicker">Par où commencer</p><h2 class="h2">Isolation ou ravalement ?</h2><p class="lead">Trois questions pour savoir quelle solution correspond à votre façade.</p></div>
<div class="quiz-box" data-quiz>
''' + ''.join(f'<div class="q" role="radiogroup" aria-labelledby="q-{n}"><p class="q-t" id="q-{n}">{t}</p><div class="opts"><label class="pill"><input type="radio" name="{n}" value="oui"><span>OUI</span></label><label class="pill"><input type="radio" name="{n}" value="non"><span>NON</span></label></div></div>\n'
              for t, n in [('Votre maison est-elle froide l’hiver, ou vos factures de chauffage élevées ?', 'froid'), ('Votre façade est-elle fissurée, tachée ou abîmée ?', 'fissures'), ('Votre maison a-t-elle été construite avant les années 2000 ?', 'ancienne')]) + '''<div class="quiz-res" data-quiz-res aria-live="polite"><div><p class="k">RÉSULTAT</p><p class="t">Répondez aux 3 questions</p><p class="x">La solution adaptée s’affichera ici.</p></div><a class="btn btn-navy" href="/devis" hidden>Demander un devis gratuit</a></div>
</div></div></section>
'''
    specs = '''<section class="sec" id="solutions"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Nos deux spécialités</p><h2 class="h2">Isoler ou rénover votre façade.</h2></div><p class="lead">Deux systèmes armés, posés par la même équipe, avec la même exigence.</p></div>
<div class="specs">
<a class="spec" href="/isolation-exterieure" data-reveal><small>01 · ISOLATION PAR L’EXTÉRIEUR</small><h3>Isolation thermique par l’extérieur</h3><p>Un isolant de 14 à 20 cm enveloppe la maison, puis un enduit neuf refait la façade. Plus de confort, moins de chauffage, et des aides possibles.</p><span class="go">Découvrir l’isolation par l’extérieur →</span></a>
<a class="spec" href="/ravalement-facade" data-reveal><small>02 · RAVALEMENT</small><h3>Ravalement de façade D3 armé</h3><p>Pour une façade fissurée ou abîmée : préparation, enduit armé d’un filet sur toute la surface et finition dans la teinte de votre choix.</p><span class="go">Découvrir le ravalement D3 armé →</span></a>
</div></div></section>
'''
    cards = '\n'.join(ba_card(c) for c in CHANTIERS)
    real = f'''<section class="sec sec-warm" id="realisations"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Réalisations</p><h2 class="h2">Avant. Après.</h2></div><p class="lead">Faites glisser pour comparer. Des chantiers réalisés en Essonne.</p></div>
<div class="filters" role="group" aria-label="Filtrer les réalisations"><button type="button" data-filter="all" aria-pressed="true">Tous les chantiers</button><button type="button" data-filter="ite" aria-pressed="false">Isolation par l’extérieur</button><button type="button" data-filter="d3" aria-pressed="false">Ravalement</button></div>
<div class="ba-grid">{cards}</div>
<p style="margin-top:28px"><a class="btn btn-outline" href="/nos-realisations">Toutes nos réalisations avant / après</a></p>
</div></section>
'''
    title = 'Isolation extérieure et ravalement en Essonne (91) | Cozybat'
    desc = 'Isolation par l’extérieur et ravalement de façade autour de Morangis (91). RGE Qualibat, décennale SMABTP, 5,0/5 sur 48 avis Google. Devis gratuit.'
    body = (head('', title, desc, ld=[ORG_LD, faq_ld(D.FAQ_HOME)], stack=True) + header() + hero + trust() + quiz + specs + real + avis_section() + team_section()
            + guides_home() + methode_section() + faq_section(D.FAQ_HOME) + devis_section() + footer(stack=True))
    write('index.html', body)

def page_system(sys):
    if sys == 'ite':
        path = 'isolation-exterieure'
        title = 'Entreprise RGE d’isolation extérieure en Essonne | Cozybat'
        desc = 'Isolation par l’extérieur (ITE) en Essonne : PSE graphité 140 à 200 mm, enduit armé. Entreprise RGE Qualibat, primes CEE, TVA 5,5 %. Devis gratuit.'
        h1, w1 = 'Entreprise RGE d’isolation thermique par l’extérieur en Essonne', 'Huit'
        sub = 'Un isolant de 14 à 20 cm enveloppe votre maison, puis un enduit neuf refait la façade. Plus de confort été comme hiver, moins de chauffage, et des aides possibles grâce à notre qualification RGE.'
        faq, projet, name, stype, other = D.FAQ_ITE, 'ite', 'Isolation thermique par l’extérieur', 'Isolation thermique par l’extérieur (ITE)', ('/ravalement-facade', 'Votre façade est seulement fissurée ? Découvrir le ravalement D3 armé')
    else:
        path = 'ravalement-facade'
        title = 'Ravalement de façade D3 armé en Essonne | Cozybat'
        desc = 'Ravalement de façade D3 armé en Essonne : traitement des fissures, enduit armé sur toute la surface, finition au choix. Décennale SMABTP. Devis gratuit.'
        h1, w1 = 'Ravalement de façade D3 armé en Essonne', 'Cinq'
        sub = 'Pour une façade fissurée, tachée ou abîmée : préparation du support, enduit armé d’un filet en fibre de verre sur toute la surface, régulateur et finition dans la teinte de votre choix.'
        faq, projet, name, stype, other = D.FAQ_D3, 'd3', 'Ravalement de façade D3 armé', 'Ravalement de façade', ('/isolation-exterieure', 'Envie d’isoler en même temps ? Découvrir l’isolation par l’extérieur')
    cr = [('Accueil', ''), (name, path)]
    hero = f'''<section class="hero" id="top">{SWOOSH}
<div class="wrap hero-grid">
<div class="hero-txt">{crumbs_html(cr)}<h1 class="eyebrow eyebrow-h1 fade" style="animation-delay:.1s">{h1}</h1>
{slogan(w1)}
<p class="hero-sub fade" style="animation-delay:.9s">{sub}</p>
<div class="hero-cta fade" style="animation-delay:1.05s"><a class="btn btn-gold btn-lg" href="/devis?projet={projet}" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline btn-lg" href="#systeme">Voir la coupe du système</a></div></div>
<div class="hero-stage"><div data-stack="hero" data-system="{sys}" style="position:absolute;inset:0"></div><p class="hero-count" data-hero-count aria-hidden="true"></p></div>
</div>
{ticker()}</section>
'''
    cards = '\n'.join(ba_card(c) for c in CHANTIERS if c['type'] == sys)
    real = f'''<section class="sec sec-warm" id="realisations"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Réalisations</p><h2 class="h2">Nos chantiers avant / après.</h2></div><p class="lead">Faites glisser pour comparer.</p></div>
<div class="ba-grid">{cards}</div>
<p style="margin-top:28px"><a class="btn btn-outline" href="/nos-realisations">Voir toutes nos réalisations</a></p>
</div></section>
'''
    cities = ''.join(f'<a class="btn btn-outline" href="/ravalement-isolation-{c["slug"]}">{e(name.split(" D3")[0])} à {e(c["name"])}</a>' for c in CITIES)
    local = f'''<section class="sec-tight"><div class="wrap">
<p class="kicker">Près de chez vous</p><h2 class="h2" style="font-size:clamp(24px,3vw,36px);margin-bottom:18px">Nos interventions en Essonne</h2>
<div class="links-row">{cities}</div>
<p style="margin-top:24px"><a class="btn btn-navy" href="{other[0]}">{other[1]}</a> <a class="btn btn-outline" href="/maconnerie-facade">Reprises d’enduit, appuis et réparations de façade</a></p>
</div></section>
'''
    ld = [service_ld(name, desc, path, stype), crumbs_ld(cr), faq_ld(faq)]
    body = (head(path, title, desc, ld=ld, stack=True) + header(sys) + hero + trust() + story_section(sys) + real + methode_section(sys)
            + price_section(sys) + faq_section(faq, dark=False) + local + cta_band(projet) + footer(stack=True))
    write(path + '.html', body)

def page_realisations():
    cr = [('Accueil', ''), ('Nos réalisations', 'nos-realisations')]
    cards = '\n'.join(ba_card(c, lcp=(i == 0)) for i, c in enumerate(CHANTIERS))
    content = f'''<section class="sec" style="padding-top:40px"><div class="wrap">
{crumbs_html(cr)}<p class="kicker">Réalisations</p><h1 class="h2" style="margin-bottom:12px">Nos réalisations de façade en Essonne</h1>
<p class="lead" style="margin-bottom:36px">Isolation par l’extérieur et ravalement : faites glisser chaque photo pour comparer avant et après.</p>
<div class="filters" role="group" aria-label="Filtrer les réalisations"><button type="button" data-filter="all" aria-pressed="true">Tous les chantiers</button><button type="button" data-filter="ite" aria-pressed="false">Isolation par l’extérieur</button><button type="button" data-filter="d3" aria-pressed="false">Ravalement</button></div>
<div class="ba-grid">{cards}</div>
</div></section>
'''
    first = f'/assets/img/chantiers/{CHANTIERS[0]["slug"]}-avant.webp'
    write('nos-realisations.html', head('nos-realisations', 'Isolation extérieure avant / après en Essonne | Cozybat',
          'Avant / après de nos chantiers d’isolation par l’extérieur et de ravalement en Essonne : Ollainville, Saint-Michel-sur-Orge, Morangis, Yerres, Brunoy…',
          ld=[crumbs_ld(cr)], preload=first) + header('real') + content + trust() + avis_section() + cta_band() + footer())

def page_case(c):
    cr = [('Accueil', ''), ('Nos réalisations', 'nos-realisations'), (f'{c["work"]} à {c["ville"]}', 'chantiers/' + c['slug'])]
    facts = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in c['facts'])
    sysp = ('/isolation-exterieure', 'Découvrir l’isolation par l’extérieur') if c['type'] == 'ite' else ('/ravalement-facade', 'Découvrir le ravalement D3 armé')
    base = f'/assets/img/chantiers/{c["slug"]}'
    w, h = img_size(base + '-avant.webp')
    city_link = ''
    if c['cityslug'] in CITY_BY:
        cc = CITY_BY[c['cityslug']]
        city_link = f'<a class="btn btn-outline" href="/ravalement-isolation-{cc["slug"]}">Nos interventions à {e(cc["name"])}</a>'
    others = [x for x in CHANTIERS if x['slug'] != c['slug'] and x['type'] == c['type']][:2]
    more = '\n'.join(ba_card(x) for x in others)
    content = f'''<div class="wrap" style="padding-top:28px">{crumbs_html(cr)}</div>
<section class="sec" style="padding-top:0"><div class="wrap">
<div class="case">
<div class="ba">
<img src="{base}-avant.webp"{srcset(base, 'avant', w).replace('440px', '640px')} alt="{e(c['work'])} à {e(c['ville'])} : façade avant les travaux" width="{w}" height="{h}" fetchpriority="high" decoding="async">
<img class="after" src="{base}-apres.webp"{srcset(base, 'apres', w).replace('440px', '640px')} alt="{e(c['work'])} à {e(c['ville'])} : façade après les travaux Cozybat" width="{w}" height="{h}" decoding="async">
<span class="bar" aria-hidden="true"></span><span class="knob" aria-hidden="true">↔</span>
<span class="tag l" aria-hidden="true">AVANT</span><span class="tag r" aria-hidden="true">APRÈS</span>
<input type="range" min="0" max="100" value="50" aria-label="Comparer avant et après, {e(c['work'].lower())} à {e(c['ville'])}">
</div>
<div class="case-txt"><p class="kicker" style="margin:0">{e(c['label'].upper())}</p>
<h1 class="h2">{e(c['h1'])}</h1><p>{e(c['desc'])}</p>
<dl class="facts">{facts}</dl>
<div class="hero-cta" style="margin-top:6px"><a class="btn btn-gold" href="/devis?projet={c['type']}" data-track="Clic devis">Demander un devis pour un projet similaire</a><a class="btn btn-outline" href="{sysp[0]}">{sysp[1]}</a>{city_link}</div>
</div></div></div></section>
'''
    if more:
        content += f'<section class="sec sec-warm"><div class="wrap"><h2 class="kicker">Autres réalisations du même type</h2><div class="ba-grid">{more}</div></div></section>\n'
    title = c['title'] + ' | Cozybat'
    if len(title) > 60: title = f"{c['work']} à {c['ville']} | Cozybat"
    desc = c['desc'] if len(c['desc']) <= 155 else c['desc'][:152].rsplit(' ', 1)[0] + '…'
    ld = [crumbs_ld(cr), service_ld(c['work'] + ' à ' + c['ville'], c['desc'], 'chantiers/' + c['slug'], c['work'])]
    write(f'chantiers/{c["slug"]}.html', head('chantiers/' + c['slug'], title, desc, ld=ld, preload=base + '-avant.webp', preload_sizes='(max-width: 860px) 92vw, 640px') + header('real') + content + trust() + cta_band(c['type']) + footer())

def page_city(cty):
    path = 'ravalement-isolation-' + cty['slug']
    cr = [('Accueil', ''), (f'Façade à {cty["name"]}', path)]
    intro = ''.join(f'<p>{e(x)}</p>' for x in cty['intro'])
    tip = ''.join(f'<p>{e(x)}</p>' for x in cty['tip'])
    own = [BYSLUG[s] for s in cty['own']]
    near = [BYSLUG[s] for s in cty['near']]
    cards = '\n'.join([ba_card(c) for c in own] + [ba_card(c, near=True) for c in near])
    real_t = f'Nos chantiers à {cty["name"]} et alentour' if own else f'Nos chantiers près de {cty["name"]}'
    others = [c for c in CITIES if c['slug'] != cty['slug']]
    olinks = ''.join(f'<a class="btn btn-outline" href="/ravalement-isolation-{c["slug"]}">Façade à {e(c["name"])}</a>' for c in others)
    content = f'''<section class="hero" id="top">{SWOOSH}
<div class="wrap" style="position:relative;padding-top:40px;padding-bottom:150px">
{crumbs_html(cr)}<p class="eyebrow">{e(cty['name'])} · {cty['cp']}</p>
<h1 class="h2" style="max-width:900px">Ravalement de façade et isolation par l’extérieur à {e(cty['name'])}</h1>
<div class="city-grid" style="margin-top:32px">
<div class="city-txt">{intro}
<div class="hero-cta"><a class="btn btn-gold btn-lg" href="/devis" data-track="Clic devis">Demander un devis gratuit à {e(cty['name'])}</a><a class="btn btn-outline btn-lg" href="tel:{TEL}">Appeler le {TEL_H}</a></div></div>
<div class="tip"><h2>{e(cty['tip_t'])}</h2>{tip}</div>
</div></div></section>
{trust()}<section class="sec" id="solutions"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Nos solutions à {e(cty['name'])}</p><h2 class="h2">Isoler ou rénover votre façade.</h2></div></div>
<div class="specs">
<a class="spec" href="/isolation-exterieure"><small>01 · ISOLATION PAR L’EXTÉRIEUR</small><h3>Isolation thermique par l’extérieur</h3><p>Isolant de 14 à 20 cm et enduit neuf : la maison est isolée et la façade refaite en une seule opération. Primes CEE possibles, entreprise RGE Qualibat.</p><span class="go">Découvrir l’isolation par l’extérieur →</span></a>
<a class="spec" href="/ravalement-facade"><small>02 · RAVALEMENT</small><h3>Ravalement de façade D3 armé</h3><p>Traitement des fissures, enduit armé d’un filet en fibre de verre sur toute la surface et finition dans la teinte de votre choix.</p><span class="go">Découvrir le ravalement D3 armé →</span></a>
</div></div></section>
<section class="sec sec-warm" id="realisations"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Réalisations</p><h2 class="h2">{real_t}</h2></div><p class="lead">Faites glisser pour comparer avant et après.</p></div>
<div class="ba-grid">{cards}</div>
</div></section>
<section class="sec-tight"><div class="wrap"><p class="kicker">Autres communes</p><h2 class="h2" style="font-size:clamp(22px,3vw,32px);margin-bottom:16px">Nous intervenons aussi dans les communes voisines</h2><div class="links-row">{olinks}</div></div></section>
'''
    title = f'Ravalement et ITE à {cty["name"]} ({cty["cp"][:2]}) | Cozybat'
    if len(title) > 60: title = f'Ravalement et ITE à {cty["name"]} | Cozybat'
    desc = f'Ravalement de façade et isolation par l’extérieur à {cty["name"]} ({cty["cp"]}) : entreprise RGE de Morangis, décennale SMABTP. Devis gratuit.'
    ld = [crumbs_ld(cr), {"@context": "https://schema.org", "@type": "Service", "name": f'Ravalement de façade et isolation par l’extérieur à {cty["name"]}',
          "serviceType": "Ravalement de façade et isolation thermique par l’extérieur", "url": DOMAIN + url(path),
          "provider": provider(),
          "areaServed": {"@type": "City", "name": cty['name'], "address": {"@type": "PostalAddress", "postalCode": cty['cp'], "addressCountry": "FR"}}}]
    write(path + '.html', head(path, title, desc, ld=ld) + header() + content + cta_band(where=f' à {cty["name"]}') + footer())

FAQ_DEVIS = [
  ('Le devis est-il vraiment gratuit ?', 'Oui. La visite technique et le devis sont gratuits et sans engagement, pour l’isolation par l’extérieur comme pour le ravalement de façade, partout en Essonne.'),
  ('Que se passe-t-il après ma demande ?', 'Nous vous rappelons sous 48 h ouvrées pour convenir d’une visite technique. Sur place, nous relevons les façades, contrôlons l’état du support et repérons les points singuliers : appuis de fenêtre, descentes d’eau, volets, coffres de volets roulants. Le devis détaillé vous est ensuite envoyé par e-mail.'),
  ('Quelles informations préparer ?', 'Quelques photos de chaque façade suffisent pour une première estimation. Si vous les avez, joignez aussi les dimensions approximatives de la maison, l’année de construction et vos factures de chauffage : elles servent à estimer les aides pour une isolation par l’extérieur.'),
  ('Faut-il être présent lors de la visite ?', 'C’est préférable : la visite dure en général entre 30 minutes et une heure, et c’est le moment de choisir ensemble la finition, la teinte et les options. Nous pouvons aussi vous recevoir dans nos locaux à Morangis pour voir des échantillons.'),
  ('Le devis précise-t-il les aides ?', 'Pour une isolation par l’extérieur, le devis indique l’isolant, son épaisseur et sa résistance thermique, ainsi que l’estimation des primes CEE selon vos revenus. Cozybat est qualifiée RGE Qualibat, condition pour en bénéficier.'),
]

def page_devis():
    cr = [('Accueil', ''), ('Devis gratuit', 'devis')]
    body = (f'<div class="wrap" style="padding-top:28px">{crumbs_html(cr)}</div>\n' + devis_section(title_tag='p', h1='Devis gratuit ITE et ravalement en Essonne') + trust()
            + methode_section() + faq_section(FAQ_DEVIS, dark=False, title='Votre demande de devis.'))
    write('devis.html', head('devis', 'Devis gratuit ITE et ravalement en Essonne | Cozybat',
          'Demandez votre devis gratuit d’isolation par l’extérieur ou de ravalement de façade en Essonne. Réponse sous 48 h ouvrées, visite technique offerte.', ld=[crumbs_ld(cr), faq_ld(FAQ_DEVIS)])
          + header() + body + footer())

def page_merci():
    content = f'''<section class="sec sec-gold"><div class="wrap" style="max-width:820px">
<h1 class="h2" style="margin-bottom:18px">Demande de devis reçue.</h1>
<p style="font-size:19px;margin:0 0 28px">Merci ! Nous vous rappelons sous 48 h ouvrées pour fixer la visite technique gratuite. Pour une question urgente : <a href="tel:{TEL}" style="color:#2E3A47;font-weight:700">{TEL_H}</a>.</p>
<div class="hero-cta"><a class="btn btn-navy" href="/nos-realisations">Voir nos réalisations</a><a class="btn btn-outline" href="{IG}" rel="noopener">Nous suivre sur Instagram</a></div>
</div></section>
'''
    write('merci.html', head('merci', 'Demande envoyée | Cozybat', 'Votre demande de devis a bien été envoyée à Cozybat.', noindex=True) + header() + content + footer())

def guide_card(g, tag='h3'):
    return f'<a class="spec" href="/guides/{g["slug"]}/"><small>GUIDE · {"ISOLATION" if g["kind"] == "ite" else "RAVALEMENT"}</small><{tag} class="spec-t">{e(g["short"])}</{tag}><p>{e(g["desc"])}</p><span class="go">Lire le guide →</span></a>'

def guides_home():
    cards = ''.join(guide_card(GBY[k]) for k in ('prix-isolation-exterieure', 'aides-isolation-exterieure', 'prix-ravalement-facade'))
    return f'''<section class="sec" id="guides"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Guides</p><h2 class="h2">Prix, aides et conseils.</h2></div><p class="lead">Tout ce qu’il faut savoir avant vos travaux de façade.</p></div>
<div class="specs">{cards}</div>
<p style="margin-top:28px"><a class="btn btn-outline" href="/guides">Voir tous nos guides</a></p>
</div></section>
'''

def page_maconnerie():
    m = maconnerie.PAGE
    path = m['path']
    cr = [('Accueil', ''), ('Maçonnerie de façade', path)]
    toc = ''.join(f'<li><a href="#s{i}">{e(h)}</a></li>' for i, (h, _) in enumerate(m['sections'], 1))
    body = ''.join(f'<h2 id="s{i}">{e(h)}</h2>{html_}' for i, (h, html_) in enumerate(m['sections'], 1))
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in m['faq'])
    cards = '\n'.join(ba_card(c) for c in CHANTIERS if c['type'] == 'd3')
    content = f"""<section class="sec" style="padding-top:40px"><div class="wrap">
{crumbs_html(cr)}<article class="guide">
<p class="kicker">Réparations de façade</p>
<h1 class="h2">{e(m['h1'])}</h1>
<p class="lead guide-intro">{e(m['intro'])}</p>
<div class="hero-cta" style="margin:0 0 28px"><a class="btn btn-gold btn-lg" href="/devis?projet=d3" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline btn-lg" href="tel:{TEL}">Appeler le {TEL_H}</a></div>
<nav class="toc" aria-label="Sommaire"><p class="toc-t">Nos interventions</p><ol>{toc}</ol></nav>
{body}
<h2 id="faq-mac">Questions fréquentes</h2>
<div class="faq-list guide-faq">{faq}</div>
</article></div></section>
{trust()}<section class="sec sec-warm"><div class="wrap"><div class="sec-head"><div><p class="kicker">Réalisations</p><h2 class="h2">Nos façades rénovées.</h2></div><p class="lead">Faites glisser pour comparer avant et après.</p></div><div class="ba-grid">{cards}</div></div></section>
"""
    desc = m['desc']
    ld = [crumbs_ld(cr), faq_ld(m['faq']), service_ld('Maçonnerie de façade : reprises, appuis et réparations', desc, path, 'Maçonnerie et réparation de façade')]
    write(path + '.html', head(path, m['title'], desc, ld=ld) + header() + content + cta_band('d3') + footer())

def page_guide(g):
    path = 'guides/' + g['slug']
    cr = [('Accueil', ''), ('Guides', 'guides'), (g['short'], path)]
    toc = ''.join(f'<li><a href="#s{i}">{e(h)}</a></li>' for i, (h, _) in enumerate(g['sections'], 1))
    body = ''.join(f'<h2 id="s{i}">{e(h)}</h2>{html_}' for i, (h, html_) in enumerate(g['sections'], 1))
    faq = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in g['faq'])
    rel = ''.join(guide_card(GBY[r]) for r in g['related'])
    svc = ('/isolation-exterieure/', 'Découvrir l’isolation par l’extérieur') if g['kind'] == 'ite' else ('/ravalement-facade/', 'Découvrir le ravalement D3 armé')
    content = f'''<section class="sec" style="padding-top:40px"><div class="wrap">
{crumbs_html(cr)}<article class="guide">
<p class="kicker">Guide · mis à jour en {MOIS}</p>
<h1 class="h2">{e(g['h1'])}</h1>
<p class="lead guide-intro">{e(g['intro'])}</p>
<nav class="toc" aria-label="Sommaire"><p class="toc-t">Sommaire</p><ol>{toc}</ol></nav>
{body}
<h2 id="faq-guide">Questions fréquentes</h2>
<div class="faq-list guide-faq">{faq}</div>
<div class="guide-cta"><p><strong>Un projet en Essonne ?</strong> Visite technique et devis gratuits, réponse sous 48 h ouvrées.</p>
<div class="hero-cta" style="margin:0"><a class="btn btn-gold" href="/devis?projet={g['kind']}" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline" href="{svc[0]}">{svc[1]}</a></div></div>
<p class="guide-by">Rédigé par Cozybat, entreprise RGE Qualibat d’isolation par l’extérieur et de ravalement à Morangis (91). Prix indicatifs TTC pour une maison individuelle en Essonne ; règles d’aides en vigueur à la date de mise à jour.</p>
</article></div></section>
{trust()}<section class="sec sec-warm"><div class="wrap"><p class="kicker">À lire aussi</p><h2 class="h2" style="font-size:clamp(24px,3vw,36px);margin-bottom:24px">Nos autres guides</h2><div class="specs">{rel}</div></div></section>
'''
    ld = [crumbs_ld(cr), faq_ld(g['faq']),
          {"@context": "https://schema.org", "@type": "Article", "headline": g['h1'], "description": g['desc'], "inLanguage": "fr-FR",
           "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": DOMAIN + url(path), "image": DOMAIN + "/assets/img/og-cozybat.jpg",
           "author": {"@type": "Organization", "name": "Cozybat", "url": DOMAIN + "/"}, "publisher": {"@type": "Organization", "name": "Cozybat", "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/img/logo-cozybat.png"}}}]
    write(path + '.html', head(path, g['title'], g['desc'], ld=ld) + header('guides') + content + cta_band(g['kind']) + footer())

def page_guides():
    cr = [('Accueil', ''), ('Guides', 'guides')]
    cards = ''.join(guide_card(g, 'h2') for g in GUIDES)
    content = f'''<section class="sec" style="padding-top:40px"><div class="wrap">
{crumbs_html(cr)}<p class="kicker">Guides</p><h1 class="h2" style="margin-bottom:12px">Guides façade : prix, aides et conseils</h1>
<p class="lead" style="margin-bottom:36px">Prix au m², aides 2026, choix de l’isolation, fissures : nos réponses aux questions que se posent les propriétaires avant des travaux de façade.</p>
<div class="specs">{cards}</div></div></section>
'''
    write('guides.html', head('guides', 'Guides façade : prix, aides et conseils | Cozybat', 'Prix de l’isolation par l’extérieur et du ravalement au m², aides 2026, isolation intérieure ou extérieure, fissures : les guides de Cozybat.', ld=[crumbs_ld(cr)]) + header('guides') + content + trust() + cta_band() + footer())

def page_404():
    content = f'''<section class="sec"><div class="wrap" style="max-width:820px"><h1 class="h2" style="margin-bottom:18px">Page introuvable</h1>
<p class="lead" style="margin-bottom:28px">Cette page n’existe pas ou a été déplacée. Voici les pages les plus consultées :</p>
<div class="links-row"><a class="btn btn-gold" href="/">Accueil Cozybat</a><a class="btn btn-outline" href="/isolation-exterieure">Isolation par l’extérieur</a><a class="btn btn-outline" href="/ravalement-facade">Ravalement de façade</a><a class="btn btn-outline" href="/nos-realisations">Nos réalisations</a><a class="btn btn-outline" href="/devis">Devis gratuit</a></div></div></section>
'''
    write('404.html', head('404', 'Page introuvable | Cozybat', 'La page demandée est introuvable sur le site de Cozybat.', noindex=True) + header() + content + footer())

def todo(x): return f'<span class="todo">{x}</span>'

def page_mentions():
    cr = [('Accueil', ''), ('Mentions légales', 'mentions-legales')]
    content = f'''<section class="sec"><div class="wrap legal">
{crumbs_html(cr)}<h1>Mentions légales</h1>
<h2>Éditeur du site</h2>
<p>Cozybat SAS, société par actions simplifiée au capital de 1 000 €, créée en 2025<br>
Siège social : 29 rue Archimède, 91420 Morangis<br>
Locaux et rendez-vous : {ADR_TXT}<br>
SIREN 993 112 788 · SIRET {SIRET_H} · RCS Évry<br>
N° de TVA intracommunautaire : FR60 993 112 788<br>
Téléphone : <a href="tel:{TEL}">{TEL_H}</a> · E-mail : <a href="mailto:{MAIL}">{MAIL}</a></p>
<p>Directeur de la publication : David De Abreu, président.</p>
<h2>Qualification et assurance</h2>
<p>Qualification RGE Qualibat n° {RGE} (7131 – isolation thermique par l’extérieur), en cours de validité.<br>
Assurance responsabilité civile décennale : SMABTP. L’attestation d’assurance est remise avec chaque devis.</p>
<h2>Hébergement</h2>
<p>Hostinger International Ltd, 61 Lordou Vironos Street, 6023 Larnaca, Chypre – <a href="https://www.hostinger.fr" rel="noopener">www.hostinger.fr</a>.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, photographies, visuels et le logo de ce site sont la propriété de Cozybat SAS. Toute reproduction sans autorisation est interdite. Les avis clients reproduits proviennent de la fiche Google de l’entreprise.</p>
<h2>Prix indicatifs</h2>
<p>Les fourchettes de prix présentées sur ce site sont indicatives, exprimées toutes taxes comprises, et ne constituent pas une offre. Seul le devis établi après visite technique fait foi.</p>
<h2>Données personnelles</h2>
<p>Le traitement des données transmises par le formulaire de devis est décrit dans notre <a href="/confidentialite">politique de confidentialité</a>.</p>
<p style="margin-top:32px;font-size:13px">Dernière mise à jour : {TODAY}</p>
</div></section>
'''
    write('mentions-legales.html', head('mentions-legales', 'Mentions légales | Cozybat', 'Mentions légales du site cozybat.fr : éditeur Cozybat SAS, SIRET, siège, directeur de publication, hébergeur, qualification et assurance.', ld=[crumbs_ld(cr)]) + header() + content + footer())

def page_confid():
    cr = [('Accueil', ''), ('Politique de confidentialité', 'confidentialite')]
    content = f'''<section class="sec"><div class="wrap legal">
{crumbs_html(cr)}<h1>Politique de confidentialité</h1>
<h2>Responsable du traitement</h2>
<p>Cozybat SAS, 29 rue Archimède, 91420 Morangis – <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>Données collectées par le formulaire de devis</h2>
<p>Nom, téléphone, e-mail et ville (si renseignés), informations sur votre projet (type de travaux, type de maison, surface, créneau de rappel, message) et, le cas échéant, les photos de votre façade.</p>
<h2>Finalité et base légale</h2>
<p>Ces données servent uniquement à vous recontacter, organiser la visite technique et établir votre devis. Le traitement repose sur votre demande (mesures précontractuelles, article 6.1.b du RGPD) et sur votre consentement exprimé dans le formulaire.</p>
<h2>Destinataires</h2>
<p>Les données sont destinées à Cozybat uniquement. Elles transitent par notre hébergeur et notre messagerie électronique. Elles ne sont ni vendues ni cédées à des tiers.</p>
<h2>Durée de conservation</h2>
<p>Trois ans à compter du dernier contact si aucun contrat n’est signé. En cas de chantier, les données liées au contrat sont conservées pendant la durée légale, notamment celle de la garantie décennale.</p>
<h2>Vos droits</h2>
<p>Vous disposez d’un droit d’accès, de rectification, d’effacement, de limitation, d’opposition et de portabilité de vos données. Pour l’exercer : <a href="mailto:{MAIL}">{MAIL}</a>. Vous pouvez aussi adresser une réclamation à la CNIL (<a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>).</p>
<h2>Cookies et mesure d’audience</h2>
<p>Ce site ne dépose aucun cookie publicitaire. Si une mesure d’audience est activée, elle utilise Plausible Analytics, un outil sans cookie qui ne collecte aucune donnée personnelle et ne permet pas de vous identifier.</p>
<h2>Polices et ressources</h2>
<p>Les polices de caractères et les images sont hébergées sur nos propres serveurs : aucune donnée n’est transmise à un service tiers lors de votre visite.</p>
<p style="margin-top:32px;font-size:13px">Dernière mise à jour : {TODAY}</p>
</div></section>
'''
    write('confidentialite.html', head('confidentialite', 'Politique de confidentialité | Cozybat', 'Comment Cozybat utilise et protège les données envoyées par le formulaire de devis : finalité, durée de conservation, droits RGPD.', ld=[crumbs_ld(cr)]) + header() + content + footer())

def stub(old, new, label):
    full = os.path.join(OUT, old)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    tgt = DOMAIN + new
    with open(full, 'w', encoding='utf-8') as f:
        f.write(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{label} (ancienne adresse) | Cozybat</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="{tgt}"><meta http-equiv="refresh" content="0; url={new}"><script>location.replace("{new}")</script></head><body><p>Cette page a été déplacée : <a href="{new}">continuer</a>.</p></body></html>\n')

def seo_files():
    # anciennes adresses .html : redirection de secours si le .htaccess n'est pas actif
    for p, lab in (('isolation-exterieure', 'Isolation par l’extérieur'), ('ravalement-facade', 'Ravalement de façade'), ('devis', 'Devis gratuit'), ('merci', 'Demande envoyée'), ('mentions-legales', 'Mentions légales'), ('confidentialite', 'Confidentialité')):
        stub(p + '.html', f'/{p}/', lab)
    stub('chantiers.html', '/nos-realisations/', 'Nos réalisations')
    stub('peinture-facade.html', '/ravalement-facade/', 'Peinture de façade')
    stub('nettoyage-facade.html', '/ravalement-facade/', 'Nettoyage de façade')
    for k, v in CH.items():
        c = BYSLUG[k]
        stub(f'chantiers/{v["old"]}.html', f'/chantiers/{k}/', f'{c["work"]} à {c["ville"]}')
    pages = '\n'.join(f'- [{t}]({DOMAIN}{u}): {d}' for t, u, d in [
        ('Isolation thermique par l’extérieur', '/isolation-exterieure/', 'système ITE sous enduit, isolants, aides, prix indicatif'),
        ('Ravalement de façade D3 armé', '/ravalement-facade/', 'traitement des fissures, enduit armé, finitions, prix indicatif'),
        ('Nos réalisations', '/nos-realisations/', 'chantiers avant / après en Essonne'),
        ('Devis gratuit', '/devis/', 'demande de devis, visite technique gratuite')] +
        [(f'Façade à {c["name"]}', f'/ravalement-isolation-{c["slug"]}/', f'ravalement et isolation par l’extérieur à {c["name"]} ({c["cp"]})') for c in CITIES])
    write('llms.txt', f'''# Cozybat

> Cozybat SAS est une entreprise d’isolation thermique par l’extérieur (ITE) et de ravalement de façade D3 armé, basée à Morangis (91420) et intervenant dans toute l’Essonne. Qualification RGE Qualibat n° {RGE}, assurance décennale SMABTP, 5,0/5 sur 48 avis Google. Société créée en 2025, métier de façade transmis de père en fils.

Contact : {TEL_H} · {MAIL} · {ADR_TXT}. Visite technique et devis gratuits, réponse sous 48 h ouvrées.

## Pages principales

{pages}

## Informations légales

- [Mentions légales]({DOMAIN}/mentions-legales/)
- [Politique de confidentialité]({DOMAIN}/confidentialite/)
''')
    prio = {'': '1.0', 'isolation-exterieure': '0.9', 'ravalement-facade': '0.9', 'maconnerie-facade': '0.8', 'devis': '0.8', 'nos-realisations': '0.8'}
    rows = ''
    for p, noindex in PAGES:
        if noindex: continue
        pr = prio.get(p, '0.7' if p.startswith('ravalement-isolation-') else ('0.6' if p.startswith('chantiers/') else '0.3'))
        rows += f'  <url><loc>{DOMAIN}{url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n'
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /outils/\nDisallow: /merci/\nDisallow: /contact.php\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    redirects = '\n'.join(f'RewriteRule ^chantiers/{old}(\\.html)?/?$ /chantiers/{new}/ [R=301,L]\nRewriteRule ^assets/img/chantiers/{old}-(avant|apres)\\.webp$ /assets/img/chantiers/{new}-$1.webp [R=301,L]' for new, old in ((k, v['old']) for k, v in CH.items()))
    redirects += '\nRewriteRule ^chantiers/?$ /nos-realisations/ [R=301,L]\nRewriteRule ^assets/img/equipe-cozybat\\.webp$ /assets/img/equipe-cozybat-facadiers-morangis.webp [R=301,L]\nRewriteRule ^assets/js/main\\.js$ /assets/js/site.js [R=301,L]'
    write('.htaccess', f'''# Cozybat — réglages serveur (Apache / LiteSpeed — Hostinger)
Options -Indexes -MultiViews
DirectoryIndex index.html index.php
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8

<IfModule mod_rewrite.c>
RewriteEngine On

# 0. Fichiers du dépôt Git jamais servis (sources, historique)
RewriteRule ^(\\.git|\\.github|_build)(/|$) - [F,L]
RewriteRule ^(README\\.md|\\.gitignore)$ - [F,L]

# 1. HTTPS obligatoire et domaine sans www
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^ https://cozybat.fr%{{REQUEST_URI}} [L,R=301]

# 2. Anciennes adresses du site
RewriteRule ^chantiers\\.html$ /nos-realisations/ [R=301,L]
RewriteRule ^(peinture|nettoyage)-facade(\\.html)?/?$ /ravalement-facade/ [R=301,L]
RewriteRule ^(realisations|chantier|admin)(\\.html)?/?$ /nos-realisations/ [R=301,L]
{redirects}

# 3. /index.html -> /  et  /page/index.html -> /page/
RewriteCond %{{THE_REQUEST}} \\s/+(.*?/)?index\\.html[\\s?] [NC]
RewriteRule ^ /%1 [R=301,L]

# 4. Anciennes pages en .html -> nouvelle adresse /page/ (seulement si la nouvelle page existe)
RewriteCond %{{THE_REQUEST}} \\s/+([^?\\s]+?)\\.html[\\s?] [NC]
RewriteCond %{{DOCUMENT_ROOT}}/%1/index.html -f
RewriteRule ^ /%1/ [R=301,L]
</IfModule>

# Compression
<IfModule mod_brotli.c>
AddOutputFilterByType BROTLI_COMPRESS text/html text/css application/javascript image/svg+xml application/json application/manifest+json text/xml application/xml
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json application/manifest+json text/xml application/xml
</IfModule>

# Cache navigateur
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/x-icon "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType application/manifest+json "access plus 1 week"
ExpiresByType text/html "access plus 0 seconds"
</IfModule>
AddType image/webp .webp
AddType font/woff2 .woff2
AddType application/manifest+json .webmanifest

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Strict-Transport-Security "max-age=31536000"
<FilesMatch "\\.(webp|png|jpe?g|ico|woff2|css|js)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
</IfModule>
''')

if __name__ == '__main__':
    page_index(); page_system('ite'); page_system('d3'); page_realisations()
    for c in CHANTIERS: page_case(c)
    for c in CITIES: page_city(c)
    page_guides(); page_maconnerie()
    for g in GUIDES: page_guide(g)
    page_devis(); page_merci(); page_404(); page_mentions(); page_confid(); seo_files()
    print('ok', len(PAGES), 'pages')
