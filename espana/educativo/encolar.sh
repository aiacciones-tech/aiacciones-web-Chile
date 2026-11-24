#!/bin/bash
# bash encolar.sh <carpeta de la lección>: encola una lección de «Análisis técnico, explicado fácil» (AIAcciones España) y su Short en
# cola-es/curso-<base>[-short]/ de la rama youtube-cola, con el mismo reparto que el vídeo diario (espana/diario/encolar.sh):
# youtube-espana.yml sube a YouTube; buffer.yml publica en X (vídeo largo) y en LinkedIn (Short como vídeo nativo), TikTok e Instagram (Reel);
# telegram-espana.yml lo publica en Telegram. Usa SCRATCH con un clon de youtube-cola ya hecho si lo hay (la rama es enorme).
set -e
ENL=$(cd "$(dirname "$0")/.." && pwd)/enlaces_cola.py
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])"); S=${SCRATCH:-/tmp/es-scratch}; mkdir -p $S
for f in leccion-$BASE.mp4 short-$BASE.mp4 meta-youtube-$BASE.json meta-short-$BASE.json miniatura-$BASE.png \
         post-x-$BASE.txt post-linkedin-$BASE.txt post-tiktok-$BASE.txt post-instagram-$BASE.txt post-telegram-$BASE.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
CANAL='https://www.youtube.com/@AIAccionesEspa%C3%B1a'
grep -q "$CANAL" $B/meta-youtube-$BASE.json && grep -q "$CANAL" $B/meta-short-$BASE.json || { echo "falta el enlace del canal en los metadatos"; exit 1; }
tail -c 200 $B/post-linkedin-$BASE.txt | grep -q "$CANAL" && grep -q "Vídeo elaborado por AIAcciones España" $B/post-linkedin-$BASE.txt || { echo "LinkedIn no cumple la regla (autoría y enlace al canal al final)"; exit 1; }
if [ ! -d $S/cola ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-es)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-es/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if s.tzinfo is None: s=s.replace(tzinfo=dt.timezone.utc)
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube España en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h, compartido con el diario y los resultados): espera antes de encolar'
PY
C=cola-es/curso-$BASE; CS=cola-es/curso-$BASE-short
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C $CS
cp $B/leccion-$BASE.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE.json $C/meta.json; cp $B/miniatura-$BASE.png $C/miniatura.png
cp $B/post-x-$BASE.txt $C/post-x.txt; cp $B/post-telegram-$BASE.txt $C/post-telegram.txt
cp $B/short-$BASE.mp4 $CS/video.mp4; cp $B/meta-short-$BASE.json $CS/meta.json
cp $B/post-tiktok-$BASE.txt $CS/post-tiktok.txt; cp $B/post-instagram-$BASE.txt $CS/post-instagram.txt
cp $B/post-linkedin-$BASE.txt $CS/post-linkedin.txt   # LinkedIn: el Short como vídeo, no como enlace (Daniel, 8-nov-2026)
[ -f $B/ab-$BASE.json ] && cp $B/ab-$BASE.json $C/ab.json   # prueba A/B del título (ab-espana.yml)
# Enlaces al capítulo anterior y a las listas del canal (sustituyen a las pantallas finales, que la API no permite)
python3 $ENL $C/meta.json cola-es curso-$BASE; python3 $ENL $CS/meta.json cola-es curso-$BASE-short
git add $C $CS; git commit -qm "Cola España: serie educativa de análisis técnico, $BASE (vídeo, Short y posts)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && [ -f $CS/resultado.json ] && [ -f $C/buffer.json ] && [ -f $CS/buffer-linkedin.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])"); SH=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "serie educativa $BASE: YouTube $V, Short $SH" | tee -a $B/ids.txt
