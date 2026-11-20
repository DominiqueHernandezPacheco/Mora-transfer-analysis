"""Genera notebooks/mora_analisis.ipynb (se ejecuta después con nbconvert). Ejecutar desde la raíz del proyecto."""
import nbformat as nbf

md = lambda s: nbf.v4.new_markdown_cell(s.strip("\n"))
code = lambda s: nbf.v4.new_code_cell(s.strip("\n"))
C = []

C.append(md("""
# Gilberto Mora: ¿qué tan real es el rumor de los 50 M$?

**Pregunta:** ¿quién es Mora hoy frente a sus pares de posición en Liga MX, qué pasó con los jugadores que dieron el salto a Europa a su edad y qué tan inusual sería un traspaso de ~45 M€?
**Lo que este análisis NO hace:** no predice si se va, no modela su valor de mercado y no estima cómo le iría en Europa (eso es el video 2).

Todo lo de aquí son datos, no opiniones. Cada cifra sale de los CSV de `data/` y cada tabla indica su fuente.
"""))

C.append(code("""
import os, sys
if os.path.basename(os.getcwd()) == "notebooks": os.chdir("..")   # trabajar desde la raíz del proyecto
sys.path.insert(0, "src")
import pandas as pd
from IPython.display import Image, display
pd.options.display.float_format = "{:.2f}".format
"""))

C.append(md("""
## 1. Datos y fuentes
Tres fuentes gratuitas. FBref y FotMob se copiaron tabla por tabla; Transfermarkt es un dataset abierto descargado.
"""))
C.append(code("""
fuentes = pd.DataFrame([
    ("FBref", "Liga MX 2025-26 completa", "minutos, goles, penales, tiros", "copiado a mano"),
    ("FotMob", "Apertura 2026/27 (11 jornadas)", "xG, xA, regates, oportunidades creadas", "copiado a mano"),
    ("Transfermarkt (dataset abierto)", "histórico, al 6-jul-2026", "posición, nacimiento, traspasos y montos", "descargado"),
], columns=["fuente", "cobertura", "qué aporta", "cómo se obtuvo"])
fuentes
"""))

C.append(md("""
## 2. Validación de la captura manual
Las tablas de FotMob se copiaron a mano. Para detectar errores se usa una identidad: si el total (xG) está bien copiado, `xG / (minutos / 90)` debe coincidir con el xG por 90 que publica la misma página.
Solo se puede revisar así donde FotMob publica el dato por 90 (xG y xA); oportunidades creadas y regates quedan sin contraste (ver limitaciones).
"""))
C.append(code("""
from showcase import validar_transcripcion          # total/(min/90) vs el dato por 90 publicado

liga = pd.read_csv("data/processed/ligamx_2026-27_apertura_fotmob_merged.csv")
for total, por90 in [("xg", "xg_per90"), ("xa", "xa_per90")]:
    d = liga.dropna(subset=[total, por90])
    print(f"{total}: {validar_transcripcion(d, total, por90):.0%} de {len(d)} jugadores cuadra (tolerancia 0.15)")
"""))

C.append(md("""
## 3. Normalizar: por 90 minutos y sin penales
- **Por 90:** convierte todo a "qué haría en un partido completo", para no favorecer a quien jugó más.
- **Sin penales:** Mora cobra penales; un penal vale ~0.8 de xG y le infla los goles.
- **Minutos mínimos (≥ 900 en FBref, ≥ 450 en FotMob):** se usan para elegir a los pares comparables, no se descarta a nadie de las tablas.
"""))
C.append(code("""
from showcase import por_90
from load_fbref import load_league

f = load_league("data/raw/ligamx_2025-26_stats.csv", "data/raw/ligamx_2025-26_shooting.csv")
mora = f[f.Player == "Gilberto Mora"]
print("Mora, Liga MX 2025-26 (FBref):", int(mora.MP.iloc[0]), "partidos,", int(mora.Min.iloc[0]), "min,",
      int(mora.Gls.iloc[0]), "goles,", int(mora.PK.iloc[0]), "de penal (cobró", int(mora.PKatt.iloc[0]), ")")
por_90(mora)
"""))

C.append(md("""
## 4. ¿Quién es Mora frente a sus pares de posición?
Pares = mediapuntas y extremos (`sub_position` de Transfermarkt: Attacking Midfield, Left Winger, Right Winger) de Liga MX. El percentil dice a cuántos de ellos supera.
"""))
C.append(code("""
from pares_posicion import percentiles
tabla = percentiles().rename(columns={"metrica": "métrica", "valor": "Mora", "pct": "percentil", "n": "pares", "fuente": "fuente"})
tabla[["métrica", "Mora", "percentil", "pares", "fuente"]].round(2)
"""))
C.append(code("""display(Image("outputs/03_pizza_pares.png", width=360))"""))

C.append(md("""
## 5. Los penales en el torneo actual
Con penales, Mora tiene el segundo xG por 90 de la liga; sin ellos baja mucho. La muestra es pequeña (7 partidos, 499 min, menos de la mitad de los 1,131 min de 2025-26).
"""))
C.append(code("""
m = pd.read_csv("data/manual.csv")
m = m[m.season.astype(str).str.startswith("2026/27") & m.metric.isin(["minutes", "matches", "goals", "penalty_goals", "xG", "npxG"])]
m[["metric", "value", "source"]]
"""))
C.append(code("""display(Image("outputs/01_penales_vertical.png", width=360))"""))

