#!/usr/bin/env python3
"""Génère toutes les pages HTML du site Cozybat dans ./site"""
import json, os, html
from datetime import date

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
DOMAIN = 'https://cozybat.fr'
TEL, TEL_H = '+33695441793', '06 95 44 17 93'
MAIL = 'contact.cozybat@gmail.com'
IG = 'https://www.instagram.com/cozybat_renovation/'
GOOGLE = 'https://share.google/EaXcsYWDln5izOgJN'
ADR_RDV = '6 avenue Évariste Galois, 91420 Morangis'
TODAY = date.today().isoformat()
import time
VER = time.strftime('%Y%m%d%H%M')
e = html.escape

# ------------------------------------------------------------------ données
LAYERS_ITE = [
  dict(id='support', name='Support existant', plain='C’est votre mur actuel. Il est vérifié et préparé avant toute pose.',
       text='Diagnostic préalable du mur : planéité, cohésion, humidité. Nettoyage, traitement des fissures et des parties non adhérentes avant pose.',
       specs=[('Nature', 'Béton, parpaing, brique, pierre'), ('Préparation', 'Selon diagnostic')]),
  dict(id='colle', name='Collage', plain='Une colle spéciale est posée au dos de chaque panneau : un cordon sur tout le tour et quelques plots au centre.',
       text='Mortier-colle appliqué au dos de chaque panneau isolant en boudin périphérique et en plots centraux. Le boudin périphérique ferme le pourtour du panneau et évite toute circulation d’air derrière l’isolant.',
       specs=[('Application', 'Boudin périphérique + plots'), ('Support', 'Au dos de chaque panneau')]),
  dict(id='isolant', name='Isolant', plain='Le cœur du système : il garde la chaleur dans la maison l’hiver et la fraîcheur l’été.',
       text='Polystyrène expansé graphité : performance élevée à épaisseur réduite, faible poids. Plaques posées en quinconce, joints serrés, sans joint filant aux angles des baies.',
       specs=[('Matériau', 'PSE graphité'), ('Conductivité', 'λ ≈ 0,031 W/m.K'), ('Épaisseur', '140 à 200 mm'), ('Résistance visée', 'R ≥ 3,7 m².K/W'), ('Autres isolants', 'Laine de roche, fibre de bois')]),
  dict(id='fixation', name='Fixation', plain='Des chevilles renforcent la tenue des panneaux, en plus de la colle.',
       text='Chevilles à rosace en complément du collage, selon la nature du support, la hauteur de l’ouvrage et l’exposition au vent. Le plan de chevillage suit les prescriptions du système.',
       specs=[('Type', 'Chevilles à rosace'), ('Densité', 'Selon plan de chevillage')]),
  dict(id='sousenduit', name='Sous-enduit', plain='Une première couche d’enduit recouvre et protège l’isolant.',
       text='Couche de base appliquée sur l’isolant. Elle reçoit l’armature et apporte la résistance mécanique de l’ensemble.',
       specs=[('Épaisseur', '3 à 5 mm'), ('Rôle', 'Résistance mécanique')]),
  dict(id='armature', name='Armature', plain='Un filet noyé dans l’enduit empêche les fissures d’apparaître.',
       text='Treillis en fibre de verre marouflé dans le sous-enduit frais, recouvrement des lés d’environ 10 cm, renforts en diagonale aux angles des ouvertures. Il limite la fissuration.',
       specs=[('Matériau', 'Fibre de verre'), ('Recouvrement', '≈ 10 cm')]),
  dict(id='intermediaire', name='Couche intermédiaire', plain='Une sous-couche d’accroche prépare l’enduit de base à recevoir les couches suivantes.',
       text='Couche d’impression appliquée sur le sous-enduit armé sec, qui favorise l’accroche des couches suivantes.',
       specs=[('Type', 'Impression d’accroche')]),
  dict(id='regulateur', name='Régulateur de fond', plain='Une couche teintée qui uniformise le fond, pour une couleur de façade bien régulière.',
       text='Régulateur de fond teinté dans le ton de la finition : il uniformise l’absorption et la couleur du support et limite les risques de nuançage de l’enduit de finition.',
       specs=[('Type', 'Régulateur de fond teinté'), ('Teinte', 'Proche de la finition')]),
  dict(id='finition', name='Couche de finition', plain='La couche visible : elle protège de la pluie et donne la couleur de votre façade.',
       text='Enduit de finition taloché, gratté ou lisse, dans la teinte de votre choix. Il protège le système des intempéries et donne l’aspect final de la façade.',
       specs=[('Aspect', 'Taloché, gratté ou lisse'), ('Teinte', 'Au choix sur nuancier'), ('Épaisseur', '1,5 à 3 mm selon grain')]),
]
D3_OVR = {
  'support': dict(name='Façade existante', plain='Votre façade actuelle, souvent fissurée. Elle est nettoyée, réparée et préparée avant tout.',
       text='Diagnostic du revêtement existant : adhérence, fissuration, humidité. Lavage, piquage des parties non adhérentes, ouverture et traitement des fissures, reprise des épaufrures.',
       specs=[('Nature', 'Enduit ancien, béton, maçonnerie enduite'), ('Préparation', 'Lavage, piquage, fissures')]),
  'sousenduit': dict(name='Couche de base', plain='Une première couche appliquée sur la façade préparée, dans laquelle le filet est noyé.',
       text='Couche de base du revêtement armé appliquée sur le support préparé, avec primaire si le système le prévoit. Elle reçoit l’armature.',
       specs=[('Rôle', 'Enrobage de l’armature'), ('Consommation', 'Selon système')]),
  'armature': dict(plain='Un filet noyé dans l’enduit, qui ponte les fissures de la façade et évite qu’elles réapparaissent.',
       text='Treillis en fibre de verre marouflé dans la couche de base fraîche, recouvrement des lés d’environ 10 cm, renforts aux angles des ouvertures. Il ponte les fissures du support et renforce le revêtement.',
       specs=[('Matériau', 'Fibre de verre'), ('Recouvrement', '≈ 10 cm')]),
}
def layers(sys):
    L = [dict(l) for l in LAYERS_ITE]
    if sys == 'd3':
        L = [l for l in L if l['id'] not in ('colle', 'isolant', 'fixation')]
        for l in L: l.update(D3_OVR.get(l['id'], {}))
    for i, l in enumerate(L): l['num'] = '%02d' % i
    return L

