<?php
// Formulario de contacto de AI ACCIONES CHILE.
// Envía el mensaje con el correo del propio hosting (función mail de PHP), sin servicios externos.
$DESTINO = 'contacto@aiacciones.cl';
$REMITENTE = 'contacto@aiacciones.cl'; // debe ser una casilla del dominio para que el hosting lo acepte

$ajax = isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false;
function responder($ok, $msg, $ajax) {
  if ($ajax) {
    header('Content-Type: application/json; charset=utf-8');
    http_response_code($ok ? 200 : 400);
    echo json_encode(['ok' => $ok, 'message' => $msg], JSON_UNESCAPED_UNICODE);
  } else {
    header('Location: contacto/index.html#' . ($ok ? 'enviado' : 'error'));
  }
  exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') responder(false, 'Método no permitido.', $ajax);

$campo = function ($k, $max) { return trim(mb_substr((string)($_POST[$k] ?? ''), 0, $max)); };
$nombre  = $campo('nombre', 100);
$email   = $campo('email', 150);
$asunto  = $campo('asunto', 100);
$mensaje = $campo('mensaje', 5000);

// Anti-spam: campo trampa oculto y tiempo mínimo para llenar el formulario (_t = ms en la página).
if ($campo('_honey', 100) !== '') responder(true, 'ok', $ajax);
$t = (int)($_POST['_t'] ?? 0);
if (isset($_POST['_t']) && $_POST['_t'] !== '' && $t < 2000) responder(true, 'ok', $ajax);

if ($nombre === '' || $mensaje === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  responder(false, 'Revisa tu nombre, tu correo y el mensaje.', $ajax);
}
// Evita inyección de cabeceras.
$limpio = function ($s) { return str_replace(["\r", "\n", "%0a", "%0d"], ' ', $s); };
$nombre = $limpio($nombre); $email = $limpio($email); $asunto = $limpio($asunto);

$titulo = 'Web AI ACCIONES CHILE: ' . ($asunto !== '' ? $asunto : 'Nuevo mensaje');
$cuerpo = "Nombre: $nombre\nCorreo: $email\nAsunto: $asunto\n\n$mensaje\n\n--\nEnviado desde el formulario de contacto de la web.";
$cabeceras = [
  'From: AI ACCIONES CHILE <' . $REMITENTE . '>',
  'Reply-To: ' . $email,
  'Content-Type: text/plain; charset=UTF-8',
  'MIME-Version: 1.0',
];
$ok = mail($DESTINO, '=?UTF-8?B?' . base64_encode($titulo) . '?=', $cuerpo, implode("\r\n", $cabeceras), '-f' . $REMITENTE);
if (!$ok) $ok = mail($DESTINO, '=?UTF-8?B?' . base64_encode($titulo) . '?=', $cuerpo, implode("\r\n", $cabeceras));
responder($ok, $ok ? 'ok' : 'El servidor no pudo enviar el correo.', $ajax);
