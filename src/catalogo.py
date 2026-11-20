"""Genera docs/CATALOGO_DATOS.md: cada CSV del proyecto con filas, fuente y el PORQUÉ de usarlo."""
import glob, gzip, os
import pandas as pd

R = "data/raw/"
CAT = [  # (patrón, fuente, para qué sirve)
    (R + "ligamx_2025-26_stats.csv", "FBref", "Torneo completo de Liga MX 2025-26 (minutos, goles, penales, asistencias): base para calcular por 90 y quitar penales"),
    (R + "ligamx_2025-26_shooting.csv", "FBref", "Tiros y tiros a puerta de esa misma temporada; se une con la tabla anterior"),
    (R + "fotmob_ligamx_2026-27_apertura_minutos.csv", "FotMob", "Minutos y partidos de TODA la liga: sin minutos no se puede normalizar nada por 90"),
    (R + "fotmob_ligamx_2026-27_apertura_xg.csv", "FotMob", "xG de toda la liga (incluye penales): ver quién crea más peligro de gol"),
    (R + "fotmob_ligamx_2026-27_apertura_xg_por90.csv", "FotMob", "xG por 90 publicado por FotMob: sirve para VALIDAR mi transcripción del xG total"),
    (R + "fotmob_ligamx_2026-27_apertura_xa.csv", "FotMob", "xA (asistencias esperadas): mide creación de juego, que las asistencias solas no capturan"),
    (R + "fotmob_ligamx_2026-27_apertura_xa_por90.csv", "FotMob", "xA por 90: comparar creación entre jugadores con distintos minutos"),
    (R + "fotmob_ligamx_2026-27_apertura_tiros_por90.csv", "FotMob", "Tiros por 90 y % de conversión: volumen y eficiencia de remate"),
    (R + "fotmob_ligamx_2026-27_apertura_oportunidades_creadas.csv", "FotMob", "Oportunidades creadas: pases que terminan en tiro, la creación de un mediapunta"),
    (R + "fotmob_ligamx_2026-27_apertura_regates_por90.csv", "FotMob", "Regates exitosos por 90: el otro rasgo que se le pide a un mediapunta o extremo"),
    (R + "players/*_fbref_standard.csv", "FBref", "Cohorte de 9 jugadores que dieron el salto: minutos, goles y asistencias por temporada, con club y edad"),
    (R + "players/*_fbref_shooting.csv", "FBref", "Cohorte: tiros y tiros a puerta por temporada"),
    ("data/external/transfermarkt_dcaribou/players.csv.gz", "Transfermarkt (dataset abierto)", "Fecha de nacimiento, posición real y valor de mercado: para comparar solo mismo puesto y calcular edades exactas"),
    ("data/external/transfermarkt_dcaribou/transfers.csv.gz", "Transfermarkt (dataset abierto)", "Todos los traspasos con fecha y monto: récords y precedentes del salto"),
    ("data/external/transfermarkt_dcaribou/clubs.csv.gz", "Transfermarkt (dataset abierto)", "A qué liga pertenece cada club: filtrar ventas desde Liga MX y hacia Europa"),
    ("data/external/transfermarkt_dcaribou/competitions.csv.gz", "Transfermarkt (dataset abierto)", "Catálogo de ligas que cubre el dataset (para saber qué NO está cubierto)"),
    ("data/processed/ligamx_2026-27_apertura_fotmob_merged.csv", "Derivado (8 tablas de FotMob)", "Una fila por jugador con todas las métricas: la tabla que se usa para percentiles"),
    ("data/processed/cohorte_traspasos.csv", "Derivado (Transfermarkt)", "Primer salto de cada jugador de la cohorte: edad exacta, monto y valor en ese momento"),
    ("data/manual.csv", "FotMob (perfil de Mora)", "Datos propios de Mora (xG, npxG, xA, rankings) con fuente y fecha"),
    ("data/cohort_players.csv", "Mío (lista de trabajo)", "Lista de jugadores a verificar, con las notas de lo que se corrigió"),
]

def filas(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f) - 1

lineas = ["# Catálogo de datos", "", "| Archivo | Filas | Fuente | ¿Por qué lo usamos? |", "|---|---|---|---|"]
for patron, fuente, porque in CAT:
    archivos = sorted(glob.glob(patron))
    if not archivos:
        continue
    n = sum(filas(a) for a in archivos)
    nombre = os.path.basename(patron) if len(archivos) == 1 else f"{os.path.basename(patron)} ({len(archivos)} archivos)"
    lineas.append(f"| `{nombre}` | {n:,} | {fuente} | {porque} |")
os.makedirs("docs", exist_ok=True)
open("docs/CATALOGO_DATOS.md", "w", encoding="utf-8").write("\n".join(lineas) + "\n")
print("\n".join(lineas))
