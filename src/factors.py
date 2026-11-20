"""Factores de traducción empíricos (Método B): razón (métrica/90 en Europa top-5) / (métrica/90 en liga de origen).

REGLAS (iguales para todos, definidas antes de ver resultados):
  origen  = las dos últimas temporadas del jugador en su liga de origen antes de irse (explícitas en ORIGEN).
  Europa  = temporadas en una liga TOP-5 (ENG/ESP/GER/ITA/FRA), en orden cronológico, sumando temporadas completas
            hasta alcanzar >= 900 min. Si no llega, se marca insuficiente y NO entra al factor.
  métricas = goles sin penal, tiros, tiros a puerta por 90 (asistencias se excluyen: demasiados ceros).
"""
import numpy as np, pandas as pd
from cohort import load_player, per90

TOP5 = ("eng ENG", "es ESP", "de GER", "it ITA", "fr FRA")
MIN_EUR = 900
METRICS = ["npG90", "Sh90", "SoT90"]

# jugador -> (filtro de origen)
ORIGEN = {
    "estevao":     lambda d: d[(d.Squad == "Palmeiras") & d.Season.isin(["2024", "2025"])],
    "mastantuono": lambda d: d[(d.Squad == "River Plate") & d.Season.isin(["2024", "2025"])],
    "endrick":     lambda d: d[(d.Squad == "Palmeiras") & d.Season.isin(["2023", "2024"])],
    "roque":       lambda d: d[(d.Squad == "Athletico–PR") & d.Season.isin(["2022", "2023"])],
    "gimenez":     lambda d: d[(d.Squad == "Cruz Azul") & d.Season.isin(["2021-2022", "2022-2023"])],
    "echeverri":   lambda d: d[(d.Squad == "River Plate") & d.Season.isin(["2023", "2024"])],
    "vinicius":    lambda d: d[(d.Squad == "Flamengo") & d.Season.isin(["2017", "2018"])],
    "rodrygo":     lambda d: d[(d.Squad == "Santos") & d.Season.isin(["2018", "2019"])],
}

def europa_top5(d):
    """Primeras temporadas en liga top-5 hasta sumar >= MIN_EUR minutos."""
    e = d[d.Country.isin(TOP5)] if "Country" in d else d
    seasons, cum, keep = sorted(e.Season.unique()), 0, []
    for s in seasons:
        keep.append(s); cum += e[e.Season == s].Min.sum()
        if cum >= MIN_EUR: break
    return e[e.Season.isin(keep)], cum

def tabla():
    filas = []
    for p, f in ORIGEN.items():
        d = load_player(p)
        o = f(d); e, mins = europa_top5(d)
        ro, re = per90(o), per90(e)
        r = {m: re[m] / ro[m] if ro[m] else np.nan for m in METRICS}
        filas.append({"jugador": p, "min_origen": ro["min"], "min_europa": mins,
                      "valido": mins >= MIN_EUR, **{f"f_{m}": r[m] for m in METRICS}})
    return pd.DataFrame(filas)

if __name__ == "__main__":
    t = tabla()
    print(t.round(2).to_string(index=False))
    # posición según Transfermarkt: Mora es mediapunta -> el grupo comparable son extremos y mediapuntas
    POS = {"estevao": "extremo", "mastantuono": "extremo", "vinicius": "extremo", "rodrygo": "extremo", "echeverri": "mediapunta",
           "endrick": "delantero centro", "roque": "delantero centro", "gimenez": "delantero centro"}
    t["posicion"] = t.jugador.map(POS)
    t["mismo_puesto"] = t.posicion.isin(["extremo", "mediapunta"])
    print("\nSolo MISMO PUESTO (extremos y mediapuntas):")
    print(t[t.mismo_puesto].round(2).to_string(index=False))
    # el mínimo de minutos es una ETIQUETA: se reporta el factor con todos y solo con los que cumplen
    for etiqueta, v in [("TODOS (incluye 'bajo mínimo')", t), (f"SOLO >= {MIN_EUR} min", t[t.valido]),
                        ("MISMO PUESTO (todos los minutos)", t[t.mismo_puesto]), ("MISMO PUESTO y >= 900 min", t[t.mismo_puesto & t.valido])]:
        print(f"\nFactores, {etiqueta}, n={len(v)}  (n pequeño: rangos, no cifras)")
        for m in METRICS:
            x = v[f"f_{m}"].dropna()
            print(f"  {m:6s} mediana={x.median():.2f}  Q1-Q3={x.quantile(.25):.2f}-{x.quantile(.75):.2f}  min-max={x.min():.2f}-{x.max():.2f}")
