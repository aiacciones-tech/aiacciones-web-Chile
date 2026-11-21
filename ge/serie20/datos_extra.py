"""Datos de las empresas que «Die Wall-Street-Giganten» (Wall Street auf Deutsch) cubre además de las 20 de Nabd.
Daniel (21-nov-2026): añadir Anthropic (ANT) y SpaceX (SPCX), las dos en el Nasdaq.
Reutiliza nabd/serie20/datos_tv.py sin modificarlo (misma fuente, TradingView, y mismo formato), solo con otra lista de empresas.
Corre en GitHub Actions (serie20-datos-GE.yml) y escribe la rama datos-serie20-ge (calendario.json y <TICKER>/datos.json).
uso: python3 ge/serie20/datos_extra.py <carpeta de salida>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nabd", "serie20"))
import datos_tv

EXTRA = [("ANT", "NASDAQ:ANT"), ("SPCX", "NASDAQ:SPCX")]

if __name__ == "__main__":
    datos_tv.EMPRESAS = EXTRA
    datos_tv.main()
