"""GIF animado para el README: los percentiles de Mora frente a sus pares de posición (las barras crecen hasta su valor).
Requiere los datos locales (ver README). Salida: docs/img/percentiles.gif"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pares_posicion import percentiles

BG, MORA, AZUL, TXT, SUAVE = "#0e1117", "#FFB000", "#5B8DEF", "#f2f2f2", "#7d8794"
df = percentiles()
df = df[df.metrica != "Asistencias"].reset_index(drop=True)             # quedan las 6 métricas de la pizza
nombres = {"Goles sin penal": "Non-penalty goals /90", "Tiros a puerta": "Shots on target /90", "Tiros": "Shots /90",
           "xA": "xA /90", "Oportunidades creadas": "Chances created /90", "Regates exitosos": "Dribbles won /90"}
df["label"] = df.metrica.map(nombres)
df = df.sort_values("pct").reset_index(drop=True)
color = [MORA if f.startswith("FBref") else AZUL for f in df.fuente]

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=80, facecolor=BG)
fig.subplots_adjust(left=0.30, right=0.93, top=0.80, bottom=0.14)
FRAMES, HOLD = 40, 25
fig.suptitle("Gilberto Mora vs. Liga MX attacking midfielders & wingers", color=TXT, fontsize=16, fontweight="bold", y=0.96)
fig.text(0.5, 0.86, "percentile among same-position peers (36-58 players per metric)", ha="center", color=SUAVE, fontsize=11)
fig.text(0.5, 0.04, "gold: FBref 2025-26 (full season)   |   blue: FotMob Apertura 2026/27 (small sample)", ha="center", color=SUAVE, fontsize=10)

def draw(k):
    ax.clear(); ax.set_facecolor(BG)
    t = min(k / FRAMES, 1); t = 1 - (1 - t) ** 3                          # ease-out
    ax.barh(df.label, df.pct * t, color=color, height=0.62)
    ax.axvline(50, color=SUAVE, lw=1.2, ls="--")
    ax.text(50, len(df) - 0.35, "median peer", color=SUAVE, ha="center", fontsize=10)
    for i, v in enumerate(df.pct * t):
        ax.text(v + 1.5, i, f"{v:.0f}", va="center", color=TXT, fontsize=14, fontweight="bold")
    ax.set_xlim(0, 105); ax.set_xticks([]); ax.tick_params(axis="y", colors=TXT, labelsize=12, length=0)
    for s in ax.spines.values(): s.set_visible(False)

os.makedirs("docs/img", exist_ok=True)
ani = FuncAnimation(fig, draw, frames=FRAMES + HOLD, interval=50)
ani.save("docs/img/percentiles.gif", writer=PillowWriter(fps=20), savefig_kwargs={"facecolor": BG})
print("ok", os.path.getsize("docs/img/percentiles.gif") // 1024, "KB")
