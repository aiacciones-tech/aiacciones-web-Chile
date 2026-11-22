#!/bin/bash
# bash encolar.sh <carpeta de la semana>: encola el Short «Wochenkalender der Quartalszahlen» en cola-ge/calendario-<fecha>/ de la rama youtube-cola.
# youtube-GE.yml lo sube como Short (público); telegram-GE.yml publica post-telegram.txt con miniatura.png y el enlace;
# buffer-GE.yml manda post-tiktok.txt (vídeo), post-instagram.txt (Reel) y post-threads.txt (con miniatura.png; espera sin error si Threads
# no está conectado en Buffer). Se encola entre las 18:00 y las 20:00 de Berlín (Daniel, 22-nov-2026).
set -e
B=$(cd "$1" && pwd); F=$(python3 -c "import json;print(json.load(open('$B/calendario.json'))['fecha'])"); S=${SCRATCH:-/tmp/ge-scratch}; mkdir -p $S
for f in calendario-$F-GE.mp4 miniatura-calendario-$F-GE.png meta-youtube-calendario-$F-GE.json; do test -s "$B/$f" || { echo "falta $B/$f"; exit 1; }; done
grep -q UC23KiHTq_lULliZwAM3dEpA $B/meta-youtube-calendario-$F-GE.json || { echo "falta el enlace del canal"; exit 1; }
[ -d $S/cola ] || git clone -q --depth 1 -b youtube-cola https://github.com/aiacciones-tech/aiacciones-web-Chile.git $S/cola; cd $S/cola; git pull -q origin youtube-cola 2>/dev/null
git config user.name "aiacciones-bot"; git config user.email "aiacciones-bot@users.noreply.github.com"
C=cola-ge/calendario-$F
[ -f $C/resultado.json ] && { echo "ya subido: $C"; exit 1; }
mkdir -p $C
cp $B/calendario-$F-GE.mp4 $C/video.mp4; cp $B/meta-youtube-calendario-$F-GE.json $C/meta.json; cp $B/miniatura-calendario-$F-GE.png $C/miniatura.png
for r in telegram tiktok instagram threads; do [ -s $B/post-$r-calendario-$F-GE.txt ] && cp $B/post-$r-calendario-$F-GE.txt $C/post-$r.txt; done
date -u +%Y-%m-%dT%H:%M:%SZ > $C/encolado.txt
git add cola-ge; git commit -qm "Cola GE: calendario semanal de resultados $F (Short)"
for i in 1 2 3 4; do git pull -q --rebase origin youtube-cola 2>/dev/null; git push -q origin HEAD:youtube-cola 2>/dev/null && break; sleep $((2**i)); done
for i in $(seq 80); do git pull -q origin youtube-cola 2>/dev/null; [ -f $C/resultado.json ] && break; sleep 15; done
V=$(python3 -c "import json;print(json.load(open('$C/resultado.json'))['videoId'])")
echo "calendario GE $F: Short https://www.youtube.com/shorts/$V" | tee -a $B/ids.txt
