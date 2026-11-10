#!/bin/bash
# Voz natural (neuronal es-ES-AlvaroNeural) para el vídeo diario y su Short (Daniel, 10-nov-2026: «sin que la voz suene robótica»).
# Uso (desde la raíz del repo): SCRATCH=/tmp/x bash espana/diario/voz.sh <carpeta del día>
# Sube los textos a la rama datos-diario-es (voz/<fecha>-<hora>/textos.json), lanza el workflow voz-espana.yml,
# espera y deja los mp3 en <carpeta>/voz/. make_video.py y make_short.py los usan solos; si falta alguno, usan Piper.
set -euo pipefail
D=$(cd "$1" && pwd); REPO=$(pwd); S=${SCRATCH:-/tmp/es-scratch}; GH=aiacciones-tech/aiacciones-web-Chile
F=$(python3 -c "import json;print(json.load(open('$D/info.json'))['fecha'])")
ID="$F-$(date -u +%H%M%S)"; W="$S/voz-rama"
rm -rf "$W"; git clone -q --depth 1 -b datos-diario-es "https://github.com/$GH.git" "$W" 2>&1 | grep -v -i moved || true
mkdir -p "$W/voz/$ID"
python3 espana/diario/make_video.py "$D" textos > "$S/t_video.json"
python3 - "$S/t_video.json" "$D/short.json" "$W/voz/$ID/textos.json" <<'PY'
import json,sys
T=json.load(open(sys.argv[1])); S=json.load(open(sys.argv[2]))
for i,e in enumerate(S["escenas"]): T[f"short_{i}"]=e["voz"]
json.dump(T,open(sys.argv[3],"w"),ensure_ascii=False,indent=1)
PY
cd "$W"; git add voz; git -c user.name=aiacciones-bot -c user.email=aiacciones-bot@users.noreply.github.com commit -qm "Textos de voz $ID"
for i in 1 2 3 4; do git push -q origin datos-diario-es 2>&1 | grep -v -i moved && break || true; git pull -q --rebase origin datos-diario-es; done
git ls-remote origin datos-diario-es | grep -q "$(git rev-parse HEAD)" || { git pull -q --rebase origin datos-diario-es; git push -q origin datos-diario-es; }
cd "$REPO"
gh workflow run voz-espana.yml --ref main -R $GH -f id="$ID" >/dev/null; sleep 8
RUN=$(gh run list -w voz-espana.yml -R $GH -L 1 --json databaseId -q '.[0].databaseId')
until [ "$(gh run view "$RUN" -R $GH --json status -q .status)" = completed ]; do sleep 10; done
[ "$(gh run view "$RUN" -R $GH --json conclusion -q .conclusion)" = success ] || { echo "voz-espana falló (run $RUN): se usará Piper"; exit 1; }
cd "$W"; git pull -q origin datos-diario-es 2>&1 | grep -v -i moved || true
mkdir -p "$D/voz"; rm -f "$D/voz/"*.mp3; cp voz/$ID/*.mp3 "$D/voz/"
echo "voz neuronal: $(ls "$D/voz" | wc -l) mp3 en $D/voz"
