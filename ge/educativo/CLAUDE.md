# Serie educativa «Charttechnik einfach erklärt» de Wall Street auf Deutsch: instrucciones (Daniel, 18-nov-2026)

Vídeos educativos de análisis técnico en alemán: **un concepto por vídeo**, explicado sobre el **gráfico real** de una acción conocida de EE. UU.
(Nvidia, Apple…). Piloto: Folge 1, «Unterstützung und Widerstand» con Nvidia. Valen todas las reglas de `ge/diario/CLAUDE.md`
(Keine Anlageberatung, transparencia IA, secretos `_GE`, todo lo que se entrega termina en `-GE`, solo se toca `ge/`, `*-GE.yml` y `cola-ge/`).
Instrucciones en español; lo que ve y oye el público, en alemán («Sie»).

Plan de temas (orden propuesto): 1 Unterstützung und Widerstand (NVDA) · 2 Gleitende Durchschnitte und 200-Tage-Linie ·
3 Trendlinien und Trendkanäle · 4 Handelsvolumen · 5 RSI · 6 MACD · 7 Kerzenmuster · 8 Chartformationen (Schulter-Kopf-Schulter, Doppelboden) ·
9 Kurslücken (Gaps) · 10 Bollinger-Bänder. La acción de ejemplo se elige porque su gráfico enseña bien el concepto (Apple, Microsoft, Tesla, Amazon…).

## Reglas de contenido
- Educación, no previsión: se describen zonas y patrones del pasado; la situación actual va como **condiciones** («Sollte der Kurs … erreichen, wird sich zeigen …»),
  nunca como previsión, Kursziel ni recomendación. La acción es «nur ein Beispiel». Sin «günstig/teuer».
- Toda cifra dicha sale de las velas de TradingView (`velas.json`) y coincide con la pantalla; cálculos propios «berechnet», zonas «eingezeichnet».
  No se explican las causas de un movimiento salvo con fuente publicada y atribuida.
- Los esquemas (`tipo: esquema`) llevan «Schematische Darstellung, keine echten Kursdaten».
- `ultima_vela`: la última sesión **cerrada** (la vela del día en curso de velas.json puede ser intradía).

## Piezas
- `video.json` por lección en `lecciones/<base>/`: base, folge, simbolo (TradingView), ticker, nombre, tema, ultima_vela, escenas, info, miniatura.
  Escenas (`tipo`): `portada`, `esquema` (modo sr / rollentausch / fehlausbruch), `puntos` (≤5 [título, texto]), `grafico` (desde, hasta, zonas
  [{de, a, texto, color}], marcas [{fecha, tipo techo|suelo, texto}], nota, volumen, ultimo, animar_velas), `fin` (claves ≤4, siguiente).
  `capitulo` en una escena = capítulo de YouTube y tramo de la barra de progreso. Para un tema nuevo que necesite otro dibujo (medias, RSI…),
  se añade una opción a `s_grafico` o un tipo nuevo en `make_leccion.py`.
- `.github/workflows/educativo-GE.yml`: al subir `video.json` a una rama `claude/ge-educativo-*`, pide las velas (solo la primera vez, se congelan)
  y genera la voz Azure de-DE-ConradNeural (mismo recurso y secretos que el diario) en `<base>/` de la rama `voz-ge-educativo`.
- `niveles.py <velas.json> [ventana] [tolerancia %] [sesiones]`: pivotes y zonas candidatas con toques y fechas, para escribir el guion.
- `make_leccion.py <carpeta> [preview]` (con `AUD`, `VELAS`, `VOZ_DIR`): 4-9 min, control de calidad, escribe mp4, times.json y guion.
- `meta_leccion.py <carpeta>`: meta de YouTube (language de), posts de Telegram, X, LinkedIn, TikTok e Instagram (Reel), miniatura (gráfico de la escena `miniatura.grafico`).
- `encolar.sh <carpeta>`: `cola-ge/<base>/` en `youtube-cola`; `youtube-GE.yml` sube, `telegram-GE.yml` y `buffer-GE.yml` publican.

## Pasos
1. Crea `lecciones/<base>/video.json` con simbolo y `"escenas": []`; súbelo a `claude/ge-educativo-<fecha>` (pide las velas, ~1 min); clona `voz-ge-educativo`.
2. `python3 niveles.py <clon>/<base>/velas.json` y mira los datos; escribe el guion: **~830 palabras ≈ 6 min** (calibrado: 836 palabras dieron 6:00 con Azure, ~139 palabras/min).
3. `AUD=<scratch> VELAS=<clon>/<base>/velas.json python3 make_leccion.py <carpeta> preview`: mira TODOS los PNG.
4. Sube `video.json` otra vez (genera la voz, 2-4 min); `git pull` del clon; render con `VOZ_DIR=<clon>/<base>`; `meta_leccion.py`.
5. `SCRATCH=<scratch> bash encolar.sh <carpeta>`; copia mp4, miniatura, meta, guion y posts a `/mnt/project-files/ge-educativo/<base>/`.
