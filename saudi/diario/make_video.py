# Video diario en árabe de la bolsa saudí (TASI y, en una frase, Nomu), unos 5 minutos con bloque técnico de 5 escenas: 1080p, voz Piper ar_JO-kareem, logo Saudi Arabia AI Stocks.
# Uso: AUD=<scratch> python3 make_video.py <carpeta del día> [preview]
#   La carpeta del día tiene mercado.json (de datos/mercado-<fecha>.json de la rama datos-diario-saudi) y video.json (textos y locución;
#   ver ejemplo-2026-11-05/). Escribe <carpeta>/video-bolsa-<fecha>-SA.mp4 y <carpeta>/times.json (capítulos).
import os, sys, json, numpy as np, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun import *
from tecnico import calc, INDICE, MESES, TZ, fecha_ar
import campana
DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
W, H, FPS = 1920, 1080, 30
AUD = os.environ.get("AUD", "aud")
M = json.load(open(f"{DIR}/mercado.json")); VJ = json.load(open(f"{DIR}/video.json"))
R, A = calc(M, VJ.get("nombres")); FECHA = dt.date.fromisoformat(R["fecha"]); FECHA_TXT = fecha_ar(FECHA)
OUT = f"{DIR}/video-bolsa-{R['fecha']}-SA.mp4"
SECS = ["الأخبار", "التحليل الأساسي", "الأسهم", "التحليل الفني", "الأجندة"]; NS = len(SECS)
LG = load_logo(130); LGS = load_logo(95); LGB = load_logo(230)
NB = 126  # unas 6 meses de sesiones
MAXS = 330  # unos 5 minutos (Daniel, 10-nov-2026); antes 180 s


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)


def base_fig(n, kicker, title, sub):
    f = fig(W, H)
    T(f, 0.94, 0.90, kicker, GOLD, 24, "bold")
    T(f, 0.94, 0.80, title, FG, 44 if len(title) <= 50 else 38, "bold")
    T(f, 0.105, 0.92, f"{n}/{NS} · {SECS[n - 1]}", MUTED, 19, "bold", ha="left")
    T(f, 0.105, 0.885, "أسهم السعودية · " + FECHA_TXT, DIM, 16, "bold", ha="left")
    w = 0.88 / NS
    for i in range(NS):  # barra de progreso de derecha a izquierda
        f.patches.append(plt.Rectangle((0.94 - (i + 1) * w + 0.008, 0.975), w - 0.008, 0.008, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))
    T(f, 0.94, 0.04, "\n".join(textwrap.wrap(sub, 150)), MUTED, 16, linespacing=1.4)
    return f


def s_title(t):
    f = fig(W, H); a = ease(t / 0.6); r = R["tasi"]; up = r["var_pct"] >= 0; cc = TEAL if up else NEG
    T(f, 0.94, 0.89, "أسهم السعودية · ملخص جلسة تداول", GOLD, 28, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.14, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, 0.94, 0.77, "جلسة " + FECHA_TXT, BG, 66, "bold", va="center", alpha=a)
    # derecha: cierre de TASI, variación en % y en puntos; izquierda: curva intradía
    T(f, 0.94, 0.615, INDICE["tasi"], MUTED, 30, "bold", alpha=a)
    f.text(0.94, 0.50, num(r["cierre"]), color=FG, fontsize=92, weight="bold", ha="right", alpha=a)
    f.text(0.94, 0.42, f"{pct(r['var_pct'])}   ({r['var_pts']:+,.2f})", color=cc, fontsize=40, weight="bold", ha="right", alpha=a)
    n_ = R["nomu"]; cn = TEAL if n_["var_pct"] >= 0 else NEG
    T(f, 0.94, 0.33, "السوق الموازية (نمو)", MUTED, 24, "bold", alpha=ease((t - 0.2) / 0.5))
    f.text(0.94, 0.275, f"{num(n_['cierre'])}   {pct(n_['var_pct'])}", color=cn, fontsize=30, weight="bold", ha="right", alpha=ease((t - 0.2) / 0.5))
    I = [v for v in M["tasi_intradia"]["velas"] if dt.datetime.fromtimestamp(v["t"], TZ).date() == FECHA]
    IC = np.array([v["c"] for v in I]); prev = r["anterior"]
    if len(IC) > 2:
        ax = f.add_axes([0.06, 0.20, 0.50, 0.40]); clean(ax)
        n = max(2, int(len(IC) * ease(t))); x = np.arange(len(IC))
        ax.plot(x[:n], IC[:n], color=cc, lw=3.5); ax.axhline(prev, color=DIM, lw=1.5, ls="--")
        ax.fill_between(x[:n], IC[:n], prev, color=cc, alpha=0.12)
        pad = (max(IC.max(), prev) - min(IC.min(), prev)) * 0.15
        ax.set_xlim(0, len(IC) - 1); ax.set_ylim(min(IC.min(), prev) - pad, max(IC.max(), prev) + pad); ax.set_yticks([])
        hrs = [dt.datetime.fromtimestamp(v["t"], TZ) for v in I]; tk = [j for j, h in enumerate(hrs) if h.minute == 0]
        ax.set_xticks(tk, [hrs[j].strftime("%H:%M") for j in tk]); ax.tick_params(labelsize=15)
        T(f, 0.56, 0.615, "حركة تاسي خلال الجلسة (كل 5 دقائق، بتوقيت الرياض)", MUTED, 18)
        T(f, 0.06, 0.615, "الإغلاق السابق " + num(prev), MUTED, 16, ha="left")
    if VJ.get("titular"): T(f, 0.94, 0.11, VJ["titular"], BLUE, 30, "bold", alpha=ease((t - 0.3) / 0.5))
    T(f, 0.94, 0.04, VJ.get("title_fuente", "البيانات: TradingView (إغلاق " + R["fecha"] + ")"), MUTED, 16)
    return with_logo(to_arr(f), LG, x=60, y=40)


