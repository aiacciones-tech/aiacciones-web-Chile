<?php
// Sincroniza la web de aiacciones.cl con la carpeta web/ de la rama main en GitHub.
// Complementa al FTP (.github/workflows/deploy.yml): si el FTP falla, este archivo trae lo que falte.
//
// Cómo se usa:
// - Webhook de GitHub (push a main): GitHub lo llama y se copian solo los archivos que cambiaron.
// - A mano en el navegador: https://www.aiacciones.cl/sincronizar.php?clave=TU_CLAVE
//   (agrega &simular=1 para ver qué cambiaría sin escribir nada).
// La clave se crea sola la primera vez que se abre la página y queda fuera de public_html,
// en ../.sincronizar-clave. Para cambiarla, borra ese archivo y vuelve a abrir la página.
// Compara cada archivo con el de GitHub (mismo hash que git) y no borra nada, igual que el FTP.

$REPO = 'aiacciones-tech/aiacciones-web-Chile';
$RAMA = 'main';
$CARPETA = 'web/';                 // carpeta del repo que se publica
$DESTINO = __DIR__;                // public_html
$PRIVADO = dirname(__DIR__);       // fuera de la web: clave, registro y candado
$CLAVE_ARCHIVO = $PRIVADO . '/.sincronizar-clave';
$REGISTRO = $PRIVADO . '/sincronizar-registro.txt';

header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex');
@set_time_limit(300);

function fin($codigo, $texto) {
  http_response_code($codigo);
  echo $texto . "\n";
  exit;
}

function anotar($linea) {
  global $REGISTRO;
  $previas = is_file($REGISTRO) ? array_slice(file($REGISTRO, FILE_IGNORE_NEW_LINES), -300) : [];
  $previas[] = gmdate('Y-m-d H:i:s') . ' UTC  ' . $linea;
  @file_put_contents($REGISTRO, implode("\n", $previas) . "\n", LOCK_EX);
}

function descargar($url, $json = false) {
  $cab = ['User-Agent: aiacciones-sincronizar'];
  if ($json) $cab[] = 'Accept: application/vnd.github+json';
  if (function_exists('curl_init')) {
    $c = curl_init($url);
    curl_setopt_array($c, [CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true,
      CURLOPT_TIMEOUT => 60, CURLOPT_HTTPHEADER => $cab]);
    $cuerpo = curl_exec($c);
    $estado = curl_getinfo($c, CURLINFO_HTTP_CODE);
    curl_close($c);
  } else {
    $ctx = stream_context_create(['http' => ['header' => implode("\r\n", $cab), 'timeout' => 60, 'ignore_errors' => true]]);
    $cuerpo = @file_get_contents($url, false, $ctx);
    $estado = isset($http_response_header[0]) && preg_match('/\s(\d{3})\s/', $http_response_header[0], $m) ? (int)$m[1] : 0;
  }
  if ($cuerpo === false || $estado !== 200) return null;
  return $json ? json_decode($cuerpo, true) : $cuerpo;
}

// --- Clave ---
if (!is_file($CLAVE_ARCHIVO)) {
  if (!is_writable($PRIVADO)) fin(500, "No puedo escribir en $PRIVADO para guardar la clave.");
  $nueva = bin2hex(random_bytes(20));
  file_put_contents($CLAVE_ARCHIVO, $nueva);
  @chmod($CLAVE_ARCHIVO, 0600);
  anotar('Clave nueva creada.');
  fin(200, "Clave creada. Guárdala, no se vuelve a mostrar:\n\n$nueva\n\n"
    . "Úsala como \"Secret\" del webhook de GitHub y en ?clave= para sincronizar a mano.\n"
    . "Para cambiarla, borra $CLAVE_ARCHIVO y abre esta página otra vez.");
}
$CLAVE = trim(file_get_contents($CLAVE_ARCHIVO));

