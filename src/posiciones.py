import sys, unicodedata, pandas as pd
D = sys.argv[1]
norm = lambda s: unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
pl = pd.read_csv(f"{D}/players.csv.gz"); comp = pd.read_csv(f"{D}/competitions.csv.gz")
pl["n"] = pl["name"].map(norm)
for q in ["estevao","franco mastantuono","claudio echeverri","diego lainez","endrick","vitor roque","santiago gimenez","gilberto mora"]:
    p = pl[pl.n.str.contains(q, regex=False)].sort_values("highest_market_value_in_eur", ascending=False).iloc[0]
    print(f"{p['name']:22s} {p.position:10s} | {p.sub_position}")
print("\nLigas que cubre el dataset (competition_id, país):")
print(comp[comp.type == "domestic_league"][["competition_id", "name", "country_name"]].to_string(index=False))
print("\nJugadores cuyo club actual juega la liga MEX1:", (pl.current_club_domestic_competition_id == "MEX1").sum())
print(pl[pl.current_club_domestic_competition_id == "MEX1"].sub_position.value_counts().to_string())
