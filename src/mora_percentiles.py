from load_fbref import load_league, per90
from scipy.stats import percentileofscore
d = per90(load_league("data/raw/ligamx_2025-26_stats.csv", "data/raw/ligamx_2025-26_shooting.csv"))
mora = d[d.Player == "Gilberto Mora"].iloc[0]
print(mora[["Squad","Min","Gls","G-PK","PK","Ast","Sh","SoT","npG_90","Ast_90","Sh_90","SoT_90"]].to_string())
for name, pool in {"toda la liga (>=900 min)": d[d.ok900],
                   "atacantes/medios (FW o MF, >=900 min)": d[d.ok900 & d.Pos.str.contains("FW|MF")]}.items():
    print(f"\nPercentiles de Mora vs {name}  (n={len(pool)})")
    for m in ["npG_90", "Ast_90", "Sh_90", "SoT_90"]:
        print(f"  {m:8s} valor={mora[m]:.2f}  percentil={percentileofscore(pool[m], mora[m]):.0f}")
