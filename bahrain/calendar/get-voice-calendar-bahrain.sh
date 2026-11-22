#!/bin/bash
# bash get-voice-calendar-bahrain.sh <week> <dir>   e.g. 2026-11-22 /tmp/voz
# After pushing bahrain/calendar/<week>-bahrain/short-<week>-bahrain.json to a claude/** branch, voz-calendar-bahrain.yml makes
# the Azure wavs. This waits (up to 10 min) until every voice line has its wav on branch voz-calendar-bahrain and copies them to
# <dir>/<week>-bahrain/. Then render with VOZ_DIR=<dir>/<week>-bahrain. Exit 2 = no Azure voice: render everything with --piper.
set -e
WK=${1:?week}; D=${2:?dir}; HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd)
for i in $(seq 40); do
  if git -C "$REPO" fetch -q --depth 1 origin voz-calendar-bahrain 2>/dev/null; then
    rm -rf "$D/$WK-bahrain"; mkdir -p "$D"
    git -C "$REPO" archive FETCH_HEAD "$WK-bahrain" 2>/dev/null | tar -x -C "$D" 2>/dev/null || true
    F=$(cd "$HERE" && python3 -c "
import json,os,sys; from voz_calendar_bahrain import clave
s=json.load(open('$WK-bahrain/short-$WK-bahrain.json',encoding='utf-8'))
print(sum(not os.path.isfile(os.path.join('$D/$WK-bahrain',clave(x['voice'])+'.wav')) for x in s['slides']))")
    [ "$F" = 0 ] && { echo "Azure voice ready in $D/$WK-bahrain"; exit 0; }
    echo "missing $F wav(s), waiting..."
  fi
  sleep 15
done
echo "No complete Azure voice after 10 min: check the 'Voz Azure del calendario semanal (Baréin)' run, or render with --piper."; exit 2
