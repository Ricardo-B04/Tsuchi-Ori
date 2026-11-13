"""Comparación cronológica de Ridge multivariado con y sin topología."""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from enfoque_pronostico.pronostico import MIN_TRAIN, PENALTY, PEAK_DATE, features, load_series
from enfoque_topologico.analisis import rips_diagrams, wasserstein

COLUMNS = (
    "pagina_visualizaciones", "pagina_espectadores", "pagina_interacciones",
    "pagina_visitas", "pagina_seguidores_metrica_diaria",
)
DIMENSION, POINTS = 7, 28
HISTORY = DIMENSION + POINTS


def topological_features(history):
    """Escala ambas nubes con los 35 días disponibles para esta comparación."""
    q1, q3 = np.quantile(history, [0.25, 0.75], axis=0)
    scale = q3 - q1
    scale[scale == 0] = 1
    scaled = (history - np.median(history, axis=0)) / scale
    vectors = [tuple(scaled[end - np.arange(DIMENSION)].ravel())
               for end in range(DIMENSION - 1, len(scaled))]
    previous = rips_diagrams(vectors[:-1])
    current = rips_diagrams(vectors[1:])
    return [wasserstein(a, b) for a, b in zip(previous, current)]


def predict(design, targets, today):
    mean = design.mean(axis=0)
    scale = design.std(axis=0)
    scale[scale == 0] = 1
    normalized = (design - mean) / scale
    center = targets.mean()
    penalty = PENALTY * np.eye(design.shape[1])
    weights = np.linalg.solve(normalized.T @ normalized + penalty,
                              normalized.T @ (targets - center))
    return max(0.0, float(np.expm1(center + ((today - mean) / scale) @ weights)))


def evaluate(dates, values):
    logs = np.log1p(values)
    start = HISTORY - 1
    common = []
    augmented = []
    for t in range(start, len(dates) - 1):
        # Los dos términos calendáricos se incluyen una sola vez.
        columns = [features(logs[:, i], dates, t, 1) for i in range(len(COLUMNS))]
        baseline = [value for column in columns for value in column[:-2]] + columns[0][-2:]
        common.append(baseline)
        augmented.append(baseline + topological_features(logs[t - start:t + 1]))
    for t in range(MIN_TRAIN - 1, len(dates) - 1):
        idx = t - start
        targets = logs[start + 1:t + 1, 0]
        yield dict(origen=dates[t], fecha=dates[t + 1], real=values[t + 1, 0],
                   ultimo_dia=values[t, 0],
                   ridge=predict(np.asarray(common[:idx]), targets, np.asarray(common[idx])),
                   ridge_tda=predict(np.asarray(augmented[:idx]), targets, np.asarray(augmented[idx])))


def main():
    dates, _ = load_series()
    with (HERE.parent / "datos/transformados/series_diarias_pagina.csv").open(
            encoding="utf-8-sig", newline="") as file:
        by_date = {row["fecha"]: row for row in csv.DictReader(file)}
    values = np.asarray([[int(by_date[d.isoformat()][key]) for key in COLUMNS] for d in dates])
    forecasts = list(evaluate(dates, values))
    with (HERE / "predicciones_ridge_tda.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=forecasts[0].keys())
        writer.writeheader()
        writer.writerows(forecasts)
    for label, rows in [("Todas", forecasts),
                        ("Sin objetivo del 26 de agosto", [r for r in forecasts if r["fecha"] != PEAK_DATE])]:
        print(label, len(rows), rows[0]["fecha"], rows[-1]["fecha"])
        for model in ("ultimo_dia", "ridge", "ridge_tda"):
            errors = np.array([r[model] - r["real"] for r in rows])
            print(model, "MAE", round(np.abs(errors).mean(), 2),
                  "RMSE", round(np.sqrt(np.mean(errors**2)), 2),
                  "MedAE", round(np.median(np.abs(errors)), 2))


if __name__ == "__main__":
    main()
