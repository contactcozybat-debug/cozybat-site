<?php
/**
 * Cozybat — réception des demandes de devis du site.
 * Envoie un e-mail récapitulatif (avec les photos jointes) puis redirige vers /merci.
 * Hébergement : Hostinger (PHP 8). Aucune base de données nécessaire.
 */

// ---------------------------------------------------------------- réglages
date_default_timezone_set('Europe/Paris');
const DESTINATAIRE = 'contact.cozybat@gmail.com'; // boîte qui reçoit les demandes
// Expéditeur technique : une adresse du domaine du site (pas besoin de créer la boîte).
// Gmail refuse ou classe en spam les messages envoyés par le serveur avec un expéditeur @gmail.com.
const EXPEDITEUR   = 'site@cozybat.fr';

// Envoi le plus fiable : passer par Gmail lui-même (SMTP).
// Mettre ici un « mot de passe d'application » Google du compte contact.cozybat@gmail.com
// (Compte Google > Sécurité > Validation en 2 étapes > Mots de passe des applications).
// Laisser vide pour utiliser l'envoi classique du serveur.
const GMAIL_MOT_DE_PASSE_APPLI = '';
const SMTP_HOTE = 'ssl://smtp.gmail.com';
const SMTP_PORT = 465;
const MAX_PHOTOS   = 5;
const MAX_PHOTO_MO = 8;                          // par photo
const MAX_TOTAL_MO = 20;                         // toutes photos confondues

// ---------------------------------------------------------------- utilitaires
function retour(string $page): void {
    header('Location: ' . $page, true, 303);
    exit;
}
function champ(string $cle, int $max = 200): string {
    $v = isset($_POST[$cle]) && is_string($_POST[$cle]) ? $_POST[$cle] : '';
    $v = trim(strip_tags($v));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
}
function ligne(string $v): string {            // valeur sur une seule ligne (anti-injection d'en-têtes)
    return trim(preg_replace('/[\r\n]+/', ' ', $v));
}

function smtp_envoi(string $a, string $sujet, string $corps, array $entetes): bool {
    $f = @stream_socket_client(SMTP_HOTE . ':' . SMTP_PORT, $no, $err, 15);
    if (!$f) return false;
    stream_set_timeout($f, 15);
    $lire = function () use ($f): string { $r = ''; while (($l = fgets($f, 515)) !== false) { $r .= $l; if (isset($l[3]) && $l[3] === ' ') break; } return $r; };
    $cmd = function (string $c, string $attendu) use ($f, $lire): bool { if ($c !== '') fwrite($f, $c . "\r\n"); return strncmp($lire(), $attendu, 3) === 0; };
    $ok = $cmd('', '220') && $cmd('EHLO cozybat.fr', '250') && $cmd('AUTH LOGIN', '334')
       && $cmd(base64_encode(DESTINATAIRE), '334') && $cmd(base64_encode(str_replace(' ', '', GMAIL_MOT_DE_PASSE_APPLI)), '235')
       && $cmd('MAIL FROM:<' . DESTINATAIRE . '>', '250') && $cmd('RCPT TO:<' . $a . '>', '250') && $cmd('DATA', '354');
    if ($ok) {
        $msg = implode("\r\n", array_merge(['To: ' . $a, 'Subject: ' . $sujet, 'Date: ' . date('r'), 'Message-ID: <' . bin2hex(random_bytes(8)) . '@cozybat.fr>'], $entetes)) . "\r\n\r\n" . $corps;
        $msg = preg_replace('/^\./m', '..', $msg);
        $ok = $cmd($msg . "\r\n.", '250');
    }
    fwrite($f, "QUIT\r\n"); fclose($f);
    return $ok;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') retour('/devis/');

// ---------------------------------------------------------------- anti-spam
if (!empty($_POST['site_web'])) retour('/merci/');                 // champ piège rempli par les robots
$ts = (int) ($_POST['ts'] ?? 0);
if ($ts > 0 && (microtime(true) * 1000 - $ts) < 3000) retour('/merci/'); // envoyé en moins de 3 s

// ---------------------------------------------------------------- données
$listes = [
    'projet'  => ['ite' => 'Isolation par l’extérieur', 'd3' => 'Ravalement D3 armé', 'autre' => 'Autre / ne sait pas'],
    'maison'  => ['individuelle' => 'Maison individuelle', 'mitoyenne' => 'Maison mitoyenne', 'autre' => 'Autre bâtiment'],
    'surface' => ['<80' => 'Moins de 80 m²', '80-150' => '80 à 150 m²', '>150' => 'Plus de 150 m²', 'nsp' => 'Ne sait pas'],
    'creneau' => ['matin' => 'Matin', 'apres-midi' => 'Après-midi', 'apres-18h' => 'Après 18 h'],
];
$choix = [];
foreach ($listes as $cle => $options) {
    $v = champ($cle, 20);
    $choix[$cle] = $options[$v] ?? 'Non précisé';
}
$nom     = ligne(champ('nom', 80));
$tel     = ligne(champ('telephone', 30));
$ville   = ligne(champ('ville', 60));
$email   = ligne(champ('email', 120));
$message = champ('message', 2000);
$consent = ($_POST['consentement'] ?? '') === 'oui';

if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) $email = '';
if ($nom === '' || $tel === '' || !$consent || !preg_match('/[0-9]{6,}/', preg_replace('/\D/', '', $tel) ?: '')) {
    retour('/devis/?erreur=1#contact');
}

