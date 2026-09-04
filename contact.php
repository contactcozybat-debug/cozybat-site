<?php
/* =========================================================================
   COZYBAT — réception des demandes de devis
   Reçoit le formulaire de index.html et envoie la demande par email.

   À RÉGLER : rien, en principe. Le destinataire est ci-dessous, l'adresse
   d'expédition est déduite du domaine du site. Ne modifiez EXPEDITEUR que
   si vous voulez forcer une adresse précise.

   Si un email n'arrive pas, la demande est écrite dans le fichier
   demandes-non-envoyees.log, à côté de ce script. Rien n'est jamais perdu.
   ========================================================================= */

const DESTINATAIRE = 'contact@cozybat.fr';
const EXPEDITEUR   = '';  // vide = noreply@<domaine du site>
const JOURNAL      = __DIR__ . '/demandes-non-envoyees.log';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function repondre($code, $data) {
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    repondre(405, array('ok' => false, 'erreur' => 'Méthode non autorisée.'));
}

$brut = file_get_contents('php://input');
if ($brut === false || strlen($brut) > 20000) {
    repondre(400, array('ok' => false, 'erreur' => 'Requête invalide.'));
}
$d = json_decode($brut, true);
if (!is_array($d)) {
    repondre(400, array('ok' => false, 'erreur' => 'Requête invalide.'));
}

/* Pot de miel : ce champ est masqué à l'écran. Seul un robot le remplit.
   On répond « ok » pour ne pas lui signaler qu'il a été repéré. */
if (trim((string)($d['website'] ?? '')) !== '') {
    repondre(200, array('ok' => true));
}

function texte($v, $max = 500) {
    $v = is_scalar($v) ? (string)$v : '';
    $v = str_replace(array("\r", "\0"), '', $v);
    $v = trim($v);
    return function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
}

$nom     = texte($d['nom'] ?? '', 120);
$tel     = texte($d['tel'] ?? '', 40);
$mail    = texte($d['mail'] ?? '', 160);
$ville   = texte($d['ville'] ?? '', 120);
$cp      = texte($d['cp'] ?? '', 10);
$surface = texte($d['surface'] ?? '', 40);
$msg     = texte($d['msg'] ?? '', 4000);
$rgpd    = !empty($d['rgpd']);

/* Mêmes règles que la validation affichée au visiteur, revérifiées ici :
   un robot peut poster directement sur ce script en contournant la page. */
$chiffres = preg_replace('/[^0-9+]/', '', $tel);
$erreurs = array();
if ($nom === '')                     $erreurs[] = 'nom';
if ($ville === '')                   $erreurs[] = 'ville';
if (strlen($chiffres) < 10)          $erreurs[] = 'tel';
if ($mail !== '' && !filter_var($mail, FILTER_VALIDATE_EMAIL)) $erreurs[] = 'mail';
if (!$rgpd)                          $erreurs[] = 'rgpd';

if ($erreurs) {
    repondre(422, array('ok' => false, 'erreur' => 'Champs invalides.', 'champs' => $erreurs));
}

$BIENS = array(
    'maison'   => 'Maison individuelle',
    'immeuble' => 'Immeuble / copropriété',
    'local'    => 'Local professionnel',
    'autre'    => 'Autre',
);
$DELAIS = array(
    'urgent' => 'Dès que possible',
    '3mois'  => 'Dans les 3 mois',
    '6mois'  => 'Dans les 6 mois',
    'etude'  => 'Je me renseigne',
);
$PRESTATIONS = array(
    'ravalement' => 'Ravalement de façade',
    'ite'        => "Isolation par l'extérieur",
    'peinture'   => 'Peinture extérieure',
    'nettoyage'  => 'Nettoyage & traitement',
);

$bien  = $BIENS[texte($d['bien'] ?? '', 20)] ?? 'Non précisé';
$delai = $DELAIS[texte($d['delai'] ?? '', 20)] ?? 'Non précisé';

$choisies = array();
foreach ((array)($d['prestations'] ?? array()) as $k) {
    $k = texte($k, 20);
    if (isset($PRESTATIONS[$k])) $choisies[] = $PRESTATIONS[$k];
}
$prestations = $choisies ? implode(', ', $choisies) : 'Non précisé';

$localite = $cp !== '' ? $ville . ' (' . $cp . ')' : $ville;
$horodate = date('d/m/Y à H:i');

$corps  = "NOUVELLE DEMANDE DE DEVIS\n";
$corps .= "Reçue le " . $horodate . "\n";
$corps .= str_repeat('=', 52) . "\n\n";
$corps .= "CONTACT\n";
$corps .= "  Nom        : " . $nom . "\n";
$corps .= "  Téléphone  : " . $tel . "\n";
$corps .= "  Email      : " . ($mail !== '' ? $mail : 'non communiqué') . "\n\n";
$corps .= "CHANTIER\n";
$corps .= "  Commune    : " . $localite . "\n";
$corps .= "  Type       : " . $bien . "\n";
$corps .= "  Surface    : " . ($surface !== '' ? $surface . ' m²' : 'non précisée') . "\n";
$corps .= "  Délai      : " . $delai . "\n";
$corps .= "  Prestations: " . $prestations . "\n\n";
if ($msg !== '') {
    $corps .= "MESSAGE\n";
    $corps .= "  " . str_replace("\n", "\n  ", $msg) . "\n\n";
}
$corps .= str_repeat('-', 52) . "\n";
$corps .= "Rappeler sous 48 h ouvrées (délai annoncé sur le site).\n";

/* L'expéditeur doit appartenir au domaine du site, sinon Gmail classe
   le message en indésirable ou le rejette. */
$hote = isset($_SERVER['HTTP_HOST']) ? strtolower($_SERVER['HTTP_HOST']) : '';
$hote = preg_replace('/[^a-z0-9.\-]/', '', $hote);
$hote = preg_replace('/^www\./', '', $hote);
$expediteur = EXPEDITEUR !== '' ? EXPEDITEUR : 'noreply@' . ($hote !== '' ? $hote : 'localhost');

$sujet = 'Demande de devis — ' . $nom . ' (' . $localite . ')';
$sujet = '=?UTF-8?B?' . base64_encode($sujet) . '?=';

$entetes  = "MIME-Version: 1.0\r\n";
$entetes .= "Content-Type: text/plain; charset=UTF-8\r\n";
$entetes .= "Content-Transfer-Encoding: 8bit\r\n";
$entetes .= 'From: =?UTF-8?B?' . base64_encode('Site Cozybat') . "?= <" . $expediteur . ">\r\n";
if ($mail !== '') {
    $entetes .= 'Reply-To: ' . $mail . "\r\n";
}

$envoye = @mail(DESTINATAIRE, $sujet, $corps, $entetes, '-f' . $expediteur);

if (!$envoye) {
    /* Filet de sécurité : l'email a échoué, on garde la demande sur le
       serveur plutôt que de la perdre. Consultable via le gestionnaire
       de fichiers Hostinger. */
    @file_put_contents(
        JOURNAL,
        "\n===== " . $horodate . " =====\n" . $corps,
        FILE_APPEND | LOCK_EX
    );
    repondre(500, array('ok' => false, 'erreur' => "L'envoi a échoué."));
}

repondre(200, array('ok' => true));
