<?php
// Publica aiacciones.es sin FTP (Daniel, 23-oct-2026). Descarga de GitHub la rama web-es-publicada
// (copia de espana/web/ que deja .github/workflows/deploy-espana.yml) y copia sus archivos aquí.
// No recibe datos: siempre baja la misma URL fija del repositorio público. Solo escribe tipos de archivo
// estáticos (nunca .php ni .htaccess) y no borra nada. ?check=1 solo comprueba que el hosting lo permite.
header('Content-Type: text/plain; charset=utf-8');
header('Cache-Control: no-store');

const ZIP_URL = 'https://codeload.github.com/aiacciones-tech/aiacciones-web-Chile/zip/refs/heads/web-es-publicada';
const ESPERA = 20; // segundos mínimos entre dos actualizaciones
const TIPOS = ['html', 'css', 'js', 'json', 'xml', 'txt', 'png', 'jpg', 'jpeg', 'webp', 'gif', 'svg', 'ico', 'webmanifest', 'woff', 'woff2'];

$dir = __DIR__;
$faltan = [];
if (!class_exists('ZipArchive')) $faltan[] = 'extensión zip';
if (!function_exists('curl_init')) $faltan[] = 'curl';
if (!is_writable($dir)) $faltan[] = 'permiso de escritura';

if (isset($_GET['check'])) {
    echo $faltan ? 'FALTA: ' . implode(', ', $faltan) . "\n" : "LISTO\n";
    exit;
}
if ($faltan) { http_response_code(500); exit('FALTA: ' . implode(', ', $faltan) . "\n"); }

$lock = $dir . '/.actualizar.lock';
if (is_file($lock) && time() - filemtime($lock) < ESPERA) { http_response_code(429); exit("ESPERA\n"); }
touch($lock);

$tmp = tempnam(sys_get_temp_dir(), 'aies');
try {
    $f = fopen($tmp, 'wb');
    $c = curl_init(ZIP_URL);
    curl_setopt_array($c, [CURLOPT_FILE => $f, CURLOPT_FOLLOWLOCATION => true, CURLOPT_MAXREDIRS => 3,
        CURLOPT_PROTOCOLS => CURLPROTO_HTTPS, CURLOPT_REDIR_PROTOCOLS => CURLPROTO_HTTPS, CURLOPT_TIMEOUT => 90,
        CURLOPT_FAILONERROR => true, CURLOPT_SSL_VERIFYPEER => true, CURLOPT_USERAGENT => 'aiacciones-actualizar']);
    $ok = curl_exec($c);
    $err = curl_error($c);
    curl_close($c);
    fclose($f);
    if (!$ok) throw new Exception('descarga: ' . $err);

    $zip = new ZipArchive();
    if ($zip->open($tmp) !== true) throw new Exception('zip no válido');
    $n = 0;
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $nombre = $zip->getNameIndex($i);
        $rel = substr($nombre, strpos($nombre, '/') + 1); // quita la carpeta raíz del zip
        if ($rel === '' || substr($rel, -1) === '/') continue;
        if (!preg_match('#^[A-Za-z0-9._/-]+$#', $rel) || strpos($rel, '..') !== false) continue;
        if (!in_array(strtolower(pathinfo($rel, PATHINFO_EXTENSION)), TIPOS, true)) continue;
        $destino = $dir . '/' . $rel;
        if (!is_dir(dirname($destino)) && !mkdir(dirname($destino), 0755, true)) throw new Exception('no se pudo crear ' . dirname($rel));
        $parcial = $destino . '.parcial';
        if (file_put_contents($parcial, $zip->getFromIndex($i)) === false || !rename($parcial, $destino)) {
            throw new Exception('no se pudo escribir ' . $rel);
        }
        $n++;
    }
    $zip->close();
    $version = is_file($dir . '/version.txt') ? trim(file_get_contents($dir . '/version.txt')) : '?';
    echo "OK $version $n\n";
} catch (Exception $e) {
    http_response_code(500);
    echo 'ERROR ' . $e->getMessage() . "\n";
} finally {
    @unlink($tmp);
}
