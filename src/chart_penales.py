"""Gráfica 1 del reel: lo que parece vs. lo que es (con y sin penales). Vertical 9:16, fondo oscuro."""
import pandas as pd, matplotlib.pyplot as plt

BG, MORA, GRAY, TXT = "#0e1117", "#FFB000", "#5b6472", "#f2f2f2"

m = pd.read_csv("data/manual.csv")
v = m[(m.player == "Gilberto Mora") & (m.season == "2026/27")].set_index("metric").value.astype(float)
n90 = v["minutes"] / 90
vals = {                                   # todo por 90 minutos
    "Goles": v["goals"] / n90,
    "xG": v["xG"] / n90,
    "Goles\nsin penal": (v["goals"] - v["penalty_goals"]) / n90,
    "npxG\n(sin penal)": v["npxG"] / n90,
}
fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100, facecolor=BG)
ax.set_facecolor(BG)
colors = [GRAY, GRAY, MORA, MORA]          # Mora resaltado = la versión "sin penales"
bars = ax.bar(list(vals), list(vals.values()), color=colors, width=0.62)
for b, x in zip(bars, vals.values()):
    ax.text(b.get_x() + b.get_width() / 2, x + 0.02, f"{x:.2f}", ha="center", color=TXT, fontsize=44, fontweight="bold")
ax.set_ylim(0, 1.15)
ax.tick_params(colors=TXT, labelsize=30, length=0); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
fig.text(0.5, 0.90, "MORA: ¿QUÉ TAN BUENO\nES SIN LOS PENALES?", ha="center", color=TXT, fontsize=52, fontweight="bold")
fig.text(0.5, 0.835, "Producción por 90 min · Apertura 2026/27", ha="center", color=MORA, fontsize=32)
fig.text(0.5, 0.135, "4 de sus 5 goles fueron de penal", ha="center", color=TXT, fontsize=40, fontweight="bold")
fig.text(0.5, 0.075, f"Muestra chica: {int(v['minutes'])} min (7 partidos)\nFuente: FotMob, 13-oct-2026", ha="center", color=GRAY, fontsize=26)
fig.subplots_adjust(left=0.08, right=0.92, bottom=0.27, top=0.78)
fig.savefig("outputs/01_penales_vertical.png", facecolor=BG)
print({k.replace("\n", " "): round(x, 2) for k, x in vals.items()})
