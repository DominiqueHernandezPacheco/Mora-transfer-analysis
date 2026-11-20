"""Carga y limpia las tablas de FBref (Standard + Shooting) de una liga-temporada.

Decisiones metodológicas:
- FBref trae 2 filas de encabezado; usamos la segunda (header=1).
- Los jugadores que cambiaron de equipo aparecen en 2+ filas: se SUMAN
  (minutos, goles, tiros...) antes de calcular por 90. Si no, un jugador
  con 500+500 minutos parecería no llegar al mínimo de 900.
- El ID de FBref (columna '-9999') distingue homónimos.
"""
import pandas as pd

def read_table(path):
    df = pd.read_csv(path, header=1, encoding="utf-8", encoding_errors="replace")
    df = df[df["Rk"] != "Rk"]                       # quita encabezados repetidos
    return df.rename(columns={"-9999": "pid"})

def load_league(stats_csv, shooting_csv):
    st, sh = read_table(stats_csv), read_table(shooting_csv)
    num_st = ["MP", "Starts", "Min", "Gls", "Ast", "G-PK", "PK", "PKatt"]
    num_sh = ["Sh", "SoT"]
    st[num_st] = st[num_st].apply(pd.to_numeric, errors="coerce")
    sh[num_sh] = sh[num_sh].apply(pd.to_numeric, errors="coerce")
    m = st[["pid", "Player", "Pos", "Squad", "Born"] + num_st].merge(
        sh[["pid", "Squad"] + num_sh], on=["pid", "Squad"], how="left")
    agg = m.groupby("pid").agg(
        Player=("Player", "first"), Pos=("Pos", "first"), Born=("Born", "first"),
        Squad=("Squad", lambda s: "/".join(s)),
        **{c: (c, "sum") for c in num_st[:1] + num_st[2:] + num_sh})
    agg["n90"] = agg["Min"] / 90
    return agg.reset_index()

def per90(df):
    """Métricas por 90 y bandera de muestra mínima (>=900 min)."""
    d = df.copy()
    d["npG_90"]  = d["G-PK"] / d["n90"]       # goles SIN penal: lo que mide el juego abierto
    d["Ast_90"]  = d["Ast"] / d["n90"]
    d["Sh_90"]   = d["Sh"] / d["n90"]
    d["SoT_90"]  = d["SoT"] / d["n90"]
    d["ok900"]   = d["Min"] >= 900
    return d
