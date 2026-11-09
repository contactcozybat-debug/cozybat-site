/* =========================================================================
   CHANTIERS COZYBAT
   Ce fichier alimente la page « Nos réalisations » ET la page de détail
   de chaque chantier. C'est le seul fichier à modifier.

   POUR AJOUTER UN CHANTIER :
   1. Déposez vos photos dans le dossier "assets" du projet.
   2. Copiez un bloc { ... } ci-dessous, collez-le en HAUT de la liste
      (le plus récent en premier) et changez les valeurs.
   3. Donnez-lui un "id" unique (sans accent ni espace) — c'est l'adresse
      de sa page de détail.
   La page, les filtres, le compteur et les pages de détail se mettent
   à jour automatiquement. La liste peut en contenir autant que vous voulez.

   LES CHAMPS
     id          : identifiant unique, ex. "savigny-2025"     (obligatoire)
     commune     : la ville du chantier                       (obligatoire)
     prestation  : "Ravalement de façade", "Isolation par l'extérieur",
                   "Peinture extérieure", "Nettoyage & traitement"
     annee       : l'année des travaux, ex. "2026"   ("" si vous ne savez pas)
     duree       : durée du chantier, ex. "3 semaines"   ("" pour masquer)
     motsCles    : la liste des mots-clés affichés en étiquettes
     description : 2 ou 3 phrases. N'écrivez que ce qui est vrai —
                   ce texte est lu par vos clients.
     photos      : la liste des photos. La PREMIÈRE sert de vignette
                   dans la galerie et d'image d'ouverture.
     grand       : true = vignette sur deux colonnes dans la galerie
   ========================================================================= */

export const chantiers = [
  {
    id: "sainte-genevieve-des-bois",
    commune: "Sainte-Geneviève-des-Bois",
    prestation: "Ravalement de façade",
    annee: "2026",
    duree: "",
    motsCles: ["Ravalement", "Maison individuelle", "Enduit de finition", "Pignon compris"],
    description: "Ravalement complet des façades d'une maison individuelle, pignon compris. Nettoyage, préparation du support puis application de l'enduit de finition. Encadrements et sous-toiture repris dans la même intervention.",
    photos: ["assets/ph-proj-4.jpg", "assets/ph-about.jpg", "assets/ph-detail-arete.jpg", "assets/ph-cta.jpg"],
    grand: true
  },
  {
    id: "saint-michel-sur-orge-extension",
    commune: "Saint-Michel-sur-Orge",
    prestation: "Ravalement de façade",
    annee: "2025",
    duree: "",
    motsCles: ["Ravalement", "Sous-enduit", "Enduit teinté", "Avant / après"],
    description: "Reprise des façades d'une extension : sous-enduit puis enduit de finition teinté. Le chantier a été mené du décroûtage jusqu'aux finitions par nos équipes.",
    photos: ["assets/chantier-enduit-ocre.jpeg", "assets/ph-ba2-avant.jpg", "assets/ph-ba2-apres.jpg", "assets/ph-svc-nettoyage.jpg"],
    grand: false
  },
  {
    id: "saint-michel-sur-orge-maison",
    commune: "Saint-Michel-sur-Orge",
    prestation: "Ravalement de façade",
    annee: "2025",
    duree: "",
    motsCles: ["Ravalement", "Façade en pierre", "Peinture des volets", "Avant / après"],
    description: "Façade en pierre entièrement reprise, avec traitement du support avant mise en peinture. Les volets ont été repeints pour accompagner la nouvelle teinte de la façade.",
    photos: ["assets/ph-ba1-apres.jpg", "assets/ph-ba1-avant.jpg", "assets/ph-svc-peinture.jpg"],
    grand: false
  },
  {
    id: "savigny-sur-orge",
    commune: "Savigny-sur-Orge",
    prestation: "Ravalement de façade",
    annee: "2024",
    duree: "",
    motsCles: ["Ravalement", "Enduit clair", "Échafaudage complet", "Encadrements"],
    description: "Ravalement des façades sur échafaudage complet. Préparation du support, reprise des encadrements puis enduit de finition clair sur l'ensemble du bâtiment.",
    photos: ["assets/ph-proj-1.jpg"],
    grand: true
  }
];
