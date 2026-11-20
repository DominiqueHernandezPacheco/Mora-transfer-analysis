"""Tabla de traspasos de la cohorte (primer salto a Europa) con edad exacta, monto y valor Transfermarkt de ese momento."""
import sys, unicodedata, pandas as pd
D, OUT = sys.argv[1], sys.argv[2]
norm = lambda s: unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
pl = pd.read_csv(f"{D}/players.csv.gz", parse_dates=["date_of_birth"]); tr = pd.read_csv(f"{D}/transfers.csv.gz", parse_dates=["transfer_date"])
pl["n"] = pl["name"].map(norm)
SALTO = {  # jugador: (nombre a buscar, fecha del traspaso del primer salto a Europa)  <- fechas verificadas en la salida anterior
    "Estêvão": ("estevao", "2025-07-14"), "Endrick": ("endrick", "2024-07-21"), "Mastantuono": ("franco mastantuono", "2025-08-14"),
    "Echeverri": ("claudio echeverri", "2024-01-25"), "Roque": ("vitor roque", "2024-01-01"),
    "Lainez": ("diego lainez", "2019-01-10"), "Vinícius": ("vinicius junior", "2018-07-12"), "Rodrygo": ("rodrygo", "2019-07-01"), "Giménez": ("santiago gimenez", "2022-07-29")}
filas = []
for j, (q, fecha) in SALTO.items():
    p = pl[pl.n.str.contains(q, regex=False)].sort_values("highest_market_value_in_eur", ascending=False).iloc[0]
    t = tr[(tr.player_id == p.player_id) & (tr.transfer_date == fecha)].iloc[0]
    filas.append({"jugador": j, "origen": t.from_club_name, "destino": t.to_club_name, "fecha": fecha,
                  "edad_al_traspaso": round((t.transfer_date - p.date_of_birth).days / 365.25, 1),
                  "monto_eur_M": t.transfer_fee / 1e6, "valor_TM_entonces_eur_M": t.market_value_in_eur / 1e6})
t = pd.DataFrame(filas)
t["monto/valor"] = (t.monto_eur_M / t.valor_TM_entonces_eur_M).round(2)
t.to_csv(OUT, index=False)
print(t.to_string(index=False))
print("\nMonto: mediana %.1f M€, rango %.1f-%.1f M€ | monto/valor TM: mediana %.2f" % (t.monto_eur_M.median(), t.monto_eur_M.min(), t.monto_eur_M.max(), t["monto/valor"].median()))
m = pl[pl.n.str.contains("gilberto mora", regex=False)].iloc[0]
print(f"\nMORA: nace {m.date_of_birth.date()} | valor Transfermarkt {m.market_value_in_eur/1e6:.1f} M€ | contrato hasta {str(m.contract_expiration_date)[:10]}")
