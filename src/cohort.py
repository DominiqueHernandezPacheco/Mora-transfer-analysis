"""Carga de un jugador de la cohorte (FBref Standard + Shooting) y razón Europa/origen por 90.
Sin xG: estas tablas de FBref no lo traen para estas ligas -> se usan goles sin penal, asistencias, tiros y tiros a puerta.

Regla de datos faltantes: FBref a veces muestra Sh=0 con SoT>0 (imposible) o deja Sh/SoT vacíos
(Liga MX antigua). Esos tiros/tiros a puerta se tratan como FALTANTES y cada métrica por 90 se
calcula solo con las temporadas donde esa métrica existe (denominador = sus propios 90s)."""
import numpy as np, pandas as pd

def load_player(name):
    p = f"data/raw/players/{name}_fbref_"
    st = pd.read_csv(p + "standard.csv", header=1, encoding="utf-8")
    sh = pd.read_csv(p + "shooting.csv", header=1, encoding="utf-8")
    d = st[["Season", "Age", "Squad", "Country", "Comp", "MP", "Min", "90s", "G-PK", "Ast"]].merge(
        sh[["Season", "Squad", "Sh", "SoT"]], on=["Season", "Squad"])
    d = d[d.Min.notna() & ~d.Season.str.contains("Season")].copy()
    bad = (d.Sh == 0) & (d.SoT > 0)                 # tiros imposibles -> faltante
    d.loc[bad, ["Sh", "SoT"]] = np.nan
    return d

def per90(rows):
    out = {"min": rows.Min.sum()}
    for col, lab in [("G-PK", "npG90"), ("Ast", "Ast90"), ("Sh", "Sh90"), ("SoT", "SoT90")]:
        ok = rows[rows[col].notna()]
        out[lab] = ok[col].sum() / ok["90s"].sum() if len(ok) else np.nan
    return pd.Series(out)

def ratio(origen, europa):
    a, b = per90(origen), per90(europa)
    r = (b / a).replace([np.inf, -np.inf], np.nan)
    return pd.DataFrame({"origen": a, "europa": b, "razon_Eur/Orig": r}).round(2)