def s_news(t):
    N_ = VJ["noticias"]; f = base_fig(1, "أخبار اليوم", N_["titulo"], N_["fuente"]); pal = [GOLD, TEAL, BLUE, NEG, FG]
    for i, (tag, txt) in enumerate(N_["items"]):
        b = ease((t - i * 0.15) / 0.4)
        if b <= 0: continue
        y = 0.66 - i * 0.14; cc = pal[i % 5]
        f.patches.append(plt.Rectangle((0.945, y - 0.035), 0.006, 0.09, transform=f.transFigure, color=cc, alpha=b, figure=f))
        T(f, 0.93, y + 0.02, tag, cc, 28, "bold", alpha=b)
        T(f, 0.93, y - 0.03, txt, FG, 25 if len(txt) <= 95 else 22, alpha=b)
    return to_arr(f)


def s_fact(t):
    F = VJ["factores"]; f = base_fig(2, "التحليل الأساسي: لماذا تحركت السوق؟", F["titulo"], F["fuente"])
    CX = dict(R["contexto"]); CX["TADAWUL:TASI"] = {"change": R["tasi"]["var_pct"]}; CX["TADAWUL:NOMUC"] = {"change": R["nomu"]["var_pct"]}
    L = [(n, (CX[v]["change"] if isinstance(v, str) else v)) for n, v in F["bolsas"] if not isinstance(v, str) or (v in CX and CX[v].get("change") is not None)]
    ax = f.add_axes([0.20, 0.13, 0.25, 0.58]); clean(ax); e = ease(t)
    y = np.arange(len(L))[::-1]; v = [x[1] for x in L]; lim = max(abs(min(v)), abs(max(v))) * 1.5
    ax.barh(y, [x * e for x in v], color=[(GOLD if "تاسي" in n or "نمو" in n else (TEAL if x > 0 else NEG)) for n, x in L], height=0.6)
    ax.set_yticks(y, [ar(n) for n, _ in L]); ax.tick_params(colors=FG, labelsize=19); ax.set_xticks([])
    ax.set_xlim(-lim if min(v) < 0 else -lim * 0.35, lim * 0.7 if max(v) > 0 else lim * 0.35); ax.axvline(0, color=DIM, lw=1.5)
    if t >= 0.6:
        for yy, x in zip(y, v): ax.text(x * e + (lim * 0.03 if x > 0 else -lim * 0.03), yy, pct(x), va="center", ha="left" if x > 0 else "right", color=FG, fontsize=18, weight="bold")
    T(f, 0.45, 0.735, F.get("bolsas_titulo", "الأسواق في الجلسة"), MUTED, 20)
    for i, (a_, b_, cc) in enumerate(F["items"]):
        b = ease((t - 0.2 - i * 0.12) / 0.4)
        if b <= 0: continue
        yy = 0.67 - i * 0.135
        T(f, 0.94, yy, a_, col(cc), 29 if len(a_) <= 36 else 25, "bold", alpha=b)
        T(f, 0.94, yy - 0.048, b_, MUTED, 22 if len(b_) <= 50 else 19, alpha=b)
    return to_arr(f)