C.append(md("""
## 6. Precedentes: jugadores que dieron el salto a Europa a los ~18 años
`monto/valor` = lo que se pagó dividido entre el valor de mercado de Transfermarkt en ese momento. Mora está valorado en 10 M€; 45 M€ serían 4.5 veces su valor.
"""))
C.append(code("""
c = pd.read_csv("data/processed/cohorte_traspasos.csv")
c.sort_values("edad_al_traspaso")
"""))
C.append(code("""
sin_lainez = c[c.jugador != "Lainez"]["monto/valor"]
print("Los otros 8 casos: de", sin_lainez.min(), "a", sin_lainez.max(), "veces su valor | Lainez:", c.loc[c.jugador == "Lainez", "monto/valor"].iloc[0])
print("Rumor / valor de Mora:", round(45 / 10, 1), "veces (45 M€ aprox. / 10 M€)")
display(Image("outputs/05_precedentes_18.png", width=360))
"""))

C.append(md("""
## 7. Récords
La venta más cara de un club de Liga MX, y los fichajes más caros de mexicanos (Transfermarkt abierto).
"""))
C.append(code("""
D = "data/external/transfermarkt_dcaribou"
tr = pd.read_csv(f"{D}/transfers.csv.gz", parse_dates=["transfer_date"]); pl = pd.read_csv(f"{D}/players.csv.gz")
cl = pd.read_csv(f"{D}/clubs.csv.gz").set_index("club_id").domestic_competition_id
tr["liga_origen"] = tr.from_club_id.map(cl)
t = tr.merge(pl[["player_id", "country_of_citizenship"]], on="player_id"); t["monto_M€"] = t.transfer_fee / 1e6
cols = ["transfer_date", "player_name", "from_club_name", "to_club_name", "monto_M€"]
print("Ventas más caras desde clubes de Liga MX:"); display(t[t.liga_origen == "MEX1"].nlargest(3, "monto_M€")[cols])
print("Fichajes más caros de mexicanos:"); display(t[t.country_of_citizenship == "Mexico"].nlargest(3, "monto_M€")[cols])
"""))
C.append(code("""display(Image("outputs/04_records.png", width=360))"""))

C.append(md("""
## 8. Conclusiones (dato + confianza)
| # | Conclusión | Dato | Confianza |
|---|---|---|---|
| 1 | Mora marca más de lo que crea | Goles sin penal p84, tiros a puerta p83 (58 pares, 2025-26); xA p35, oportunidades p32, regates p44 (36-37 pares, Apertura 26/27) | **Media** (muestras chicas, dos temporadas) |
| 2 | Su torneo actual depende de penales | 4 de 5 goles de penal; npxG 0.35 por 90 en 499 min. En 2025-26: 0 goles de penal | **Alta** en el dato, **baja** para proyectar |
| 3 | ~45 M€ serían la venta más cara de un club de Liga MX | Récord actual: 15 M€, compartido por Álvarez (2019) y Valencia (2014) | **Alta** |
| 4 | No sería el mexicano más caro | Lozano: 50 M€ (2019) | **Alta** |
| 5 | El precio sería inusual frente a su valor | 8 de 9 casos entre 0.75 y 1.54 veces el valor; Mora: 4.5 veces | **Media** (n = 9) |
| — | Probabilidad de que se vaya | No calculable con estos datos | — |

"Inflado" es lectura de estos datos, no un hecho: un club puede pagar por proyección y este análisis no la mide.
"""))

C.append(md("""
## 9. Limitaciones
- **Muestras pequeñas:** 9 traspasos, 36-58 pares por métrica, 499 minutos en el torneo actual.
- **Dos temporadas distintas** en la pizza (goles y tiros: 2025-26; xA, oportunidades y regates: Apertura 2026/27).
- **Sin xG/npxG de Liga MX en FBref**; el xG de FotMob incluye penales.
- **Captura manual:** validada para xG y xA; oportunidades creadas y regates no tienen contraste.
- **Sin ajuste por fuerza de liga** (Liga MX, Brasileirão y Liga Argentina no son equivalentes; no se encontró fuente pública de coeficientes).
- **Transfermarkt abierto** está pausado desde el 6-jul-2026; las posiciones cubren 75-80% de los jugadores de Liga MX.
- **Los 50 M$ son un rumor de prensa**; la conversión a euros es aproximada.
- **Sin datos de salarios ni de lesiones.** No se sabe por qué Mora tiene 7 partidos en 11 jornadas, ni por qué algunos casos del salto a Europa tuvieron poca continuidad.
- **No se hizo:** validación leave-one-out, bootstrap (sin datos por partido) ni similitud entre jugadores (video 2).
"""))

C.append(md("""
## 10. Las tres funciones que se enseñan en pantalla (`src/showcase.py`)
"""))
C.append(code("""
import inspect, showcase
for fn in (showcase.por_90, showcase.percentil_entre_pares, showcase.validar_transcripcion):
    print(inspect.getsource(fn))
"""))

nb = nbf.v4.new_notebook(cells=C)
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nbf.write(nb, "notebooks/mora_analisis.ipynb")
print("ok", len(C), "celdas")