CHANTIERS = [
  dict(slug='ite-ollainville', type='ite', ville='Ollainville', label='ITE · PSE 140 mm',
       h1='Isolation par l’extérieur à Ollainville', title='ITE en polystyrène 140 mm à Ollainville (91)',
       desc='Isolation par l’extérieur en polystyrène 140 mm : l’ancien crépi disparaît sous un enduit neuf, lisse et blanc.',
       facts=[('Prestation', 'Isolation thermique par l’extérieur'), ('Isolant', 'PSE graphité 140 mm'), ('Finition', 'Enduit blanc'), ('Commune', 'Ollainville (91)')]),
  dict(slug='ite-saint-michel-sur-orge', type='ite', ville='Saint-Michel-sur-Orge', label='ITE',
       h1='Isolation par l’extérieur à Saint-Michel-sur-Orge', title='Isolation par l’extérieur d’une maison à Saint-Michel-sur-Orge (91)',
       desc='Isolation par l’extérieur d’une maison sur deux niveaux : la surélévation en brique et l’ancien enduit disparaissent sous un même enduit neuf, sans démarcation.',
       facts=[('Prestation', 'Isolation thermique par l’extérieur'), ('Particularité', 'Surélévation en brique'), ('Période', 'Hiver 2025'), ('Commune', 'Saint-Michel-sur-Orge (91)')]),
  dict(slug='ite-lucarnes-sainte-genevieve-des-bois', type='ite', ville='Sainte-Geneviève-des-Bois', label='ITE · Lucarnes',
       h1='Isolation des lucarnes à Sainte-Geneviève-des-Bois', title='ITE des lucarnes à Sainte-Geneviève-des-Bois (91)',
       desc='Isolation par l’extérieur des lucarnes : la brique apparente disparaît sous un enduit neuf, dans la teinte du reste de la façade.',
       facts=[('Prestation', 'Isolation thermique par l’extérieur'), ('Ouvrage', 'Lucarnes'), ('Finition', 'Teinte assortie à la façade'), ('Commune', 'Sainte-Geneviève-des-Bois (91)')]),
  dict(slug='ravalement-morangis', type='d3', ville='Morangis', label='Ravalement D3 armé',
       h1='Ravalement D3 armé à Morangis', title='Ravalement de façade D3 armé à Morangis (91)',
       desc='Façade délavée et encrassée remise à neuf : préparation du support, enduit armé sur toute la surface et finition en deux teintes.',
       facts=[('Prestation', 'Ravalement D3 armé'), ('Finition', 'Deux teintes'), ('Commune', 'Morangis (91)')]),
  dict(slug='ravalement-yerres', type='d3', ville='Yerres', label='Ravalement D3 armé',
       h1='Ravalement D3 armé à Yerres', title='Ravalement de façade D3 armé à Yerres (91)',
       desc='Façade grise et tachée reprise en enduit armé, finition beige ; les câbles apparents sont désormais dissimulés sous des moulures blanches.',
       facts=[('Prestation', 'Ravalement D3 armé'), ('Finition', 'Beige'), ('Détail', 'Câbles sous moulures'), ('Commune', 'Yerres (91)')]),
  dict(slug='ravalement-brunoy', type='d3', ville='Brunoy', label='Ravalement armé',
       h1='Ravalement armé à Brunoy', title='Ravalement de façade armé à Brunoy (91)',
       desc='L’ancien crépi gris laisse place à un enduit armé lisse, soubassement compris, souligné par une bande de séparation.',
       facts=[('Prestation', 'Ravalement armé'), ('Détail', 'Soubassement et bande de séparation'), ('Commune', 'Brunoy (91)')]),
]
AVIS = [
  ('Laura J.', 'FAÇADE', 'Nous avons fait appel à la société Cozybat pour la façade de notre maison. Ils sont professionnels, engagés, ponctuels et compétents. Le travail est propre et soigné. […] Nous leur donnons d’ailleurs un autre chantier au printemps !'),
  ('Johan F.', 'ITE', 'Nous avons réalisé l’isolation par l’extérieur avec Cozybat et nous sommes entièrement satisfaits. Du premier rendez-vous jusqu’à la fin des travaux tout a été parfait. Merci à eux et nous les recommandons vivement.'),
  ('Ambra N.', 'PEINTURE · FAÇADE', 'Derrière cette jeune entreprise se cachent un véritable savoir-faire, un grand professionnalisme et une belle histoire familiale dans le bâtiment. […] Le résultat est tout simplement impeccable ! […] Le chantier a été réalisé dans les délais annoncés, dans une ambiance agréable et avec un excellent rapport qualité-prix.'),
  ('Florence M.', 'RAVALEMENT', 'Ils ont fait un devis très détaillé, m’ont expliqué toutes les étapes et le pourquoi des produits utilisés. Ils se sont déplacés à plusieurs reprises pour me montrer des échantillons, ont fait des photos de simulation […]. Ma maison a une centaine d’années, elle était très abîmée et maintenant j’ai la plus jolie maison de la rue.'),
  ('Tsimba R.', 'ITE', 'L’équipe de Cozybat a été à l’écoute de notre projet et a su y répondre avec professionnalisme. Malgré la contrainte de temps, l’équipe a réussi à répondre à nos attentes : isoler par l’extérieur les chiens-assis.'),
  ('Julien C.', 'CRÉPI', 'Entreprise professionnelle, donne plusieurs possibilités avec de bons conseils. J’avais pas mal de crépis à refaire. Au top, vous pouvez compter dessus. Chantier bien nettoyé en repartant, même chez le voisin.'),
  ('Clotilde Y.', 'RAVALEMENT · ITE', 'L’entreprise a réalisé un ravalement complet de notre maison ainsi qu’une isolation par l’extérieur. Travail très soigné, l’équipe est réactive et à l’écoute.'),
]
TICKER = [('Le travail est propre et soigné', 'Laura J.'), ('Le résultat est tout simplement impeccable !', 'Ambra N.'),
          ('Du premier rendez-vous jusqu’à la fin des travaux tout a été parfait', 'Johan F.'),
          ('Chantier bien nettoyé en repartant, même chez le voisin', 'Julien C.'), ('J’ai la plus jolie maison de la rue', 'Florence M.')]
