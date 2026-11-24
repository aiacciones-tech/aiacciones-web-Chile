#!/bin/bash
# bash ge/dax/encolar.sh <carpeta del día>: encola el Short «DAX am Abend» en cola-ge/dax-<fecha>/ de la rama youtube-cola.
# youtube-GE.yml lo sube como Short (público); buffer-GE.yml manda post-tiktok.txt (vídeo) y post-instagram.txt (Reel).
# Sin Telegram ni X durante la prueba, para no cargar esos canales con un segundo post diario.
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/short.json'))['fecha'])"); S=${SCRATCH:-/tmp/ge-scratch}; mkdir -p $S
for f in dax-$F-GE.mp4 meta-youtube-dax-$F-GE.json; do test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }; done
grep -q UC23KiHTq_lULliZwAM3dEpA $B/meta-youtube-dax-$F-GE.json || { echo "falta el enlace del canal"; exit 1; }
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
python3 - <<PY
import json,glob,datetime as dt
now=dt.datetime.now(dt.timezone.utc); n=0
for p in glob.glob('cola-ge/*/resultado.json'):
    try: s=dt.datetime.fromisoformat(json.load(open(p))['subido'].replace('Z','+00:00'))
    except Exception: continue
    if now-s<dt.timedelta(hours=24): n+=1
print('subidas a YouTube (GE) en 24 h:',n); assert n<=8, 'límite de YouTube (~10/24 h por canal): espera antes de encolar'
PY
C=cola-ge/dax-$F
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C
cp $B/dax-$F-GE.mp4 $C/video.mp4; cp $B/meta-youtube-dax-$F-GE.json $C/meta.json
for r in tiktok instagram; do [ -s $B/post-$r-dax-$F-GE.txt ] && cp $B/post-$r-dax-$F-GE.txt $C/post-$r.txt; done
date -u +%Y-%m-%dT%H:%M:%SZ > $C/encolado.txt
git add cola-ge; git commit -qm "Cola GE: Short DAX am Abend $F"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])")
echo "DAX GE $F: Short https://www.youtube.com/shorts/$V" | tee -a $B/ids.txt