def s_movers(t):
    V_ = VJ["valores"]; MOT = V_.get("motivos", {}); sub = R["tasi"]["suben"]; baj = R["tasi"]["bajan"]
    f = base_fig(3, "الأسهم الأكثر ارتفاعًا وانخفاضًا في السوق الرئيسية", V_.get("titulo", f"ارتفع {sub} سهمًا وانخفض {baj}"), V_["fuente"])
    mx = max(abs(x["cambio"]) for x in R["mejores"] + R["peores"])
    for xr, lst, cc, title in [(0.94, R["mejores"], TEAL, "الأكثر ارتفاعًا"), (0.48, R["peores"], NEG, "الأكثر انخفاضًا")]:
        T(f, xr, 0.715, title, cc, 26, "bold")
        for i, m in enumerate(lst):
            b = ease((t - i * 0.08) / 0.4)
            if b <= 0: continue
            y = 0.635 - i * 0.098; bw = 0.10 * abs(m["cambio"]) / mx * b; x0 = xr - 0.265
            T(f, xr, y, m["nombre"], FG, 24, "bold", alpha=b)
            f.patches.append(plt.Rectangle((x0 - bw, y - 0.002), bw, 0.032, transform=f.transFigure, color=cc, figure=f))
            f.text(x0 - bw - 0.006, y, pct(m["cambio"]), color=FG, fontsize=21, weight="bold", ha="right", alpha=b)
            T(f, xr, y - 0.036, m["ticker"] + " · " + MOT.get(m["ticker"], "لا يوجد خبر محدد في الصحافة"), MUTED, 16, alpha=b)
    if V_.get("extra"): T(f, 0.94, 0.135, V_["extra"], BLUE, 24, "bold", alpha=ease((t - 0.5) / 0.4))
    return to_arr(f)


def tech(k, n_sec, t):
    TJ = VJ["tecnico"][k]; r = R[k]; a_ = A[k]
    f = base_fig(4, f"التحليل الفني (1/{NT}) · " + INDICE[k], TJ["titulo"],
                 "شموع يومية لآخر 6 أشهر من TradingView (TADAWUL:TASI). المتوسطات والدعوم والمقاومات (قمم وقيعان حديثة) و RSI والعشوائي: محسوبة. حجم التداول مقابل متوسط 10 جلسات: محسوب. هذه بيانات وليست إشارات شراء أو بيع.")
    dates, o, hi, lo, c, S50, S200 = (a_[x] for x in ("dates", "o", "hi", "lo", "c", "S50", "S200"))
    n = len(c); idx = np.arange(n - NB, n); x = np.arange(NB); m = max(2, int(NB * ease(t / 0.8)))
    ax = f.add_axes([0.05, 0.36, 0.56, 0.38]); clean(ax)
    span = hi[idx].max() - lo[idx].min()
    for j in range(m):
        i = idx[j]; cc = TEAL if c[i] >= o[i] else NEG
        ax.vlines(j, lo[i], hi[i], color=cc, lw=1.2); ax.add_patch(plt.Rectangle((j - 0.35, min(o[i], c[i])), 0.7, max(abs(c[i] - o[i]), span * 0.002), color=cc))
    ax.plot(x[:m], S50[idx][:m], color=BLUE, lw=2.5, label=ar("متوسط 50 جلسة"))
    ax.plot(x[:m], S200[idx][:m], color=GOLD, lw=2.5, label=ar("متوسط 200 جلسة"))
    al = ease((t - 0.6) / 0.4); LEV = [l for l in r["niveles"] if lo[idx].min() - span * 0.25 <= l["valor"] <= hi[idx].max() + span * 0.25]
    for l in LEV:
        cc = NEG if l["tipo"] == "res" else TEAL
        ax.axhline(l["valor"], color=cc, lw=1.1, ls="--", alpha=al)
    vals = [l["valor"] for l in LEV]
    ax.set_xlim(-1, NB); ax.set_ylim(min(lo[idx].min(), np.nanmin(S200[idx]), *vals) - span * 0.05, max(hi[idx].max(), np.nanmax(S200[idx]), *vals) + span * 0.05)
    tk = [j for j in range(NB) if j == 0 or dates[idx[j]].month != dates[idx[j - 1]].month]
    ax.set_xticks(tk, [ar(MESES[dates[idx[j]].month - 1]) for j in tk]); ax.tick_params(labelsize=16)
    ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14)
    ax.legend(frameon=False, labelcolor=FG, fontsize=17, loc=TJ.get("leyenda", "upper left"), ncol=2)
    ax2 = f.add_axes([0.05, 0.13, 0.56, 0.17]); clean(ax2)
    ax2.axhspan(70, 100, color=NEG, alpha=0.07); ax2.axhspan(0, 30, color=TEAL, alpha=0.07)
    for lv in (20, 30, 70, 80): ax2.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax2.plot(x[:m], a_["RSI"][idx][:m], color=BLUE, lw=2.2, label="RSI 14")
    ax2.plot(x[:m], a_["K"][idx][:m], color=TEAL, lw=1.6, label="%K"); ax2.plot(x[:m], a_["D"][idx][:m], color=NEG, lw=1.6, label="%D")
    ax2.set_xlim(-1, NB); ax2.set_ylim(0, 100); ax2.set_xticks([]); ax2.yaxis.tick_right(); ax2.set_yticks([20, 50, 80])
    ax2.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper left", ncol=3)
    vr = r["volumen_vs_media10_pct"]
    filas = [("الإغلاق", num(r["cierre"]), FG),
             ("متوسط 50 جلسة", f"{num(r['sma50'])}  ({pct(r['dist_sma50_pct'], 1)})", BLUE),
             ("متوسط 200 جلسة", f"{num(r['sma200'])}  ({pct(r['dist_sma200_pct'], 1)})", GOLD)]
    filas += [(("مقاومة" if l["tipo"] == "res" else "دعم") + " · " + l["et"], num(l["valor"]), NEG if l["tipo"] == "res" else TEAL) for l in TJ["niveles"]]
    filas += [("RSI 14", num(r["rsi14"], 1) + "  · " + TJ["rsi_txt"], BLUE),
              ("العشوائي (14، 3، 3)", f"%K {num(r['estoc_k'], 0)} · %D {num(r['estoc_d'], 0)}", TEAL),
              ("حجم التداول", ("—" if vr is None else f"{pct(vr, 0)}") + " عن متوسط 10 جلسات", MUTED)]
    for i, (lab, val, cc) in enumerate(filas):
        b = ease((t - 0.3 - i * 0.05) / 0.4)
        if b <= 0: continue
        y = 0.715 - i * 0.063
        T(f, 0.94, y, lab, MUTED, 19, alpha=b)
        T(f, 0.67, y, val, cc, 21, "bold", ha="left", alpha=b)
    return to_arr(f)


