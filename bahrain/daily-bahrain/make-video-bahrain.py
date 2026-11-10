# Daily Arabic video of Bahrain Bourse (Bahrain All Share Index): 1080p, Piper voice ar_JO-kareem, Bahrain AI Stocks logo.
# Usage: AUD=<scratch> python3 make-video-bahrain.py <day folder> [preview]
#   The day folder has market-bahrain.json (data/market-<date>-bahrain.json from branch daily-data-bahrain) and video-bahrain.json
#   (screen texts and voice; see sample-2026-11-05-bahrain/). Writes <folder>/video-<date>-bahrain.mp4 and <folder>/times-bahrain.json (chapters).
import os, sys, json, numpy as np, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import importlib.util
def _load(n):
    sp = importlib.util.spec_from_file_location(n.replace("-", "_"), os.path.join(HERE, n + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
_C = _load("common-bahrain"); globals().update({k: getattr(_C, k) for k in dir(_C) if not k.startswith("__")})
_T = _load("technical-bahrain"); calc, INDICE, MESES, TZ, fecha_ar = _T.calc, _T.INDICE, _T.MESES, _T.TZ, _T.fecha_ar
DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
W, H, FPS = 1920, 1080, 30
AUD = os.environ.get("AUD", "aud")
M = json.load(open(f"{DIR}/market-bahrain.json")); VJ = json.load(open(f"{DIR}/video-bahrain.json"))
R, A = calc(M, VJ.get("nombres")); FECHA = dt.date.fromisoformat(R["fecha"]); FECHA_TXT = fecha_ar(FECHA)
OUT = f"{DIR}/video-{R['fecha']}-bahrain.mp4"
SECS = ["الأخبار", "التحليل الأساسي", "الأسهم", "التحليل الفني", "الأجندة"]; NS = len(SECS)
LG = load_logo(130); LGS = load_logo(95); LGB = load_logo(230)
NB = 126  # unas 6 meses de sesiones


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)


def base_fig(n, kicker, title, sub):
    f = fig(W, H)
    T(f, 0.94, 0.90, kicker, GOLD, 24, "bold")
    T(f, 0.94, 0.80, title, FG, 44 if len(title) <= 50 else 38, "bold")
    T(f, 0.105, 0.92, f"{n}/{NS} · {SECS[n - 1]}", MUTED, 19, "bold", ha="left")
    T(f, 0.105, 0.885, "أسهم البحرين · " + FECHA_TXT, DIM, 16, "bold", ha="left")
    w = 0.88 / NS
    for i in range(NS):  # barra de progreso de derecha a izquierda
        f.patches.append(plt.Rectangle((0.94 - (i + 1) * w + 0.008, 0.975), w - 0.008, 0.008, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))
    T(f, 0.94, 0.04, "\n".join(textwrap.wrap(sub, 150)), MUTED, 16, linespacing=1.4)
    return f


def s_title(t):
    f = fig(W, H); a = ease(t / 0.6); r = R["bax"]; up = r["var_pct"] >= 0; cc = TEAL if up else NEG
    T(f, 0.94, 0.89, "أسهم البحرين · ملخص جلسة بورصة البحرين", GOLD, 28, "bold", alpha=a)
    f.patches.append(plt.Rectangle((0, 0.70), 1.0, 0.14, transform=f.transFigure, color=BAND, alpha=a, figure=f))
    T(f, 0.94, 0.77, "جلسة " + FECHA_TXT, FG, 66, "bold", va="center", alpha=a)
    # right: index close, change in % and points; left: intraday curve
    T(f, 0.94, 0.615, INDICE["bax"], MUTED, 30, "bold", alpha=a)
    f.text(0.94, 0.50, num(r["cierre"]), color=FG, fontsize=92, weight="bold", ha="right", alpha=a)
    f.text(0.94, 0.42, f"{pct(r['var_pct'])}   ({r['var_pts']:+,.2f})", color=cc, fontsize=40, weight="bold", ha="right", alpha=a)
    b = ease((t - 0.2) / 0.5)
    T(f, 0.94, 0.33, VJ.get("linea_sesion", f"ارتفع {r['suben']} · انخفض {r['bajan']} · دون تغيير {r['sin_cambio']}"), MUTED, 24, "bold", alpha=b)
    if VJ.get("linea_valor"): T(f, 0.94, 0.275, VJ["linea_valor"], FG, 26, "bold", alpha=b)
    I = [v for v in M["bax_intradia"]["velas"] if dt.datetime.fromtimestamp(v["t"], TZ).date() == FECHA]
    IC = np.array([v["c"] for v in I]); prev = r["anterior"]
    if len(IC) > 2:
        ax = f.add_axes([0.06, 0.20, 0.50, 0.40]); clean(ax)
        n = max(2, int(len(IC) * ease(t))); hrs = [dt.datetime.fromtimestamp(v["t"], TZ) for v in I]
        x = np.array([(h - hrs[0]).total_seconds() / 60 for h in hrs])  # minutes since the open (trades are irregular)
        ax.step(x[:n], IC[:n], where="post", color=cc, lw=3.5); ax.axhline(prev, color=DIM, lw=1.5, ls="--")
        ax.fill_between(x[:n], IC[:n], prev, step="post", color=cc, alpha=0.12)
        lo_, hi_ = min(IC.min(), prev, r["min_dia"]), max(IC.max(), prev, r["max_dia"]); pad = (hi_ - lo_) * 0.15
        ax.set_xlim(0, x[-1]); ax.set_ylim(lo_ - pad, hi_ + pad); ax.set_yticks([])
        h0 = hrs[0].replace(minute=0, second=0); tk = [h0 + dt.timedelta(hours=j) for j in range(1, 5) if h0 + dt.timedelta(hours=j) <= hrs[-1]]
        ax.set_xticks([(h - hrs[0]).total_seconds() / 60 for h in tk], [h.strftime("%H:%M") for h in tk]); ax.tick_params(labelsize=15)
        T(f, 0.56, 0.615, "حركة المؤشر العام خلال الجلسة (بتوقيت المنامة)", MUTED, 18)
        T(f, 0.06, 0.615, "الإغلاق السابق " + num(prev), MUTED, 16, ha="left")
    if VJ.get("titular"): T(f, 0.94, 0.11, VJ["titular"], BLUE, 30, "bold", alpha=ease((t - 0.3) / 0.5))
    T(f, 0.94, 0.04, VJ.get("title_fuente", "البيانات: مباشر (إغلاق " + R["fecha"] + ")"), MUTED, 16)
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
    CX = dict(R["contexto"]); CX["BAHRAIN:BHBX"] = {"change": R["bax"]["var_pct"]}
    L = [(n, (CX[v]["change"] if isinstance(v, str) else v)) for n, v in F["bolsas"] if not isinstance(v, str) or (v in CX and CX[v].get("change") is not None)]
    ax = f.add_axes([0.20, 0.13, 0.25, 0.58]); clean(ax); e = ease(t)
    y = np.arange(len(L))[::-1]; v = [x[1] for x in L]; lim = max(abs(min(v)), abs(max(v))) * 1.5
    ax.barh(y, [x * e for x in v], color=[(GOLD if "البحرين" in n else (TEAL if x > 0 else NEG)) for n, x in L], height=0.6)
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
    V_ = VJ["valores"]; MOT = V_.get("motivos", {}); sub = R["bax"]["suben"]; baj = R["bax"]["bajan"]
    f = base_fig(3, "الأسهم الأكثر ارتفاعًا وانخفاضًا في بورصة البحرين", V_.get("titulo", f"ارتفع {sub} سهمًا وانخفض {baj}"), V_["fuente"])
    mx = max([abs(x["cambio"]) for x in R["mejores"] + R["peores"]] + [0.01])
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
        if len(lst) < 5:  # thin market: say so instead of padding the list
            T(f, xr, 0.635 - len(lst) * 0.098, f"لم يتحرك سوى {len(lst)} في هذا الاتجاه" if lst else "لا يوجد", MUTED, 19, alpha=ease((t - 0.4) / 0.4))
    if V_.get("extra"): T(f, 0.94, 0.135, V_["extra"], BLUE, 24, "bold", alpha=ease((t - 0.5) / 0.4))
    return to_arr(f)


def tech(k, n_sec, t):
    TJ = VJ["tecnico"][k]; r = R[k]; a_ = A[k]
    f = base_fig(4, "التحليل الفني · " + INDICE[k], TJ["titulo"],
                 "شموع يومية لآخر 6 أشهر من مباشر (مؤشر البحرين العام BHBX). المتوسطات والدعوم والمقاومات (قمم وقيعان حديثة) و RSI والعشوائي: محسوبة. حجم التداول مقابل متوسط 10 جلسات: محسوب. هذه بيانات وليست إشارات شراء أو بيع.")
    dates, o, hi, lo, c, S50, S200 = (a_[x] for x in ("dates", "o", "hi", "lo", "c", "S50", "S200"))
    n = len(c); idx = np.arange(n - NB, n); x = np.arange(NB); m = max(2, int(NB * ease(t / 0.8)))
    ax = f.add_axes([0.05, 0.36, 0.56, 0.38]); clean(ax)
    span = hi[idx].max() - lo[idx].min()
    for j in range(m):
        i = idx[j]; cc = TEAL if c[i] >= o[i] else NEG
        ax.vlines(j, lo[i], hi[i], color=cc, lw=1.2); ax.add_patch(plt.Rectangle((j - 0.35, min(o[i], c[i])), 0.7, max(abs(c[i] - o[i]), span * 0.002), color=cc))
    ax.plot(x[:m], S50[idx][:m], color=BLUE, lw=2.5, label=ar("متوسط 50 جلسة"))
    ax.plot(x[:m], S200[idx][:m], color=GOLD, lw=2.5, label=ar("متوسط 200 جلسة"))
    al = ease((t - 0.6) / 0.4); LEV = [l for l in (TJ.get("niveles") or r["niveles"]) if lo[idx].min() - span * 0.25 <= l["valor"] <= hi[idx].max() + span * 0.25]
    for l in LEV:
        cc = NEG if l["tipo"] == "res" else TEAL
        ax.axhline(l["valor"], color=cc, lw=1.1, ls="--", alpha=al)
    vals = [l["valor"] for l in LEV]
    ax.set_xlim(-1, NB); ax.set_ylim(min(lo[idx].min(), np.nanmin(S200[idx]), *vals) - span * 0.05, max(hi[idx].max(), np.nanmax(S200[idx]), *vals) + span * 0.05)
    tk = [j for j in range(1, NB) if dates[idx[j]].month != dates[idx[j - 1]].month]
    if not tk or tk[0] > 12: tk = [0] + tk  # label the first month only if it does not collide with the next one
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


def s_tech(t): return tech("bax", 4, t)


def _tabla(f, filas, t, y0=0.715, dy=0.063, xv=0.67):
    for i, (lab, val, cc) in enumerate(filas):
        b = ease((t - 0.3 - i * 0.05) / 0.4)
        if b <= 0: continue
        y = y0 - i * dy
        T(f, 0.94, y, lab, MUTED, 19, alpha=b)
        T(f, xv, y, val, cc, 21, "bold", ha="left", alpha=b)


def _eje_meses(ax, dates, idx):
    tk = [j for j in range(1, NB) if dates[idx[j]].month != dates[idx[j - 1]].month]
    if not tk or tk[0] > 12: tk = [0] + tk
    ax.set_xticks(tk, [ar(MESES[dates[idx[j]].month - 1]) for j in tk]); ax.tick_params(labelsize=15)


def s_tech_mom(t):
    """Momentum: RSI 14, stochastic and MACD (12, 26, 9) of the index over 6 months."""
    TJ = VJ["tecnico"].get("momentum", {}); r = R["bax"]; mo = r["momentum"]; a_ = A["bax"]
    f = base_fig(4, "التحليل الفني · الزخم", TJ.get("titulo", f"القوة النسبية {num(r['rsi14'], 1)} · MACD {num(mo['macd'], 1)}"),
                 "RSI 14 والعشوائي (14، 3، 3) و MACD (12، 26، 9): محسوبة من شموع مباشر اليومية لمؤشر البحرين العام. هذه بيانات وليست إشارات شراء أو بيع.")
    n = len(a_["c"]); idx = np.arange(n - NB, n); x = np.arange(NB); m = max(2, int(NB * ease(t / 0.8)))
    ax = f.add_axes([0.05, 0.53, 0.56, 0.21]); clean(ax)
    ax.axhspan(70, 100, color=NEG, alpha=0.07); ax.axhspan(0, 30, color=TEAL, alpha=0.07)
    for lv in (30, 50, 70): ax.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax.plot(x[:m], a_["RSI"][idx][:m], color=BLUE, lw=2.4, label="RSI 14")
    ax.set_xlim(-1, NB); ax.set_ylim(0, 100); ax.set_xticks([]); ax.yaxis.tick_right(); ax.set_yticks([30, 50, 70]); ax.tick_params(axis="y", labelsize=14)
    ax.legend(frameon=False, labelcolor=FG, fontsize=15, loc="upper left")
    ax2 = f.add_axes([0.05, 0.36, 0.56, 0.15]); clean(ax2)
    for lv in (20, 80): ax2.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax2.plot(x[:m], a_["K"][idx][:m], color=TEAL, lw=1.8, label="%K"); ax2.plot(x[:m], a_["D"][idx][:m], color=NEG, lw=1.8, label="%D")
    ax2.set_xlim(-1, NB); ax2.set_ylim(0, 100); ax2.set_xticks([]); ax2.yaxis.tick_right(); ax2.set_yticks([20, 80]); ax2.tick_params(axis="y", labelsize=14)
    ax2.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper left", ncol=2)
    ax3 = f.add_axes([0.05, 0.13, 0.56, 0.21]); clean(ax3)
    hh = a_["HIST"][idx]
    ax3.bar(x[:m], hh[:m], color=[TEAL if v >= 0 else NEG for v in hh[:m]], width=0.8, alpha=0.6)
    ax3.plot(x[:m], a_["MACD"][idx][:m], color=BLUE, lw=2, label="MACD"); ax3.plot(x[:m], a_["SIG"][idx][:m], color=GOLD, lw=1.8, label=ar("خط الإشارة"))
    ax3.axhline(0, color=DIM, lw=0.8); ax3.set_xlim(-1, NB); ax3.yaxis.tick_right(); ax3.tick_params(axis="y", labelsize=13)
    ax3.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper right", ncol=2); _eje_meses(ax3, a_["dates"], idx)
    hist_txt = ("يتسع" if abs(mo["macd_hist"]) > abs(mo["macd_hist_prev"]) else "يضيق") + (" موجبًا" if mo["macd_hist"] >= 0 else " سالبًا")
    filas = [("RSI 14 اليوم", num(r["rsi14"], 1), BLUE),
             ("RSI قبل 5 جلسات", num(mo["rsi_5"], 1), MUTED),
             ("RSI قبل 20 جلسة", num(mo["rsi_20"], 1), MUTED),
             ("أدنى RSI في 6 أشهر", num(mo["rsi_min_6m"], 1), MUTED),
             ("جلسات متتالية دون 30", str(mo["rsi_sesiones_bajo_30"]) if mo["rsi_sesiones_bajo_30"] else "لا يوجد", TEAL),
             ("العشوائي %K / %D", f"{num(r['estoc_k'], 0)} / {num(r['estoc_d'], 0)}" + ("  · %K فوق %D" if mo["estoc_k_sobre_d"] else "  · %K دون %D"), TEAL),
             ("MACD / خط الإشارة", f"{num(mo['macd'], 2)} / {num(mo['macd_senal'], 2)}", BLUE),
             ("مدرج MACD", f"{num(mo['macd_hist'], 2)}  · {hist_txt}", TEAL if mo["macd_hist"] >= 0 else NEG)]
    _tabla(f, filas, t)
    return to_arr(f)


def s_tech_vol(t):
    """Volume against its 10 and 50-session averages, ATR and performance over several horizons."""
    TJ = VJ["tecnico"].get("volumen", {}); r = R["bax"]; mo = r["momentum"]; a_ = A["bax"]
    f = base_fig(4, "التحليل الفني · الحجم والتقلب والأداء", TJ.get("titulo", f"{'ارتفاع' if mo['perf_ytd'] >= 0 else 'تراجع'} {num(abs(mo['perf_ytd']), 1)}% منذ بداية العام"),
                 "الحجم ومتوسطاه و ATR 14 والتقلب السنوي (20 جلسة) والأداء: محسوبة من بيانات مباشر لمؤشر البحرين العام. هذه بيانات وليست إشارات شراء أو بيع.")
    n = len(a_["c"]); idx = np.arange(n - NB, n); x = np.arange(NB); m = max(2, int(NB * ease(t / 0.8)))
    ax = f.add_axes([0.05, 0.40, 0.56, 0.34]); clean(ax)
    vv = a_["vol"][idx] / 1e6
    ax.bar(x[:m], vv[:m], color=MUTED, width=0.8, alpha=0.55)
    ax.plot(x[:m], a_["V10"][idx][:m] / 1e6, color=BLUE, lw=2.2, label=ar("متوسط 10 جلسات"))
    ax.plot(x[:m], a_["V50"][idx][:m] / 1e6, color=GOLD, lw=2.2, label=ar("متوسط 50 جلسة"))
    ax.set_xlim(-1, NB); ax.set_xticks([]); ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=13)
    ax.set_ylim(0, np.nanpercentile(vv, 98) * 1.25)
    ax.legend(frameon=False, labelcolor=FG, fontsize=15, loc="upper left", ncol=2)
    T(f, 0.05, 0.755, "حجم التداول (مليون سهم)", MUTED, 16, ha="left")
    ax2 = f.add_axes([0.05, 0.13, 0.56, 0.22]); clean(ax2)
    ax2.plot(x[:m], a_["ATR"][idx][:m], color=NEG, lw=2.2, label="ATR 14")
    ax2.set_xlim(-1, NB); ax2.yaxis.tick_right(); ax2.tick_params(axis="y", labelsize=13)
    ax2.legend(frameon=False, labelcolor=FG, fontsize=14, loc="lower left"); _eje_meses(ax2, a_["dates"], idx)
    vm = lambda v: "—" if v is None else f"{v / 1e6:,.2f} م"
    filas = [("حجم اليوم", vm(mo["vol_hoy"]), FG), ("متوسط 10 / 50 جلسة", f"{vm(mo['vol_media10'])} / {vm(mo['vol_media50'])}", BLUE),
             ("ATR 14", f"{num(mo['atr14'], 2)} · {num(mo['atr14_pct'], 2)}%", NEG),
             ("التقلب السنوي (20 جلسة)", f"{num(mo['volatilidad20_anual_pct'], 1)}%", NEG),
             ("عن قمة 52 أسبوعًا", pct(mo["dist_max52_pct"], 1), NEG), ("عن قاع 52 أسبوعًا", pct(mo["dist_min52_pct"], 1), TEAL)]
    _tabla(f, filas, t, y0=0.715, dy=0.058)
    # performance bars, right to left
    P = [("أسبوع", mo["perf_1s"]), ("شهر", mo["perf_1m"]), ("3 أشهر", mo["perf_3m"]), ("6 أشهر", mo["perf_6m"]), ("منذ بداية العام", mo["perf_ytd"])]
    P = [(l, v) for l, v in P if v is not None]; mx = max([abs(v) for _, v in P] + [0.5])
    T(f, 0.94, 0.36, "الأداء (محسوب)", GOLD, 21, "bold", alpha=ease((t - 0.5) / 0.4))
    for i, (l, v) in enumerate(P):
        b = ease((t - 0.55 - i * 0.05) / 0.35)
        if b <= 0: continue
        y = 0.31 - i * 0.04; cx = 0.78; bw = 0.10 * abs(v) / mx * b; cc = TEAL if v >= 0 else NEG
        T(f, 0.94, y, l, MUTED, 17, alpha=b)
        f.patches.append(plt.Rectangle((cx if v >= 0 else cx - bw, y - 0.002), bw, 0.024, transform=f.transFigure, color=cc, figure=f))
        f.text(cx + bw + 0.006 if v >= 0 else cx - bw - 0.006, y, pct(v, 1), color=FG, fontsize=16, weight="bold", ha="left" if v >= 0 else "right", alpha=b)
    return to_arr(f)


