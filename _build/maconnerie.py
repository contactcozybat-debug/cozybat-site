# Page service « Maçonnerie de façade » (/maconnerie-facade/) — remplace l'ancienne page maconnerie-facade.html
from guides import ul, p, table

PAGE = dict(
  path='maconnerie-facade',
  title='Maçonnerie de façade : reprises et appuis (91) | Cozybat',
  desc='Reprises d’enduit, réparation de fissures, appuis de fenêtre, balcons et couvertines en Essonne. Façadier RGE à Morangis, décennale SMABTP. Devis gratuit.',
  h1='Maçonnerie de façade en Essonne : reprises, appuis et réparations',
  intro='Une façade ne se résume pas à son enduit. Appuis de fenêtre fissurés, crépi qui s’écaille, béton de balcon éclaté, rebords sans protection : Cozybat répare ces points avant qu’ils n’abîment le mur, seuls ou dans le cadre d’un ravalement ou d’une isolation par l’extérieur.',
  sections=[
    ('Reprises d’enduit et de crépi',
     p('Un enduit qui sonne creux ou qui s’écaille n’adhère plus au mur : l’eau s’infiltre derrière et le décollement s’étend. La façade est d’abord sondée pour repérer toutes les zones non adhérentes.')
     + ul('purge des parties creuses ou décollées jusqu’au support sain ;',
          'traitement du support : brossage, dépoussiérage, primaire d’accrochage si nécessaire ;',
          'reprise au mortier ou ragréage pour retrouver une surface plane ;',
          'finition raccordée à l’existant, ou intégrée à un ravalement complet.')
     + p('Quand une grande partie de la façade n’adhère plus, une reprise ponctuelle ne suffit plus : un décapage puis une réfection d’enduit ou un <a href="/ravalement-facade/">ravalement D3 armé</a> est plus durable. Voir aussi notre guide pour <a href="/guides/refaire-crepi-facade/">refaire le crépi de sa façade</a>.')),
    ('Réparation des fissures de façade',
     p('Les fissures sont ouvertes, dépoussiérées et rebouchées avec un produit adapté à leur largeur. Sur une façade très fissurée, la réparation est complétée par un enduit armé d’un filet en fibre de verre, qui ponte les fissures sur toute la surface.',
       'Les lézardes larges ou évolutives demandent d’abord un diagnostic de structure : nous vous le disons clairement lors de la visite. Notre <a href="/guides/fissures-facade/">guide des fissures de façade</a> explique comment les reconnaître.')),
    ('Appuis de fenêtre',
     p('Les appuis de fenêtre reçoivent l’eau de pluie de toute la menuiserie : ce sont souvent les premiers éléments à se fissurer ou à s’épaufrer.')
     + ul('réparation des épaufrures et des fissures, ragréage et reprofilage pour que l’eau s’écoule vers l’extérieur ;',
          'enduit et peinture de protection dans la teinte de la façade ;',
          'pose de couvertines ou de bavettes en aluminium pour protéger durablement l’appui ;',
          'en isolation par l’extérieur : prolongation ou remplacement des appuis pour couvrir l’épaisseur de l’isolant.')),
    ('Balcons, sous-faces et béton éclaté',
     p('Quand les armatures d’un balcon ou d’un linteau rouillent, elles gonflent et font éclater le béton. Il ne suffit pas de reboucher : la rouille continuerait son travail.')
     + ul('purge du béton dégradé jusqu’aux aciers ;',
          'traitement des armatures apparentes (brossage et produit de passivation) ;',
          'reconstitution au mortier de réparation ;',
          'finition des sous-faces de balcon, par exemple en revêtement plastique épais (RPE) assorti à la façade.')),
    ('Couvertines, rebords et soubassements',
     ul('pose de couvertines sur les rebords de balcon, murets et acrotères pour empêcher l’eau de pénétrer par le dessus ;',
        'reprise des soubassements dégradés par les éclaboussures et les remontées d’humidité ;',
        'bandes de séparation entre soubassement et façade.')),
    ('Seules ou avec un ravalement',
     p('Ces réparations peuvent être réalisées seules, quand le reste de la façade est en bon état. Elles sont aussi la première étape de tout <a href="/ravalement-facade/">ravalement</a> ou de toute <a href="/isolation-exterieure/">isolation par l’extérieur</a> : un enduit neuf ou un isolant posé sur un support mal préparé ne tient pas dans le temps.')
     + table(['Situation', 'Ce que nous proposons'],
             [['Quelques appuis ou fissures isolées, façade saine', 'Réparations ponctuelles, chiffrées au forfait'],
              ['Enduit fatigué ou fissuré sur toute la façade', 'Réparations puis ravalement D3 armé'],
              ['Maison froide ou chère à chauffer', 'Réparations puis isolation par l’extérieur']])
     + p('Chaque intervention est chiffrée sur devis après la visite technique gratuite, poste par poste.')),
  ],
  faq=[
    ('Faites-vous des petites réparations de façade sans ravalement complet ?', 'Oui. Reprises d’enduit, fissures, appuis de fenêtre, sous-faces de balcon ou couvertines peuvent être réalisés seuls, quand le reste de la façade est en bon état. Ils sont chiffrés au forfait après la visite.'),
    ('Comment réparer un appui de fenêtre en béton fissuré ?', 'Les parties abîmées sont purgées, puis l’appui est ragréé et reprofilé pour évacuer l’eau, avant un enduit ou une peinture de protection. Pour une protection durable, une couvertine en aluminium peut être posée par-dessus.'),
    ('Que faire quand le crépi se décolle ?', 'Il faut sonder la façade, purger toutes les zones creuses jusqu’au support sain puis reprendre au mortier. Si une grande partie de la surface n’adhère plus, un décapage et une réfection complète sont plus durables.'),
    ('Le béton de mon balcon éclate, est-ce grave ?', 'C’est le signe que les armatures rouillent. Il faut purger le béton, traiter les aciers et reconstituer au mortier de réparation avant que la corrosion ne s’étende. Pour des dégradations importantes, un avis de structure peut être nécessaire.'),
  ],
)