def s_tech(t): return tech("tasi", 4, t)


# --- Bloque técnico ampliado (formato de unos 5 min, Daniel 10-nov-2026): 4 escenas más, todo calculado y presentado como datos ---
NT = 5  # partes del bloque técnico
FUENTE_T = "شموع يومية من TradingView (TADAWUL:TASI). كل المؤشرات محسوبة. هذه بيانات وليست إشارات شراء أو بيع."
fd = lambda iso: (lambda d: f"{d.day} {MESES[d.month - 1]}")(dt.date.fromisoformat(iso))
DIRC = {"arriba": "صاعد", "abajo": "هابط"}


def titulo_t(clave, defecto): return VJ.get("tecnico", {}).get(clave, {}).get("titulo", defecto)


def tabla(f, filas, t, y0=0.715, dy=0.063, x_lab=0.94, x_val=0.67):
    for i, (lab, val, cc) in enumerate(filas):
        b = ease((t - 0.3 - i * 0.05) / 0.4)
        if b <= 0: continue
        T(f, x_lab, y0 - i * dy, lab, MUTED, 19, alpha=b)
        T(f, x_val, y0 - i * dy, val, cc, 21, "bold", ha="left", alpha=b)


def ejes_fecha(ax, dates, idx, NBx):
    tk = [j for j in range(NBx) if j == 0 or dates[idx[j]].month != dates[idx[j - 1]].month]
    ax.set_xticks(tk, [ar(MESES[dates[idx[j]].month - 1]) for j in tk]); ax.tick_params(labelsize=15)


