"""Tres funciones para mostrar en cámara: cada una cabe en una captura de 2-3 segundos."""
import pandas as pd
from scipy.stats import percentileofscore


def por_90(df):
    """Todo por 90 min y SIN penales: Mora cobra penales y eso infla sus goles."""
    n90 = df["Min"] / 90
    return pd.DataFrame({
        "goles_sin_penal": df["G-PK"] / n90,      # goles menos penales anotados
        "tiros":           df["Sh"] / n90,
        "tiros_a_puerta":  df["SoT"] / n90,
    })


def percentil_entre_pares(valor, pares):
    """¿Qué % de sus pares de posición (mediapuntas y extremos) tiene menos que él?"""
    return percentileofscore(pares, valor)


def validar_transcripcion(df, total, por90, minutos="minutes", tol=0.15):
    """Si copié bien, total / (minutos/90) debe coincidir con lo que FotMob publica por 90."""
    calculado = df[total] / (df[minutos] / 90)
    return (calculado - df[por90]).abs().le(tol).mean()     # fracción de filas que cuadra


if __name__ == "__main__":
    from load_fbref import load_league
    liga = load_league("data/raw/ligamx_2025-26_stats.csv", "data/raw/ligamx_2025-26_shooting.csv")
    mora = liga[liga.Player == "Gilberto Mora"]
    print("1) por_90 de Mora (FBref 2025-26):\n", por_90(mora).round(2).to_string(index=False))

    from pares_posicion import percentiles
    p = percentiles().set_index("metrica")
    print("\n2) percentil de Mora entre sus pares: goles sin penal =", round(p.loc["Goles sin penal", "pct"]))

    m = pd.read_csv("data/processed/ligamx_2026-27_apertura_fotmob_merged.csv").dropna(subset=["xg", "xg_per90"])
    print("\n3) validar_transcripcion (xG vs xG/90):", f"{validar_transcripcion(m, 'xg', 'xg_per90'):.0%} de las filas cuadra",
          f"({len(m)} jugadores)")
