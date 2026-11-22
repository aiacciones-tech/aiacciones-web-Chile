#!/bin/bash
# bash encolar.sh <carpeta de la semana>: encola el Short «تقويم النتائج الأسبوعي» en cola-nabd/<base>-short/ de la rama youtube-cola.
# Sale el domingo entre las 19:00 y las 21:00 de Riad (16:00-18:00 UTC): si se llama antes de las 16:00 UTC, espera hasta esa hora
# (NO_ESPERAR=1 para saltarlo). Después, sin pasos a mano: youtube-Nabd.yml sube el Short; telegram-Nabd.yml publica post-telegram.txt
# con la portada (miniatura.png); buffer-Nabd.yml manda post-x.txt (X), post-linkedin.txt (LinkedIn, con el vídeo), post-tiktok.txt (TikTok),
# y post-instagram.txt (Reel). Facebook y Threads: fuera hasta nuevo aviso (Daniel, 22-nov-2026).
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;print(json.load(open('$B/video.json'))['base'])"); S=${SCRATCH:-/tmp/nabd-scratch}; mkdir -p $S
POSTS="x telegram linkedin tiktok instagram"  # Facebook y Threads fuera hasta nuevo aviso (Daniel, 22-nov-2026)
for f in $BASE-Nabd.mp4 meta-short-$BASE-Nabd.json miniatura-$BASE-Nabd.png $(for p in $POSTS; do echo post-$p-$BASE-Nabd.txt; done); do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q UCRU3n034y5dJBEGnhAKjhfQ $B/meta-short-$BASE-Nabd.json || { echo "falta el enlace del canal"; exit 1; }
if [ "$NO_ESPERAR" != 1 ]; then
  while [ "$(date -u +%H%M)" -lt 1600 ]; do echo "esperando a las 16:00 UTC (19:00 Riad); ahora $(date -u +%H:%M) UTC"; sleep 120; done
  [ "$(date -u +%H%M)" -lt 1800 ] || echo "AVISO: pasan las 18:00 UTC (21:00 Riad); se publica igual."
fi
if [ ! -d $S/cola ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-nabd)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-nabd/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (Nabd) en 24 h:',n); assert n<=7, 'límite de YouTube (~10/24 h por canal): espera antes de encolar'
PY
C=cola-nabd/$BASE-short
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C
cp $B/$BASE-Nabd.mp4 $C/video.mp4; cp $B/meta-short-$BASE-Nabd.json $C/meta.json; cp $B/miniatura-$BASE-Nabd.png $C/miniatura.png
TZ=Asia/Riyadh date +%F' '%H:%M > $C/encolado.txt
git add $C; git commit -qm "Cola Nabd: calendario de resultados, $BASE (Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
# Los posts van en un segundo push, con el vídeo ya en la rama (Buffer toma el vídeo del Short desde GitHub).
for p in $POSTS; do cp $B/post-$p-$BASE-Nabd.txt $C/post-$p.txt; done
git add $C; git diff --cached --quiet || git commit -qm "Cola Nabd: posts del calendario de resultados, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
SH=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])")
echo "calendario Nabd $BASE: Short https://youtube.com/shorts/$SH" | tee -a $B/ids.txt
