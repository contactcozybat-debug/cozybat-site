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
  related=['comment-isoler-mur-exterieur', 'prix-isolation-exterieure', 'aides-isolation-exterieure'],
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
  related=['prix-ravalement-facade', 'refaire-crepi-facade', 'prix-isolation-exterieure'],
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
  related=['comment-isoler-mur-exterieur', 'prix-isolation-exterieure', 'aides-isolation-exterieure'],
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
  related=['prix-ravalement-facade', 'fissures-facade', 'enduit-gratte-taloche-ribbe'],
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
  slug='comment-isoler-mur-exterieur', kind='ite', short='Comment isoler un mur extérieur ?',
  title='Comment isoler un mur extérieur : les étapes | Cozybat',
  desc='Comment isoler un mur extérieur de maison : techniques, étapes du chantier, épaisseur d’isolant, erreurs à éviter, démarches et budget en 2026.',
  h1='Comment isoler un mur extérieur de maison ?',
  intro='Les murs non isolés d’une maison font partie des principales sources de déperdition de chaleur. Voici comment on les isole concrètement : quelle technique choisir, ce qu’il faut vérifier avant de commencer, et comment se déroule un chantier, étape par étape.',
  sections=[
    ('Deux façons d’isoler un mur donnant sur l’extérieur',
     p('Un mur extérieur peut s’isoler de deux côtés : par l’intérieur, en doublant le mur dans chaque pièce, ou par l’extérieur, en enveloppant la maison d’un isolant recouvert d’une nouvelle façade.',
       'Par l’extérieur, l’isolant passe devant les planchers et les murs de refend : les ponts thermiques sont traités, vous ne perdez aucune surface habitable et vous restez chez vous pendant les travaux. Par l’intérieur, le chantier coûte moins cher mais se fait pièce par pièce. Notre ' + LINK_ITI + ' détaille les cas où chaque solution l’emporte. La suite de ce guide porte sur l’isolation par l’extérieur.')),
    ('Les techniques d’isolation par l’extérieur',
     table(['Technique', 'Principe', 'Pour quelle maison'],
           [['ITE sous enduit', 'Panneaux isolants collés et chevillés sur le mur, puis enduit armé et finition', 'La plupart des maisons enduites, en parpaing, brique ou béton'],
            ['Bardage ventilé', 'Ossature fixée au mur, isolant entre les montants, lame d’air et bardage (bois, composite, fibres-ciment)', 'Maisons à l’aspect bois ou contemporain, murs irréguliers'],
            ['Enduit isolant', 'Enduit chargé de granulats isolants, appliqué en plusieurs centimètres', 'Murs anciens en pierre, quand une isolation épaisse est impossible : performance limitée']])
     + p('Sur les pavillons de l’Essonne, l’ITE sous enduit est de loin la technique la plus courante : elle isole et refait la façade en une seule opération, en conservant l’aspect d’une maison enduite. Le système complet est présenté couche par couche sur notre page ' + LINK_ITE + '.')),
    ('Ce qu’il faut vérifier avant de commencer',
     ul('<strong>L’état du mur.</strong> L’isolant se colle sur un support sain : les parties d’enduit qui sonnent creux sont purgées, les fissures repérées. Une lézarde qui évolue demande un diagnostic de structure avant tout ; voir notre ' + LINK_FISS + '.',
        '<strong>L’humidité.</strong> Un mur humide doit être assaini avant d’être isolé : on recherche la cause (remontées du sol, gouttière défectueuse, fuite) et on la traite d’abord.',
        '<strong>La place disponible.</strong> L’isolation ajoute 15 à 20 cm à l’épaisseur des murs : il faut vérifier le débord de toiture, les appuis de fenêtre, les passages étroits et les murs en limite de propriété.',
        '<strong>Les règles d’urbanisme.</strong> Une isolation par l’extérieur modifie l’aspect de la façade : une déclaration préalable de travaux en mairie est en général nécessaire, et le PLU peut encadrer les teintes.')),
    ('Les étapes d’un chantier d’ITE sous enduit',
     '<ol>'
     + ''.join(f'<li>{x}</li>' for x in [
        '<strong>Visite technique et devis.</strong> Relevé des façades, diagnostic du support, repérage des points singuliers, choix de l’isolant, de l’épaisseur et de la finition.',
        '<strong>Aides et démarches.</strong> Inscription à l’offre de prime CEE <strong>avant</strong> de signer le devis, puis dépôt de la déclaration préalable en mairie.',
        '<strong>Installation et préparation.</strong> Montage de l’échafaudage, protection des abords, dépose des descentes d’eau, luminaires et gonds de volets, nettoyage et reprise du support.',
        '<strong>Pose de l’isolant.</strong> Un rail de départ est fixé en bas de façade, puis les panneaux sont collés et chevillés en quinconce, joints serrés, jusqu’en haut des murs.',
        '<strong>Points singuliers.</strong> Retours d’isolant dans les tableaux de fenêtres, prolongement ou remplacement des appuis, profilés d’angle et de raccord, couvertines en tête de mur.',
        '<strong>Enduit et finition.</strong> Enduit de base armé d’un filet en fibre de verre, sous-couche, puis finition dans la teinte choisie.',
        '<strong>Repose et réception.</strong> Repose des équipements, repli de l’échafaudage, nettoyage, puis réception contradictoire des travaux.'])
     + '</ol>'
     + p('Pour une maison individuelle, le chantier dure en général quelques semaines, selon la surface, le nombre de points singuliers et la météo : les enduits ne s’appliquent ni par temps de gel ni sous la pluie.')),
    ('Quelle épaisseur d’isolant ?',
     p('Pour ouvrir droit aux primes CEE, l’isolation des murs doit atteindre une résistance thermique R ≥ 3,7 m².K/W. Avec un polystyrène graphité, cela correspond en général à 120 à 140 mm. Nous posons le plus souvent 140 à 200 mm : quelques centimètres de plus améliorent nettement le confort pour un surcoût limité, tant que les appuis et les débords de toiture le permettent.',
       'Le choix entre polystyrène graphité, laine de roche et fibre de bois change l’épaisseur nécessaire, le confort d’été et l’acoustique : voir notre <a href="/guides/isolant-isolation-exterieure/">comparatif des isolants pour l’ITE</a>.')),
    ('Les erreurs à éviter',
     ul('Isoler un mur humide sans avoir traité la cause de l’humidité.',
        'Signer le devis avant de s’être inscrit à l’offre CEE : la prime est alors perdue.',
        'Négliger les points singuliers : un appui de fenêtre non prolongé ou un tableau non isolé crée un pont thermique et une entrée d’eau.',
        'Mélanger les produits de plusieurs fabricants : isolant, colle, enduits et finition doivent appartenir au même système.',
        'Choisir une teinte très foncée sur isolant : elle chauffe fortement au soleil et fait travailler l’enduit.')),
    ('Peut-on isoler son mur extérieur soi-même ?',
     p('C’est techniquement possible, mais l’ITE est un travail de façade en hauteur, sur échafaudage, où chaque détail compte pour l’étanchéité. Surtout, les primes CEE et l’éco-prêt à taux zéro exigent que les travaux soient réalisés par une entreprise qualifiée RGE. Une entreprise apporte aussi la garantie décennale sur l’ouvrage : Cozybat est qualifiée RGE Qualibat et assurée en décennale chez SMABTP.')),
    ('Budget et aides',
     p('Chez Cozybat, une isolation par l’extérieur sous enduit coûte 180 à 210 € TTC par m² de mur isolé en Essonne, échafaudage, préparation et finition compris, avant déduction des primes. Les exemples chiffrés sont dans notre guide du ' + LINK_PRIX_ITE + '.',
       'Depuis le 1er janvier 2026, MaPrimeRénov’ par geste ne finance plus l’isolation des murs ; elle reste possible dans le cadre d’une rénovation d’ampleur avec MaPrimeRénov’ Parcours accompagné. Les primes CEE, la TVA à 5,5 % et l’éco-PTZ restent mobilisables : tout est détaillé dans notre ' + LINK_AIDES + '. Pour un projet précis, faites une ' + LINK_DEVIS + ' : la visite technique est gratuite.')),
  ],
  faq=[
    ('Quelle est la meilleure façon d’isoler un mur extérieur ?', 'Pour une maison enduite, l’isolation par l’extérieur sous enduit est en général la plus efficace : elle supprime les ponts thermiques, ne réduit pas la surface habitable et refait la façade en même temps. L’isolation par l’intérieur reste pertinente pour une façade de caractère à préserver.'),
    ('Quelle épaisseur d’isolant pour un mur extérieur ?', 'Il faut atteindre au moins R = 3,7 m².K/W pour les primes CEE, soit en général 120 à 140 mm de polystyrène graphité. Chez Cozybat, nous posons le plus souvent 140 à 200 mm selon la maison.'),
    ('Faut-il une autorisation pour isoler par l’extérieur ?', 'En général oui : l’isolation modifie l’aspect de la façade et demande une déclaration préalable de travaux en mairie. Le PLU peut aussi encadrer les teintes et les débords sur la voie publique.'),
    ('Combien de temps dure une isolation par l’extérieur ?', 'Pour une maison individuelle, comptez en général quelques semaines de chantier, selon la surface, les points singuliers et la météo. Vous restez dans votre maison pendant toute la durée des travaux.'),
  ],
  related=['prix-isolation-exterieure', 'isolant-isolation-exterieure', 'aides-isolation-exterieure'],
),
]