def s_tech_acc(t):
    """Technical snapshot of the biggest stocks of the index (TradingView scanner)."""
    TJ = VJ["tecnico"].get("acciones", {}); L = R["tecnico_acciones"]
    f = base_fig(4, "التحليل الفني · أكبر أسهم المؤشر", TJ.get("titulo", "المؤشرات الفنية لأكبر الأسهم"),
                 "أكبر أسهم المؤشر بالقيمة السوقية. RSI 14 والعشوائي %K والمتوسطات والأداء: TradingView؛ البعد عن المتوسطات: محسوب. هذه بيانات وليست إشارات شراء أو بيع.")
    cols = [(0.94, "السهم", "right"), (0.66, "الإغلاق", "left"), (0.57, "اليوم", "left"), (0.48, "RSI 14", "left"), (0.40, "%K", "left"),
            (0.32, "عن م 50", "left"), (0.23, "عن م 200", "left"), (0.13, "3 أشهر", "left")]
    for xc, h, ha in cols: T(f, xc if ha == "right" else xc, 0.70, h, GOLD, 20, "bold", ha="right" if ha == "right" else "right")
    sg = lambda v: MUTED if v is None else (TEAL if v >= 0 else NEG)
    rc = lambda v: MUTED if v is None else BLUE  # neutral colour: levels are data, not signals
    for i, s in enumerate(L):
        b = ease((t - 0.15 - i * 0.07) / 0.4)
        if b <= 0: continue
        y = 0.63 - i * 0.075
        T(f, 0.94, y, s["nombre"], FG, 22, "bold", alpha=b); T(f, 0.94, y - 0.03, s["ticker"], MUTED, 14, alpha=b)
        vals = [(num(s["cierre"], 3), FG), (pct(s["cambio"]) if s["cambio"] is not None else "—", sg(s["cambio"])),
                (num(s["rsi"], 0) if s["rsi"] is not None else "—", rc(s["rsi"])), (num(s["estoc_k"], 0) if s["estoc_k"] is not None else "—", rc(s["estoc_k"])),
                (pct(s["dist_sma50_pct"], 1) if s["dist_sma50_pct"] is not None else "—", sg(s["dist_sma50_pct"])),
                (pct(s["dist_sma200_pct"], 1) if s["dist_sma200_pct"] is not None else "—", sg(s["dist_sma200_pct"])),
                (pct(s["perf_3m"], 1) if s["perf_3m"] is not None else "—", sg(s["perf_3m"]))]
        for (xc, _, _), (v, cc) in zip(cols[1:], vals):
            f.text(xc, y, v, color=cc, fontsize=21, weight="bold", ha="right", alpha=b)
    if TJ.get("nota"): T(f, 0.94, 0.15, TJ["nota"], BLUE, 21, "bold", alpha=ease((t - 0.6) / 0.4))
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
    T(f, 0.94, 0.80, "أسهم البحرين · " + FECHA_TXT, FG, 50, "bold", alpha=a)
    T(f, 0.94, 0.715, "\n".join(textwrap.wrap(Fn["titular"], 52)), GOLD, 32, "bold", alpha=a, linespacing=1.35, va="top")
    T(f, 0.94, 0.56, "ملخص يومي بعد إغلاق كل جلسة في بورصة البحرين", BLUE, 27, alpha=a)
    f.text(0.94, 0.505, CANAL.replace("https://www.", ""), color=BLUE, fontsize=27, ha="right", weight="bold", alpha=a)
    if cta_activa(FECHA): T(f, 0.94, 0.42, "◀ " + CTA_TXT, FG, 30, "bold", alpha=ease((t - 0.3) / 0.5))
    aviso = ("إخلاء مسؤولية: هذا المحتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية أو دعوة لشراء أو بيع أي ورقة مالية أو استشارة مالية شخصية، "
             "ولا يراعي وضعك أو أهدافك أو مدى تحملك للمخاطر. استشر جهة مرخصة من مصرف البحرين المركزي قبل أي قرار استثماري. "
             "الأرقام من مصادر عامة مذكورة (" + Fn["fuentes"] + ")، والحسابات الخاصة موضحة بعبارة «محسوب». "
             "التحليل الفني يصف حركة الأسعار في الماضي وليس إشارات شراء أو بيع ولا يتنبأ بالمستقبل. "
             "لا نملك مراكز في الأسهم المذكورة ولا نتلقى أي مقابل من الشركات. الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال، والأداء السابق لا يضمن النتائج المستقبلية. "
             "النص والرسوم والصوت (صوت اصطناعي) من إعداد أدوات الذكاء الاصطناعي ومراجعة مع المصادر.")
    T(f, 0.94, 0.07, "\n".join(textwrap.wrap(aviso, 125)), MUTED, 17, linespacing=1.55, alpha=a)
    return with_logo(to_arr(f), LGB, x=110, y=90)