VILLES = ['Morangis', 'Savigny-sur-Orge', 'Athis-Mons', 'Juvisy-sur-Orge', 'Chilly-Mazarin', 'Wissous', 'Paray-Vieille-Poste', 'Longjumeau', 'Massy', 'Palaiseau', 'Épinay-sur-Orge', 'Viry-Châtillon', 'Morsang-sur-Orge', 'Sainte-Geneviève-des-Bois', 'Saint-Michel-sur-Orge', 'Brétigny-sur-Orge', 'Villemoisson-sur-Orge', 'Montlhéry', 'Linas', 'Marcoussis', 'Arpajon', 'Ollainville', 'Villebon-sur-Yvette', 'Les Ulis', 'Orsay', 'Gif-sur-Yvette', 'Igny', 'Verrières-le-Buisson', 'Grigny', 'Ris-Orangis', 'Évry-Courcouronnes', 'Corbeil-Essonnes', 'Draveil', 'Vigneux-sur-Seine', 'Montgeron', 'Yerres', 'Brunoy', 'Mennecy', 'Étampes']
FAQ_HOME = [
  ('Combien de temps dure un chantier ?', 'Quelques semaines pour une maison individuelle, selon la surface, l’état du support et la météo. La durée est précisée sur le devis.'),
  ('Faut-il une autorisation de la mairie ?', 'Dès que l’aspect extérieur change (isolation, changement de teinte), une déclaration préalable de travaux est nécessaire. Le PLU de votre commune peut imposer certaines teintes. Nous vous accompagnons pour le dossier.'),
  ('Peut-on rester chez soi pendant les travaux ?', 'Oui. Tout se fait depuis l’extérieur, sur échafaudage : l’intérieur de la maison n’est pas touché.'),
  ('Quelle est la différence entre ITE et ravalement D3 armé ?', 'L’ITE ajoute un isolant sur les murs avant l’enduit : la maison est mieux isolée et la façade refaite. Le ravalement D3 armé ne comporte pas d’isolant : il traite les fissures avec un enduit armé d’un filet et redonne un aspect neuf à la façade.'),
  ('Quelles aides pour l’isolation par l’extérieur ?', 'Depuis 2026, l’ITE seule n’est plus financée par MaPrimeRénov’ par geste. Elle reste aidée par les primes CEE (entreprise RGE obligatoire, ce qui est notre cas), la TVA à 5,5 % et l’éco-prêt à taux zéro, et par MaPrimeRénov’ dans le cadre d’une rénovation d’ampleur. Le montant est estimé lors du devis.'),
  ('Quelles garanties ?', 'Nos travaux d’isolation et de ravalement sont couverts par une assurance décennale SMABTP. L’attestation est remise avec le devis.'),
  ('Le devis est-il gratuit ?', 'Oui. Réponse sous 48 h ouvrées, puis visite technique et devis détaillé gratuits, sans engagement.'),
]
FAQ_ITE = [
  ('Quelles aides pour une isolation par l’extérieur ?', 'Les primes CEE, la TVA à 5,5 % et l’éco-prêt à taux zéro réduisent le coût, selon vos revenus et la performance de l’isolant (résistance R ≥ 3,7 m².K/W). Depuis 2026, MaPrimeRénov’ ne finance l’ITE que dans le cadre d’une rénovation d’ampleur (Parcours accompagné). Cozybat est qualifiée RGE Qualibat. Le détail est dans notre guide des aides.'),
  ('Quelle épaisseur d’isolant faut-il ?', 'En général 140 à 200 mm de polystyrène graphité pour atteindre la performance demandée par les aides. Nous proposons aussi la laine de roche et la fibre de bois selon le projet.'),
  ('Combien de temps dure une ITE ?', 'Quelques semaines pour une maison individuelle, selon la surface, les points singuliers (appuis, descentes, volets) et la météo.'),
  ('Faut-il une autorisation ?', 'Oui : l’isolation par l’extérieur modifie l’aspect de la façade, une déclaration préalable de travaux est donc nécessaire. Nous vous accompagnons pour le dossier.'),
  ('Que deviennent mes volets et mes appuis de fenêtre ?', 'Ils sont traités au cas par cas lors de la visite technique : adaptation ou remplacement des appuis, des gonds et des volets. Tout est chiffré sur le devis.'),
  ('Quelle garantie ?', 'Nos travaux sont couverts par une assurance décennale SMABTP, attestation remise avec le devis.'),
]
FAQ_D3 = [
  ('Quelle différence entre un ravalement D3 armé et une peinture ?', 'Une peinture redonne de la couleur mais ne traite pas les fissures. Le D3 armé intègre un filet en fibre de verre noyé dans l’enduit sur toute la surface : il ponte les fissures du support et limite leur réapparition.'),
  ('Les fissures peuvent-elles revenir ?', 'L’armature limite fortement la réapparition des microfissures. Les fissures structurelles (mouvement du bâtiment) relèvent d’un diagnostic spécifique : nous vous le signalons lors de la visite.'),
  ('Faut-il une autorisation ?', 'Un changement de teinte ou d’aspect demande une déclaration préalable de travaux, et certaines communes l’imposent pour tout ravalement. Nous vérifions les règles de votre commune.'),
  ('Combien de temps dure un ravalement ?', 'En général une à trois semaines pour une maison individuelle, selon l’état du support et la météo.'),
  ('Y a-t-il des aides pour un ravalement ?', 'Un ravalement seul n’ouvre pas droit aux aides à la rénovation énergétique, mais bénéficie d’une TVA à 10 % pour un logement de plus de deux ans. Si vous envisagez aussi d’isoler, l’ITE combine les deux et ouvre droit aux primes CEE et à la TVA à 5,5 %.'),
  ('Quelle garantie ?', 'Nos travaux de ravalement sont couverts par notre assurance décennale SMABTP.'),
]
PERKS = {
  'ite': [('Ponts thermiques traités', 'L’isolant enveloppe la façade en continu, y compris au droit des planchers.'),
          ('Aucune surface perdue', 'Travaux depuis l’extérieur : les pièces restent habitables pendant le chantier.'),
          ('Façade rénovée', 'Isolation et ravalement en une seule opération.'),
          ('Aides mobilisables', 'Primes CEE, TVA à 5,5 % et éco-PTZ, sous conditions de performance et de ressources.')],
  'd3': [('Fissures traitées', 'L’armature ponte les fissures du support et limite leur réapparition.'),
         ('Façade protégée', 'Le revêtement protège le mur des infiltrations d’eau de pluie.'),
         ('Aspect neuf', 'Choix de la finition et de la teinte, pour un rendu homogène.'),
         ('Logement occupé', 'Travaux entièrement depuis l’extérieur, sans gêne à l’intérieur.')],
}
METHODE = [('01', 'Visite technique', 'Relevé des façades, diagnostic du support, repérage des points singuliers : appuis, tableaux, descentes, coffres.'),
           ('02', 'Devis détaillé', 'Chiffrage couche par couche, finition et teinte au choix, et montage des dossiers d’aides pour l’ITE.'),
           ('03', 'Chantier', 'Échafaudage, préparation du support, pose du système, finitions et nettoyage.'),
           ('04', 'Réception', 'Contrôle contradictoire, remise des documents, ouvrage couvert par l’assurance décennale.')]
PRIX = {
  'ite': dict(code='01 · ISOLATION PAR L’EXTÉRIEUR', title='ITE sous enduit', amt='180 €', unit='TTC / m² ISOLÉ', href='isolation-exterieure.html', projet='ite',
              pts=['Isolant PSE graphité 14 cm, système sous Avis Technique', 'Échafaudage, préparation, enduit et finition compris', 'TVA 5,5 % · primes CEE et MaPrimeRénov’ déductibles selon vos ressources']),
  'd3': dict(code='02 · RAVALEMENT', title='Ravalement D3 armé', amt='100 €', unit='TTC / m² DE FAÇADE', href='ravalement-facade.html', projet='d3',
             pts=['Lavage, traitement des fissures et des parties abîmées', 'Enduit armé d’un filet sur toute la surface, régulateur et finition', 'TVA 10 % · échafaudage et nettoyage compris']),
}

# ------------------------------------------------------------------ fragments
ICON_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
ICON_IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'

def head(b, title, desc, path, extra_ld=None, noindex=False):
    canon = DOMAIN + '/' + path if path else DOMAIN + '/'
    ld = [ORG_LD] + (extra_ld or [])
    lds = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in ld)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
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
<meta property="og:image" content="{DOMAIN}/assets/img/og-cozybat.jpg">
<meta name="theme-color" content="#2E3A47">
<link rel="icon" href="{b}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{b}assets/img/fav-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{b}assets/img/fav-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="{b}assets/img/fav-180.png">
<link rel="manifest" href="{b}site.webmanifest">
<link rel="preload" href="{b}assets/fonts/poppins-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{b}assets/css/style.css?v={VER}">
{lds}<!-- Statistiques sans cookie (Plausible) : retirez les commentaires une fois le compte créé sur plausible.io
<script defer data-domain="cozybat.fr" src="https://plausible.io/js/script.js"></script>
-->
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''

ORG_LD = {
  "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": DOMAIN + "/#entreprise",
  "name": "Cozybat", "legalName": "Cozybat SAS", "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo-cozybat.png",
  "image": DOMAIN + "/assets/img/og-cozybat.jpg", "telephone": TEL, "email": MAIL,
  "description": "Isolation thermique par l’extérieur (ITE) et ravalement de façade D3 armé en Essonne. Entreprise RGE Qualibat.",
  "address": {"@type": "PostalAddress", "streetAddress": "6 avenue Évariste Galois", "postalCode": "91420", "addressLocality": "Morangis", "addressRegion": "Île-de-France", "addressCountry": "FR"},
  "areaServed": {"@type": "AdministrativeArea", "name": "Essonne"},
  "sameAs": [IG], "vatID": "FR60993112788",
  "knowsAbout": ["Isolation thermique par l’extérieur", "Ravalement de façade", "Enduit armé D3"]
}

