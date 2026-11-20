"""¿Cómo se veían los otros chicos al irse? Producción en su liga de origen en las 2 últimas temporadas antes de salir,
frente a Mora (FBref Liga MX 2025-26). Sin ajuste de liga: Brasil/Argentina/Liga MX NO son equivalentes."""
import pandas as pd
from cohort import load_player, per90
from load_fbref import load_league, per90 as lg_per90

ORIG = {   # jugador: (archivo, club de origen, temporadas)
    "Estêvão":     ("estevao",     "Palmeiras",    ["2024", "2025"]),
    "Mastantuono": ("mastantuono", "River Plate",  ["2024", "2025"]),
    "Endrick":     ("endrick",     "Palmeiras",    ["2023", "2024"]),
    "Roque":       ("roque",       "Athletico–PR", ["2022", "2023"]),
    "Echeverri":   ("echeverri",   "River Plate",  ["2023", "2024"]),
    "Vinícius":    ("vinicius",    "Flamengo",     ["2017", "2018"]),
    "Rodrygo":     ("rodrygo",     "Santos",       ["2018", "2019"]),
    "Giménez":     ("gimenez",     "Cruz Azul",    ["2021-2022", "2022-2023"]),
    "Lainez":      ("lainez",      "América",      ["2017-2018", "2018-2019"]),
}

def tabla_origen():
    """Una fila por jugador (más MORA) con minutos y métricas por 90 en su liga de origen."""
    filas = []
    for nombre, (f, club, temps) in ORIG.items():
        d = load_player(f); o = d[(d.Squad == club) & d.Season.isin(temps)]
        p = per90(o)
        filas.append({"jugador": nombre, "liga": o.Comp.iloc[0].replace("1. ", ""), "edad": f"{int(o.Age.min())}-{int(o.Age.max())}",
                      "min": int(p["min"]), "npG90": p.npG90, "Sh90": p.Sh90, "SoT90": p.SoT90, "Ast90": p.Ast90})
    m = lg_per90(load_league("data/raw/ligamx_2025-26_stats.csv", "data/raw/ligamx_2025-26_shooting.csv"))
    m = m[m.Player == "Gilberto Mora"].iloc[0]
    filas.append({"jugador": "MORA", "liga": "Liga MX", "edad": "16-17", "min": int(m.Min), "npG90": m.npG_90,
                  "Sh90": m.Sh_90, "SoT90": m.SoT_90, "Ast90": m.Ast_90})
    return pd.DataFrame(filas)

if __name__ == "__main__":
    t = tabla_origen()
    print(t.round(2).to_string(index=False))
    print("\nPosición de Mora (1 = el más alto):")
    for c in ["npG90", "Sh90", "SoT90", "Ast90"]:
        print(f"  {c:6s}", int(t[c].rank(ascending=False)[t.jugador == "MORA"].iloc[0]), "de", t[c].notna().sum())
