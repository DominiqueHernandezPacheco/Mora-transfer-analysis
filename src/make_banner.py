"""Banner del README (1280x400) e imagen de vista previa social de GitHub (1280x640). Salida: docs/img/"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG, CARD, MORA, TXT, SUAVE = "#0e1117", "#1a2029", "#FFB000", "#f2f2f2", "#7d8794"
STATS = [("p84", "non-penalty goals per 90\nvs. same-position peers"),
         ("4 of 5", "current-tournament goals\nare penalties (7 matches)"),
         ("4.5x", "the rumored fee vs.\nhis Transfermarkt value")]


def lienzo(w, h, alto_cards, y_cards, y_titulo, y_sub, nombre):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, h - 8), w, 8, boxstyle="square,pad=0", facecolor=MORA, edgecolor=MORA))
    ax.text(w / 2, y_titulo, "Is the Gilberto Mora transfer rumor real?", ha="center", va="center", color=TXT,
            fontsize=36 if h < 500 else 38, fontweight="bold")
    ax.text(w / 2, y_sub, "A data check on the ~€45M talk: Liga MX peers, penalties, and 9 precedents", ha="center",
            va="center", color=MORA, fontsize=16.5 if h < 500 else 18)
    ancho, sep = 360, 30
    x0 = (w - (3 * ancho + 2 * sep)) / 2
    for i, (grande, chico) in enumerate(STATS):
        x = x0 + i * (ancho + sep)
        ax.add_patch(FancyBboxPatch((x, y_cards), ancho, alto_cards, boxstyle="round,pad=0,rounding_size=14",
                                    facecolor=CARD, edgecolor="#2a323d", linewidth=2))
        ax.text(x + ancho / 2, y_cards + alto_cards * 0.64, grande, ha="center", va="center", color=MORA,
                fontsize=h / 9, fontweight="bold")
        ax.text(x + ancho / 2, y_cards + alto_cards * 0.22, chico, ha="center", va="center", color=SUAVE,
                fontsize=h / 34, linespacing=1.3)
    os.makedirs("docs/img", exist_ok=True)
    fig.savefig(f"docs/img/{nombre}", facecolor=BG)
    plt.close(fig)


lienzo(1280, 400, 170, 40, 338, 292, "banner.png")
lienzo(1280, 640, 280, 70, 545, 480, "social_preview.png")
print("ok")