def header(b, active=''):
    def cur(k): return ' aria-current="page"' if k == active else ''
    return f'''<header class="hd">
<div class="wrap hd-in">
<a class="hd-logo" href="{b}index.html" aria-label="Cozybat, accueil"><img src="{b}assets/img/logo-cozybat.png" alt="Cozybat" width="600" height="300"></a>
<nav class="hd-nav" aria-label="Navigation principale">
<a href="{b}isolation-exterieure.html"{cur('ite')}>Isolation extérieure</a>
<a href="{b}ravalement-facade.html"{cur('d3')}>Ravalement</a>
<a href="{b}chantiers.html"{cur('chantiers')}>Réalisations</a>
<a href="{b}index.html#avis">Avis</a>
<a class="hd-tel" href="tel:{TEL}">{TEL_H}</a>
<a class="btn btn-gold" href="{b}devis.html" data-track="Clic devis">Devis gratuit</a>
</nav>
<div class="hd-mob">
<a class="icon-btn gold" href="tel:{TEL}" aria-label="Appeler le {TEL_H}">{ICON_TEL}</a>
<button class="icon-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="mnav" aria-label="Menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div>
</div>
<nav class="mnav" id="mnav" aria-label="Menu mobile">
<a href="{b}isolation-exterieure.html">Isolation par l’extérieur</a>
<a href="{b}ravalement-facade.html">Ravalement de façade</a>
<a href="{b}chantiers.html">Réalisations</a>
<a href="{b}index.html#avis">Avis clients</a>
<a href="{b}index.html#faq">Questions fréquentes</a>
<a class="btn btn-gold" href="{b}devis.html">Demander un devis gratuit</a>
</nav>
</header>
<main id="contenu">
'''

def footer(b):
    return f'''</main>
<footer class="ft">
<div class="wrap ft-grid">
<div>
<img src="{b}assets/img/logo-cozybat-clair.png" alt="Cozybat" width="600" height="300" loading="lazy">
<p>Isolation thermique par l’extérieur et ravalement de façade en Essonne.</p>
<p style="margin-top:10px"><a class="ig" href="{IG}" rel="noopener">{ICON_IG}@cozybat_renovation</a></p>
</div>
<div>
<h2>Contact</h2>
<ul>
<li><a href="tel:{TEL}">{TEL_H}</a></li>
<li><a href="mailto:{MAIL}">{MAIL}</a></li>
<li>Rendez-vous : {ADR_RDV}</li>
<li><a href="{b}devis.html">Demander un devis gratuit</a></li>
</ul>
</div>
<div>
<h2>Nos spécialités</h2>
<ul>
<li><a href="{b}isolation-exterieure.html">Isolation par l’extérieur</a></li>
<li><a href="{b}ravalement-facade.html">Ravalement D3 armé</a></li>
<li><a href="{b}chantiers.html">Nos réalisations</a></li>
</ul>
</div>
<div>
<h2>Garanties</h2>
<ul>
<li>RGE Qualibat n° E-E213612</li>
<li>Assurance décennale SMABTP</li>
<li>5,0/5 sur 44 avis Google</li>
</ul>
</div>
</div>
<div class="wrap ft-bot">
<p>© {date.today().year} Cozybat SAS · SIRET 993 112 788 00019 · Morangis (91)</p>
<p><a href="{b}mentions-legales.html">Mentions légales</a> · <a href="{b}confidentialite.html">Confidentialité</a></p>
</div>
</footer>
<nav class="callbar" aria-label="Contact rapide">
<a class="c1" href="tel:{TEL}">Appeler</a>
<a class="c2" href="{b}devis.html" data-track="Clic devis">Devis gratuit</a>
</nav>
<script src="{b}assets/js/main.js?v={VER}" defer></script>
</body>
</html>
'''

SWOOSH = '''<svg class="hero-swoosh" aria-hidden="true" viewBox="0 0 1440 260" preserveAspectRatio="none"><path d="M0,210 C280,90 760,40 1440,120 L1440,150 C820,80 360,120 40,236 Z" fill="#EDAA30"/><path d="M120,238 C380,150 700,128 1040,140 C720,150 420,180 210,250 Z" fill="#EDAA30" opacity=".75"/></svg>'''

def h1_lines(w1, extra=None):
    return f'''<h1 class="h1"><span class="ln"><span class="rise" style="animation-delay:.15s">{w1}</span></span><span class="ln"><span class="rise" style="animation-delay:.3s">couches.</span></span><span class="ln"><span class="rise hl" style="animation-delay:.45s">Zéro</span></span><span class="ln"><span class="rise hl" style="animation-delay:.6s">raccourci.</span></span>{extra or ''}</h1>'''

def ticker():
    items = ''.join(f'<span class="tk"><span class="st" aria-hidden="true">★★★★★</span><q>{e(q)}</q><b>{e(n)}</b></span>' for q, n in TICKER * 2)
    return f'<div class="ticker" role="region" aria-label="Extraits d’avis Google"><div class="ticker-track">{items}</div></div>\n'

def trust(b):
    return f'''<section class="trust" aria-label="Pourquoi nous faire confiance"><div class="wrap trust-grid">
<a class="trust-it" href="{GOOGLE}" rel="noopener"><strong>5,0 <em>★★★★★</em></strong><span>44 avis Google →</span></a>
<div class="trust-it"><strong>RGE</strong><span>Qualibat E-E213612 · ITE</span></div>
<div class="trust-it"><strong>De père en fils</strong><span>Un métier de famille</span></div>
<div class="trust-it"><strong>Décennale</strong><span>Assurée chez SMABTP</span></div>
<div class="trust-it"><strong>48 h</strong><span>Réponse · visite et devis gratuits</span></div>
</div></section>
'''

def ba_card(b, c, link=True, tag='h3'):
    img = f'{b}assets/img/chantiers/{c["slug"]}'
    title = f'<a href="{b}chantiers/{c["slug"]}.html">{e(c["ville"])}</a>' if link else f'<strong>{e(c["ville"])}</strong>'
    return f'''<figure class="ba-card" data-type="{c['type']}">
<div class="ba">
<img src="{img}-avant.webp" alt="Façade avant travaux, {e(c['ville'])}" width="900" height="1100" loading="lazy" decoding="async">
<img class="after" src="{img}-apres.webp" alt="Façade après travaux, {e(c['ville'])}" width="900" height="1100" loading="lazy" decoding="async">
<span class="bar" aria-hidden="true"></span><span class="knob" aria-hidden="true">↔</span>
<span class="tag l" aria-hidden="true">AVANT</span><span class="tag r" aria-hidden="true">APRÈS</span>
<input type="range" min="0" max="100" value="50" aria-label="Comparer avant et après, {e(c['ville'])}">
</div>
<figcaption class="ba-cap">{title}<span>{e(c['label'].upper())}</span><p>{e(c['desc'])}</p></figcaption>
</figure>'''

def avis_section(b):
    cards = ''.join(f'''<figure class="avis"><div class="avis-top"><span class="st" aria-label="5 étoiles sur 5">★★★★★</span><small>{t}</small></div><blockquote>« {e(x)} »</blockquote><figcaption>— {e(n)}</figcaption></figure>''' for n, t, x in AVIS)
    return f'''<section class="sec sec-dark" id="avis"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Avis clients</p><h2 class="h2">Ils nous ont confié leur façade.</h2></div>
<a class="score" href="{GOOGLE}" rel="noopener"><strong>5,0 <em>★★★★★</em></strong><span>LES 44 AVIS SUR GOOGLE →</span></a></div>
<div class="avis-cols">{cards}</div>
</div></section>
'''

