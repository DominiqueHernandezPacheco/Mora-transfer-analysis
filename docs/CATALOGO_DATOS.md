# Catálogo de datos

| Archivo | Filas | Fuente | ¿Por qué lo usamos? |
|---|---|---|---|
| `ligamx_2025-26_stats.csv` | 612 | FBref | Torneo completo de Liga MX 2025-26 (minutos, goles, penales, asistencias): base para calcular por 90 y quitar penales |
| `ligamx_2025-26_shooting.csv` | 612 | FBref | Tiros y tiros a puerta de esa misma temporada; se une con la tabla anterior |
| `fotmob_ligamx_2026-27_apertura_minutos.csv` | 451 | FotMob | Minutos y partidos de TODA la liga: sin minutos no se puede normalizar nada por 90 |
| `fotmob_ligamx_2026-27_apertura_xg.csv` | 367 | FotMob | xG de toda la liga (incluye penales): ver quién crea más peligro de gol |
| `fotmob_ligamx_2026-27_apertura_xg_por90.csv` | 290 | FotMob | xG por 90 publicado por FotMob: sirve para VALIDAR mi transcripción del xG total |
| `fotmob_ligamx_2026-27_apertura_xa.csv` | 448 | FotMob | xA (asistencias esperadas): mide creación de juego, que las asistencias solas no capturan |
| `fotmob_ligamx_2026-27_apertura_xa_por90.csv` | 317 | FotMob | xA por 90: comparar creación entre jugadores con distintos minutos |
| `fotmob_ligamx_2026-27_apertura_tiros_por90.csv` | 290 | FotMob | Tiros por 90 y % de conversión: volumen y eficiencia de remate |
| `fotmob_ligamx_2026-27_apertura_oportunidades_creadas.csv` | 341 | FotMob | Oportunidades creadas: pases que terminan en tiro, la creación de un mediapunta |
| `fotmob_ligamx_2026-27_apertura_regates_por90.csv` | 256 | FotMob | Regates exitosos por 90: el otro rasgo que se le pide a un mediapunta o extremo |
| `*_fbref_standard.csv (9 archivos)` | 85 | FBref | Cohorte de 9 jugadores que dieron el salto: minutos, goles y asistencias por temporada, con club y edad |
| `*_fbref_shooting.csv (9 archivos)` | 83 | FBref | Cohorte: tiros y tiros a puerta por temporada |
| `players.csv.gz` | 50,149 | Transfermarkt (dataset abierto) | Fecha de nacimiento, posición real y valor de mercado: para comparar solo mismo puesto y calcular edades exactas |
| `transfers.csv.gz` | 175,165 | Transfermarkt (dataset abierto) | Todos los traspasos con fecha y monto: récords y precedentes del salto |
| `clubs.csv.gz` | 796 | Transfermarkt (dataset abierto) | A qué liga pertenece cada club: filtrar ventas desde Liga MX y hacia Europa |
| `competitions.csv.gz` | 65 | Transfermarkt (dataset abierto) | Catálogo de ligas que cubre el dataset (para saber qué NO está cubierto) |
| `ligamx_2026-27_apertura_fotmob_merged.csv` | 451 | Derivado (8 tablas de FotMob) | Una fila por jugador con todas las métricas: la tabla que se usa para percentiles |
| `cohorte_traspasos.csv` | 9 | Derivado (Transfermarkt) | Primer salto de cada jugador de la cohorte: edad exacta, monto y valor en ese momento |
| `manual.csv` | 27 | FotMob (perfil de Mora) | Datos propios de Mora (xG, npxG, xA, rankings) con fuente y fecha |
| `cohort_players.csv` | 13 | Mío (lista de trabajo) | Lista de jugadores a verificar, con las notas de lo que se corrigió |
