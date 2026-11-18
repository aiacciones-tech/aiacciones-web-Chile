#!/bin/bash
# Pide a Azure (es-CL-LorenzoNeural) las locuciones de un video y espera sus wav.
# uso: bash voz-cl/pedir.sh <id> <dir_destino> <fuente>...
#   <id>: único por video, p. ej. falabella-3T26 o diario-2026-11-18 (letras, números y guiones).
#   <fuente>: narracion*.py, video.json, short*.json o .txt (ver voz_cl.py).
# Sube voz-cl/pedidos/<id>.json a la rama voz-cl-pedido-<id> (desde main); voz-chile.yml sintetiza, guarda los wav en la rama voz-cl
# (carpeta <id>/) y borra la rama del pedido. Luego copia los wav a <dir_destino>. Para renderizar con esa voz:
#   PYTHONPATH=<repo>/voz-cl/shim VOZ_DIR=<dir_destino> python3 make_video....py   (Piper si falta algún wav)
# Sale con 1 si en 15 min no hay voz (render con Piper, sin VOZ_DIR) o con 2 si Azure dejó locuciones sin hacer.
set -e
ID="$1"; DEST="$2"; shift 2
[[ "$ID" =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "id inválido: $ID"; exit 1; }
R="$(cd "$(dirname "$0")/.." && pwd)"
TMP=$(mktemp -d)
python3 "$R/voz-cl/voz_cl.py" pedido "$ID" "$@" > "$TMP/$ID.json"
python3 -c "import json,sys;p=json.load(open(sys.argv[1]));print('pedido',p['id'],len(p['textos']),'locuciones',p['caracteres'],'caracteres')" "$TMP/$ID.json"
SHA=$(sha1sum "$TMP/$ID.json" | cut -c1-16)
git -C "$R" fetch -q --depth 1 origin main
git -C "$R" worktree add -q --detach "$TMP/w" FETCH_HEAD
mkdir -p "$TMP/w/voz-cl/pedidos" && cp "$TMP/$ID.json" "$TMP/w/voz-cl/pedidos/"
git -C "$TMP/w" add voz-cl/pedidos
git -C "$TMP/w" -c user.name="aiacciones-bot" -c user.email="aiacciones-bot@users.noreply.github.com" commit -qm "Pedido de voz Azure $ID"
for i in 1 2 3 4; do git -C "$TMP/w" push -qf origin "HEAD:refs/heads/voz-cl-pedido-$ID" && break; sleep $((i*5)); done
git -C "$R" worktree remove --force "$TMP/w"
echo "esperando la voz (voz-chile.yml)..."
for i in $(seq 1 60); do
  sleep 15
  git -C "$R" fetch -q --depth 1 origin voz-cl 2>/dev/null || continue
  if [ "$(git -C "$R" show "FETCH_HEAD:$ID/pedido.sha" 2>/dev/null)" = "$SHA" ]; then
    rm -rf "$DEST"; mkdir -p "$DEST"
    git -C "$R" archive FETCH_HEAD "$ID" | tar -x -C "$TMP" && cp -r "$TMP/$ID/." "$DEST/"
    cat "$DEST/manifest.json"; echo
    python3 "$R/voz-cl/voz_cl.py" faltan "$DEST" "$@" | tail -1
    python3 -c "import json,sys;sys.exit(2 if json.load(open(sys.argv[1]))['fallos'] else 0)" "$DEST/manifest.json"
    exit $?
  fi
done
echo "Sin voz de Azure en 15 min: renderiza con Piper (sin VOZ_DIR) y dilo en el mensaje."
exit 1
