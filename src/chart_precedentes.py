"""Los que se fueron a Europa a los ~18: cuánto se pagó y cuánto los valoraba Transfermarkt en ese momento. Vertical 9:16.
Datos: data/processed/cohorte_traspasos.csv (Transfermarkt, dataset abierto). Rodrygo y Vinícius incluidos."""
import pandas as pd, matplotlib.pyplot as plt

BG, MORA, GRIS, TXT, SUAVE, MX = "#0e1117", "#FFB000", "#5b6472", "#f2f2f2", "#7d8794", "#2FB5A0"
t = pd.read_csv("data/processed/cohorte_traspasos.csv").sort_values("monto_eur_M").reset_index(drop=True)
etiq = [f"{j}\n{e:.1f} años" for j, e in zip(t.jugador, t.edad_al_traspaso)]
colores = [MX if j in ("Lainez", "Giménez") else GRIS for j in t.jugador]      # verde = mexicanos

fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100, facecolor=BG)
ax.set_facecolor(BG)
y = range(len(t))
ax.barh(y, t.monto_eur_M, color=colores, height=0.62)
ax.scatter(t.valor_TM_entonces_eur_M, y, marker="D", s=260, color=MORA, zorder=3, edgecolor=BG, linewidth=2)
for i, m in zip(y, t.monto_eur_M):
    ax.text(m + 1, i, f"{m:g}", va="center", color=TXT, fontsize=30, fontweight="bold")
ax.axvline(10, color=MORA, lw=3, ls="--", zorder=1)
ax.text(10.4, len(t) - 0.35, "Valor de Mora\n(Transfermarkt): 10 M€", color=MORA, fontsize=22, va="bottom")
ax.set_yticks(list(y)); ax.set_yticklabels(etiq); ax.set_xlim(0, 66); ax.set_ylim(-0.6, len(t) + 0.7)
ax.tick_params(axis="y", colors=TXT, labelsize=21, length=0); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
fig.subplots_adjust(left=0.21, right=0.96, top=0.78, bottom=0.27)

fig.text(0.5, 0.925, "LOS QUE SE FUERON\nA EUROPA A LOS 18", ha="center", va="center", color=TXT, fontsize=52, fontweight="bold", linespacing=1.05)
fig.text(0.5, 0.835, "Monto pagado (M€) y valor que les daba Transfermarkt", ha="center", color=MORA, fontsize=24)
fig.text(0.5, 0.215, "Los de 45 M€:\nVinícius, Rodrygo, Estêvão y Mastantuono", ha="center", va="center", color=TXT, fontsize=28, fontweight="bold", linespacing=1.2)
fig.text(0.5, 0.15, "El único mexicano a esa edad:\nLainez (14 M€, no se asentó)", ha="center", va="center", color=MX, fontsize=28, fontweight="bold", linespacing=1.2)
fig.text(0.5, 0.07, "Barra: monto pagado · ◆ dorado: valor de Transfermarkt entonces\nVerde: mexicanos · Giménez se fue a los 21; el resto, a los 18.0-18.8\n"
                    "Fuente: Transfermarkt (dataset abierto). 9 casos:\nreferencia, no predicción.",
         ha="center", va="center", color=SUAVE, fontsize=19)
fig.savefig("outputs/05_precedentes_18.png", facecolor=BG)
print(t[["jugador", "edad_al_traspaso", "monto_eur_M", "valor_TM_entonces_eur_M"]].to_string(index=False))
