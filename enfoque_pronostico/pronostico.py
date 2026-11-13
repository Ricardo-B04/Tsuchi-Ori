"""Evaluación retrospectiva de visualizaciones con origen móvil."""
import csv
from datetime import date, timedelta
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
PEAK_DATE = date(2026, 8, 26)
MIN_TRAIN = 56
LOOKBACK = 14
PENALTY = 10.0


def load_series():
    source = HERE.parent / "datos" / "transformados" / "series_diarias_pagina.csv"
    with source.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    dates = [date.fromisoformat(row["fecha"]) for row in rows]
    values = np.asarray([int(row["pagina_visualizaciones"]) for row in rows])
    if any(next_day - day != timedelta(days=1) for day, next_day in zip(dates, dates[1:])):
        raise ValueError("La serie debe tener una fila por día calendario consecutivo.")
    start = next(i for i, value in enumerate(values) if value > 0)
    return dates[start:], values[start:]


def features(log_values, dates, origin, horizon):
    history = log_values[:origin + 1]
    weekday = (dates[origin] + timedelta(days=horizon)).weekday()
    return [
        history[-1], history[-2], history[-7], history[-14],
        history[-7:].mean(), history[-14:].mean(),
        np.sin(2 * np.pi * weekday / 7), np.cos(2 * np.pi * weekday / 7),
    ]


def ridge_prediction(values, dates, horizon, cap):
    origin = len(values) - 1
    if cap:
        values = np.minimum(values, np.quantile(values, .95))
    logs = np.log1p(values)
    origins = range(LOOKBACK - 1, origin - horizon + 1)
    design = np.array([features(logs, dates, t, horizon) for t in origins])
    targets = np.array([logs[t + horizon] for t in origins])
    mean = design.mean(axis=0)
    scale = design.std(axis=0)
    scale[scale == 0] = 1
    normalized = (design - mean) / scale
    penalty = PENALTY * np.eye(design.shape[1])
    weights = np.linalg.solve(normalized.T @ normalized + penalty,
                              normalized.T @ (targets - targets.mean()))
    next_features = (np.array(features(logs, dates, origin, horizon)) - mean) / scale
    return max(0, float(np.expm1(targets.mean() + next_features @ weights)))


def evaluate(dates, values):
    for horizon in [1, 7]:
        for origin in range(MIN_TRAIN - 1, len(values) - horizon):
            history = values[:origin + 1]
            yield {
                "horizonte": horizon,
                "origen": dates[origin],
                "fecha": dates[origin + horizon],
                "real": values[origin + horizon],
                "ultimo_dia": history[-1],
                "ingenuo_semanal": history[horizon - 8],
                "mediana_7d": np.median(history[-7:]),
                "ridge_log": ridge_prediction(history, dates, horizon, cap=False),
                "ridge_log_tope_p95": ridge_prediction(history, dates, horizon, cap=True),
            }


def main():
    dates, values = load_series()
    forecasts = list(evaluate(dates, values))
    with (HERE / "predicciones.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=forecasts[0].keys())
        writer.writeheader()
        writer.writerows(forecasts)

    results = []
    for horizon in [1, 7]:
        rows = [row for row in forecasts if row["horizonte"] == horizon]
        for subset in ["todos", "sin_objetivo_26_ago"]:
            selected = [row for row in rows if subset == "todos" or row["fecha"] != PEAK_DATE]
            for model in list(rows[0])[4:]:
                errors = np.array([row[model] - row["real"] for row in selected])
                results.append({
                    "horizonte": horizon, "muestra": subset, "modelo": model,
                    "n": len(errors), "mae": round(float(np.abs(errors).mean()), 2),
                    "rmse": round(float(np.sqrt(np.mean(errors ** 2))), 2),
                    "mediana_error_absoluto": round(float(np.median(np.abs(errors))), 2),
                })
    with (HERE / "metricas.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"Tramo activo: {dates[0]} a {dates[-1]}, {len(values)} días")
    for horizon in [1, 7]:
        days = [row["fecha"] for row in forecasts if row["horizonte"] == horizon]
        print(horizon, len(days), days[0], days[-1])


if __name__ == "__main__":
    main()
