import os, re
S = "site"
def rd(p): return open(os.path.join(S, p), encoding="utf-8").read()
def wr(p, t): open(os.path.join(S, p), "w", encoding="utf-8").write(t)
BANNER = '<div class="period"><span class="period-tag">2T 2026</span><p><b>Resultados del segundo trimestre de 2026 (abril a junio).</b> Hacemos estos comparadores cada trimestre: cuando salgan los resultados del 3T 2026 los actualizaremos.</p></div>'
PAGE = '<div class="period"><span class="period-tag">2T 2026</span><p><b>Período analizado: segundo trimestre de 2026 (abril a junio).</b> Este comparador se actualiza cada trimestre.</p></div>'
p = "comparadores/index.html"; t = rd(p)
if 'class="period"' not in t:
    t = t.replace('<div class="cmp-cards">', BANNER + '<div class="cmp-cards">', 1)
    t = t.replace('<span class="cm">', '<span class="cm"><b class="period-mini">2T 2026</b> ')
    wr(p, t)
for d in os.listdir(os.path.join(S, "comparadores")):
    p = f"comparadores/{d}/index.html"
    if not os.path.isfile(os.path.join(S, p)): continue
    t = rd(p)
    if 'class="period"' in t: continue
    t, k = re.subn(r'(<section class="page-head">.*?</h1>)', lambda m: m.group(1) + PAGE, t, count=1, flags=re.S)
    t = t.replace('<p class="eyebrow">Comparador</p>', '<p class="eyebrow">Comparador · 2T 2026</p>', 1)
    print(d, k); wr(p, t)
p = "assets/styles.css"; t = rd(p)
if ".period {" not in t:
    t += "\n.period { display: flex; gap: 14px; align-items: center; margin: 14px 0 22px; padding: 12px 16px; border: 1px solid var(--line); border-left: 3px solid #3b86e6; border-radius: 6px; background: rgba(59,134,230,.08); }\n.period p { margin: 0; font-size: 15px; }\n.period-tag { flex: none; font: 600 13px/1 var(--f-mono); padding: 7px 10px; border-radius: 4px; background: #3b86e6; color: #fff; letter-spacing: .04em; }\n.period-mini { font: 600 11px/1 var(--f-mono); padding: 3px 6px; margin-right: 4px; border-radius: 3px; background: #3b86e6; color: #fff; }\n"
    wr(p, t)
