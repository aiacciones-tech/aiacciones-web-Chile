#!/bin/bash
# bash encolar.sh <carpeta del episodio>: encola un episodio de «Die Wall-Street-Giganten» (Wall Street auf Deutsch) en cola-ge/serie20-<ticker>-<fecha>/ de la rama youtube-cola.
# youtube-GE.yml lo sube; telegram-GE.yml publica post-telegram.txt y buffer-GE.yml manda post-x.txt a X. Sin Short (máx. 3 vídeos de la serie al día).
# encolado.txt guarda la hora: plan.py cuenta los del día para no pasar de 3.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;v=json.load(open('$B/video.json'));print(f\"serie20-{v['ticker'].lower()}-{v['fecha_resultados']}\")")
S=${SCRATCH:-/tmp/ge-scratch}; mkdir -p $S
for f in $BASE-GE.mp4 meta-youtube-$BASE-GE.json miniatura-$BASE-GE.png post-telegram-$BASE-GE.txt post-x-$BASE-GE.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q UC23KiHTq_lULliZwAM3dEpA $B/meta-youtube-$BASE-GE.json || { echo "falta el enlace del canal"; exit 1; }
if [ ! -d $S/cola ]; then
  git clone -q --depth 1 --filter=blob:none --sparse -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola
  (cd $S/cola && git sparse-checkout set cola-ge)
fi
cd $S/cola; git pull -q origin youtube-cola 2>/dev/null || true
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-ge/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (GE) en 24 h:',n); assert n<=7, 'límite de YouTube (~10/24 h por canal): espera antes de encolar'
PY
C=cola-ge/$BASE
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C
cp $B/$BASE-GE.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE-GE.json $C/meta.json; cp $B/miniatura-$BASE-GE.png $C/miniatura.png
cp $B/post-telegram-$BASE-GE.txt $C/post-telegram.txt; cp $B/post-x-$BASE-GE.txt $C/post-x.txt
[ -s $B/post-tiktok-$BASE-GE.txt ] && cp $B/post-tiktok-$BASE-GE.txt $C/post-tiktok.txt   # TikTok vía buffer-GE.yml
[ -s $B/post-linkedin-$BASE-GE.txt ] && cp $B/post-linkedin-$BASE-GE.txt $C/post-linkedin.txt   # LinkedIn vía buffer-GE.yml
TZ=Europe/Berlin date +%F' '%H:%M > $C/encolado.txt
git add $C; git commit -qm "Cola GE: serie 20 acciones, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 60); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['url'])")
echo "serie20 $BASE: $V" | tee -a $B/ids.txt