def team_section(b):
    chips = ''.join(f'<li>{e(v)}</li>' for v in VILLES)
    return f'''<section class="sec sec-warm" id="equipe"><div class="wrap team">
<div class="team-photo" data-reveal><img src="{b}assets/img/equipe-cozybat.webp" alt="David et Vincent, les associés de Cozybat, devant une maison en meulière" width="820" height="1093" loading="lazy"></div>
<div class="team-txt">
<div><p class="kicker">Qui sommes-nous</p><h2 class="h2" style="margin-bottom:18px">Une jeune équipe, un métier de famille.</h2>
<p>Cozybat, ce sont David et Vincent, associés et présents sur chaque chantier avec leur équipe. Le métier de façadier se transmet de père en fils dans la famille : nous avons appris sur les chantiers bien avant de créer Cozybat, et nous sommes spécialisés en ravalement et en isolation par l’extérieur.</p>
<p style="margin-top:12px">Un seul interlocuteur de la visite à la réception, et des rendez-vous possibles dans nos locaux à Morangis.</p></div>
<div class="zone"><h3>Zone d’intervention · toute l’Essonne (91)</h3><ul class="chips">{chips}</ul>
<p>Votre commune n’apparaît pas ? <a href="tel:{TEL}">Appelez-nous</a> : nous intervenons aussi dans les départements voisins.</p></div>
</div></div></section>
'''

def methode_section(sys=None):
    st = ''.join(f'<div class="st4"><div class="line"><i style="transition-delay:{i*.15:.2f}s"></i></div><small>{n}</small><h3>{t}</h3><p>{x}</p></div>' for i, (n, t, x) in enumerate(METHODE))
    perks = ''
    if sys:
        perks = '<div class="perks">' + ''.join(f'<div class="perk"><h3>{t}</h3><p>{x}</p></div>' for t, x in PERKS[sys]) + '</div>'
    return f'''<section class="sec sec-dark" id="methode"><div class="wrap" data-reveal>
<p class="kicker">Méthode</p><h2 class="h2" style="margin-bottom:48px">Du diagnostic à la réception.</h2>
<div class="steps4">{st}</div>{perks}
</div></section>
'''

def price_card(b, k, dark=False):
    p = PRIX[k]
    pts = ''.join(f'<li>{x}</li>' for x in p['pts'])
    return f'''<div class="price{' dark' if dark else ''}"><small>{p['code']}</small><h3>{p['title']}</h3>
<p class="amt"><span>à partir de</span><b>{p['amt']}</b><i>{p['unit']}</i></p><ul>{pts}</ul>
<a class="btn {'btn-gold' if dark else 'btn-navy'}" href="{b}devis.html?projet={p['projet']}" data-track="Clic devis">Demander mon devis</a></div>'''

def prix_section(b, keys):
    cards = ''.join(price_card(b, k, dark=(i == 0)) for i, k in enumerate(keys))
    return f'''<section class="sec sec-warm" id="prix"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Prix</p><h2 class="h2">Combien ça coûte ?</h2></div>
<p class="lead">Des prix clairs, tout compris : échafaudage, préparation, pose et nettoyage du chantier.</p></div>
<div class="prices">{cards}</div>
<p class="note">Prix indicatifs pour une maison individuelle en Essonne. Le prix exact dépend de la surface, de l’état du support et des points singuliers (appuis, descentes, volets) : il est fixé après la visite technique gratuite.</p>
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

def form_block(b):
    def pills(name, opts, req=False):
        return '<div class="choice">' + ''.join(f'<label class="pill"><input type="radio" name="{name}" value="{v}"{" required" if req and i == 0 else ""}><span>{l}</span></label>' for i, (v, l) in enumerate(opts)) + '</div>'
    return f'''<form class="form" data-wizard method="post" action="{b}contact.php" enctype="multipart/form-data" aria-label="Demande de devis">
<div class="form-top"><span data-form-num>DEMANDE DE DEVIS</span><span data-form-name></span></div>
<div class="prog" aria-hidden="true"><i data-form-prog></i></div>
<fieldset class="fs" data-name="VOTRE PROJET"><legend>Quel est votre projet ?</legend>
{pills('projet', [('ite', 'Isolation par l’extérieur'), ('d3', 'Ravalement D3 armé'), ('autre', 'Autre / je ne sais pas')])}
</fieldset>
<fieldset class="fs" data-name="VOTRE MAISON"><legend>Votre maison</legend>
{pills('maison', [('individuelle', 'Maison individuelle'), ('mitoyenne', 'Maison mitoyenne'), ('autre', 'Autre bâtiment')])}
<span class="lbl">Surface de façade approximative</span>
{pills('surface', [('<80', 'Moins de 80 m²'), ('80-150', '80 à 150 m²'), ('>150', 'Plus de 150 m²'), ('nsp', 'Je ne sais pas')])}
<div class="form-nav form-nav-js"><button class="btn btn-back" type="button" data-prev>← Retour</button><button class="btn btn-navy" type="button" data-next>Continuer →</button></div>
</fieldset>
<fieldset class="fs" data-name="VOS COORDONNÉES"><legend>Vos coordonnées</legend>
<div class="field"><label class="lbl" for="f-nom">Nom *</label><input id="f-nom" name="nom" type="text" autocomplete="name" required maxlength="80"></div>
<div class="row2">
<div class="field"><label class="lbl" for="f-tel">Téléphone *</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" required maxlength="30"></div>
<div class="field"><label class="lbl" for="f-ville">Ville</label><input id="f-ville" name="ville" type="text" autocomplete="address-level2" maxlength="60"></div>
</div>
<div class="field"><label class="lbl" for="f-mail">E-mail</label><input id="f-mail" name="email" type="email" autocomplete="email" maxlength="120"></div>
<span class="lbl">Quand vous rappeler ?</span>
{pills('creneau', [('matin', 'Matin'), ('apres-midi', 'Après-midi'), ('apres-18h', 'Après 18 h')])}
<div class="field"><label class="lbl" for="f-msg">Votre message (facultatif)</label><textarea id="f-msg" name="message" maxlength="2000"></textarea></div>
<div class="field"><label class="lbl" for="f-photos">Photos de la façade (facultatif, 5 max.)</label><input id="f-photos" name="photos[]" type="file" accept="image/jpeg,image/png,image/webp,image/heic" multiple></div>
<label class="consent"><input type="checkbox" name="consentement" value="oui" required><span>J’accepte que Cozybat utilise ces informations pour me recontacter au sujet de mon projet. <a href="{b}confidentialite.html">En savoir plus</a></span></label>
<div class="hp" aria-hidden="true"><label>Ne pas remplir <input type="text" name="site_web" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="ts" value="">
<p class="form-err" role="alert"></p>
<div class="form-nav"><button class="btn btn-back form-nav-js" type="button" data-prev>← Retour</button><button class="btn btn-navy btn-lg" type="submit">Envoyer ma demande →</button></div>
<p class="no-js-note">* champs obligatoires</p>
</fieldset>
</form>'''

def devis_section(b, h='h2'):
    return f'''<section class="sec sec-gold" id="contact"><div class="wrap devis">
<div class="devis-txt"><{h} class="h2">Parlons de votre façade.</{h}>
<div class="devis-info"><a href="tel:{TEL}">{TEL_H}</a><a href="mailto:{MAIL}">{MAIL}</a><span>Rendez-vous : {ADR_RDV}</span><span>Réponse sous 48 h ouvrées · visite et devis gratuits</span></div></div>
{form_block(b)}
</div></section>
'''

def cta_band(b, projet=''):
    q = f'?projet={projet}' if projet else ''
    return f'''<section class="sec-tight sec-gold"><div class="wrap cta-band">