def s_tend(t):
    r = R["tasi"]; a_ = A["tasi"]; c = a_["c"]; dates = a_["dates"]
    f = base_fig(4, f"التحليل الفني (2/{NT}) · الاتجاه والمتوسطات المتحركة", titulo_t("tendencia", "الاتجاه: موقع المؤشر من متوسطاته"), FUENTE_T)
    NBx = 250; n = len(c); idx = np.arange(n - NBx, n); x = np.arange(NBx); m = max(2, int(NBx * ease(t / 0.8)))
    ax = f.add_axes([0.05, 0.40, 0.56, 0.34]); clean(ax)
    ax.plot(x[:m], c[idx][:m], color=FG, lw=2.2, label=ar("الإغلاق"))
    for arr, cc, lab in ((a_["S20"], MUTED, "متوسط 20"), (a_["S50"], BLUE, "متوسط 50"), (a_["S200"], GOLD, "متوسط 200")):
        ax.plot(x[:m], arr[idx][:m], color=cc, lw=2, label=ar(lab))
    cr = r.get("cruce_50_200")
    if cr and cr["sesiones"] < NBx and t > 0.7:
        j = NBx - 1 - cr["sesiones"]; ax.axvline(j, color=NEG if cr["tipo"] == "abajo" else TEAL, lw=1.5, ls=":")
        ax.text(j, np.nanmax(c[idx]), ar("تقاطع " + DIRC[cr["tipo"]] + " " + fd(cr["fecha"])), color=MUTED, fontsize=14, ha="center", va="bottom")
    ax.set_xlim(-1, NBx); ejes_fecha(ax, dates, idx, NBx); ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14)
    ax.legend(frameon=False, labelcolor=FG, fontsize=15, loc=VJ.get("tecnico", {}).get("tendencia", {}).get("leyenda", "lower left"), ncol=4)
    # rendimientos (calculados)
    P = r["rendimiento"]; L = [("أسبوع", P["semana"]), ("شهر", P["mes"]), ("3 أشهر", P["3meses"]), ("6 أشهر", P["6meses"]), ("سنة", P["anio"]), ("منذ بداية العام", P["en_el_anio"])]
    L = [(a, b) for a, b in L if b is not None]
    ax2 = f.add_axes([0.05, 0.12, 0.56, 0.19]); clean(ax2); e = ease((t - 0.4) / 0.5)
    xs = np.arange(len(L)); v = [b for _, b in L]
    ax2.bar(xs, [b * e for b in v], color=[TEAL if b >= 0 else NEG for b in v], width=0.55); ax2.axhline(0, color=DIM, lw=1.2)
    ax2.set_xticks(xs, [ar(a) for a, _ in L]); ax2.tick_params(labelsize=16, colors=FG); ax2.set_yticks([])
    lim = max(abs(min(v)), abs(max(v))) * 1.45; ax2.set_ylim(-lim if min(v) < 0 else -lim * 0.2, lim if max(v) > 0 else lim * 0.2)
    if e > 0.9:
        for xx, b in zip(xs, v): ax2.text(xx, b + (lim * 0.08 if b >= 0 else -lim * 0.08), pct(b), ha="center", va="bottom" if b >= 0 else "top", color=FG, fontsize=15, weight="bold")
    T(f, 0.61, 0.325, "أداء تاسي (محسوب)", MUTED, 17)
    cp = r.get("cruce_precio_sma50")
    filas = [("متوسط 20 جلسة", f"{num(r['sma20'])}  ({pct(r['dist_sma20_pct'], 1)})", MUTED),
             ("متوسط 50 جلسة", f"{num(r['sma50'])}  ({pct(r['dist_sma50_pct'], 1)})", BLUE),
             ("متوسط 200 جلسة", f"{num(r['sma200'])}  ({pct(r['dist_sma200_pct'], 1)})", GOLD),
             ("ميل متوسط 50 في 20 جلسة", pct(r["pendiente_sma50_20s_pct"]), TEAL if r["pendiente_sma50_20s_pct"] >= 0 else NEG),
             ("ميل متوسط 200 في 20 جلسة", pct(r["pendiente_sma200_20s_pct"]), TEAL if r["pendiente_sma200_20s_pct"] >= 0 else NEG)]
    if cr: filas.append(("آخر تقاطع لمتوسطي 50 و200", f"{DIRC[cr['tipo']]} · {fd(cr['fecha'])}", NEG if cr["tipo"] == "abajo" else TEAL))
    if cp: filas.append(("السعر ومتوسط 50 جلسة", ("فوقه" if cp["tipo"] == "arriba" else "دونه") + f" منذ {fd(cp['fecha'])}", TEAL if cp["tipo"] == "arriba" else NEG))
    tabla(f, filas, t, dy=0.075)
    return to_arr(f)


def s_osc(t):
    r = R["tasi"]; a_ = A["tasi"]; dates = a_["dates"]
    f = base_fig(4, f"التحليل الفني (3/{NT}) · مؤشرات الزخم", titulo_t("momento", "الزخم: RSI والعشوائي وMACD"), FUENTE_T + " MACD (12، 26، 9).")
    NBx = 63; n = len(a_["c"]); idx = np.arange(n - NBx, n); x = np.arange(NBx); m = max(2, int(NBx * ease(t / 0.8)))
    ax1 = f.add_axes([0.05, 0.56, 0.56, 0.18]); clean(ax1)
    ax1.axhspan(70, 100, color=NEG, alpha=0.07); ax1.axhspan(0, 30, color=TEAL, alpha=0.07)
    for lv in (30, 50, 70): ax1.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax1.plot(x[:m], a_["RSI"][idx][:m], color=BLUE, lw=2.4, label="RSI 14"); ax1.set_ylim(0, 100); ax1.set_yticks([30, 50, 70])
    ax2 = f.add_axes([0.05, 0.345, 0.56, 0.18]); clean(ax2)
    ax2.axhspan(80, 100, color=NEG, alpha=0.07); ax2.axhspan(0, 20, color=TEAL, alpha=0.07)
    for lv in (20, 80): ax2.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax2.plot(x[:m], a_["K"][idx][:m], color=TEAL, lw=2, label="%K"); ax2.plot(x[:m], a_["D"][idx][:m], color=NEG, lw=2, label="%D")
    ax2.set_ylim(0, 100); ax2.set_yticks([20, 80])
    ax3 = f.add_axes([0.05, 0.12, 0.56, 0.19]); clean(ax3)
    hh = a_["HIST"][idx]; ax3.bar(x[:m], hh[:m], color=[TEAL if v >= 0 else NEG for v in hh[:m]], width=0.7, alpha=0.6)
    ax3.plot(x[:m], a_["MACD"][idx][:m], color=BLUE, lw=2, label="MACD"); ax3.plot(x[:m], a_["SIG"][idx][:m], color=GOLD, lw=2, label=ar("الإشارة"))
    ax3.axhline(0, color=DIM, lw=1)
    for ax in (ax1, ax2, ax3):
        ax.set_xlim(-1, NBx); ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=13); ax.set_xticks([])
        ax.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper left", ncol=3)
    ejes_fecha(ax3, dates, idx, NBx)
    kd = r.get("cruce_k_d"); cm = r.get("cruce_macd"); sube = r["macd_hist"] >= r["macd_hist_prev"]
    filas = [("RSI 14 اليوم", num(r["rsi14"], 1), BLUE), ("RSI قبل 5 جلسات", num(r["rsi14_hace5"], 1), MUTED),
             ("مدى RSI في 3 أشهر", f"{num(r['rsi14_min_3m'], 1)} – {num(r['rsi14_max_3m'], 1)}", MUTED),
             ("العشوائي: K و D", f"{num(r['estoc_k'], 0)} · {num(r['estoc_d'], 0)}", TEAL)]
    if kd: filas.append(("آخر تقاطع بين K و D", f"{DIRC[kd['tipo']]} · {fd(kd['fecha'])}", TEAL if kd["tipo"] == "arriba" else NEG))
    filas += [("MACD · الإشارة", f"{num(r['macd'], 1)} · {num(r['macd_senal'], 1)}", BLUE),
              ("مدرج MACD", f"{num(r['macd_hist'], 1)} (" + ("يتسع" if sube else "يضيق") + ")", TEAL if r["macd_hist"] >= 0 else NEG)]
    if cm: filas.append(("آخر تقاطع لـ MACD", f"{DIRC[cm['tipo']]} · {fd(cm['fecha'])}", TEAL if cm["tipo"] == "arriba" else NEG))
    tabla(f, filas, t, dy=0.072)
    return to_arr(f)


