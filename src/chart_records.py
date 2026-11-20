"""¿Récord? Traspasos más caros de mexicanos y de clubes de Liga MX frente al rumor. Vertical 9:16, fondo oscuro.
Datos: Transfermarkt (dataset abierto dcaribou, al 2026-07-06). El rumor es de prensa y NO está verificado."""
import matplotlib.pyplot as plt

BG, MORA, GRIS, TEAL, TXT, SUAVE = "#0e1117", "#FFB000", "#5b6472", "#2FB5A0", "#f2f2f2", "#7d8794"
# (etiqueta, millones de euros, tipo)   tipo: mx = fichaje de un mexicano (cualquier club); liga = venta desde un club de Liga MX; rumor
datos = [
    ("Rumor: Mora\n≈ 50 M$ ≈ 45 M€", 45.0, "rumor"),
    ("Lozano\nPSV→Napoli 2019", 50.0, "mx"),
    ("Álvarez\nAjax→West Ham 2023", 38.0, "mx"),
    ("Jiménez\nBenfica→Wolves 2019", 38.0, "mx"),
    ("Giménez\nFeyenoord→Milan 2025", 30.2, "mx"),
    ("Récord Liga MX\nÁlvarez 2019 =\nValencia 2014", 15.0, "liga"),
]
datos = sorted(datos, key=lambda x: x[1])
color = {"rumor": MORA, "mx": GRIS, "liga": TEAL}

fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100, facecolor=BG)
ax.set_facecolor(BG)
bars = ax.barh([d[0] for d in datos], [d[1] for d in datos], color=[color[d[2]] for d in datos], height=0.62)
for b, d in zip(bars, datos):
    ax.text(b.get_width() + 0.8, b.get_y() + b.get_height() / 2, f"{d[1]:g} M€" + ("*" if d[2] == "rumor" else ""),
            va="center", color=TXT, fontsize=34, fontweight="bold")
ax.set_xlim(0, 70)
ax.tick_params(axis="y", colors=TXT, labelsize=20, length=0); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
fig.subplots_adjust(left=0.37, right=0.97, top=0.76, bottom=0.34)

fig.text(0.5, 0.925, "50 MILLONES\nDE DÓLARES:\n¿RÉCORD?", ha="center", va="center", color=TXT, fontsize=56, fontweight="bold", linespacing=1.05)
fig.text(0.5, 0.815, "Los fichajes más caros de mexicanos", ha="center", color=MORA, fontsize=30)
fig.text(0.5, 0.265, "Venta más cara de un club de Liga MX:\nSÍ, por mucho", ha="center", va="center", color=TEAL, fontsize=30, fontweight="bold", linespacing=1.2)
fig.text(0.5, 0.195, "Mexicano más caro de la historia:\nNO (Lozano, 50 M€)", ha="center", va="center", color=TXT, fontsize=30, fontweight="bold", linespacing=1.2)
fig.text(0.5, 0.09, "* Rumor de prensa, no verificado.\nConversión de dólares a euros aproximada.\n"
                    "Fuente: Transfermarkt (dataset abierto, al 6-jul-2026).\n"
                    "Gris: mexicano en cualquier club · Verde: venta desde Liga MX",
         ha="center", va="center", color=SUAVE, fontsize=20)
fig.savefig("outputs/04_records.png", facecolor=BG)
print("ok")