<h2 class="h2">Un projet de façade ?</h2>
<div class="hero-cta" style="margin:0"><a class="btn btn-navy btn-lg" href="{b}devis.html{q}" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline btn-lg" href="tel:{TEL}">{TEL_H}</a></div>
</div></section>
'''

def story_section(sys):
    L = layers(sys)
    steps = ''
    for l in L:
        specs = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in l['specs'])
        steps += f'''<article class="step" data-num="{l['num']}" data-name="{e(l['name'].upper())}"><span class="n" aria-hidden="true">{l['num']}</span><h3>{e(l['name'])}</h3><p class="plain">{e(l['plain'])}</p>
<details><summary>+ DÉTAIL TECHNIQUE</summary><p>{e(l['text'])}</p><dl class="specs-tbl">{specs}</dl></details></article>
'''
    return f'''<section class="sec-dark" id="systeme"><div class="wrap" style="padding-top:104px">
<p class="kicker">Le système</p><h2 class="h2">Le chantier, couche par couche.</h2>
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
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)

# ------------------------------------------------------------------ pages
def page_index():
    b = ''
    copy_ite = f'''<div data-sys-copy="ite"><p class="eyebrow fade" style="animation-delay:.1s">Isolation par l’extérieur · Essonne</p>
{h1_lines('Huit')}
<p class="hero-sub fade" style="animation-delay:.9s">Isolation thermique par l’extérieur et ravalement en Essonne. Un métier de façadier transmis de père en fils, posé dans les règles du système, du collage à la dernière passe d’enduit.</p></div>'''
    copy_d3 = f'''<div data-sys-copy="d3" hidden><p class="eyebrow">Ravalement D3 armé · Essonne</p>
<p class="h1" aria-hidden="true"><span class="ln">Cinq</span><span class="ln">couches.</span><span class="ln"><span class="hl">Zéro</span></span><span class="ln"><span class="hl">raccourci.</span></span></p>
<p class="hero-sub">Ravalement armé pour façades fissurées : préparation du support, enduit armé d’un filet en fibre de verre et finition, posés dans les règles du système.</p></div>'''
    hero = f'''<section class="hero" id="top">{SWOOSH}
<div class="wrap hero-grid">
<div class="hero-txt">
<div class="tabs" role="group" aria-label="Voir la coupe du système">
<button class="tab" type="button" data-sys-tab="ite" aria-pressed="true"><small>01</small><span>Isolation par l’extérieur</span></button>
<button class="tab" type="button" data-sys-tab="d3" aria-pressed="false"><small>02</small><span>Ravalement D3 armé</span></button>
</div>
{copy_ite}
{copy_d3}
<div class="hero-cta fade" style="animation-delay:1.05s"><a class="btn btn-gold btn-lg" href="devis.html" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline btn-lg" href="#solutions">Nos solutions ↓</a></div>
</div>
<div class="hero-stage"><div data-stack="hero" data-system="ite" style="position:absolute;inset:0"></div><p class="hero-count" data-hero-count aria-hidden="true"></p></div>
</div>
{ticker()}</section>
'''
    quiz = f'''<section class="sec sec-dark" id="orientation"><div class="wrap quiz">
<div class="quiz-intro"><p class="kicker">Par où commencer</p><h2 class="h2">Isolation ou ravalement ?</h2><p class="lead">Trois questions pour savoir quelle solution correspond à votre façade.</p></div>
<div class="quiz-box" data-quiz>
<div class="q" role="radiogroup" aria-labelledby="q-froid"><p class="q-t" id="q-froid">Votre maison est-elle froide l’hiver, ou vos factures de chauffage élevées ?</p><div class="opts"><label class="pill"><input type="radio" name="froid" value="oui"><span>OUI</span></label><label class="pill"><input type="radio" name="froid" value="non"><span>NON</span></label></div></div>
<div class="q" role="radiogroup" aria-labelledby="q-fissures"><p class="q-t" id="q-fissures">Votre façade est-elle fissurée, tachée ou abîmée ?</p><div class="opts"><label class="pill"><input type="radio" name="fissures" value="oui"><span>OUI</span></label><label class="pill"><input type="radio" name="fissures" value="non"><span>NON</span></label></div></div>
<div class="q" role="radiogroup" aria-labelledby="q-ancienne"><p class="q-t" id="q-ancienne">Votre maison a-t-elle été construite avant les années 2000 ?</p><div class="opts"><label class="pill"><input type="radio" name="ancienne" value="oui"><span>OUI</span></label><label class="pill"><input type="radio" name="ancienne" value="non"><span>NON</span></label></div></div>
<div class="quiz-res" data-quiz-res aria-live="polite"><div><p class="k">RÉSULTAT</p><p class="t">Répondez aux 3 questions</p><p class="x">La solution adaptée s’affichera ici.</p></div><a class="btn btn-navy" href="devis.html" hidden></a></div>
</div></div></section>
'''
    specs = f'''<section class="sec" id="solutions"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Nos deux spécialités</p><h2 class="h2">Isoler ou rénover votre façade.</h2></div><p class="lead">Deux systèmes armés, posés par la même équipe, avec la même exigence.</p></div>
<div class="specs">
<a class="spec" href="isolation-exterieure.html" data-reveal><small>01 · ISOLATION PAR L’EXTÉRIEUR</small><h3>ITE sous enduit</h3><p>Un isolant de 14 à 20 cm enveloppe la maison, puis un enduit neuf refait la façade. Plus de confort, moins de chauffage, et des aides possibles.</p><span class="go">Voir le système en 3D →</span></a>
<a class="spec" href="ravalement-facade.html" data-reveal><small>02 · RAVALEMENT</small><h3>Ravalement D3 armé</h3><p>Pour une façade fissurée ou abîmée : préparation, enduit armé d’un filet sur toute la surface et finition dans la teinte de votre choix.</p><span class="go">Voir le système en 3D →</span></a>
</div></div></section>
'''
    cards = '\n'.join(ba_card(b, c) for c in CHANTIERS)
    real = f'''<section class="sec sec-warm" id="realisations"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Réalisations</p><h2 class="h2">Avant. Après.</h2></div><p class="lead">Faites glisser pour comparer. Des chantiers réalisés en Essonne.</p></div>
<div class="filters" role="group" aria-label="Filtrer les réalisations"><button type="button" data-filter="all" aria-pressed="true">Tous</button><button type="button" data-filter="ite" aria-pressed="false">Isolation par l’extérieur</button><button type="button" data-filter="d3" aria-pressed="false">Ravalement</button></div>
<div class="ba-grid">{cards}</div>
<p style="margin-top:28px"><a class="btn btn-outline" href="chantiers.html">Toutes nos réalisations →</a></p>
</div></section>
'''
    body = (head(b, 'Cozybat · Isolation par l’extérieur et ravalement de façade en Essonne (91)',
                 'Isolation thermique par l’extérieur et ravalement de façade D3 armé en Essonne. Entreprise RGE Qualibat, décennale SMABTP, 5,0/5 sur 44 avis Google. Visite et devis gratuits.', '')
            + header(b) + hero + trust(b) + quiz + specs + real + avis_section(b) + team_section(b) + methode_section()
            + faq_section(FAQ_HOME) + devis_section(b) + footer(b))
    write('index.html', body)