def s_vol(t):
    r = R["tasi"]; a_ = A["tasi"]; dates = a_["dates"]; o, hi, lo, c, vol = (a_[k] for k in ("o", "hi", "lo", "c", "vol"))
    f = base_fig(4, f"التحليل الفني (4/{NT}) · الحجم والتذبذب", titulo_t("volatilidad", "الحجم ونطاق بولينجر ومتوسط المدى الحقيقي"), FUENTE_T + " بولينجر (20، 2) وATR 14.")
    NBx = 63; n = len(c); idx = np.arange(n - NBx, n); x = np.arange(NBx); m = max(2, int(NBx * ease(t / 0.8)))
    ax = f.add_axes([0.05, 0.36, 0.56, 0.38]); clean(ax); span = hi[idx].max() - lo[idx].min()
    ax.fill_between(x[:m], a_["BBl"][idx][:m], a_["BBu"][idx][:m], color=BLUE, alpha=0.10)
    ax.plot(x[:m], a_["BBu"][idx][:m], color=BLUE, lw=1.5, label=ar("بولينجر العلوي والسفلي")); ax.plot(x[:m], a_["BBl"][idx][:m], color=BLUE, lw=1.5)
    ax.plot(x[:m], a_["S20"][idx][:m], color=GOLD, lw=1.6, ls="--", label=ar("متوسط 20"))
    for j in range(m):
        i = idx[j]; cc = TEAL if c[i] >= o[i] else NEG
        ax.vlines(j, lo[i], hi[i], color=cc, lw=1.4); ax.add_patch(plt.Rectangle((j - 0.35, min(o[i], c[i])), 0.7, max(abs(c[i] - o[i]), span * 0.003), color=cc))
    ax.set_xlim(-1, NBx); ax.set_xticks([]); ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14)
    ax.legend(frameon=False, labelcolor=FG, fontsize=15, loc=VJ.get("tecnico", {}).get("volatilidad", {}).get("leyenda", "upper right"), ncol=2)
    ax2 = f.add_axes([0.05, 0.12, 0.56, 0.20]); clean(ax2)
    vv = vol[idx] / 1e6
    if np.isfinite(vv).sum() > 5:
        ax2.bar(x[:m], np.nan_to_num(vv[:m]), color=[TEAL if c[i] >= o[i] else NEG for i in idx[:m]], width=0.7, alpha=0.75)
        v10 = np.array([np.nanmean(vol[i - 10:i]) / 1e6 for i in idx]); ax2.plot(x[:m], v10[:m], color=GOLD, lw=2, label=ar("متوسط 10 جلسات"))
        ax2.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper left")
    ax2.set_xlim(-1, NBx); ax2.yaxis.tick_right(); ax2.tick_params(axis="y", labelsize=13); ejes_fecha(ax2, dates, idx, NBx)
    T(f, 0.61, 0.325, "الحجم (مليون سهم)", MUTED, 16)
    v10p, v50p = r["volumen_vs_media10_pct"], r.get("volumen_vs_media50_pct")
    filas = [("الحجم مقابل متوسط 10 جلسات", "—" if v10p is None else pct(v10p, 0), MUTED),
             ("الحجم مقابل متوسط 50 جلسة", "—" if v50p is None else pct(v50p, 0), MUTED),
             ("قيمة التداول", f"{r['valor_negociado_sar'] / 1e9:.1f} مليار ريال", FG),
             ("ATR 14 (نقاط · نسبة)", f"{num(r['atr14'], 0)} · {num(r['atr14_pct'], 2)}%", BLUE),
             ("مدى جلسة اليوم", f"{num(r['rango_dia_pct'], 2)}%", BLUE),
             ("بولينجر العلوي · السفلي", f"{num(r['bb_sup'], 0)} · {num(r['bb_inf'], 0)}", BLUE),
             ("عرض نطاق بولينجر", f"{num(r['bb_ancho_pct'], 1)}%", MUTED), ("أضيق عرض في 6 أشهر", f"{num(r['bb_ancho_min_6m_pct'], 1)}%", MUTED),
             ("موقع الإغلاق داخل النطاق", f"{num(r['pct_b'], 0)}%", GOLD)]
    tabla(f, filas, t, dy=0.072)
    return to_arr(f)


