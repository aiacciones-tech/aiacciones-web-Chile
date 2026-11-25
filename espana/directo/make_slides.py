# Diapositivas y guion del directo semanal «El IBEX de la semana, en directo» de @AIAccionesEspaña (viernes 17:45 Madrid;
# Daniel lo eligió el 24-nov-2026 y lo emite él con OBS o el móvil). Lee el mercado-<fecha>.json del vídeo diario (rama datos-diario-es)
# y semana.json (noticias, agenda y notas que escribe Claude con fuentes). Escribe PNG 1920x1080, un PDF con todas y guion.md.
# Uso: python3 espana/directo/make_slides.py <mercado.json> <semana.json> <carpeta de salida>
import json, os, sys, datetime as dt, zoneinfo
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "educativo")); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun_leccion import *          # marca: colores, logo, fig, to_arr, with_logo, clean, sma
from tecnico import NOMBRES

MER = json.load(open(sys.argv[1])); SEM = json.load(open(sys.argv[2])); OUT = os.path.abspath(sys.argv[3]); os.makedirs(OUT, exist_ok=True)
Z = zoneinfo.ZoneInfo("Europe/Madrid"); W, H = 1920, 1080; XL = 0.05
fecha = lambda t: dt.datetime.fromtimestamp(t, Z).date()
num = lambda v, d=2: f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
pct = lambda v, d=2: ("+" if v > 0 else "−" if v < 0 else "") + num(abs(v), d) + " %"
cpct = lambda v: ACC if v > 0 else NEG if v < 0 else MUTED
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
fl = lambda d: f"{DIAS[d.weekday()]} {d.day} de {MESES_L[d.month - 1]}"

# ---------- datos de la semana (calculado de los cierres diarios de Yahoo; contexto: TradingView) ----------
IB = MER["ibex_diario"]["velas"]; HOY = fecha(IB[-1]["t"]); LUN = HOY - dt.timedelta(days=HOY.weekday())
SEMV = [v for v in IB if fecha(v["t"]) >= LUN]; PREV = [v for v in IB if fecha(v["t"]) < LUN][-1]
CIERRE = IB[-1]["c"]; SEM_P = (CIERRE / PREV["c"] - 1) * 100; DIA_P = (CIERRE / IB[-2]["c"] - 1) * 100
TVI = MER.get("tv", {}).get("BME:IBC", {})
ANIO = [v for v in IB if fecha(v["t"]).year < HOY.year]; YTD = (CIERRE / ANIO[-1]["c"] - 1) * 100 if ANIO else TVI.get("Perf.YTD")


def semana_valor(tk):
    V = MER["valores"].get(tk, {}).get("velas", [])
    a = [v for v in V if fecha(v["t"]) < LUN]; b = [v for v in V if fecha(v["t"]) <= HOY]
    if not a or not b: return None
    c = b[-1]["c"]
    if fecha(b[-1]["t"]) != HOY:   # Yahoo a veces aún no tiene la vela del día: cierre de TradingView si es de hoy
        t = MER.get("tv", {}).get("BME:" + tk, {})
        if not t.get("close") or not t.get("time") or fecha(t["time"]) != HOY: return None
        c = t["close"]
    return (c / a[-1]["c"] - 1) * 100, c


VAL = sorted(((tk, *r) for tk in MER["valores"] if (r := semana_valor(tk))), key=lambda x: -x[1])
SUBEN = sum(1 for x in VAL if x[1] > 0)
CTX = [("Euro Stoxx 50", "TVC:SX5E"), ("DAX (Alemania)", "XETR:DAX"), ("CAC 40 (Francia)", "TVC:CAC40"), ("FTSE MIB (Italia)", "FTSEMIB:FTSEMIB"),
       ("S&P 500 (EE. UU.)", "SP:SPX"), ("Nasdaq 100", "NASDAQ:NDX"), ("Euro/dólar", "FX:EURUSD"), ("Brent (dólares)", "TVC:UKOIL"), ("Oro (dólares)", "TVC:GOLD")]