def page_system(sys):
    b = ''
    if sys == 'ite':
        path, title = 'isolation-exterieure.html', 'Isolation thermique par l’extérieur (ITE) en Essonne · Cozybat, entreprise RGE'
        desc = 'Isolation par l’extérieur sous enduit en Essonne : PSE graphité 140 à 200 mm, système sous Avis Technique, entreprise RGE Qualibat. Aides CEE et MaPrimeRénov’, visite et devis gratuits.'
        eyebrow, w1 = 'Isolation par l’extérieur · Essonne', 'Huit'
        h1x = '<span class="sr-only"> Isolation thermique par l’extérieur en Essonne</span>'
        sub = 'Un isolant de 14 à 20 cm enveloppe votre maison, puis un enduit neuf refait la façade. Plus de confort été comme hiver, moins de chauffage, et des aides possibles grâce à notre qualification RGE.'
        faq, perks_k, projet = FAQ_ITE, 'ite', 'ite'
    else:
        path, title = 'ravalement-facade.html', 'Ravalement de façade D3 armé en Essonne · Cozybat'
        desc = 'Ravalement de façade D3 armé en Essonne : traitement des fissures, enduit armé d’un filet sur toute la surface, régulateur et finition. Visite et devis gratuits.'
        eyebrow, w1 = 'Ravalement D3 armé · Essonne', 'Cinq'
        h1x = '<span class="sr-only"> Ravalement de façade D3 armé en Essonne</span>'
        sub = 'Pour une façade fissurée, tachée ou abîmée : préparation du support, enduit armé d’un filet en fibre de verre sur toute la surface, régulateur et finition dans la teinte de votre choix.'
        faq, perks_k, projet = FAQ_D3, 'd3', 'd3'
    hero = f'''<section class="hero" id="top">{SWOOSH}
<div class="wrap hero-grid">
<div class="hero-txt"><p class="eyebrow fade" style="animation-delay:.1s">{eyebrow}</p>
{h1_lines(w1, h1x)}
<p class="hero-sub fade" style="animation-delay:.9s">{sub}</p>
<div class="hero-cta fade" style="animation-delay:1.05s"><a class="btn btn-gold btn-lg" href="devis.html?projet={projet}" data-track="Clic devis">Demander un devis gratuit</a><a class="btn btn-outline btn-lg" href="#systeme">Voir la coupe ↓</a></div></div>
<div class="hero-stage"><div data-stack="hero" data-system="{sys}" style="position:absolute;inset:0"></div><p class="hero-count" data-hero-count aria-hidden="true"></p></div>
</div>
{ticker()}</section>
'''
    cards = '\n'.join(ba_card(b, c) for c in CHANTIERS if c['type'] == sys)
    real = f'''<section class="sec sec-warm" id="realisations"><div class="wrap">
<div class="sec-head"><div><p class="kicker">Réalisations</p><h2 class="h2">Avant. Après.</h2></div><p class="lead">Faites glisser pour comparer.</p></div>
<div class="ba-grid">{cards}</div>
<p style="margin-top:28px"><a class="btn btn-outline" href="chantiers.html">Toutes nos réalisations →</a></p>
</div></section>
'''
    other = ('ravalement-facade.html', 'Votre façade est seulement fissurée ? Découvrez le ravalement D3 armé →') if sys == 'ite' else ('isolation-exterieure.html', 'Envie d’isoler en même temps ? Découvrez l’isolation par l’extérieur →')
    cross = f'<section class="sec-tight"><div class="wrap"><a class="btn btn-outline" href="{other[0]}">{other[1]}</a></div></section>\n'
    body = (head(b, title, desc, path, extra_ld=[faq_ld(faq)]) + header(b, sys) + hero + trust(b) + story_section(sys)
            + real + methode_section(perks_k) + faq_section(faq, dark=False) + cross + devis_section(b) + footer(b))
    write(path, body)

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def page_chantiers():
    b = ''
    cards = '\n'.join(ba_card(b, c) for c in CHANTIERS)
    content = f'''<section class="sec"><div class="wrap">
<p class="kicker">Réalisations</p><h1 class="h2" style="margin-bottom:12px">Nos chantiers en Essonne.</h1>
<p class="lead" style="margin-bottom:36px">Isolation par l’extérieur et ravalement : faites glisser chaque photo pour comparer avant et après.</p>
<div class="filters" role="group" aria-label="Filtrer les réalisations"><button type="button" data-filter="all" aria-pressed="true">Tous</button><button type="button" data-filter="ite" aria-pressed="false">Isolation par l’extérieur</button><button type="button" data-filter="d3" aria-pressed="false">Ravalement</button></div>
<div class="ba-grid">{cards}</div>
</div></section>
'''
    write('chantiers.html', head(b, 'Nos réalisations · ITE et ravalement en Essonne · Cozybat',
          'Avant / après de nos chantiers d’isolation par l’extérieur et de ravalement en Essonne : Ollainville, Saint-Michel-sur-Orge, Sainte-Geneviève-des-Bois, Morangis, Yerres, Brunoy.', 'chantiers.html')
          + header(b, 'chantiers') + content + avis_section(b) + cta_band(b) + footer(b))

def page_case(c):
    b = '../'
    facts = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in c['facts'])
    sysp = ('isolation-exterieure.html', 'Découvrir l’isolation par l’extérieur') if c['type'] == 'ite' else ('ravalement-facade.html', 'Découvrir le ravalement D3 armé')
    img = f'{b}assets/img/chantiers/{c["slug"]}'
    others = [x for x in CHANTIERS if x['slug'] != c['slug'] and x['type'] == c['type']][:2]
    more = '\n'.join(ba_card(b, x) for x in others)
    content = f'''<div class="wrap"><p class="crumbs"><a href="{b}index.html">Accueil</a> › <a href="{b}chantiers.html">Réalisations</a> › {e(c['ville'])}</p></div>
<section class="sec" style="padding-top:8px"><div class="wrap">
<div class="case">
<div class="ba">
<img src="{img}-avant.webp" alt="Façade avant travaux, {e(c['ville'])}" width="900" height="1100" decoding="async">
<img class="after" src="{img}-apres.webp" alt="Façade après travaux, {e(c['ville'])}" width="900" height="1100" decoding="async">
<span class="bar" aria-hidden="true"></span><span class="knob" aria-hidden="true">↔</span>
<span class="tag l" aria-hidden="true">AVANT</span><span class="tag r" aria-hidden="true">APRÈS</span>
<input type="range" min="0" max="100" value="50" aria-label="Comparer avant et après">
</div>
<div class="case-txt"><p class="kicker" style="margin:0">{e(c['label'].upper())}</p>
<h1 class="h2">{e(c['h1'])}</h1><p>{e(c['desc'])}</p>
<dl class="facts">{facts}</dl>
<div class="hero-cta" style="margin-top:6px"><a class="btn btn-gold" href="{b}devis.html?projet={c['type']}" data-track="Clic devis">Un projet similaire ? Devis gratuit</a><a class="btn btn-outline" href="{b}{sysp[0]}">{sysp[1]}</a></div>
</div></div></div></section>
'''
    if more:
        content += f'<section class="sec sec-warm"><div class="wrap"><p class="kicker">Autres réalisations</p><div class="ba-grid">{more}</div></div></section>\n'
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Réalisations", "item": DOMAIN + "/chantiers.html"},
        {"@type": "ListItem", "position": 3, "name": c['ville'], "item": f"{DOMAIN}/chantiers/{c['slug']}.html"}]}
    write(f'chantiers/{c["slug"]}.html', head(b, c['title'] + ' · Cozybat', c['desc'], f'chantiers/{c["slug"]}.html', extra_ld=[ld])
          + header(b, 'chantiers') + content + cta_band(b, c['type']) + footer(b))

def page_devis():
    b = ''
    write('devis.html', head(b, 'Demander un devis gratuit · Cozybat', 'Demandez votre devis gratuit d’isolation par l’extérieur ou de ravalement en Essonne. Réponse sous 48 h ouvrées, visite technique offerte.', 'devis.html')
          + header(b) + devis_section(b, h='h1') + trust(b) + footer(b))

