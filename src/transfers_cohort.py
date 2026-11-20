"""Verifica la cohorte con datos reales de Transfermarkt (dataset abierto dcaribou): nacimiento, traspasos, montos."""
import sys, unicodedata, pandas as pd
D = sys.argv[1]
norm = lambda s: unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
pl = pd.read_csv(f"{D}/players.csv.gz"); tr = pd.read_csv(f"{D}/transfers.csv.gz")
pl["n"] = pl["name"].map(norm)
buscar = {"Estêvão": "estevao", "Endrick": "endrick", "Mastantuono": "franco mastantuono", "Echeverri": "claudio echeverri",
          "Roque": "vitor roque", "Lainez": "diego lainez", "Giménez": "santiago gimenez", "MORA": "gilberto mora"}
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
for etiqueta, q in buscar.items():
    c = pl[pl.n.str.contains(q, regex=False)].sort_values("highest_market_value_in_eur", ascending=False).head(2)
    print(f"\n=== {etiqueta}: coincidencias {len(c)}")
    if c.empty: continue
    j = c.iloc[0]
    print(f"{j['name']} | id {j.player_id} | nac. {j.date_of_birth} | club actual: {j.current_club_name} | valor TM: {j.market_value_in_eur} | máx: {j.highest_market_value_in_eur} | contrato hasta: {j.contract_expiration_date}")
    t = tr[tr.player_id == j.player_id].sort_values("transfer_date")
    print(t[["transfer_date", "from_club_name", "to_club_name", "transfer_fee", "market_value_in_eur"]].to_string(index=False))