def s_niv(t):
    r = R["tasi"]; cl = r["cierre"]
    f = base_fig(4, f"التحليل الفني (5/{NT}) · خريطة المستويات", titulo_t("niveles", "المستويات القريبة والمسافة إليها"),
                 "المستويات: قمم وقيعان حديثة، متوسطات متحركة، نطاق بولينجر ونقاط الارتكاز الكلاسيكية لجلسة الغد (محسوبة). المسافة من إغلاق اليوم. هذه بيانات وليست إشارات شراء أو بيع.")
    L = [(("مقاومة" if l["tipo"] == "res" else "دعم") + " · " + l["et"], l["valor"]) for l in VJ["tecnico"]["tasi"]["niveles"]]
    L += [("متوسط 20 جلسة", r["sma20"]), ("متوسط 50 جلسة", r["sma50"]), ("متوسط 200 جلسة", r["sma200"]),
          ("بولينجر العلوي", r["bb_sup"]), ("بولينجر السفلي", r["bb_inf"]),
          ("ارتكاز الغد R1", r["pivotes"]["R1"]), ("ارتكاز الغد P", r["pivotes"]["P"]), ("ارتكاز الغد S1", r["pivotes"]["S1"]),
          (f"قمة 52 أسبوعًا ({fd(r['max_52s_fecha'])})", r["max_52s"])]
    L = [x for x in L if abs(x[1] / cl - 1) <= 0.12]; L.append(("إغلاق اليوم", cl))
    seen, M_ = set(), []
    for lab, v in sorted(L, key=lambda x: -x[1]):
        if round(v) in seen and lab != "إغلاق اليوم": continue
        seen.add(round(v)); M_.append((lab, v))
    M_ = M_[:14]; vals = [v for _, v in M_]
    ax = f.add_axes([0.06, 0.12, 0.22, 0.62]); clean(ax); e = ease(t / 0.6)
    for lab, v in M_:
        cc = FG if lab == "إغلاق اليوم" else (NEG if v > cl else TEAL)
        ax.hlines(v, 0, 1, color=cc, lw=4 if lab == "إغلاق اليوم" else 2, alpha=e)
    pad = (max(vals) - min(vals)) * 0.06; ax.set_ylim(min(vals) - pad, max(vals) + pad); ax.set_xlim(0, 1); ax.set_xticks([])
    ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=13)
    dy = min(0.062, 0.62 / max(1, len(M_)))
    for i, (lab, v) in enumerate(M_):
        b = ease((t - 0.2 - i * 0.04) / 0.4)
        if b <= 0: continue
        y = 0.715 - i * dy; hoy = lab == "إغلاق اليوم"; cc = FG if hoy else (NEG if v > cl else TEAL)
        T(f, 0.94, y, lab, FG if hoy else MUTED, 20 if hoy else 18, "bold" if hoy else "normal", alpha=b)
        T(f, 0.56, y, num(v), cc, 20, "bold", ha="left", alpha=b)
        if not hoy: T(f, 0.40, y, pct(v / cl * 100 - 100, 1), cc, 18, ha="left", alpha=b)
    return to_arr(f)


def s_agenda(t):
    G = VJ["agenda"]; f = base_fig(5, "الأجندة", G["titulo"], G["fuente"])
    for i, (d_, e_, s_) in enumerate(G["filas"]):
        b = ease((t - i * 0.12) / 0.4); y = 0.64 - i * 0.095
        T(f, 0.94, y, d_, GOLD, 27, "bold", alpha=b)
        T(f, 0.76, y, e_, FG, 26 if len(e_) <= 55 else 22, alpha=b)
        T(f, 0.06, y, s_, MUTED, 19, ha="left", alpha=b)
    return to_arr(f)