def page_merci():
    b = ''
    content = f'''<section class="sec sec-gold"><div class="wrap" style="max-width:820px">
<h1 class="h2" style="margin-bottom:18px">Demande reçue.</h1>
<p style="font-size:19px;margin:0 0 28px">Merci ! Nous vous rappelons sous 48 h ouvrées pour fixer la visite technique gratuite. Pour une question urgente : <a href="tel:{TEL}" style="color:#2E3A47;font-weight:700">{TEL_H}</a>.</p>
<div class="hero-cta"><a class="btn btn-navy" href="chantiers.html">Voir nos réalisations</a><a class="btn btn-outline" href="{IG}" rel="noopener">Nous suivre sur Instagram</a></div>
</div></section>
'''
    write('merci.html', head(b, 'Merci · Cozybat', 'Votre demande de devis a bien été envoyée.', 'merci.html', noindex=True) + header(b) + content + footer(b))

def page_erreur():
    b = '/'
    content = f'''<section class="sec"><div class="wrap" style="max-width:820px"><h1 class="h2" style="margin-bottom:18px">Page introuvable.</h1>
<p class="lead" style="margin-bottom:28px">Cette page n’existe pas ou a été déplacée.</p><a class="btn btn-gold" href="/index.html">Retour à l’accueil</a></div></section>
'''
    write('404.html', head(b, 'Page introuvable · Cozybat', 'Page introuvable.', '404.html', noindex=True) + header(b) + content + footer(b))

def todo(x): return f'<span class="todo">{x}</span>'

def page_mentions():
    b = ''
    content = f'''<section class="sec"><div class="wrap legal">
<h1>Mentions légales</h1>
<h2>Éditeur du site</h2>
<p>Cozybat SAS, société par actions simplifiée au capital de {todo('[CAPITAL] €')}<br>
Siège social : 29 rue Archimède, 91420 Morangis<br>
SIREN 993 112 788 · SIRET 993 112 788 00019 · RCS Évry<br>
N° de TVA intracommunautaire : FR60 993 112 788<br>
Téléphone : <a href="tel:{TEL}">{TEL_H}</a> · E-mail : <a href="mailto:{MAIL}">{MAIL}</a></p>
<p>Directeur de la publication : David De Abreu.</p>
<h2>Qualification et assurance</h2>
<p>Qualification RGE Qualibat n° E-E213612 (7131 – isolation thermique par l’extérieur), en cours de validité.<br>
Assurance responsabilité civile décennale : SMABTP. L’attestation d’assurance est remise avec chaque devis.</p>
<h2>Médiation de la consommation</h2>
<p>Conformément aux articles L.611-1 et suivants du Code de la consommation, le client consommateur peut recourir gratuitement au médiateur de la consommation dont relève Cozybat : {todo('[NOM DU MÉDIATEUR, adresse postale et site internet]')}, après avoir tenté de résoudre le litige directement auprès de l’entreprise par écrit.</p>
<h2>Hébergement</h2>
<p>Hostinger International Ltd, 61 Lordou Vironos Street, 6023 Larnaca, Chypre – <a href="https://www.hostinger.fr" rel="noopener">www.hostinger.fr</a>.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, photographies, visuels et le logo de ce site sont la propriété de Cozybat SAS. Toute reproduction sans autorisation est interdite. Les avis clients reproduits proviennent de la fiche Google de l’entreprise.</p>
<p style="margin-top:32px;font-size:13px">Dernière mise à jour : {TODAY}</p>
</div></section>
'''
    write('mentions-legales.html', head(b, 'Mentions légales · Cozybat', 'Mentions légales du site cozybat.fr.', 'mentions-legales.html') + header(b) + content + footer(b))

def page_confid():
    b = ''
    content = f'''<section class="sec"><div class="wrap legal">
<h1>Politique de confidentialité</h1>
<h2>Responsable du traitement</h2>
<p>Cozybat SAS, 29 rue Archimède, 91420 Morangis – <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>Données collectées</h2>
<p>Lorsque vous remplissez le formulaire de demande de devis, nous recueillons : nom, téléphone, e-mail et ville (si renseignés), informations sur votre projet (type de travaux, type de maison, surface, créneau de rappel, message) et, le cas échéant, les photos de votre façade.</p>
<h2>Finalité et base légale</h2>
<p>Ces données servent uniquement à vous recontacter, organiser la visite technique et établir votre devis. Le traitement repose sur votre demande (mesures précontractuelles) et sur votre consentement exprimé dans le formulaire.</p>
<h2>Destinataires</h2>
<p>Les données sont destinées à Cozybat uniquement. Elles transitent par notre hébergeur et notre messagerie. Elles ne sont ni vendues ni cédées à des tiers.</p>
<h2>Durée de conservation</h2>
<p>Trois ans à compter du dernier contact si aucun contrat n’est signé. En cas de chantier, les données liées au contrat sont conservées pendant la durée légale (notamment la garantie décennale).</p>
<h2>Vos droits</h2>
<p>Vous disposez d’un droit d’accès, de rectification, d’effacement, de limitation, d’opposition et de portabilité de vos données. Pour l’exercer : <a href="mailto:{MAIL}">{MAIL}</a>. Vous pouvez aussi adresser une réclamation à la CNIL (<a href="https://www.cnil.fr" rel="noopener">www.cnil.fr</a>).</p>
<h2>Cookies et mesure d’audience</h2>
<p>Ce site ne dépose aucun cookie publicitaire. Si une mesure d’audience est activée, elle utilise Plausible Analytics, un outil sans cookie qui ne collecte aucune donnée personnelle et ne permet pas de vous identifier.</p>
<h2>Polices et ressources</h2>
<p>Les polices de caractères et les images sont hébergées sur nos propres serveurs : aucune donnée n’est transmise à un service tiers lors de votre visite.</p>
<p style="margin-top:32px;font-size:13px">Dernière mise à jour : {TODAY}</p>
</div></section>
'''
    write('confidentialite.html', head(b, 'Politique de confidentialité · Cozybat', 'Comment Cozybat utilise et protège vos données personnelles.', 'confidentialite.html') + header(b) + content + footer(b))

def seo_files():
    urls = ['', 'isolation-exterieure.html', 'ravalement-facade.html', 'chantiers.html', 'devis.html', 'mentions-legales.html', 'confidentialite.html'] + [f'chantiers/{c["slug"]}.html' for c in CHANTIERS]
    prio = {'': '1.0', 'isolation-exterieure.html': '0.9', 'ravalement-facade.html': '0.9', 'devis.html': '0.8', 'chantiers.html': '0.8'}
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{DOMAIN}/{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(u, "0.6" if u.startswith("chantiers/") else "0.3")}</priority></url>\n' for u in urls) + '</urlset>\n'
    write('sitemap.xml', sm)
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /outils/\nDisallow: /merci.html\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    write('.htaccess', '''# Cozybat — réglages serveur (Apache / Hostinger)
ErrorDocument 404 /404.html

# HTTPS obligatoire
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</IfModule>

# Compression
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json text/xml application/xml
</IfModule>

# Cache navigateur
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType image/webp "access plus 6 months"
ExpiresByType image/png "access plus 6 months"
ExpiresByType image/jpeg "access plus 6 months"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType text/css "access plus 1 week"
ExpiresByType application/javascript "access plus 1 week"
ExpiresByType text/html "access plus 0 seconds"
</IfModule>
AddType image/webp .webp
AddType font/woff2 .woff2

# Sécurité de base
<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
</IfModule>
''')

if __name__ == '__main__':
    page_index(); page_system('ite'); page_system('d3'); page_chantiers()
    for c in CHANTIERS: page_case(c)
    page_devis(); page_merci(); page_erreur(); page_mentions(); page_confid(); seo_files()
    print('ok')