TV = MER.get("tv", {})
ES, DE = TV.get("TVC:ES10Y", {}).get("close"), TV.get("TVC:DE10Y", {}).get("close")
PRIMA = round((ES - DE) * 100) if ES and DE else None
GUION = []


def T(f, x, y, s, c=FG, fs=30, w="normal", ha="left", **k): return f.text(x, y, s, color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def cab(f, k, titulo, n):
    T(f, XL, 0.93, f"EL IBEX DE LA SEMANA · EN DIRECTO · {fl(HOY).upper()}", ACC, 22, "bold")
    T(f, 0.95, 0.93, f"{n}/{TOT}", MUTED, 22, "bold", ha="right")
    T(f, XL, 0.875, k.upper(), ACC2, 24, "bold"); T(f, XL, 0.80, titulo, FG, 46, "bold")
    T(f, XL, 0.025, "AIAcciones España · contenido informativo, no es una recomendación de inversión · datos: Yahoo Finance y TradingView; variaciones: calculado",
      MUTED, 15)


def guardar(f, nombre, logo=True):
    a = to_arr(f); a = with_logo(a, load_logo(300), x=W - 300 - 50, y=H - 130) if logo else a
    p = f"{OUT}/{nombre}.png"; Image.fromarray(a).save(p); return p


S = []
TOT = 8


def s_portada():
    f = fig(W, H)
    T(f, XL, 0.82, "EN DIRECTO · CADA VIERNES A LAS 17:45", NEG, 30, "bold")
    f.patches.append(plt.Rectangle((0, 0.55), 1, 0.2, transform=f.transFigure, color=ACC, figure=f))
    T(f, XL, 0.65, "El IBEX de la semana", BG, 96, "bold", va="center")
    T(f, XL, 0.45, fl(HOY).capitalize() + f" de {HOY.year}", FG, 44, "bold")
    T(f, XL, 0.36, f"IBEX 35: {num(CIERRE, 1)} puntos · {pct(SEM_P)} en la semana", cpct(SEM_P), 44, "bold")
    T(f, XL, 0.24, "Escribe tus preguntas en el chat: las respondemos al final", ACC2, 34, "bold")
    T(f, XL, 0.10, "Contenido informativo. No es una recomendación de inversión ni asesoramiento personalizado.", MUTED, 24)
    a = with_logo(to_arr(f), load_logo(520), x=W - 520 - 80, y=60); p = f"{OUT}/01-portada.png"; Image.fromarray(a).save(p)
    GUION.append(("Portada", [f"Bienvenida: «El IBEX de la semana, en directo», {fl(HOY)}.",
                              f"Titular: el IBEX 35 cierra la semana en {num(CIERRE, 1)} puntos, {pct(SEM_P)} (calculado frente al cierre del {fl(fecha(PREV['t']))}).",
                              "Pide preguntas en el chat; se responden al final. Recuerda: contenido informativo, no recomendación."]))
    return p


def s_ibex():
    f = fig(W, H); cab(f, "El índice", f"IBEX 35: {pct(SEM_P)} en la semana", 2)
    kp = [(num(CIERRE, 1), "Cierre (puntos)", FG), (pct(DIA_P), "Hoy", cpct(DIA_P)), (pct(SEM_P), "Semana", cpct(SEM_P))]
    if YTD is not None: kp.append((pct(YTD), f"En {HOY.year}", cpct(YTD)))
    for k, (v, lab, c) in enumerate(kp):
        x = XL + k * 0.225; f.patches.append(plt.Rectangle((x, 0.56), 0.21, 0.16, transform=f.transFigure, color=PANEL, figure=f))
        T(f, x + 0.015, 0.645, v, c, 50, "bold"); T(f, x + 0.015, 0.585, lab, MUTED, 22, "bold")
    ax = f.add_axes([XL + 0.03, 0.12, 0.5, 0.38]); clean(ax)
    xs = [PREV] + SEMV; ys = [v["c"] for v in xs]
    ax.plot(range(len(xs)), ys, color=ACC2, lw=4, marker="o", ms=10)
    ax.set_xticks(range(len(xs)), ["vie. ant."] + [DIAS[fecha(v["t"]).weekday()][:3] + "." for v in SEMV])
    ax.tick_params(labelsize=18); ax.grid(axis="y", color=DIM, lw=0.6)
    filas = []
    for a, b in zip(xs[:-1], xs[1:]):
        d_ = fecha(b["t"]); filas.append((f"{DIAS[d_.weekday()].capitalize()} {d_.day}", num(b["c"], 1), (b["c"] / a["c"] - 1) * 100))
    for k, (d, c, p) in enumerate(filas):
        y = 0.45 - k * 0.065; T(f, 0.62, y, d, FG, 26, "bold"); T(f, 0.84, y, c, MUTED, 26, ha="right"); T(f, 0.95, y, pct(p), cpct(p), 26, "bold", ha="right")
    p = guardar(f, "02-ibex")
    GUION.append(("El IBEX 35", [f"Cierre: {num(CIERRE, 1)} puntos; hoy {pct(DIA_P)}; semana {pct(SEM_P)}" + (f"; en {HOY.year}, {pct(YTD)}." if YTD is not None else "."),
                                  "Día a día: " + "; ".join(f"{d} {pct(p)}" for d, c, p in filas) + ".",
                                  f"Amplitud: {SUBEN} de {len(VAL)} valores suben en la semana (calculado)."] + SEM.get("notas", {}).get("ibex", [])))
    return p


def s_valores():
    f = fig(W, H); cab(f, "Los valores", "Mejor y peor semana del IBEX 35", 3)
    top, bot = VAL[:5], VAL[-5:][::-1]
    for j, (grupo, tit, c) in enumerate([(top, "Mejor semana", ACC), (bot, "Peor semana", NEG)]):
        x0 = XL + j * 0.46; T(f, x0, 0.70, tit.upper(), c, 28, "bold")
        m = max(abs(x[1]) for x in VAL[:5] + VAL[-5:]) or 1
        for k, (tk, p, cierre) in enumerate(grupo):
            y = 0.61 - k * 0.095
            T(f, x0, y, NOMBRES.get(tk, tk), FG, 28, "bold", va="center"); T(f, x0 + 0.40, y, pct(p), cpct(p), 28, "bold", ha="right", va="center")
            f.patches.append(plt.Rectangle((x0, y - 0.04), 0.40 * abs(p) / m, 0.012, transform=f.transFigure, color=cpct(p), figure=f))
    T(f, XL, 0.13, f"{SUBEN} de {len(VAL)} valores del IBEX 35 suben en la semana · variación frente al cierre del {fl(fecha(PREV['t']))} (calculado)", MUTED, 22)
    p = guardar(f, "03-valores")
    GUION.append(("Los valores", ["Mejor semana: " + ", ".join(f"{NOMBRES.get(t, t)} {pct(p)}" for t, p, _ in top) + ".",
                                   "Peor semana: " + ", ".join(f"{NOMBRES.get(t, t)} {pct(p)}" for t, p, _ in bot) + ".",
                                   "Motivos solo con fuente publicada (ver notas); si no hay noticia, decirlo: «sin noticia concreta en prensa»."]
                  + SEM.get("notas", {}).get("valores", [])))
    return p


def s_mercados():
    f = fig(W, H); cab(f, "Fuera de España", "Bolsas, bono, divisa y materias primas", 4)
    filas = [(n, TV[s]["close"], TV[s].get("Perf.W")) for n, s in CTX if s in TV and TV[s].get("close") is not None]
    if ES: filas.insert(6, ("Bono español a 10 años", ES, None))
    for k, (n, c, w) in enumerate(filas):
        y = 0.70 - k * 0.062; x = XL if k < 6 else XL
        T(f, XL, y, n, FG, 26, "bold"); T(f, 0.55, y, num(c, 4 if n == "Euro/dólar" else 2) + (" %" if "Bono" in n else ""), MUTED, 26, ha="right")
        if w is not None: T(f, 0.75, y, pct(w), cpct(w), 26, "bold", ha="right")
    T(f, 0.75, 0.75, "Semana", MUTED, 20, "bold", ha="right")
    if PRIMA is not None: T(f, XL, 0.10, f"Prima de riesgo (bono español menos alemán a 10 años): {PRIMA} puntos básicos (calculado)", ACC2, 24, "bold")
    p = guardar(f, "04-mercados")
    GUION.append(("Fuera de España", [f"{n}: {pct(w)} en la semana" for n, c, w in filas if w is not None] +
                  ([f"Bono español a 10 años: {num(ES, 2)} %; prima de riesgo {PRIMA} pb (calculado)."] if ES and PRIMA is not None else [])
                  + ["Fuente: TradingView (variación semanal de TradingView)."] + SEM.get("notas", {}).get("mercados", [])))
    return p


def lista(n, nombre, k, titulo, items, vacio):
    f = fig(W, H); cab(f, k, titulo, n)
    if not items: T(f, XL, 0.6, vacio, MUTED, 30, "bold")
    for j, it in enumerate(items[:5]):
        y = 0.70 - j * 0.115; t, txt = it[0], it[1]
        f.patches.append(plt.Rectangle((XL, y - 0.075), 0.90, 0.1, transform=f.transFigure, color=PANEL, figure=f))
        T(f, XL + 0.012, y, t, ACC, 26, "bold", va="center")
        T(f, XL + 0.25, y, "\n".join(partir(txt, 85)[:2]), FG, 22, va="center", linespacing=1.25)
    fu = [it[2] for it in items[:5] if len(it) > 2 and it[2]]
    if fu: T(f, XL, 0.075, "Fuentes: " + "; ".join(dict.fromkeys(fu)), MUTED, 16, style="italic")
    return guardar(f, nombre)


def s_tecnico():
    f = fig(W, H); C = np.array([v["c"] for v in IB]); s50, s200 = sma(C, 50), sma(C, 200)
    n = 126; cab(f, "El gráfico", "IBEX 35: seis meses y sus medias de 50 y 200", 6)
    ax = f.add_axes([XL + 0.04, 0.12, 0.62, 0.6]); clean(ax); xs = np.arange(n)
    ax.plot(xs, C[-n:], color=FG, lw=2.6); ax.plot(xs, s50[-n:], color=ACC2, lw=2.4); ax.plot(xs, s200[-n:], color=PUR, lw=2.4)
    tk = list(range(0, n, 21)); ax.set_xticks(tk, [f"{fecha(IB[-n + i]['t']).day} {MESES[fecha(IB[-n + i]['t']).month - 1]}" for i in tk])
    ax.grid(axis="y", color=DIM, lw=0.6)
    m20 = max(v["h"] for v in IB[-20:]); n20 = min(v["l"] for v in IB[-20:])
    dat = [("Cierre", num(C[-1], 1), FG), ("Media 50", num(s50[-1], 1), ACC2), ("Media 200", num(s200[-1], 1), PUR),
           ("Máximo 20 sesiones", num(m20, 1), ACC), ("Mínimo 20 sesiones", num(n20, 1), NEG)]
    for k, (a, b, c) in enumerate(dat): T(f, 0.72, 0.68 - k * 0.09, a, MUTED, 22, "bold"); T(f, 0.72, 0.64 - k * 0.09, b, c, 32, "bold")
    T(f, XL, 0.07, "Datos, no señales · medias y extremos: calculado", NEG, 20, "bold")
    p = guardar(f, "06-tecnico")
    pos = lambda a, b: "por encima" if a > b else "por debajo"
    GUION.append(("El gráfico", [f"Cierre {num(C[-1], 1)}, {pos(C[-1], s50[-1])} de su media de 50 ({num(s50[-1], 1)}) y {pos(C[-1], s200[-1])} de la de 200 ({num(s200[-1], 1)}).",
                                 f"Rango de las últimas 20 sesiones: {num(n20, 1)} a {num(m20, 1)}.",
                                 "Siempre como condiciones, nunca como previsión («si cerrara por debajo de…, la lectura cambiaría»)."] + SEM.get("notas", {}).get("tecnico", [])))
    return p


def s_cierre():
    f = fig(W, H); cab(f, "Para terminar", "Tus preguntas", 8)
    T(f, XL, 0.66, "Respondemos las preguntas del chat", FG, 44, "bold")
    for k, t in enumerate(["De lunes a viernes, a las 18:05: el vídeo diario del IBEX 35", "Los domingos: «Análisis técnico, explicado fácil» y el calendario de resultados",
                           "Suscríbete y activa la campana para el directo del próximo viernes"]):
        T(f, XL, 0.52 - k * 0.08, "• " + t, ACC2 if k == 2 else FG, 30, "bold" if k == 2 else "normal")
    T(f, XL, 0.16, "\n".join(partir("AVISO: contenido informativo y educativo. No es una recomendación de inversión, ni una invitación a comprar o vender valores, "
                                     "ni asesoramiento personalizado. AIAcciones España no tiene posiciones en los valores citados. Invertir conlleva riesgo de pérdida.", 150)),
      MUTED, 18, linespacing=1.5)
    p = guardar(f, "08-preguntas")
    GUION.append(("Preguntas y cierre", ["Responder preguntas del chat sin recomendar valores concretos (nada de comprar/vender, precio objetivo, cara/barata).",
                                          "Despedida: vídeo diario 18:05, curso los domingos, próximo directo el viernes que viene a las 17:45."]))
    return p


S.append(s_portada()); S.append(s_ibex()); S.append(s_valores()); S.append(s_mercados())
S.append(lista(5, "05-noticias", "Lo que ha pasado", "Las noticias de la semana", SEM.get("noticias", []), "Sin noticias destacadas con fuente."))
GUION.append(("Las noticias de la semana", [f"{n[0]}: {n[1]}" + (f" (fuente: {n[2]})" if len(n) > 2 else "") for n in SEM.get("noticias", [])]))
S.append(s_tecnico())
S.append(lista(7, "07-agenda", "Lo que viene", "La agenda de la semana que viene", SEM.get("agenda", []), "Sin citas destacadas."))
GUION.append(("La agenda", [f"{a[0]}: {a[1]}" + (f" (fuente: {a[2]})" if len(a) > 2 else "") for a in SEM.get("agenda", [])]))
S.append(s_cierre())
ims = [Image.open(p).convert("RGB") for p in S]
ims[0].save(f"{OUT}/diapositivas-{HOY.isoformat()}.pdf", save_all=True, append_images=ims[1:], resolution=100)
with open(f"{OUT}/guion-{HOY.isoformat()}.md", "w") as g:
    g.write(f"# El IBEX de la semana, en directo · {fl(HOY)} de {HOY.year}\n\nDatos hasta el cierre del {fl(HOY)} (Yahoo Finance y TradingView; generado {MER.get('generado', '')}). "
            "Duración objetivo: 15-20 minutos, unos 2 minutos por diapositiva.\n")
    orden = ["Portada", "El IBEX 35", "Los valores", "Fuera de España", "Las noticias de la semana", "El gráfico", "La agenda", "Preguntas y cierre"]
    D = dict(GUION)
    for k, t in enumerate(orden, 1):
        g.write(f"\n## {k}. {t}\n" + "".join(f"- {x}\n" for x in D.get(t, [])))
print("ok", HOY, "IBEX", num(CIERRE, 1), pct(SEM_P), "diapositivas", len(S), OUT)
