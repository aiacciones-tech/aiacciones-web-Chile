"""Datos de la serie «عمالقة وول ستريت» (Nabd Wall Street): para cada una de las 20 empresas, la fecha de su último informe de resultados,
el trimestre publicado, sus cifras (ingresos, beneficio, BPA, flujo de caja, balance), el historial trimestral, las estimaciones de los
analistas y la sorpresa frente a ellas, y la próxima fecha de resultados. Fuente: escáner de TradingView (la misma del vídeo diario;
la SEC bloquea las descargas automáticas desde GitHub Actions con 403 «Undeclared Automated Tool», 13-nov-2026).
Corre en GitHub Actions (serie20-datos-Nabd.yml): el contenedor de Claude no llega a TradingView.
uso: python3 datos_tv.py <carpeta de salida>   -> calendario.json y <TICKER>/datos.json. Solo biblioteca estándar."""
import json, os, sys, datetime as dt, urllib.request
from zoneinfo import ZoneInfo

INICIO = os.environ.get("SERIE20_INICIO", "2026-10-01")   # «a partir de este trimestre» (Daniel, 13-nov-2026)
NY = ZoneInfo("America/New_York")
EMPRESAS = [("NVDA", "NASDAQ:NVDA"), ("MSFT", "NASDAQ:MSFT"), ("AAPL", "NASDAQ:AAPL"), ("GOOGL", "NASDAQ:GOOGL"), ("AMZN", "NASDAQ:AMZN"),
            ("META", "NASDAQ:META"), ("AVGO", "NASDAQ:AVGO"), ("TSLA", "NASDAQ:TSLA"), ("BRK", "NYSE:BRK.A"), ("JPM", "NYSE:JPM"),
            ("LLY", "NYSE:LLY"), ("WMT", "NASDAQ:WMT"), ("ORCL", "NYSE:ORCL"), ("V", "NYSE:V"), ("MA", "NYSE:MA"), ("XOM", "NYSE:XOM"),
            ("NFLX", "NASDAQ:NFLX"), ("COST", "NASDAQ:COST"), ("JNJ", "NYSE:JNJ"), ("PLTR", "NASDAQ:PLTR")]
COLS = """description close market_cap_basic earnings_release_date earnings_release_next_date fiscal_period_current fiscal_period_end_fq
total_revenue_fq total_revenue_ttm net_income_fq net_income_ttm earnings_per_share_diluted_fq gross_profit_fq oper_income_fq
total_revenue_yoy_growth_fq net_income_yoy_growth_fq earnings_per_share_diluted_yoy_growth_fq
earnings_per_share_forecast_fq revenue_forecast_fq eps_surprise_fq eps_surprise_percent_fq revenue_surprise_fq revenue_surprise_percent_fq
earnings_per_share_forecast_next_fq revenue_forecast_next_fq gross_margin operating_margin net_margin
free_cash_flow_fq free_cash_flow_ttm cash_f_operating_activities_fq cash_f_operating_activities_ttm capital_expenditures_fq capital_expenditures_ttm
cash_n_short_term_invest_fq total_debt_fq total_assets_fq total_liabilities_fq total_equity_fq debt_to_equity_fq dividends_yield
total_revenue_fq_h net_income_fq_h earnings_per_share_diluted_fq_h free_cash_flow_fq_h cash_f_operating_activities_fq_h
capital_expenditures_fq_h oper_income_fq_h""".split()


def scan(cols):
    body = json.dumps({"symbols": {"tickers": [e[1] for e in EMPRESAS]}, "columns": cols}).encode()
    r = urllib.request.urlopen(urllib.request.Request("https://scanner.tradingview.com/america/scan", body,
                                                      {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}), timeout=60)
    return {x["s"]: dict(zip(cols, x["d"])) for x in json.loads(r.read())["data"]}


def todo():
    try:
        return scan(COLS)
    except Exception as ex:  # una columna desconocida tumba la petición: se piden de una en una
        print("petición conjunta falló:", ex); out = {}
        for c in COLS:
            try:
                for s, d in scan([c]).items(): out.setdefault(s, {}).update(d)
            except Exception as e2:
                print("columna no disponible:", c, e2)
        return out


ts = lambda v: dt.datetime.fromtimestamp(v, dt.timezone.utc) if v else None


def etiquetas(fp, n):
    """'2026-Q4' -> ['2026-Q4', '2026-Q3', ...] (año fiscal de la empresa)."""
    try:
        y, q = int(fp[:4]), int(fp[-1])
    except Exception:
        return [None] * n
    out = []
    for _ in range(n):
        out.append(f"{y}-Q{q}"); q -= 1
        if q == 0: y, q = y - 1, 4
    return out


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True); D = todo(); ahora = dt.datetime.now(dt.timezone.utc)
    cal = {"generado": ahora.isoformat(timespec="seconds"), "inicio": INICIO, "fuente": "TradingView", "empresas": []}
    for t, s in EMPRESAS:
        x = D.get(s, {}); rel, nxt, fin = ts(x.get("earnings_release_date")), ts(x.get("earnings_release_next_date")), ts(x.get("fiscal_period_end_fq"))
        fecha = rel.astimezone(NY).date().isoformat() if rel else None
        # datos listos: el último trimestre de TradingView es el del informe (cierre del trimestre menos de 100 días antes del informe)
        listos = bool(rel and fin and 0 <= (rel - fin).days <= 100 and x.get("total_revenue_fq"))
        ev = {"fecha": fecha, "hora_utc": rel.isoformat(timespec="minutes"), "periodo": x.get("fiscal_period_current"),
              "fin_periodo": fin.date().isoformat() if fin else None, "datos_listos": listos} if fecha and fecha >= INICIO else None
        n = len(x.get("total_revenue_fq_h") or [])
        lab = etiquetas(x.get("fiscal_period_current") or "", min(n, 12))
        H = lambda k: (x.get(k) or [])[:12]
        tri = []
        for i in range(min(n, 12)):
            g = lambda k: (H(k)[i] if i < len(H(k)) else None)
            tri.append({"periodo": lab[i], "ingresos": g("total_revenue_fq_h"), "beneficio_neto": g("net_income_fq_h"), "eps_diluido": g("earnings_per_share_diluted_fq_h"),
                        "resultado_operativo": g("oper_income_fq_h"), "flujo_operativo": g("cash_f_operating_activities_fq_h"),
                        "capex": g("capital_expenditures_fq_h"), "flujo_libre": g("free_cash_flow_fq_h")})
        datos = {"ticker": t, "simbolo": s, "nombre": x.get("description"), "evento": ev, "precio": x.get("close"), "cap_mercado": x.get("market_cap_basic"),
                 "trimestres": tri[::-1], "ultimo": {k: x.get(k) for k in COLS if not k.endswith("_h")},
                 "fuente": "TradingView (escáner de datos fundamentales, basado en los informes de la empresa)", "generado": cal["generado"]}
        d = os.path.join(out, t); os.makedirs(d, exist_ok=True)
        json.dump(datos, open(os.path.join(d, "datos.json"), "w"), ensure_ascii=False, indent=1)
        cal["empresas"].append({"ticker": t, "simbolo": s, "cap": x.get("market_cap_basic"), "evento": ev,
                                "proxima": nxt.isoformat(timespec="minutes") if nxt else None,
                                "proxima_ny": nxt.astimezone(NY).date().isoformat() if nxt else None})
        print(t, "último informe", fecha, x.get("fiscal_period_current"), "listos" if listos else "-", "próximo", nxt and nxt.astimezone(NY).date())
    json.dump(cal, open(os.path.join(out, "calendario.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
