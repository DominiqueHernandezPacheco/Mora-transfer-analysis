"""¿Sería récord? Traspasos más caros (a) desde clubes de Liga MX y (b) de jugadores con nacionalidad mexicana. Dataset abierto TM."""
import sys, pandas as pd
D = sys.argv[1]
tr = pd.read_csv(f"{D}/transfers.csv.gz", parse_dates=["transfer_date"]); pl = pd.read_csv(f"{D}/players.csv.gz", parse_dates=["date_of_birth"]); cl = pd.read_csv(f"{D}/clubs.csv.gz")
comp = cl.set_index("club_id").domestic_competition_id
tr["lig_o"] = tr.from_club_id.map(comp); tr["lig_d"] = tr.to_club_id.map(comp)
t = tr.merge(pl[["player_id", "date_of_birth", "country_of_citizenship", "sub_position"]], on="player_id")
t["edad"] = ((t.transfer_date - t.date_of_birth).dt.days / 365.25).round(1); t["fee_M"] = t.transfer_fee / 1e6
cols = ["transfer_date", "player_name", "edad", "from_club_name", "to_club_name", "fee_M"]
print("(a) Traspasos más caros DESDE un club de Liga MX (cualquier nacionalidad):")
print(t[t.lig_o == "MEX1"].nlargest(10, "fee_M")[cols + ["country_of_citizenship"]].to_string(index=False))
print("\n(b) Traspasos más caros de jugadores MEXICANOS (cualquier club):")
print(t[t.country_of_citizenship == "Mexico"].nlargest(10, "fee_M")[cols].to_string(index=False))
print("\n(c) Cuántos traspasos de >= 30 M€ hay de mexicanos / desde Liga MX:", ((t.country_of_citizenship == "Mexico") & (t.fee_M >= 30)).sum(), "/", ((t.lig_o == "MEX1") & (t.fee_M >= 30)).sum())