SEQ = [s_title, s_news, s_fact, s_movers, s_tech, s_tech_mom, s_tech_vol] + ([s_tech_acc] if R["tecnico_acciones"] else []) + [s_agenda, s_fin]
BIG = {s_title, s_fin}
def frame(fn, t):
    arr = fn(t); return arr if fn in BIG else with_logo(arr, LGS, x=60, y=48)


if __name__ == "__main__":
    os.makedirs(AUD, exist_ok=True)
    if PREVIEW:
        for fn in SEQ: Image.fromarray(frame(fn, 1.0)).save(os.path.join(AUD, "prev_" + fn.__name__ + ".png"))
        sys.exit()
    if cta_activa(FECHA): VJ["voz"]["s_fin"] = VJ["voz"]["s_fin"].rstrip() + " " + CTA_VOZ
    clips = [voz(VJ["voz"][fn.__name__], os.path.join(AUD, fn.__name__ + ".wav")) for fn in SEQ]; sr = clips[0][1]
    LEAD, TAIL = 0.12, 0.45
    durs = [LEAD + len(a) / sr + TAIL for a, _ in clips]; durs[0] += 0.4; durs[-1] += 1.5
    print("duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if sum(durs) > 300: sys.exit(f"Video demasiado largo: {sum(durs):.1f} s (máx. 300, 5 minutos). Acorta la locución.")
    leads = [LEAD + (0.4 if j == 0 else 0) for j in range(len(SEQ))]
    times, t0 = render([lambda t, fn=fn: frame(fn, t) for fn in SEQ], durs, ([a for a, _ in clips], leads), sr, W, H, FPS, OUT,
                       os.path.join(AUD, "video-silent.mp4"), os.path.join(AUD, "full.wav"))
    json.dump([(fn.__name__, tt) for fn, tt in zip(SEQ, times)], open(os.path.join(DIR, "times-bahrain.json"), "w")); print("listo", round(t0, 1), "s", OUT)