// ---------------------------------------------------------------- photos jointes
$pieces = [];
$total = 0;
if (!empty($_FILES['photos']) && is_array($_FILES['photos']['name'])) {
    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $autorises = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp', 'image/heic' => 'heic', 'image/heif' => 'heic'];
    $n = min(count($_FILES['photos']['name']), MAX_PHOTOS);
    for ($i = 0; $i < $n; $i++) {
        if (($_FILES['photos']['error'][$i] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) continue;
        $tmp  = $_FILES['photos']['tmp_name'][$i];
        $size = (int) $_FILES['photos']['size'][$i];
        if (!is_uploaded_file($tmp) || $size <= 0 || $size > MAX_PHOTO_MO * 1048576) continue;
        if ($total + $size > MAX_TOTAL_MO * 1048576) break;
        $mime = $finfo->file($tmp) ?: '';
        if (!isset($autorises[$mime])) continue;
        $pieces[] = ['nom' => 'photo-' . ($i + 1) . '.' . $autorises[$mime], 'mime' => $mime, 'data' => file_get_contents($tmp)];
        $total += $size;
    }
}

// ---------------------------------------------------------------- e-mail
$date  = date('d/m/Y à H:i');
$sujet = 'Demande de devis – ' . $choix['projet'] . ' – ' . ($ville !== '' ? $ville : $nom);
$texte = "Nouvelle demande de devis reçue le $date via cozybat.fr\n\n"
       . "Projet : {$choix['projet']}\n"
       . "Bâtiment : {$choix['maison']}\n"
       . "Surface de façade : {$choix['surface']}\n\n"
       . "Nom : $nom\n"
       . "Téléphone : $tel\n"
       . "E-mail : " . ($email ?: 'non renseigné') . "\n"
       . "Ville : " . ($ville ?: 'non renseignée') . "\n"
       . "Rappel souhaité : {$choix['creneau']}\n\n"
       . "Message :\n" . ($message !== '' ? $message : '(aucun)') . "\n\n"
       . "Photos jointes : " . count($pieces) . "\n"
       . "Consentement au recontact : oui\n";

$frontiere = 'cz_' . bin2hex(random_bytes(12));
$smtp = GMAIL_MOT_DE_PASSE_APPLI !== '';
$entetes   = [
    'MIME-Version: 1.0',
    'From: Site Cozybat <' . ($smtp ? DESTINATAIRE : EXPEDITEUR) . '>',
    'X-Mailer: Cozybat',
    'Content-Type: multipart/mixed; boundary="' . $frontiere . '"',
];
if ($email !== '') $entetes[] = 'Reply-To: ' . mb_encode_mimeheader($nom, 'UTF-8') . ' <' . $email . '>';

$corps  = "--$frontiere\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n";
$corps .= chunk_split(base64_encode($texte)) . "\r\n";
foreach ($pieces as $p) {
    $corps .= "--$frontiere\r\nContent-Type: {$p['mime']}; name=\"{$p['nom']}\"\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"{$p['nom']}\"\r\n\r\n";
    $corps .= chunk_split(base64_encode($p['data'])) . "\r\n";
}
$corps .= "--$frontiere--\r\n";

$sujet_enc = mb_encode_mimeheader($sujet, 'UTF-8');
$ok = $smtp ? smtp_envoi(DESTINATAIRE, $sujet_enc, $corps, $entetes) : false;
if (!$ok) {
    $entetes[1] = 'From: Site Cozybat <' . EXPEDITEUR . '>';
    $ok = mail(DESTINATAIRE, $sujet_enc, $corps, implode("\r\n", $entetes), '-f' . EXPEDITEUR);
}

// Copie de chaque demande sur le serveur (même si l'e-mail est parti), hors du dossier public si possible :
// dossier « demandes-devis » à côté de public_html, visible dans le Gestionnaire de fichiers Hostinger.
{
    $dossier = dirname(__DIR__) . '/demandes-devis';
    if (!is_dir($dossier)) @mkdir($dossier, 0700, true);
    if (!is_dir($dossier) || !is_writable($dossier)) {
        $dossier = __DIR__ . '/demandes-devis';
        if (!is_dir($dossier)) @mkdir($dossier, 0700, true);
        @file_put_contents($dossier . '/.htaccess', "Require all denied\n");
    }
    @file_put_contents($dossier . '/' . date('Ymd-His') . '-' . bin2hex(random_bytes(3)) . '.txt', $texte . "\nE-mail envoyé : " . ($ok ? 'oui' : 'NON') . ($smtp ? ' (Gmail)' : ' (serveur)') . "\n");
}

retour('/merci/');
