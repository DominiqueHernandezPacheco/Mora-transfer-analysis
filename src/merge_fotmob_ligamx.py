"""Une las 8 tablas FotMob (Liga MX Apertura 2026/27) por fotmob_id y valida la transcripción.

Validación cruzada: FotMob publica xG total, minutos y xG/90 en tablas distintas.
Si xG / (min/90) != xg_per90 (tolerancia por redondeo), alguna de las tres tiene un error.
"""
import pandas as pd
P = "data/raw/fotmob_ligamx_2026-27_apertura_{}.csv"
t = {k: pd.read_csv(P.format(k)) for k in
     ["minutos", "xg", "xa", "xg_por90", "xa_por90", "tiros_por90", "oportunidades_creadas", "regates_por90"]}

base = t["minutos"].copy()
for k, cols in {"xg": ["goals", "xg"], "xa": ["assists", "xa"],
                "xg_por90": ["goals_per90", "xg_per90"], "xa_por90": ["assists_per90", "xa_per90"],
                "tiros_por90": ["shot_conversion_pct", "shots_per90"],
                "oportunidades_creadas": ["chances_created_per90", "chances_created_total"],
                "regates_por90": ["dribble_success_pct", "dribbles_won_per90"]}.items():
    base = base.merge(t[k][["fotmob_id"] + cols], on="fotmob_id", how="left")
base["n90"] = base.minutes / 90

def check(total, per90, tol, label):
    d = base.dropna(subset=[total, per90]).copy()
    d["calc"] = d[total] / d.n90
    d["err"] = (d.calc - d[per90]).abs()
    bad = d[d.err > tol]
    print(f"{label}: {len(d)} jugadores comparables, {len(bad)} con diferencia > {tol}")
    print(bad[["fotmob_id", "player", "minutes", total, per90, "calc"]].round(2).head(12).to_string(index=False))

check("xg", "xg_per90", 0.15, "xG vs xG/90")        # xG total viene redondeado a 1 decimal -> tolerancia
check("xa", "xa_per90", 0.15, "xA vs xA/90")
check("chances_created_total", "chances_created_per90", 0.15, "Oportunidades total vs /90")
base.to_csv("data/processed/ligamx_2026-27_apertura_fotmob_merged.csv", index=False)
print("\nGuardado data/processed/ligamx_2026-27_apertura_fotmob_merged.csv", base.shape)
print(base[base.fotmob_id == 1670377].T.to_string())