def s_fin(t):
    Fn = VJ["fin"]; f = fig(W, H); a = ease(t / 0.5)
    T(f, 0.94, 0.80, "أسهم السعودية · " + FECHA_TXT, FG, 50, "bold", alpha=a)
    T(f, 0.94, 0.715, "\n".join(textwrap.wrap(Fn["titular"], 52)), GOLD, 32, "bold", alpha=a, linespacing=1.35, va="top")
    T(f, 0.94, 0.56, "ملخص يومي بعد إغلاق كل جلسة في السوق المالية السعودية (تداول)", BLUE, 27, alpha=a)
    f.text(0.94, 0.505, CANAL.replace("https://www.", ""), color=BLUE, fontsize=27, ha="right", weight="bold", alpha=a)
    aviso = ("إخلاء مسؤولية: هذا المحتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية أو دعوة لشراء أو بيع أي ورقة مالية أو استشارة مالية شخصية، "
             "ولا يراعي وضعك أو أهدافك أو مدى تحملك للمخاطر. استشر جهة مرخصة من هيئة السوق المالية قبل أي قرار استثماري. "
             "الأرقام من مصادر عامة مذكورة (" + Fn["fuentes"] + ")، والحسابات الخاصة موضحة بعبارة «محسوب». "
             "التحليل الفني يصف حركة الأسعار في الماضي وليس إشارات شراء أو بيع ولا يتنبأ بالمستقبل. "
             "لا نملك مراكز في الأسهم المذكورة ولا نتلقى أي مقابل من الشركات. الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال، والأداء السابق لا يضمن النتائج المستقبلية. "
             "النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي ومراجعة مع المصادر.")
    T(f, 0.94, 0.07, "\n".join(textwrap.wrap(aviso, 125)), MUTED, 17, linespacing=1.55, alpha=a)
    return with_logo(to_arr(f), LGB, x=110, y=90)


def s_cta(t):
    """Tarjeta final de la campaña de comentarios y suscripción (campana.py; se apaga sola después de campana.HASTA)."""
    f = fig(W, H); a = ease(t / 0.5); b = ease((t - 0.2) / 0.5); c = ease((t - 0.4) / 0.5)
    T(f, 0.94, 0.62, campana.TITULO, GOLD, 72, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0.94 - 0.20, 0.585), 0.20, 0.007, transform=f.transFigure, color=GOLD, alpha=a, figure=f))
    T(f, 0.94, 0.46, campana.LINEA1, FG, 40, "bold", alpha=b)
    T(f, 0.94, 0.33, campana.LINEA2, TEAL, 40, "bold", alpha=c)
    f.text(0.94, 0.24, CANAL.replace("https://www.", ""), color=BLUE, fontsize=32, ha="right", weight="bold", alpha=c)
    return with_logo(to_arr(f), LGB, x=110, y=90)


SEQ = [s_title, s_news, s_fact, s_movers, s_tech, s_tend, s_osc, s_vol, s_niv, s_agenda] + ([s_cta] if campana.activa() else []) + [s_fin]; BIG = {s_title, s_cta, s_fin}
def frame(fn, t):
    arr = fn(t); return arr if fn in BIG else with_logo(arr, LGS, x=60, y=48)


if __name__ == "__main__":
    os.makedirs(AUD, exist_ok=True)
    if PREVIEW:
        for fn in SEQ: Image.fromarray(frame(fn, 1.0)).save(os.path.join(AUD, "prev_" + fn.__name__ + ".png"))
        sys.exit()
    texto = lambda fn: campana.VOZ if fn is s_cta else VJ["voz"][fn.__name__]
    clips = [voz(texto(fn), os.path.join(AUD, fn.__name__ + ".wav")) for fn in SEQ]; sr = clips[0][1]
    LEAD, TAIL = 0.12, 0.45
    durs = [LEAD + len(a) / sr + TAIL for a, _ in clips]; durs[0] += 0.4; durs[-1] += 1.5
    print("duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if sum(durs) > MAXS: sys.exit(f"Video demasiado largo: {sum(durs):.1f} s (máx. {MAXS}). Acorta la locución"
                                 + (" (la tarjeta de comentarios y suscripción de campana.py suma unos 10 s)." if s_cta in SEQ else "."))
    leads = [LEAD + (0.4 if j == 0 else 0) for j in range(len(SEQ))]
    times, t0 = render([lambda t, fn=fn: frame(fn, t) for fn in SEQ], durs, ([a for a, _ in clips], leads), sr, W, H, FPS, OUT,
                       os.path.join(AUD, "video-silent.mp4"), os.path.join(AUD, "full.wav"))
    json.dump([(fn.__name__, tt) for fn, tt in zip(SEQ, times)], open(os.path.join(DIR, "times.json"), "w")); print("listo", round(t0, 1), "s", OUT)
