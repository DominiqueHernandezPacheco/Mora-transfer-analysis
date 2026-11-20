"""De dónde salen los datos: tres tarjetas apiladas -> un análisis. Vertical 9:16, fondo oscuro."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG, MORA, TXT, SUAVE, CARD = "#0e1117", "#FFB000", "#f2f2f2", "#7d8794", "#1a2029"
TARJETAS = [  # (fuente, color, qué aporta, línea de detalle)
    ("FBref", "#2FB5A0", "LA TEMPORADA COMPLETA", "Liga MX 2025-26\nminutos · goles · penales · tiros"),
    ("FotMob", "#5B8DEF", "LO MÁS AVANZADO", "Apertura 2026/27\nxG · xA · regates · oportunidades"),
    ("Transfermarkt", "#E4572E", "EL CONTEXTO", "puesto · fecha de nacimiento\ntraspasos y montos"),
]

fig = plt.figure(figsize=(10.8, 19.2), dpi=100, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_facecolor(BG)

ax.text(0.5, 0.90, "3 FUENTES", ha="center", va="center", color=TXT, fontsize=64, fontweight="bold")
ax.text(0.5, 0.845, "todas gratis", ha="center", va="center", color=MORA, fontsize=34)

y0, alto, sep = 0.735, 0.14, 0.17
for i, (nombre, c, rol, detalle) in enumerate(TARJETAS):
    y = y0 - i * sep
    ax.add_patch(FancyBboxPatch((0.07, y - alto / 2), 0.86, alto, boxstyle="round,pad=0.0,rounding_size=0.025",
                                facecolor=CARD, edgecolor=c, linewidth=4))
    ax.text(0.11, y + 0.038, nombre, ha="left", va="center", color=c, fontsize=44, fontweight="bold")
    ax.text(0.11, y + 0.000, rol, ha="left", va="center", color=TXT, fontsize=24, fontweight="bold")
    ax.text(0.11, y - 0.036, detalle, ha="left", va="center", color=SUAVE, fontsize=21, linespacing=1.3)

ax.annotate("", xy=(0.5, 0.215), xytext=(0.5, 0.275), arrowprops=dict(arrowstyle="-|>", color=MORA, lw=6, mutation_scale=45))
ax.add_patch(FancyBboxPatch((0.07, 0.10), 0.86, 0.10, boxstyle="round,pad=0.0,rounding_size=0.025", facecolor=MORA, edgecolor=MORA))
ax.text(0.5, 0.15, "1 ANÁLISIS", ha="center", va="center", color=BG, fontsize=46, fontweight="bold")
ax.text(0.5, 0.045, "Datos de FBref, FotMob y Transfermarkt\n"
                    "(dataset abierto, al 6-jul-2026).", ha="center", va="center", color=SUAVE, fontsize=20, linespacing=1.4)
fig.savefig("outputs/00_fuentes.png", facecolor=BG)
print("ok")
