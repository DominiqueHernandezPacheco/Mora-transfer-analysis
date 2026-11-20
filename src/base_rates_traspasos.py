"""Traspasos de jóvenes (<=19 años) desde ligas de origen (México, Brasil, Argentina) a ligas europeas, 2015-2026.
Fuente: dataset abierto de Transfermarkt. Montos 0 pueden ser cesiones/libres: se reportan aparte."""
import sys, pandas as pd
D = sys.argv[1]
tr = pd.read_csv(f"{D}/transfers.csv.gz", parse_dates=["transfer_date"]); pl = pd.read_csv(f"{D}/players.csv.gz", parse_dates=["date_of_birth"])
cl = pd.read_csv(f"{D}/clubs.csv.gz")
comp = cl.set_index("club_id").domestic_competition_id
tr["lig_o"] = tr.from_club_id.map(comp); tr["lig_d"] = tr.to_club_id.map(comp)
EURO = {"ES1", "GB1", "IT1", "L1", "FR1", "NL1", "PO1", "BE1", "TR1", "SC1", "A1", "GR1", "DK1", "C1"}
TOP5 = {"ES1", "GB1", "IT1", "L1", "FR1"}
t = tr.merge(pl[["player_id", "date_of_birth", "sub_position", "country_of_citizenship"]], on="player_id")
t["edad"] = (t.transfer_date - t.date_of_birth).dt.days / 365.25
t = t[(t.transfer_date >= "2015-01-01") & t.lig_o.isin(["MEX1", "BRA1", "ARG1"]) & t.lig_d.isin(EURO) & (t.edad <= 19.99)]
t["pais_origen"] = t.lig_o.map({"MEX1": "México", "BRA1": "Brasil", "ARG1": "Argentina"})
t["fee_M"] = t.transfer_fee / 1e6
print("Traspasos de <=19 años de ligas MEX/BRA/ARG a Europa (2015-jul 2026):", len(t))
con_fee = t[t.fee_M > 0]
print("\nPor país de origen (solo con monto > 0):")
print(con_fee.groupby("pais_origen").fee_M.agg(n="count", mediana="median", p25=lambda x: x.quantile(.25), p75=lambda x: x.quantile(.75), maximo="max").round(1).to_string())
print("\nCon monto > 0 y destino TOP-5:"); print(con_fee[con_fee.lig_d.isin(TOP5)].groupby("pais_origen").fee_M.agg(n="count", mediana="median", maximo="max").round(1).to_string())
print("\nDe México (<=19 años) a Europa, con nombre:")
x = t[t.pais_origen == "México"].sort_values("transfer_date")[["transfer_date", "player_name", "edad", "from_club_name", "to_club_name", "fee_M", "market_value_in_eur", "sub_position"]]
x["edad"] = x.edad.round(1); x["market_value_in_eur"] = (x.market_value_in_eur / 1e6).round(1)
print(x.to_string(index=False))
print("\nTop-10 montos de brasileños/argentinos <=19 a Europa:")
print(t[t.pais_origen != "México"].nlargest(10, "fee_M")[["transfer_date", "player_name", "edad", "pais_origen", "to_club_name", "fee_M"]].round(1).to_string(index=False))
