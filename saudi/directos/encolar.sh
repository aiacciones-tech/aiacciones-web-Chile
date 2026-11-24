#!/bin/bash
# bash encolar.sh <carpeta del evento>: encola un directo de Saudi Arabia AI Stocks en cola-sa/directo-<base>/ de la rama youtube-cola.
# directo-saudi.yml crea la emisión programada (página "Próximamente" + miniatura), lanza Buffer (X, Threads, Facebook) y Telegram
# para anunciarla con su enlace, y a la hora fijada emite el vídeo. Encolar al menos 30 min antes del inicio (mejor 1-3 h).
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])"); S=${SCRATCH:-/tmp/saudi-directo-scratch}; mkdir -p $S
for f in live-$BASE-saudi.mp4 directo-$BASE-saudi.json thumbnail-$BASE-saudi.png post-x-$BASE-saudi.txt post-threads-$BASE-saudi.txt \
         post-facebook-$BASE-saudi.txt post-telegram-$BASE-saudi.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
for p in threads facebook telegram; do grep -q "SaudiArabiaAIStocks" $B/post-$p-$BASE-saudi.txt || { echo "falta el enlace del canal en post-$p"; exit 1; }; done
python3 - "$B/directo-$BASE-saudi.json" <<'PY'
import json, sys, datetime as dt
d = json.load(open(sys.argv[1])); ini = dt.datetime.fromisoformat(d["inicio"].replace("Z", "+00:00"))
falta = (ini - dt.datetime.now(dt.timezone.utc)).total_seconds() / 60
print(f"el directo empieza en {falta:.0f} min"); assert falta >= 20, "demasiado tarde: cambia 'inicio' en video.json y vuelve a generar los metadatos"
PY
if [ ! -d $S/cola ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-sa)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
CS=cola-sa/directo-$BASE
[ -e $CS ] && { echo "ya encolado: $CS"; exit 1; }
mkdir -p $CS
cp $B/live-$BASE-saudi.mp4 $CS/video.mp4; cp $B/thumbnail-$BASE-saudi.png $CS/miniatura.png
for p in x threads facebook telegram; do cp $B/post-$p-$BASE-saudi.txt $CS/post-$p.txt; done
cp $B/directo-$BASE-saudi.json $CS/directo.json
git add cola-sa; git commit -qm "Cola Arabia Saudita: directo $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 40); do git pull -q origin youtube-cola 2>/dev/null; [ -f $CS/resultado.json ] && break; sleep 15; done
test -f $CS/resultado.json || { echo "la emisión todavía no está creada: mira el run de 'Directos (Arabia Saudita)' en Actions"; exit 1; }
V=$(python3 -c "import json;print(json.load(open('$CS/resultado.json'))['videoId'])")
echo "directo $BASE: https://www.youtube.com/watch?v=$V" | tee -a $B/ids.txt
