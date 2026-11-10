# Guides conseils Cozybat — contenu des pages /guides/...
# Chaque guide : slug, titre SEO (≤ 60), description (≤ 155), h1, intro, sections [(h2, html)], faq [(q, r)], liens associés.
# Règles d'aides vérifiées en novembre 2026 (MaPrimeRénov' par geste : isolation des murs exclue depuis le 1er janvier 2026).

def ul(*items): return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
def p(*paras): return ''.join(f'<p>{x}</p>' for x in paras)
def table(head, rows):
    h = ''.join(f'<th scope="col">{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join((f'<th scope="row">{c}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
def key(title, big, small, note=''):
    return f'<div class="key"><p class="key-t">{title}</p><p class="key-b">{big}</p><p class="key-s">{small}</p>{f"<p class=key-n>{note}</p>" if note else ""}</div>'

LINK_ITE = '<a href="/isolation-exterieure/">isolation thermique par l’extérieur</a>'
LINK_D3 = '<a href="/ravalement-facade/">ravalement de façade D3 armé</a>'
LINK_DEVIS = '<a href="/devis/">demande de devis gratuit</a>'
LINK_AIDES = '<a href="/guides/aides-isolation-exterieure/">guide des aides à l’isolation par l’extérieur</a>'
LINK_PRIX_ITE = '<a href="/guides/prix-isolation-exterieure/">prix de l’isolation par l’extérieur</a>'
LINK_PRIX_RAV = '<a href="/guides/prix-ravalement-facade/">prix d’un ravalement de façade</a>'
LINK_FISS = '<a href="/guides/fissures-facade/">guide des fissures de façade</a>'
LINK_ITI = '<a href="/guides/isolation-interieure-ou-exterieure/">comparatif isolation intérieure ou extérieure</a>'

GUIDES = [
dict(
  slug='prix-isolation-exterieure', kind='ite', short='Prix de l’isolation par l’extérieur',
  title='Prix isolation extérieure au m² en 2026 | Cozybat',
  desc='Prix de l’isolation par l’extérieur au m² en 2026 : fourchette, exemples chiffrés, ce qui fait varier le devis et les aides qui s’en déduisent.',
  h1='Prix de l’isolation par l’extérieur au m² en 2026',
  intro='Combien coûte une isolation thermique par l’extérieur (ITE) pour une maison ? Voici les prix que nous pratiquons en Essonne, des exemples chiffrés et les points qui font monter ou baisser un devis.',
  sections=[
    ('Le prix au m² d’une ITE sous enduit',
     key('Prix indicatif Cozybat · Essonne', '180 à 210 €', 'TTC par m² de mur isolé, posé et fini', 'Isolant PSE graphité 140 à 200 mm, échafaudage, préparation, enduit armé et finition compris. Avant déduction des primes CEE.')
     + p('Le prix d’une isolation par l’extérieur se calcule au m² de mur isolé : la surface des façades, ouvertures déduites. Il comprend tout le système, de l’échafaudage à la dernière couche d’enduit : collage et chevillage de l’isolant, enduit de base armé d’un filet en fibre de verre, sous-couche, régulateur de fond et finition dans la teinte choisie.',
         'Cette fourchette correspond à une maison individuelle en bon état, avec un isolant en polystyrène graphité. Le prix exact est fixé après la visite technique, car il dépend surtout des points singuliers de votre maison.')),
    ('Exemples de budget pour une maison',
     p('La surface de façade d’une maison n’est pas sa surface habitable : une maison de plain-pied de 100 m² compte souvent 90 à 110 m² de murs à isoler, une maison à étage de 120 m² environ 150 à 180 m².')
     + table(['Surface de murs isolés', 'Budget indicatif TTC', 'Exemple de maison'],
             [['90 m²', '16 200 à 18 900 €', 'Plain-pied, environ 100 m² habitables'],
              ['130 m²', '23 400 à 27 300 €', 'Maison à étage, environ 100 m² habitables'],
              ['170 m²', '30 600 à 35 700 €', 'Maison à étage, environ 140 m² habitables']])
     + p('Ces montants s’entendent avant déduction des primes CEE, avec une TVA à 5,5 %. Les aides disponibles en 2026 sont détaillées dans notre ' + LINK_AIDES + '.')),
    ('Ce qui fait varier le prix',
     ul('<strong>L’isolant.</strong> Le polystyrène graphité est le plus économique à performance égale. La laine de roche et la fibre de bois coûtent plus cher, mais améliorent le confort acoustique et, pour la fibre de bois, le confort d’été.',
        '<strong>L’épaisseur.</strong> 120 à 140 mm suffisent en général pour atteindre la résistance thermique demandée pour les primes (R ≥ 3,7 m².K/W). Aller jusqu’à 160 ou 200 mm améliore le confort, mais demande d’adapter davantage les appuis et les débords de toiture.',
        '<strong>Les points singuliers.</strong> Appuis de fenêtre à prolonger ou remplacer, tableaux et voussures, gonds de volets, coffres de volets roulants, descentes d’eau pluviale, couvertines, unités extérieures de pompe à chaleur : ce sont eux qui font la différence entre deux devis.',
        '<strong>La finition.</strong> Enduit mince taloché, ribbé ou gratté, ou finition plus épaisse : l’aspect choisi change le coût de la dernière couche.',
        '<strong>L’accès et l’état du support.</strong> Hauteur, accès de l’échafaudage, mitoyenneté, ancien enduit qui s’écaille et doit être purgé, fissures à traiter avant la pose.')),
    ('Comparer les isolants',
     table(['Isolant', 'Prix relatif', 'Thermique', 'Acoustique', 'Points forts'],
           [['Polystyrène graphité (PSE)', 'Le plus économique', 'Très bonne', 'Faible', 'Léger, performant à faible épaisseur'],
            ['Laine de roche', 'Plus cher', 'Bonne', 'Bonne', 'Incombustible, atténue les bruits extérieurs'],
            ['Fibre de bois', 'Le plus cher', 'Bonne', 'Bonne', 'Biosourcé, bon confort d’été']])
     + p('Nous vous présentons les options lors de la visite, avec leur épaisseur, leur prix et leur effet sur les aides. Le détail est dans notre <a href="/guides/isolant-isolation-exterieure/">comparatif des isolants pour l’ITE</a>.')),
    ('Bien lire un devis d’isolation par l’extérieur',
     p('Un devis sérieux détaille chaque couche du système. Vérifiez qu’il précise :')
     + ul('la marque, la nature, l’épaisseur et la résistance thermique R de l’isolant ;',
          'le mode de fixation (collage, chevillage) et l’armature de l’enduit de base ;',
          'la finition et la teinte ;',
          'le traitement de chaque point singulier : appuis, tableaux, volets, descentes, couvertines ;',
          'l’échafaudage, la protection des abords et le nettoyage du chantier ;',
          'la qualification RGE de l’entreprise et son attestation d’assurance décennale.')
     + p('Un devis global « au m² » sans ces détails ne permet pas de comparer deux offres. Pour voir le système couche par couche, consultez notre page ' + LINK_ITE + '.')),
  ],
  faq=[
    ('Quel est le prix moyen d’une isolation par l’extérieur ?', 'Chez Cozybat, en Essonne, comptez 180 à 210 € TTC par m² de mur isolé, échafaudage et finition compris, avant déduction des primes CEE. Pour une maison à étage avec 130 m² de murs, le budget se situe autour de 23 000 à 27 000 € TTC.'),
    ('L’échafaudage est-il compris dans le prix au m² ?', 'Oui, dans nos devis l’échafaudage, la préparation du support, la pose du système complet et le nettoyage du chantier sont compris dans le prix au m².'),
    ('Pourquoi deux devis d’ITE peuvent-ils être très différents ?', 'Parce que l’isolant, son épaisseur et surtout le traitement des points singuliers (appuis, volets, descentes) changent beaucoup d’un devis à l’autre. Un devis bas peut omettre ces postes ou prévoir un isolant moins épais.'),
    ('Peut-on payer moins cher grâce aux aides ?', 'Oui : les primes CEE se déduisent du prix, la TVA est à 5,5 % et l’éco-prêt à taux zéro permet d’étaler le financement. Depuis 2026, MaPrimeRénov’ ne finance plus l’isolation des murs seule, sauf dans le cadre d’une rénovation d’ampleur.'),
  ],
  related=['aides-isolation-exterieure', 'isolant-isolation-exterieure', 'isolation-interieure-ou-exterieure'],
),
dict(
  slug='prix-ravalement-facade', kind='d3', short='Prix d’un ravalement de façade',
  title='Prix d’un ravalement de façade au m² en 2026 | Cozybat',
  desc='Prix d’un ravalement de façade au m² en 2026 : fourchette pour un D3 armé, exemples de budget, différences avec une peinture et facteurs de prix.',
  h1='Prix d’un ravalement de façade au m² en 2026',
  intro='Combien coûte un ravalement de façade ? Tout dépend de l’état de votre façade et du type de ravalement. Voici nos prix en Essonne pour un ravalement D3 armé, des exemples de budget et les différences entre les solutions.',
  sections=[
    ('Le prix au m² d’un ravalement D3 armé',
     key('Prix indicatif Cozybat · Essonne', '100 à 120 €', 'TTC par m² de façade', 'Lavage, traitement des fissures, enduit armé d’un filet sur toute la surface, régulateur et finition. Échafaudage et nettoyage compris.')
     + p('Le ravalement D3 armé est un revêtement épais renforcé par un filet en fibre de verre noyé dans un enduit sur toute la surface. C’est la solution adaptée à une façade fissurée, tachée ou dont l’enduit est fatigué, quand les murs sont sains et qu’aucune isolation n’est prévue.',
         'Le prix exact est fixé après la visite technique, car il dépend avant tout de l’état du support.')),
    ('Exemples de budget',
     table(['Surface de façade', 'Budget indicatif TTC', 'Exemple de maison'],
           [['90 m²', '9 000 à 10 800 €', 'Plain-pied, environ 100 m² habitables'],
            ['130 m²', '13 000 à 15 600 €', 'Maison à étage, environ 100 m² habitables'],
            ['170 m²', '17 000 à 20 400 €', 'Maison à étage, environ 140 m² habitables']])
     + p('Un ravalement sans isolation bénéficie d’une TVA à 10 % pour un logement achevé depuis plus de deux ans. Il n’ouvre pas droit aux aides à la rénovation énergétique ; si la maison est mal isolée, comparez avec le ' + LINK_PRIX_ITE + ', qui refait la façade et isole en même temps.')),
    ('Peinture, D3 armé ou réfection d’enduit : quelles différences ?',
     table(['Solution', 'Quand la choisir', 'Effet sur les fissures'],
           [['Peinture de façade', 'Façade saine, simple changement de teinte ou encrassement léger', 'Aucun : les fissures réapparaissent'],
            ['Ravalement D3 armé', 'Façade fissurée, tachée, enduit fatigué mais adhérent', 'Les microfissures sont pontées par l’armature'],
            ['Réfection d’enduit', 'Enduit qui sonne creux ou se décolle sur de grandes surfaces', 'Traitées après purge et nouvel enduit'],
            ['Isolation par l’extérieur', 'Maison froide ou chère à chauffer', 'Nouvelle façade complète sur l’isolant']])
     + p('Une peinture coûte moins cher sur le moment, mais ne protège pas une façade fissurée : l’eau continue de s’infiltrer. Notre ' + LINK_FISS + ' vous aide à lire l’état de votre façade, et notre guide pour <a href="/guides/refaire-crepi-facade/">refaire le crépi de sa façade</a> détaille les solutions.')),
    ('Ce qui fait varier le prix',
     ul('<strong>L’état du support.</strong> Un enduit qui s’écaille doit être purgé ; au-delà d’une certaine surface non adhérente, il faut décaper ou refaire l’enduit.',
        '<strong>Les fissures.</strong> Leur nombre et leur largeur déterminent le traitement préalable.',
        '<strong>Les surfaces annexes.</strong> Soubassement, sous-faces de balcon, appuis, corniches, murets de clôture.',
        '<strong>La hauteur et l’accès.</strong> Une façade haute ou difficile d’accès demande plus d’échafaudage.',
        '<strong>La finition.</strong> Aspect taloché, ribbé ou gratté, une ou deux teintes, bande de soubassement.')),
    ('Ravalement : obligations et démarches',
     p('Un ravalement qui modifie l’aspect de la façade (teinte, finition) demande une déclaration préalable de travaux en mairie, et le PLU de la commune peut imposer certaines teintes. Certaines communes peuvent aussi rendre le ravalement obligatoire à intervalle régulier par arrêté. Près d’un monument historique, l’avis de l’Architecte des Bâtiments de France peut être requis.',
       'Nous vérifions les règles de votre commune et vous aidons à préparer le dossier. Pour le détail du système, consultez notre page ' + LINK_D3 + '.')),
  ],
  faq=[
    ('Quel est le prix d’un ravalement de façade au m² ?', 'Chez Cozybat, un ravalement D3 armé coûte 100 à 120 € TTC par m² de façade en Essonne, échafaudage, préparation, enduit armé et finition compris.'),
    ('Combien coûte le ravalement d’une maison de 100 m² ?', 'Une maison de 100 m² habitables compte en général 90 à 130 m² de façade selon qu’elle est de plain-pied ou à étage, soit un budget d’environ 9 000 à 15 600 € TTC pour un ravalement D3 armé.'),
    ('Quelle TVA pour un ravalement de façade ?', 'Une TVA à 10 % s’applique pour un logement achevé depuis plus de deux ans. Si le ravalement est réalisé avec une isolation par l’extérieur, la TVA passe à 5,5 % sous conditions de performance de l’isolant.'),
    ('Tous les combien faut-il ravaler sa façade ?', 'En moyenne tous les 10 à 20 ans selon l’exposition et le revêtement. Certaines communes peuvent imposer un ravalement périodique par arrêté.'),
  ],
  related=['refaire-crepi-facade', 'enduit-gratte-taloche-ribbe', 'prix-isolation-exterieure'],
),
dict(
  slug='aides-isolation-exterieure', kind='ite', short='Aides à l’isolation par l’extérieur',
  title='Aides isolation extérieure 2026 : CEE, TVA, PTZ | Cozybat',
  desc='Aides pour l’isolation par l’extérieur en 2026 : primes CEE, TVA à 5,5 %, éco-PTZ et MaPrimeRénov’ en rénovation d’ampleur. Conditions et démarches.',
  h1='Aides à l’isolation par l’extérieur en 2026',
  intro='Les aides pour isoler sa maison par l’extérieur ont changé au 1er janvier 2026. Voici ce qui reste possible, à quelles conditions, et dans quel ordre faire les démarches.',
  sections=[
    ('Ce qui a changé en 2026',
     p('Depuis le 1er janvier 2026, l’isolation des murs par l’extérieur comme par l’intérieur n’est plus financée par <strong>MaPrimeRénov’ par geste</strong>. Une isolation des murs réalisée seule n’ouvre donc plus droit à ce forfait, quel que soit le niveau de revenus.',
       'L’isolation par l’extérieur reste néanmoins aidée par plusieurs dispositifs, qui se cumulent :')
     + ul('les <strong>primes CEE</strong> (certificats d’économies d’énergie) ;', 'la <strong>TVA à taux réduit de 5,5 %</strong> ;', 'l’<strong>éco-prêt à taux zéro</strong> ;', '<strong>MaPrimeRénov’ Parcours accompagné</strong>, dans le cadre d’une rénovation d’ampleur.')),
    ('Les primes CEE',
     p('Les primes CEE sont versées par les fournisseurs d’énergie, ou leurs partenaires, pour financer des travaux d’économies d’énergie. Pour l’isolation des murs, elles relèvent de la fiche d’opération standardisée BAR-EN-102.')
     + ul('Résistance thermique de l’isolant : R ≥ 3,7 m².K/W, soit en général 120 à 140 mm de polystyrène graphité.',
          'Travaux réalisés par une entreprise qualifiée RGE : Cozybat est qualifiée RGE Qualibat.',
          'Logement achevé depuis plus de deux ans.',
          'Montant calculé au m² isolé, variable selon vos revenus, votre zone climatique, votre mode de chauffage et l’offre choisie.')
     + p('<strong>Attention à l’ordre des démarches :</strong> la demande de prime doit être faite <strong>avant la signature du devis</strong>. Un devis signé avant l’inscription à l’offre CEE fait perdre la prime.')),
    ('La TVA à 5,5 %',
     p('Les travaux d’isolation thermique des murs bénéficient d’un taux de TVA réduit de 5,5 % au lieu de 10 %, dans un logement achevé depuis plus de deux ans, lorsque l’isolant est fourni et posé par l’entreprise et respecte les critères de performance. Le taux est appliqué directement sur la facture : vous n’avez aucune démarche à faire.',
       'Les travaux indissociablement liés à l’isolation (reprise des appuis, déplacement des descentes d’eau…) en bénéficient aussi.')),
    ('L’éco-prêt à taux zéro',
     p('L’éco-PTZ est un prêt sans intérêts accordé par les banques partenaires de l’État pour financer des travaux de rénovation énergétique. Pour une isolation des murs réalisée seule, il peut atteindre 15 000 € ; il monte jusqu’à 50 000 € pour un bouquet de travaux ou une rénovation globale. Le dispositif est prolongé jusqu’au 31 décembre 2027.',
       'Il se cumule avec les primes CEE et la TVA à 5,5 %. Notre devis détaillé sert de base à votre demande auprès de la banque.')),
    ('MaPrimeRénov’ Parcours accompagné',
     p('MaPrimeRénov’ peut encore financer une isolation par l’extérieur si elle fait partie d’une <strong>rénovation d’ampleur</strong> :')
     + ul('logement classé E, F ou G au diagnostic de performance énergétique (DPE) et achevé depuis plus de 15 ans ;',
          'projet permettant de gagner au moins deux classes de DPE, souvent en associant l’isolation des murs à d’autres travaux (toiture, menuiseries, chauffage, ventilation) ;',
          'accompagnement obligatoire par un Mon Accompagnateur Rénov’ et rendez-vous préalable avec un conseiller France Rénov’.')
     + p('L’aide correspond à un pourcentage du coût des travaux selon vos revenus, dans la limite d’un plafond de dépenses fixé selon le nombre de classes gagnées. Le premier pas est de contacter le conseiller France Rénov’ de votre secteur (france-renov.gouv.fr), qui étudie gratuitement votre projet.')),
    ('Les aides locales en Essonne',
     p('Le Département de l’Essonne a mis en place ces dernières années la Prime éco-logis 91 pour aider les propriétaires à rénover leur résidence principale, et certaines communes ou intercommunalités proposent leurs propres aides. Leurs conditions et leurs budgets changent souvent : avant de signer, vérifiez auprès du conseiller France Rénov’ de votre secteur ou sur le site du Département quelles aides locales sont ouvertes à la date de votre projet.')),
    ('Exemple pour une maison en Essonne',
     p('Pour 130 m² de murs isolés à 190 € TTC/m², les travaux coûtent environ 24 700 € TTC avec une TVA à 5,5 %. Au taux de 10 %, les mêmes travaux coûteraient environ 1 050 € de plus. La prime CEE se déduit ensuite de ce montant, et le reste peut être financé par l’éco-PTZ.',
       'Nous chiffrons ces aides pour votre situation lors du devis. Pour le détail des prix, consultez notre guide du ' + LINK_PRIX_ITE + '.')),
  ],
  faq=[
    ('MaPrimeRénov’ finance-t-elle encore l’isolation par l’extérieur en 2026 ?', 'Pas pour une isolation des murs réalisée seule : depuis le 1er janvier 2026, elle est exclue de MaPrimeRénov’ par geste. Elle reste finançable par MaPrimeRénov’ Parcours accompagné, dans le cadre d’une rénovation d’ampleur qui fait gagner au moins deux classes de DPE.'),
    ('Quelles aides pour une isolation par l’extérieur seule ?', 'Les primes CEE, la TVA à 5,5 % et l’éco-prêt à taux zéro, jusqu’à 15 000 € pour une isolation des murs seule. Ces trois dispositifs se cumulent.'),
    ('Quand faut-il demander la prime CEE ?', 'Avant de signer le devis. La prime n’est versée que si l’inscription à l’offre CEE précède l’engagement des travaux.'),
    ('Faut-il une entreprise RGE ?', 'Oui pour les primes CEE, l’éco-PTZ et MaPrimeRénov’. Cozybat est qualifiée RGE Qualibat n° E-E213612.'),
  ],
  related=['prix-isolation-exterieure', 'isolant-isolation-exterieure', 'isolation-interieure-ou-exterieure'],
),
dict(
  slug='isolation-interieure-ou-exterieure', kind='ite', short='Isolation intérieure ou extérieure ?',
  title='Isolation intérieure ou extérieure : que choisir ? | Cozybat',
  desc='Isolation des murs par l’intérieur ou par l’extérieur : performance, surface habitable, travaux, coût et cas où chaque solution est la meilleure.',
  h1='Isolation intérieure ou extérieure : que choisir ?',
  intro='Pour isoler les murs d’une maison, deux techniques existent : par l’intérieur (ITI) ou par l’extérieur (ITE). Voici leurs différences, sans détour, pour choisir celle qui convient à votre maison.',
  sections=[
    ('Le comparatif en un coup d’œil',
     table(['Critère', 'Isolation par l’extérieur', 'Isolation par l’intérieur'],
           [['Ponts thermiques', 'Traités : l’isolant est continu, y compris au droit des planchers', 'Persistent au droit des planchers et des murs de refend'],
            ['Surface habitable', 'Aucune perte', 'Perte de 10 à 15 cm sur chaque mur isolé'],
            ['Pendant les travaux', 'Vous restez chez vous, tout se fait depuis l’extérieur', 'Pièces à vider, travaux à l’intérieur'],
            ['Façade', 'Refaite à neuf en même temps', 'Inchangée'],
            ['Inertie et confort d’été', 'Les murs restent du côté chaud et stockent la fraîcheur', 'Les murs sont isolés du logement'],
            ['Coût', 'Plus élevé, mais façade comprise', 'Moins élevé, hors finitions intérieures'],
            ['Démarches', 'Déclaration préalable de travaux', 'Aucune en général']])),
    ('Quand l’isolation par l’extérieur est la meilleure solution',
     ul('La façade a besoin d’être refaite : l’ITE isole et ravale en une seule opération.',
        'Vous voulez garder toute votre surface habitable et rester chez vous pendant les travaux.',
        'Les planchers et les murs de refend créent des ponts thermiques importants.',
        'Vous cherchez aussi un meilleur confort l’été.')
     + p('C’est le cas de la plupart des maisons enduites des années 1950 à 2000 en Essonne. Le détail du système est présenté sur notre page ' + LINK_ITE + '.')),
    ('Quand l’isolation par l’intérieur reste préférable',
     ul('La façade a un caractère à préserver : meulière, pierre ou brique apparente.',
        'Le mur est en limite de propriété et le voisin s’oppose au surplomb, ou l’espace manque.',
        'Le PLU ou l’Architecte des Bâtiments de France refuse la modification de l’aspect de la façade.',
        'Une pièce doit être rénovée de toute façon à l’intérieur.')
     + p('Il est aussi possible de combiner les deux : isoler par l’extérieur les façades enduites et par l’intérieur une façade de caractère.')),
    ('Et les aides ?',
     p('Depuis le 1er janvier 2026, ni l’isolation des murs par l’extérieur ni celle par l’intérieur ne sont financées par MaPrimeRénov’ par geste. Les deux restent éligibles aux primes CEE, à la TVA à 5,5 % et à l’éco-prêt à taux zéro. Le détail est dans notre ' + LINK_AIDES + '.')),
  ],
  faq=[
    ('Quelle est la plus efficace, l’isolation intérieure ou extérieure ?', 'À épaisseur égale, l’isolation par l’extérieur est plus efficace, car elle supprime les ponts thermiques au droit des planchers et des murs de refend et conserve l’inertie des murs.'),
    ('L’isolation par l’extérieur est-elle plus chère ?', 'Oui au m², mais elle comprend la rénovation complète de la façade. Si un ravalement est de toute façon nécessaire, l’écart se réduit fortement.'),
    ('Peut-on isoler par l’extérieur une maison mitoyenne ?', 'Oui. Les façades sur rue et sur jardin s’isolent normalement ; seul le raccord avec la maison voisine demande un traitement soigné. Pour un mur en limite de propriété, un droit de surplomb existe sous conditions.'),
  ],
  related=['prix-isolation-exterieure', 'aides-isolation-exterieure', 'prix-ravalement-facade'],
),
dict(
  slug='fissures-facade', kind='d3', short='Fissures de façade',
  title='Fissures de façade : causes et solutions | Cozybat',
  desc='Microfissure, fissure ou lézarde : reconnaître les fissures de façade, leurs causes en Essonne (sols argileux) et savoir quand un ravalement suffit.',
  h1='Fissures de façade : causes, gravité et solutions',
  intro='Une fissure sur une façade n’est pas toujours grave, mais elle n’est jamais à ignorer : c’est une porte d’entrée pour l’eau. Voici comment les reconnaître et savoir quand un ravalement suffit.',
  sections=[
    ('Reconnaître le type de fissure',
     table(['Type', 'Largeur', 'Ce que cela indique', 'Solution habituelle'],
           [['Microfissure (faïençage)', 'Moins de 0,2 mm', 'Vieillissement ou retrait de l’enduit', 'Ravalement D3 armé'],
            ['Fissure fine', '0,2 à 2 mm', 'Retrait, dilatation, mouvements légers du support', 'Traitement de la fissure puis ravalement armé'],
            ['Lézarde', 'Plus de 2 mm, souvent traversante', 'Mouvement de la structure ou des fondations', 'Diagnostic de structure avant tout ravalement']])
     + p('Une fissure en escalier dans la maçonnerie, une fissure qui s’élargit d’une saison à l’autre, ou des portes et fenêtres qui coincent sont des signes de mouvement structurel.')),
    ('Les causes les plus fréquentes en Essonne',
     ul('<strong>Le retrait et le vieillissement de l’enduit</strong>, qui provoquent un faïençage en surface.',
        '<strong>La dilatation thermique</strong>, surtout sur les façades exposées au sud et à l’ouest.',
        '<strong>Les jonctions entre matériaux différents</strong> : extension, surélévation, linteaux, planchers.',
        '<strong>Les sols argileux</strong>, très présents en Essonne, qui gonflent l’hiver et se rétractent en période de sécheresse, et font bouger les fondations.')),
    ('Pourquoi il faut traiter une fissure',
     p('Même fine, une fissure laisse entrer l’eau de pluie dans le mur. L’humidité dégrade l’enduit, fait gonfler le support au gel et peut atteindre l’intérieur de la maison. Plus elle est traitée tôt, plus le ravalement reste simple et économique.')),
    ('Quand un ravalement suffit',
     p('Pour les microfissures et les fissures fines, un ' + LINK_D3 + ' est la solution adaptée : les fissures sont ouvertes et traitées, puis un enduit armé d’un filet en fibre de verre est appliqué sur toute la surface. L’armature ponte les fissures du support et limite fortement leur réapparition. Une simple peinture, elle, ne fait que masquer les fissures quelques mois.',
       'Le budget est détaillé dans notre guide du ' + LINK_PRIX_RAV + '.')),
    ('Quand il faut d’abord un diagnostic',
     p('Pour une lézarde, une fissure traversante ou qui évolue, aucun revêtement ne règle le problème : il faut d’abord identifier la cause du mouvement. Posez un témoin (une jauge de fissure ou un trait daté) pour suivre son évolution, et faites appel à un bureau d’études ou à un expert.',
       'Si votre commune a fait l’objet d’un arrêté de catastrophe naturelle pour sécheresse, les dommages liés au retrait-gonflement des argiles peuvent être pris en charge par votre assurance habitation : déclarez-les rapidement. Lors de notre visite technique gratuite, nous vous disons clairement si un ravalement suffit ou non.')),
  ],
  faq=[
    ('Une fissure de façade est-elle grave ?', 'Une microfissure ou une fissure fine de moins de 2 mm relève en général du vieillissement de l’enduit et se traite par un ravalement armé. Une fissure plus large, en escalier ou qui s’élargit peut révéler un mouvement de structure et demande un diagnostic.'),
    ('Peut-on peindre sur une façade fissurée ?', 'Une peinture masque les fissures mais ne les traite pas : elles réapparaissent rapidement. Un revêtement armé D3 ponte les fissures grâce à son filet en fibre de verre.'),
    ('Les fissures liées à la sécheresse sont-elles couvertes par l’assurance ?', 'Elles peuvent l’être si un arrêté de catastrophe naturelle a été publié pour votre commune et la période concernée. Rapprochez-vous de votre assureur habitation.'),
  ],
  related=['prix-ravalement-facade', 'refaire-crepi-facade', 'appui-fenetre-beton'],
),
]

GUIDES += [
dict(
  slug='isolant-isolation-exterieure', kind='ite', short='Quel isolant pour une ITE ?',
  title='Isolant ITE : polystyrène, laine de roche, fibre de bois',
  desc='Polystyrène graphité, laine de roche ou fibre de bois : quel isolant choisir pour une isolation par l’extérieur sous enduit ? Performance, épaisseur, prix.',
  h1='Quel isolant pour une isolation par l’extérieur sous enduit ?',
  intro='Une isolation thermique par l’extérieur sous enduit peut se poser avec trois grandes familles d’isolants. Voici leurs différences concrètes pour choisir celui qui convient à votre maison et à votre budget.',
  sections=[
    ('L’ITE sous enduit, en deux mots',
     p('Dans une ITE sous enduit, des panneaux isolants sont collés, et chevillés si besoin, directement sur les murs. Ils sont ensuite recouverts d’un enduit de base armé d’un filet en fibre de verre, puis d’une finition. Le système complet, isolant compris, doit être posé selon les règles du fabricant : on ne mélange pas les produits de plusieurs systèmes.',
       'C’est la technique la plus courante sur les maisons enduites, parce qu’elle isole et refait la façade en une seule opération. Le détail couche par couche est présenté sur notre page ' + LINK_ITE + '.')),
    ('Le polystyrène graphité (PSE gris)',
     p('C’est l’isolant le plus utilisé en ITE sous enduit. Le graphite améliore la performance du polystyrène : à épaisseur égale, il isole mieux qu’un polystyrène blanc.')
     + ul('<strong>Points forts :</strong> le meilleur rapport performance / prix, léger, facile à mettre en œuvre, 120 à 140 mm suffisent en général pour la résistance thermique demandée par les primes.',
          '<strong>Limites :</strong> faible affaiblissement acoustique, confort d’été moyen, et des règles particulières de protection incendie (bandes coupe-feu) selon la hauteur du bâtiment.',
          '<strong>Pour qui :</strong> la plupart des maisons individuelles, quand l’objectif principal est le confort d’hiver et la baisse du chauffage.')),
    ('La laine de roche',
     ul('<strong>Points forts :</strong> incombustible, bon affaiblissement des bruits extérieurs, perméable à la vapeur d’eau.',
        '<strong>Limites :</strong> plus lourde et plus chère que le polystyrène, il faut une épaisseur un peu plus importante pour la même performance.',
        '<strong>Pour qui :</strong> les maisons exposées au bruit (route, voie ferrée, couloir aérien d’Orly) ou quand la sécurité incendie est prioritaire.')),
    ('La fibre de bois',
     ul('<strong>Points forts :</strong> isolant biosourcé, excellent confort d’été grâce à sa forte capacité à stocker la chaleur, bon confort acoustique, perméable à la vapeur d’eau.',
        '<strong>Limites :</strong> l’isolant le plus cher, plus épais à performance égale, il demande une pose soignée et un support sain.',
        '<strong>Pour qui :</strong> les projets qui privilégient les matériaux naturels et le confort l’été, ou les murs anciens qui doivent rester respirants.')),
    ('Le comparatif',
     table(['Critère', 'PSE graphité', 'Laine de roche', 'Fibre de bois'],
           [['Prix', 'Le plus économique', 'Intermédiaire', 'Le plus cher'],
            ['Épaisseur pour R ≈ 3,7 à 4,4', 'Environ 120 à 140 mm', 'Environ 140 à 160 mm', 'Environ 150 à 180 mm'],
            ['Confort d’été', 'Moyen', 'Moyen', 'Très bon'],
            ['Acoustique', 'Faible', 'Bonne', 'Bonne'],
            ['Réaction au feu', 'Protection spécifique', 'Incombustible', 'Protection spécifique'],
            ['Perméabilité à la vapeur', 'Faible', 'Élevée', 'Élevée']])
     + p('Les épaisseurs sont des ordres de grandeur : la résistance thermique exacte dépend du produit et figure sur sa fiche technique. Pour les primes CEE, l’isolation des murs doit atteindre R ≥ 3,7 m².K/W ; voir notre ' + LINK_AIDES + '.')),
    ('Comment nous vous conseillons',
     p('Lors de la visite technique, nous regardons la nature et l’état de vos murs, l’exposition au bruit et au soleil, les débords de toiture et les appuis de fenêtre, qui limitent parfois l’épaisseur possible. Nous vous chiffrons ensuite une ou deux options, avec l’effet de chacune sur le budget, détaillé dans notre guide du ' + LINK_PRIX_ITE + '.')),
  ],
  faq=[
    ('Quel est le meilleur isolant pour une isolation par l’extérieur ?', 'Il n’y a pas d’isolant meilleur dans tous les cas. Le polystyrène graphité offre le meilleur rapport performance / prix ; la laine de roche est incombustible et meilleure contre le bruit ; la fibre de bois apporte le meilleur confort d’été.'),
    ('Quelle épaisseur de polystyrène pour une ITE ?', 'En général 120 à 140 mm de polystyrène graphité pour atteindre la résistance thermique demandée pour les primes CEE (R ≥ 3,7 m².K/W). Une épaisseur de 160 à 200 mm améliore encore le confort.'),
    ('Le polystyrène en façade est-il dangereux en cas d’incendie ?', 'Sur une maison individuelle, les systèmes d’ITE sous enduit en polystyrène sont autorisés ; ils comportent des dispositions de protection prévues par les règles de pose, par exemple autour des baies ou en partie haute selon la configuration.'),
  ],
  related=['prix-isolation-exterieure', 'aides-isolation-exterieure', 'isolation-interieure-ou-exterieure'],
),
dict(
  slug='refaire-crepi-facade', kind='d3', short='Refaire le crépi de sa façade',
  title='Refaire le crépi de sa façade : quand et comment | Cozybat',
  desc='Crépi de façade fissuré, encrassé ou qui s’écaille : quand le refaire, quelles solutions (peinture, RPE, enduit armé D3) et quel budget prévoir.',
  h1='Refaire le crépi de sa façade : quand et comment ?',
  intro='Le crépi protège vos murs de la pluie. Quand il se fissure, s’encrasse ou se décolle, il ne joue plus son rôle. Voici comment savoir s’il faut le refaire, et quelle solution choisir.',
  sections=[
    ('Crépi, enduit, RPE : de quoi parle-t-on ?',
     p('Dans le langage courant, le « crépi » désigne le revêtement qui recouvre une façade. Techniquement, il peut s’agir d’un enduit minéral à base de ciment ou de chaux, souvent projeté, ou d’un revêtement plastique épais (RPE), un revêtement organique appliqué en couche épaisse.',
       'Savoir lequel recouvre votre maison compte, car on ne traite pas un enduit minéral et un RPE de la même façon.')),
    ('Les signes qu’il faut refaire le crépi',
     ul('<strong>Des fissures</strong>, fines ou plus larges, par lesquelles l’eau s’infiltre ; voir notre ' + LINK_FISS + '.',
        '<strong>Un crépi qui s’écaille ou sonne creux</strong> quand on le tapote : il n’adhère plus au mur.',
        '<strong>Des traces noires, vertes ou des coulures</strong> qui reviennent après nettoyage.',
        '<strong>Des taches d’humidité</strong> à l’intérieur, sur les murs extérieurs.',
        '<strong>Un soubassement dégradé</strong> par les éclaboussures et les remontées d’humidité.')),
    ('Faire le bon diagnostic avant de choisir',
     p('Avant tout devis, le crépi doit être sondé, par exemple au marteau sur toute la façade : on repère les zones creuses et non adhérentes. Elles doivent être purgées, c’est-à-dire retirées jusqu’au support sain. Quand une grande partie de la surface n’adhère plus, il est plus économique et plus sûr de décaper l’ensemble que de multiplier les reprises.',
       'C’est aussi le moment de vérifier les fissures : celles de l’enduit se traitent au ravalement, celles de la structure demandent un diagnostic spécifique.')),
    ('Les solutions possibles',
     table(['Solution', 'Adaptée quand…', 'Limites'],
           [['Nettoyage et peinture', 'Le crépi est sain et adhérent, sans fissures', 'Ne traite pas les fissures, qui réapparaissent'],
            ['Ravalement D3 armé', 'Le crépi est fissuré ou fatigué mais adhérent', 'Les zones non adhérentes doivent être purgées avant'],
            ['Réfection complète de l’enduit', 'Le crépi se décolle sur de grandes surfaces', 'Plus long, nécessite un séchage entre les couches'],
            ['Isolation par l’extérieur', 'La maison est aussi froide ou chère à chauffer', 'Budget plus élevé, mais isolation et façade neuve']])
     + p('Pour des reprises ponctuelles (zones décollées, appuis, balcons), voir notre page <a href="/maconnerie-facade/">maçonnerie de façade</a>. Le ravalement D3 armé est souvent le meilleur compromis : un enduit armé d’un filet en fibre de verre recouvre toute la façade, ponte les microfissures et offre une finition neuve dans la teinte choisie. Le système est détaillé sur notre page ' + LINK_D3 + '.')),
    ('Quel budget prévoir ?',
     p('Pour un ravalement D3 armé, comptez chez Cozybat 100 à 120 € TTC par m² de façade en Essonne, échafaudage et finition compris ; les zones à purger sont chiffrées en plus selon leur surface. Les exemples de budget figurent dans notre guide du ' + LINK_PRIX_RAV + '.',
       'Si vous hésitez avec une isolation, comparez avec le ' + LINK_PRIX_ITE + ' : quand le crépi est à refaire de toute façon, l’écart entre les deux solutions se réduit.')),
    ('Démarches',
     p('Refaire le crépi en changeant de teinte ou d’aspect demande une déclaration préalable de travaux en mairie, et le PLU peut imposer certaines couleurs. Nous vérifions les règles de votre commune et vous aidons à préparer le dossier.')),
  ],
  faq=[
    ('Quand faut-il refaire le crépi d’une maison ?', 'Quand il est fissuré, qu’il s’écaille ou sonne creux, que les salissures reviennent après nettoyage ou que l’humidité traverse le mur. En moyenne, une façade se rénove tous les 10 à 20 ans selon son exposition.'),
    ('Peut-on refaire un crépi par-dessus l’ancien ?', 'Oui si l’ancien crépi est sain et adhérent : après lavage et traitement des fissures, un enduit armé peut être appliqué par-dessus. Les zones creuses ou qui s’écaillent doivent d’abord être purgées.'),
    ('Quelle différence entre un crépi et un RPE ?', 'Le crépi traditionnel est un enduit minéral (ciment ou chaux). Le RPE est un revêtement plastique épais, organique, appliqué en couche épaisse. Leur rénovation demande des produits compatibles avec chacun.'),
  ],
  related=['appui-fenetre-beton', 'fissures-facade', 'enduit-gratte-taloche-ribbe'],
),
]

GUIDES += [
dict(
  slug='enduit-gratte-taloche-ribbe', kind='d3', short='Enduit gratté, taloché ou ribbé ?',
  title='Enduit gratté, taloché ou ribbé : que choisir ? | Cozybat',
  desc='Enduit de façade gratté, taloché, ribbé ou lisse : aspect, résistance aux salissures, compatibilité avec l’isolation par l’extérieur et conseils de choix.',
  h1='Enduit gratté, taloché ou ribbé : quelle finition choisir ?',
  intro='La finition de l’enduit donne à votre façade son aspect pour les quinze ou vingt prochaines années. Gratté, taloché, ribbé ou lisse : voici ce qui distingue chaque finition, comment elle vieillit et laquelle convient à votre maison.',
  sections=[
    ('Les finitions d’enduit en un coup d’œil',
     p('La finition est la dernière couche d’un ravalement ou d’une isolation par l’extérieur. Elle ne change pas la protection du mur, assurée par les couches inférieures, mais elle détermine le relief, la façon dont la lumière accroche la façade et la vitesse à laquelle elle se salit.')
     + table(['Finition', 'Aspect', 'Tenue aux salissures', 'Pour quelle façade'],
             [['Gratté', 'Mat, finement rugueux, très régulier', 'Très bonne', 'La plupart des maisons, façades exposées'],
              ['Taloché', 'Grain régulier, plus ou moins fin selon le grain', 'Bonne en grain fin', 'Maisons contemporaines, ITE'],
              ['Ribbé', 'Petits sillons qui donnent du relief', 'Moyenne : le relief retient la poussière', 'Façades abritées, effet décoratif'],
              ['Lisse', 'Uni, sans relief', 'Moyenne : les traces se voient vite', 'Petites surfaces, encadrements, style épuré']])),
    ('L’enduit gratté',
     p('C’est l’une des finitions les plus répandues sur les maisons d’Île-de-France. Traditionnellement, l’enduit est appliqué en épaisseur puis, après quelques heures de prise, sa surface est grattée avec une taloche à pointes. Le grattage retire la pellicule superficielle et laisse un aspect mat, finement rugueux et très homogène.')
     + ul('<strong>Points forts :</strong> il masque bien les petites irrégularités du mur, vieillit de façon régulière et se salit peu, car son relief est fin et sans creux marqués.',
          '<strong>Limites :</strong> le rendu dépend beaucoup du moment du grattage et de la main de l’applicateur ; une reprise ponctuelle se voit davantage qu’avec un aspect plus marqué.',
          '<strong>Pour qui :</strong> la plupart des pavillons, notamment ceux exposés à la pluie et à la circulation, quand on cherche une façade sobre qui reste propre longtemps.')),
    ('L’enduit taloché',
     p('Pour un enduit taloché, la finition est serrée à la taloche, souvent en mouvements circulaires, jusqu’à obtenir un grain régulier. La taille du grain de l’enduit fixe le rendu : un grain fin donne une surface presque veloutée, un grain plus gros une texture plus visible.')
     + ul('<strong>Points forts :</strong> rendu net et contemporain, grande régularité sur les grandes surfaces, finition courante des systèmes d’isolation par l’extérieur sous enduit.',
          '<strong>Limites :</strong> en grain gros, la poussière s’accroche davantage ; les traces de reprise doivent être évitées en travaillant chaque pan de mur d’un seul tenant.',
          '<strong>Pour qui :</strong> les maisons au style actuel, les extensions, et la plupart des ITE.')),
    ('L’enduit ribbé, et les autres aspects',
     p('L’enduit ribbé contient des grains plus gros qui roulent sous la taloche et creusent de petits sillons. Selon le geste, les sillons sont droits, circulaires ou irréguliers. Le relief donne du caractère à la façade et joue avec la lumière rasante.',
       'Ce relief a un revers : il retient davantage la poussière et la pollution, surtout sur une façade orientée au nord ou sous des arbres. Le ribbé convient bien aux façades abritées ou aux pans de mur qu’on veut distinguer.',
       'L’<strong>enduit lisse</strong>, lui, est réservé en général aux encadrements de fenêtres, aux bandeaux ou aux petites surfaces : sur une grande façade, il révèle le moindre défaut de planéité et la moindre coulure. D’autres aspects existent (écrasé, projeté, rustique), plus rares aujourd’hui sur les maisons de l’Essonne.')),
    ('Finition et isolation par l’extérieur',
     p('Sur une ' + LINK_ITE + ', la finition fait partie d’un système complet défini par le fabricant : isolant, enduit de base armé, sous-couche et finition sont prévus pour fonctionner ensemble. Les finitions possibles sont donc celles du système retenu, en général des enduits de finition de faible épaisseur en aspect taloché, ribbé ou gratté.',
       'Deux points comptent particulièrement sur un isolant :')
     + ul('<strong>La teinte.</strong> Une couleur très foncée absorbe la chaleur du soleil et fait travailler l’enduit sur l’isolant. Les fabricants limitent donc les teintes trop sombres ; nous vous indiquons les teintes autorisées pour le système choisi.',
          '<strong>L’uniformité.</strong> La finition est appliquée par pans entiers, d’un angle à l’autre, pour éviter les traces de reprise visibles sur une façade neuve.')),
    ('Finition et ravalement D3 armé',
     p('Pour un ' + LINK_D3 + ', l’enduit armé d’un filet en fibre de verre ponte les fissures du support, puis une finition talochée, grattée ou lisse redonne à la façade un aspect neuf dans la teinte choisie. Si votre façade est déjà en gratté et que vous voulez garder le même aspect, c’est possible ; changer d’aspect l’est aussi.',
       'Avant de choisir, vérifiez l’état de l’enduit existant : un crépi qui sonne creux ou s’écaille doit être purgé, quelle que soit la finition prévue. Notre guide pour <a href="/guides/refaire-crepi-facade/">refaire le crépi de sa façade</a> détaille ce diagnostic.')),
    ('Comment bien choisir',
     ul('<strong>L’exposition.</strong> Façade sur rue, face aux pluies dominantes ou sous des arbres : privilégiez un gratté ou un taloché fin, qui se salissent moins.',
        '<strong>Le style de la maison.</strong> Le gratté s’accorde avec les pavillons traditionnels, le taloché avec les maisons contemporaines, le ribbé apporte du relief.',
        '<strong>La cohérence du quartier.</strong> Le PLU de votre commune peut encadrer les teintes et parfois l’aspect des enduits ; en secteur protégé, l’Architecte des Bâtiments de France peut donner son avis.',
        '<strong>Un échantillon sur place.</strong> Une teinte paraît toujours plus claire sur une grande façade en plein soleil que sur un nuancier : regardez un échantillon sur le mur, à différentes heures.')),
    ('Prix et démarches',
     p('Chez Cozybat, la finition est comprise dans nos prix indicatifs en Essonne : 100 à 120 € TTC par m² de façade pour un ravalement D3 armé, 180 à 210 € TTC par m² de mur isolé pour une isolation par l’extérieur. L’aspect et la teinte choisis peuvent faire légèrement varier le coût de la dernière couche ; nous vous le précisons au devis. Les budgets complets sont dans nos guides du ' + LINK_PRIX_RAV + ' et du ' + LINK_PRIX_ITE + '.',
       'Changer la teinte ou l’aspect d’une façade modifie son aspect extérieur : cela demande en général une déclaration préalable de travaux en mairie. Même un ravalement à l’identique peut y être soumis en secteur protégé ou si la commune l’a décidé. Nous vérifions les règles de votre commune et vous aidons à préparer le dossier. Pour choisir votre finition sur votre propre façade, faites une ' + LINK_DEVIS + ' : la visite technique est gratuite.')),
  ],
  faq=[
    ('Quelle différence entre un enduit gratté et un enduit taloché ?', 'L’enduit gratté est raclé avec une taloche à pointes après un début de prise : il est mat, finement rugueux et très homogène. L’enduit taloché est serré à la taloche jusqu’à obtenir un grain régulier, plus ou moins fin selon le produit.'),
    ('Quelle finition de façade se salit le moins ?', 'Les finitions au relief fin, comme le gratté ou le taloché à grain fin, retiennent le moins la poussière. Le ribbé et les aspects rustiques, plus creusés, se salissent plus vite, surtout au nord ou sous des arbres.'),
    ('Peut-on choisir sa finition sur une isolation par l’extérieur ?', 'Oui, parmi les finitions prévues par le système d’isolation retenu, en général taloché, ribbé ou gratté. Les teintes très foncées sont limitées sur isolant, car elles chauffent fortement au soleil.'),
    ('Faut-il une autorisation pour changer la finition ou la couleur de sa façade ?', 'En général oui : un changement d’aspect ou de teinte relève d’une déclaration préalable de travaux en mairie, et le PLU peut imposer certaines couleurs. Renseignez-vous auprès du service urbanisme de votre commune avant de commander les travaux.'),
  ],
  related=['refaire-crepi-facade', 'prix-ravalement-facade', 'prix-isolation-exterieure'],
),
]

GUIDES += [
dict(
  slug='appui-fenetre-beton', kind='d3', short='Appui de fenêtre en béton',
  title='Appui de fenêtre béton : réparer ou remplacer ? | Cozybat',
  desc='Appui de fenêtre en béton fissuré, épaufré ou aux aciers rouillés : comment le réparer, quand le remplacer et que faire en isolation par l’extérieur.',
  h1='Appui de fenêtre en béton : réparer ou remplacer ?',
  intro='L’appui de fenêtre reçoit toute l’eau qui ruisselle sur la vitre et la menuiserie. C’est souvent le premier élément d’une façade à se fissurer. Voici comment juger son état, quand une réparation suffit, quand il vaut mieux le remplacer, et ce qui change avec une isolation par l’extérieur.',
  sections=[
    ('À quoi sert un appui de fenêtre',
     p('L’appui, ou rebord extérieur, est la pièce en béton, en pierre ou en métal posée sous la fenêtre. Son rôle est simple : recueillir l’eau de pluie et l’éloigner du mur. Pour cela, un appui en bon état réunit trois détails :')
     + ul('<strong>une pente vers l’extérieur</strong>, pour que l’eau ne stagne pas contre la menuiserie ;',
          '<strong>un rejingot</strong>, le petit relief à l’arrière de l’appui contre lequel vient la fenêtre, qui empêche l’eau de passer dessous ;',
          '<strong>un débord et une goutte d’eau</strong> (ou larmier), la petite rainure sous le nez de l’appui qui fait tomber les gouttes au lieu de les laisser couler sur la façade.')
     + p('Quand l’un de ces détails manque ou se dégrade, l’eau ruisselle sur l’enduit, s’infiltre sous l’appui et finit par abîmer le mur et parfois l’intérieur de la maison.')),
    ('Les signes d’un appui abîmé',
     ul('<strong>Des fissures</strong> sur le dessus ou en travers de l’appui, souvent aux extrémités, là où il est encastré dans le mur.',
        '<strong>Des épaufrures</strong> : des morceaux de béton qui éclatent, en général sur le nez de l’appui.',
        '<strong>Des aciers apparents et rouillés</strong> : l’armature a gonflé en s’oxydant et fait éclater le béton qui la couvrait.',
        '<strong>Des coulures noires</strong> sous chaque fenêtre : la goutte d’eau ne fonctionne plus, ou n’a jamais existé.',
        '<strong>De l’eau qui stagne</strong> sur l’appui après la pluie : la pente est insuffisante ou inversée.',
        '<strong>Des traces d’humidité</strong> à l’intérieur, sous la fenêtre ou dans les angles du tableau.')
     + p('Une fissure fine en surface n’a pas la même gravité qu’un appui fendu sur toute son épaisseur. Si les fissures se prolongent dans le mur, en escalier ou depuis les angles de la fenêtre, le problème peut venir de la structure : notre ' + LINK_FISS + ' vous aide à faire la différence.')),
    ('Réparer : quand et comment',
     p('Une réparation suffit quand l’appui est entier, bien fixé, avec une pente correcte, et que les dégâts restent en surface : fissures fines, épaufrures localisées, aciers peu corrodés. Une réparation bien faite suit toujours le même ordre :')
     + ul('<strong>Purger</strong> le béton abîmé jusqu’au support sain, au marteau et au burin.',
          '<strong>Dégager et traiter les aciers</strong> : brossage de la rouille, puis produit passivant qui les protège de la corrosion.',
          '<strong>Reconstituer</strong> l’appui avec un mortier de réparation adapté au béton, en reformant les arêtes.',
          '<strong>Reprofiler</strong> la pente et recréer la goutte d’eau sous le nez de l’appui.',
          '<strong>Protéger</strong> avec un revêtement adapté, ou poser une couvertine en aluminium par-dessus pour une protection durable.')
     + p('La couvertine, ou bavette, est une tôle d’aluminium laquée qui recouvre l’appui existant. Elle évite de casser un appui simplement vieilli, cache les reprises et apporte une goutte d’eau neuve. Elle doit être posée sur un appui sain : on ne recouvre pas un béton qui continue d’éclater.')),
    ('Remplacer : dans quels cas',
     p('Le remplacement s’impose quand la réparation ne tiendrait pas :')
     + ul('l’appui est fendu sur toute son épaisseur, cassé ou descellé ;',
          'les aciers sont fortement corrodés sur une grande longueur ;',
          'la pente est inversée et ramène l’eau vers la fenêtre ;',
          'l’appui est trop court pour la nouvelle épaisseur de façade, par exemple après une isolation par l’extérieur.')
     + p('Remplacer un appui en béton est un travail délicat : il faut le déposer sans abîmer la menuiserie ni le mur, puis poser un appui neuf (préfabriqué ou coulé en place) avec la bonne pente, un rejingot et une étanchéité soignée sous la fenêtre. Sur certaines fenêtres, la dépose de l’appui oblige à intervenir sur la menuiserie : c’est un point à vérifier lors de la visite.')
     + table(['Situation', 'Solution habituelle'],
             [['Fissures fines, appui sain et bien en pente', 'Traitement des fissures et revêtement de protection'],
              ['Épaufrures, aciers peu rouillés', 'Purge, passivation des aciers, mortier de réparation'],
              ['Appui vieilli mais solide, coulures sur la façade', 'Réparation puis couvertine en aluminium'],
              ['Appui fendu, descellé ou pente inversée', 'Remplacement de l’appui'],
              ['Isolation par l’extérieur prévue', 'Prolongation ou remplacement pour couvrir l’isolant']])),
    ('Appuis de fenêtre et isolation par l’extérieur',
     p('Avec une ' + LINK_ITE + ', la façade avance de l’épaisseur de l’isolant et de l’enduit, souvent 15 à 20 cm. Un appui d’origine qui dépassait de quelques centimètres se retrouve alors en retrait : l’eau tomberait directement sur l’enduit neuf. Chaque appui doit donc être traité pour retrouver un débord suffisant au-delà de la nouvelle façade.',
       'Selon les cas, nous posons un appui rapporté en aluminium par-dessus l’ancien, avec un isolant glissé dessous pour limiter le pont thermique, ou nous remplaçons l’appui. Les jonctions avec l’isolant sont protégées par des profilés et joints prévus par le système d’isolation, pour que l’eau ne s’infiltre pas derrière l’enduit. Ce traitement est chiffré fenêtre par fenêtre sur le devis.')),
    ('Prix et TVA',
     p('Les réparations et remplacements d’appuis sont chiffrés <strong>sur devis</strong> chez Cozybat, après visite : le coût dépend du nombre d’appuis, de leur longueur, de leur état et de l’accès. Ils peuvent être réalisés seuls, ou au sein d’un chantier plus large. Lors d’un ' + LINK_D3 + ' (100 à 120 € TTC par m² de façade, prix indicatifs en Essonne), il est logique de remettre les appuis en état avant l’enduit. Lors d’une isolation par l’extérieur (180 à 210 € TTC par m² de mur isolé), leur adaptation fait partie des points singuliers qui expliquent l’écart entre deux devis ; voir notre guide du ' + LINK_PRIX_ITE + '.',
       'Pour un logement achevé depuis plus de deux ans, des travaux de réparation relèvent en général du taux de TVA de 10 %. Dans le cadre d’une isolation par l’extérieur, les travaux liés à l’isolation peuvent bénéficier du taux de 5,5 % : nous vous indiquons le taux applicable sur le devis. Pour les aides à l’isolation, consultez notre ' + LINK_AIDES + ' ou un conseiller France Rénov’.',
       'Des reprises ponctuelles d’appuis, de balcons ou d’enduit sont présentées sur notre page <a href="/maconnerie-facade/">maçonnerie de façade</a>. Pour faire chiffrer vos appuis, faites une ' + LINK_DEVIS + '.')),
  ],
  faq=[
    ('Comment réparer un appui de fenêtre en béton fissuré ?', 'On purge le béton abîmé jusqu’au support sain, on traite les aciers apparents contre la rouille, puis on reconstitue l’appui avec un mortier de réparation en reformant la pente et la goutte d’eau. Une couvertine en aluminium peut ensuite le protéger durablement.'),
    ('Faut-il remplacer un appui de fenêtre dont les aciers sont visibles ?', 'Pas forcément. Si la rouille est localisée et l’appui solide, une réparation avec traitement des aciers suffit. Si les aciers sont corrodés sur une grande longueur ou si l’appui est fendu, le remplacement est plus sûr.'),
    ('Peut-on poser une couvertine aluminium sur un vieil appui en béton ?', 'Oui, si l’appui est sain et bien fixé. La couvertine recouvre l’appui, apporte une nouvelle goutte d’eau et évite de le casser. Elle ne doit pas cacher un béton qui continue d’éclater, qu’il faut réparer avant.'),
    ('Que deviennent les appuis de fenêtre lors d’une isolation par l’extérieur ?', 'Ils doivent dépasser la nouvelle façade pour éloigner l’eau de l’enduit. Selon leur état, ils sont prolongés par un appui rapporté en aluminium ou remplacés ; ce traitement est chiffré fenêtre par fenêtre sur le devis.'),
  ],
  related=['fissures-facade', 'refaire-crepi-facade', 'prix-isolation-exterieure'],
),
]
