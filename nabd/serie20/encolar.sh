#!/bin/bash
# bash encolar.sh <carpeta del episodio>: encola un episodio de «عمالقة وول ستريت» en cola-nabd/serie20-<ticker>-<fecha>/ de la rama youtube-cola.
# youtube-Nabd.yml lo sube; telegram-Nabd.yml publica post-telegram.txt y buffer-Nabd.yml manda post-x.txt a X. Sin Short (máx. 3 vídeos de la serie al día).
# encolado.txt guarda la hora: plan.py cuenta los del día para no pasar de 3.
set -e
B=$(cd "$1" && pwd); BASE=$(python3 -c "import json;v=json.load(open('$B/video.json'));print(f\"serie20-{v['ticker'].lower()}-{v['fecha_resultados']}\")")
S=${SCRATCH:-/tmp/nabd-scratch}; mkdir -p $S
for f in $BASE-Nabd.mp4 meta-youtube-$BASE-Nabd.json miniatura-$BASE-Nabd.png post-telegram-$BASE-Nabd.txt post-x-$BASE-Nabd.txt; do
  test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }
done
grep -q UCRU3n034y5dJBEGnhAKjhfQ $B/meta-youtube-$BASE-Nabd.json || { echo "falta el enlace del canal"; exit 1; }
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
C=cola-nabd/$BASE
[ -e $C ] && { echo "ya encolado: $C"; exit 1; }
mkdir -p $C
cp $B/$BASE-Nabd.mp4 $C/video.mp4; cp $B/meta-youtube-$BASE-Nabd.json $C/meta.json; cp $B/miniatura-$BASE-Nabd.png $C/miniatura.png
cp $B/post-telegram-$BASE-Nabd.txt $C/post-telegram.txt; cp $B/post-x-$BASE-Nabd.txt $C/post-x.txt
TZ=Asia/Riyadh date +%F' '%H:%M > $C/encolado.txt
git add $C; git commit -qm "Cola Nabd: serie 20 acciones, $BASE"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 60); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['url'])")
echo "serie20 $BASE: $V" | tee -a $B/ids.txt
