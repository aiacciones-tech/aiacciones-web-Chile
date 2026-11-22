#!/bin/bash
# bash encolar_cal.sh <carpeta de la semana>: encola el Short «Calendario semanal de resultados» en cola-es/calendario-<semana>-short/
# de la rama youtube-cola. Después: youtube-espana.yml lo sube a YouTube (público al momento: encola entre las 18:00 y las 20:00 de Madrid),
# buffer.yml lo publica en X, LinkedIn (vídeo), TikTok, Instagram (Reel) y Threads (si hay canal) y telegram-espana.yml en Telegram.
# Usa un clon parcial y ligero de youtube-cola (la rama completa pesa varios GB).
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/calendario.json'))['semana'])"); S=${SCRATCH:-/tmp/es-scratch}/cola-cal; mkdir -p $(dirname $S)
if [ ! -d $S/.git ]; then
  git clone -q --depth 1 --filter=blob:none --no-checkout -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S
  cd $S; git sparse-checkout set --no-cone '/cola-es/*/resultado.json' '/cola-es/calendario-*/' '/cola-es/*/telegram.json'; git checkout -q youtube-cola
else cd $S; git pull -q --depth 1 --rebase origin youtube-cola 2>/dev/null || true; fi
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-es/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'])
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube España en 24 h:',n); assert n<=9, 'límite de YouTube (~10/24 h): espera antes de encolar'
PY
CS=cola-es/calendario-$F-short
[ -f $CS/resultado.json ] && { echo "ya subido: $CS"; exit 1; }
mkdir -p $CS
cp $B/short-calendario-$F.mp4 $CS/video.mp4; cp $B/meta-short.json $CS/meta.json; cp $B/portada.png $CS/miniatura.png
for r in x linkedin tiktok instagram threads telegram; do cp $B/post-$r.txt $CS/post-$r.txt; done
git add $CS; git -c user.name=aiacciones-bot -c user.email=aiacciones-bot@users.noreply.github.com commit -qm "Cola España: calendario semanal de resultados $F (Short y posts)"
for i in 1 2 3 4 5; do git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); git pull -q --depth 1 --rebase origin youtube-cola 2>/dev/null || true; done
git ls-remote origin youtube-cola | grep -q "$(git rev-parse HEAD)" || { echo "no se pudo subir a youtube-cola"; exit 1; }
echo "encolado $CS; esperando la subida a YouTube..."
for i in $(seq 80); do git pull -q --depth 1 --rebase origin youtube-cola 2>/dev/null || true; [ -f $CS/resultado.json ] && [ -f $CS/buffer.json ] && break; sleep 15; done
SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "calendario $F: Short https://youtube.com/shorts/$SH" | tee -a $B/ids.txt
ls $CS
