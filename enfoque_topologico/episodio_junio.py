"""Inspección de H1 y sensibilidad al pico del 15 de junio."""
import csv
import json
from math import log1p
from statistics import median

from analisis import HERE, METRIC, rips_diagrams, wasserstein


def main():
    with (HERE.parent / "datos" / "transformados" / "series_diarias_pagina.csv").open(encoding="utf-8-sig", newline="") as stream:
        source = list(csv.DictReader(stream))
    dates = [row["fecha"] for row in source]
    values = [int(row[METRIC]) for row in source]
    peak = dates.index("2026-06-15")
    comparison = values.copy()
    comparison[peak] = median(values[peak - 7:peak] + values[peak + 1:peak + 8])
    output = {}
    for label, series in (("observada", values), ("pico_sustituido", comparison)):
        transformed = list(map(log1p, series))
        previous = None
        entries = []
        for end in range(peak, peak + 3):
            cloud = [tuple(transformed[t - lag] for lag in range(7))
                     for t in range(end - 27, end + 1)]
            _, diagram = rips_diagrams(cloud)
            entries.append({
                "fecha": dates[end],
                "visualizaciones": series[end],
                "diagrama_h1": sorted(diagram, key=lambda point: point[0] - point[1]),
                "wasserstein_h1": None if previous is None else wasserstein(previous, diagram),
            })
            previous = diagram
        output[label] = entries
    with (HERE / "distancias.csv").open(newline="") as stream:
        active = [row for row in csv.DictReader(stream)
                  if (row["escala"], row["dimension"], row["puntos"]) == ("log1p", "7", "28")
                  and row["inicio_ventana"] > "2026-04-08" and row["wasserstein_h1"]]
    ranked = sorted(active, key=lambda row: float(row["wasserstein_h1"]), reverse=True)
    output["ventanas_comparadas_en_tramo_activo"] = len(active)
    output["mayores_distancias_en_tramo_activo"] = [
        {"fecha": row["fecha"], "wasserstein_h1": float(row["wasserstein_h1"])}
        for row in ranked[:5]
    ]
    (HERE / "episodio_junio.json").write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
