"""¿Qué hace bien Mora frente a SUS pares de posición en Liga MX? (mediapuntas + extremos)
Posición: Transfermarkt (dataset abierto, jugadores cuyo club actual juega MEX1). Se une por nombre normalizado."""
import sys, unicodedata, pandas as pd
from scipy.stats import percentileofscore
from load_fbref import load_league, per90

TM_DIR = "data/external/transfermarkt_dcaribou"
PARES = ["Attacking Midfield", "Left Winger", "Right Winger"]
norm = lambda s: unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()

def _posiciones(D):
    tm = pd.read_csv(f"{D}/players.csv.gz")
    tm = tm[tm.current_club_domestic_competition_id == "MEX1"].copy(); tm["n"] = tm["name"].map(norm)
    return tm.drop_duplicates("n").set_index("n").sub_position

def percentiles(D=TM_DIR):
    """Devuelve una fila por métrica: etiqueta, valor de Mora, percentil entre pares, n de pares, fuente."""
    pos = _posiciones(D)
    # FBref 2025-26 (torneo completo): pares con >= 900 min
    f = per90(load_league("data/raw/ligamx_2025-26_stats.csv", "data/raw/ligamx_2025-26_shooting.csv"))
    f["pos"] = f.Player.map(norm).map(pos)
    g, mora = f[f.ok900 & f.pos.isin(PARES)], f[f.Player == "Gilberto Mora"].iloc[0]
    # FotMob Apertura 2026/27 (11 jornadas): pares con >= 450 min
    m = pd.read_csv("data/processed/ligamx_2026-27_apertura_fotmob_merged.csv"); m["pos"] = m.player.map(norm).map(pos)
    h, mo = m[(m.minutes >= 450) & m.pos.isin(PARES)], m[m.fotmob_id == 1670377].iloc[0]
    filas = []
    for c, lab in [("npG_90", "Goles sin penal"), ("SoT_90", "Tiros a puerta"), ("Sh_90", "Tiros"), ("Ast_90", "Asistencias")]:
        filas.append(dict(metrica=lab, valor=mora[c], pct=percentileofscore(g[c], mora[c]), n=len(g), fuente="FBref 2025-26", grupo="marca"))
    for c, lab, grp in [("xa_per90", "xA", "crea"), ("chances_created_per90", "Oportunidades creadas", "crea"), ("dribbles_won_per90", "Regates exitosos", "regate")]:
        x = h[c].dropna()
        filas.append(dict(metrica=lab, valor=mo[c], pct=percentileofscore(x, mo[c]), n=len(x), fuente="FotMob Apertura 26/27", grupo=grp))
    return pd.DataFrame(filas)

if __name__ == "__main__":
    print(percentiles(sys.argv[1] if len(sys.argv) > 1 else TM_DIR).round(2).to_string(index=False))
