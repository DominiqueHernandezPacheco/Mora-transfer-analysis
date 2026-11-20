"""Pizza de Mora frente a mediapuntas y extremos de Liga MX (percentiles). Vertical 9:16, fondo oscuro."""
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from pares_posicion import percentiles

BG, MORA, CREA, TXT, GRIS = "#0e1117", "#FFB000", "#4EA8DE", "#f2f2f2", "#7d8794"
d = percentiles()
etiquetas = {"Goles sin penal": "Goles sin\npenal /90", "Tiros a puerta": "Tiros a\npuerta /90", "Tiros": "Tiros\n/90",
             "Asistencias": "Asistencias\n/90", "xA": "xA\n/90", "Oportunidades creadas": "Oport.\ncreadas /90",
             "Regates exitosos": "Regates\nexitosos /90"}
params = [etiquetas[m] for m in d.metrica]
values = [round(p) for p in d.pct]
colores = [MORA if g == "marca" else CREA for g in d.grupo]

baker = PyPizza(params=params, background_color=BG, straight_line_color=BG, straight_line_lw=1,
                last_circle_lw=0, other_circle_lw=0, inner_circle_size=18)
fig, ax = baker.make_pizza(
    values, figsize=(10.8, 10.8), color_blank_space=["#232a35"] * len(values), slice_colors=colores,
    value_colors=["#111"] * len(values), value_bck_colors=colores, blank_alpha=1,
    kwargs_slices=dict(edgecolor=BG, zorder=2, linewidth=2),
    kwargs_params=dict(color=TXT, fontsize=21, va="center"),
    kwargs_values=dict(color="#111", fontsize=30, fontweight="bold", zorder=3,
                       bbox=dict(edgecolor=BG, facecolor="cornflowerblue", boxstyle="round,pad=0.25", lw=1)))
fig.set_size_inches(10.8, 19.2)
ax.set_position([0.14, 0.36, 0.72, 0.405])
fig.set_facecolor(BG)

fig.text(0.5, 0.925, "GILBERTO MORA", ha="center", color=TXT, fontsize=58, fontweight="bold")
fig.text(0.5, 0.885, "¿Qué hace bien frente a sus pares?", ha="center", color=MORA, fontsize=34)
fig.text(0.5, 0.855, "Percentil entre mediapuntas y extremos de Liga MX", ha="center", color=TXT, fontsize=24)
fig.text(0.5, 0.305, "Marca:  gol y puntería arriba del promedio", ha="center", color=MORA, fontsize=30, fontweight="bold")
fig.text(0.5, 0.268, "Crea y regatea:  por debajo del promedio", ha="center", color=CREA, fontsize=30, fontweight="bold")
n1, n2a, n2b = d.n.iloc[0], d.n.iloc[4:].min(), d.n.iloc[4:].max()
fig.text(0.5, 0.14, f"Dorado: FBref 2025-26 (n={n1}, 900+ min)\nAzul: FotMob Apertura 26/27 (n={n2a}-{n2b}, 450+ min)\n"
                     "Posición: Transfermarkt · Muestras chicas · Sin ajuste de liga\nMora tenía 16-17 años en la muestra 2025-26",
         ha="center", color=GRIS, fontsize=20)
fig.savefig("outputs/03_pizza_pares.png", facecolor=BG)
print(d.round(2).to_string(index=False))