// --- Quién llama: webhook de GitHub (firma HMAC) o a mano (?clave=) ---
$cuerpo = file_get_contents('php://input');
$firma = $_SERVER['HTTP_X_HUB_SIGNATURE_256'] ?? '';
$evento = $_SERVER['HTTP_X_GITHUB_EVENT'] ?? '';
$webhook = $firma !== '';
if ($webhook) {
  if (!hash_equals('sha256=' . hash_hmac('sha256', $cuerpo, $CLAVE), $firma)) fin(403, 'Firma inválida.');
  if ($evento === 'ping') fin(200, 'pong');
  $datos = json_decode($cuerpo, true);
  if ($evento !== 'push' || ($datos['ref'] ?? '') !== "refs/heads/$RAMA") fin(200, 'Nada que hacer (no es un push a main).');
  $commit = $datos['after'] ?? $RAMA;
} else {
  if (!hash_equals($CLAVE, (string)($_GET['clave'] ?? ''))) fin(403, 'Clave incorrecta.');
  $commit = $RAMA;
}
$simular = !$webhook && !empty($_GET['simular']);

// Un solo proceso a la vez.
$candado = fopen($PRIVADO . '/.sincronizar.lock', 'c');
if (!$candado || !flock($candado, LOCK_EX | LOCK_NB)) fin(409, 'Ya hay una sincronización en curso.');

// GitHub corta el webhook a los 10 s: se responde altiro y se sigue trabajando.
if ($webhook) {
  ignore_user_abort(true);
  echo "Recibido, sincronizando $commit\n";
  if (function_exists('fastcgi_finish_request')) fastcgi_finish_request();
  else { header('Connection: close'); header('Content-Length: ' . ob_get_length()); @ob_end_flush(); flush(); }
}

// --- Lista de archivos de web/ en GitHub (una sola llamada a la API) ---
$arbol = descargar("https://api.github.com/repos/$REPO/git/trees/" . rawurlencode($commit) . '?recursive=1', true);
if (!$arbol || empty($arbol['tree'])) { anotar("ERROR: no pude leer el árbol de $commit en GitHub."); fin(502, 'No pude leer la lista de archivos de GitHub.'); }
if (!empty($arbol['truncated'])) anotar('AVISO: GitHub truncó la lista de archivos.');
$sha_commit = $arbol['sha'];

$cambios = [];
foreach ($arbol['tree'] as $item) {
  if ($item['type'] !== 'blob' || strpos($item['path'], $CARPETA) !== 0) continue;
  $rel = substr($item['path'], strlen($CARPETA));
  if ($rel === '' || strpos($rel, '..') !== false || $rel[0] === '/') continue;
  $local = $DESTINO . '/' . $rel;
  // Mismo hash que usa git para un archivo: sha1("blob <tamaño>\0<contenido>").
  $igual = is_file($local) && sha1('blob ' . filesize($local) . "\0" . file_get_contents($local)) === $item['sha'];
  if (!$igual) $cambios[] = $rel;
}

if ($simular) fin(200, count($cambios) ? "Cambiarían " . count($cambios) . " archivos:\n" . implode("\n", $cambios) : 'Todo al día, no cambiaría nada.');

$ok = 0; $fallas = [];
foreach ($cambios as $rel) {
  $url = "https://raw.githubusercontent.com/$REPO/$sha_commit/$CARPETA" . implode('/', array_map('rawurlencode', explode('/', $rel)));
  $contenido = descargar($url);
  if ($contenido === null) { $fallas[] = $rel; continue; }
  $local = $DESTINO . '/' . $rel;
  if (!is_dir(dirname($local)) && !@mkdir(dirname($local), 0755, true)) { $fallas[] = $rel; continue; }
  // Se escribe en un temporal y se renombra, así nunca queda un archivo a medias.
  $tmp = $local . '.sinc-tmp';
  if (@file_put_contents($tmp, $contenido) === false || !@rename($tmp, $local)) { @unlink($tmp); $fallas[] = $rel; continue; }
  $ok++;
}

$resumen = sprintf('%s %s: %d archivos actualizados%s', $webhook ? 'Webhook' : 'Manual', substr($sha_commit, 0, 7), $ok,
  $fallas ? ', fallaron ' . count($fallas) . ': ' . implode(', ', array_slice($fallas, 0, 20)) : '');
anotar($resumen);
fin($fallas ? 500 : 200, $resumen . ($ok ? "\n" . implode("\n", array_diff($cambios, $fallas)) : ''));
