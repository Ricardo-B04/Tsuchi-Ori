"""Takens, Vietoris–Rips sobre F2 y Wasserstein-1 de diagramas diarios."""

import csv
from datetime import date, timedelta
from itertools import combinations, pairwise
from math import dist, inf, log1p, sqrt
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
METRIC = "pagina_visualizaciones"


def rips_diagrams(cloud):
    """Reduce la matriz de fronteras de vértices, aristas y triángulos."""
    size = len(cloud)
    edges = {edge: dist(cloud[edge[0]], cloud[edge[1]])
             for edge in combinations(range(size), 2)}
    simplices = [(0.0, (i,)) for i in range(size)]
    simplices.extend((scale, edge) for edge, scale in edges.items())
    simplices.extend(
        (max(edges[edge] for edge in combinations(face, 2)), face)
        for face in combinations(range(size), 3)
    )
    simplices.sort(key=lambda item: (item[0], len(item[1]), item[1]))
    index = {face: i for i, (_, face) in enumerate(simplices)}
    reduced = {}
    births = set()
    diagrams = [[], []]
    for column, (death, face) in enumerate(simplices):
        boundary = sum(1 << index[subface]
                       for subface in combinations(face, len(face) - 1)) if len(face) > 1 else 0
        while boundary:
            pivot = boundary.bit_length() - 1
            if pivot not in reduced:
                reduced[pivot] = boundary
                birth, born_face = simplices[pivot]
                if death > birth:
                    diagrams[len(born_face) - 1].append((birth, death))
                break
            boundary ^= reduced[pivot]
        if not boundary and len(face) <= 2:
            births.add(column)
    for column in sorted(births - reduced.keys()):
        birth, face = simplices[column]
        diagrams[len(face) - 1].append((birth, inf))
    return diagrams


def assignment_cost(cost):
    """Algoritmo húngaro para asignación de costo mínimo en matriz cuadrada."""
    n = len(cost)
    row_potential = [0.0] * (n + 1)
    col_potential = [0.0] * (n + 1)
    matched_row = [0] * (n + 1)
    predecessor = [0] * (n + 1)
    for row in range(1, n + 1):
        matched_row[0] = row
        col = 0
        visited = [False] * (n + 1)
        slack = [inf] * (n + 1)
        while True:
            visited[col] = True
            current = matched_row[col]
            delta, next_col = inf, 0
            for candidate in range(1, n + 1):
                if visited[candidate]:
                    continue
                reduced = (cost[current - 1][candidate - 1]
                           - row_potential[current] - col_potential[candidate])
                if reduced < slack[candidate]:
                    slack[candidate] = reduced
                    predecessor[candidate] = col
                if slack[candidate] < delta:
                    delta, next_col = slack[candidate], candidate
            for candidate in range(n + 1):
                if visited[candidate]:
                    row_potential[matched_row[candidate]] += delta
                    col_potential[candidate] -= delta
                else:
                    slack[candidate] -= delta
            col = next_col
            if matched_row[col] == 0:
                break
        while col:
            previous = predecessor[col]
            matched_row[col] = matched_row[previous]
            col = previous
    return sum(cost[matched_row[col] - 1][col - 1] for col in range(1, n + 1))


def wasserstein(first, second):
    """Orden 1 con norma L-infinito y emparejamiento a la diagonal."""
    left = [point for point in first if point[1] != inf]
    right = [point for point in second if point[1] != inf]
    left_diag = [(death - birth) / 2 for birth, death in left]
    right_diag = [(death - birth) / 2 for birth, death in right]
    cost = [
        [max(abs(a - c), abs(b - d)) for c, d in right] + [delete] * len(left)
        for (a, b), delete in zip(left, left_diag)
    ]
    cost.extend([right_diag + [0.0] * len(left) for _ in right])
    return assignment_cost(cost)


def scan(dates, values, dimension=7, points=28, transform=log1p):
    transformed = [transform(value) for value in values]
    clouds = [tuple(transformed[i - lag] for lag in range(dimension))
              for i in range(dimension - 1, len(dates))]
    previous = None
    previous_mean = None
    support = dimension + points - 1
    for stop in range(points, len(clouds) + 1):
        end = stop + dimension - 2
        start = end - support + 1
        current = rips_diagrams(clouds[stop - points:stop])
        mean_log = mean(transformed[start:end + 1])
        yield dict(
            fecha=dates[end], inicio_ventana=dates[start], visualizaciones=values[end],
            wasserstein_h0=None if previous is None else wasserstein(previous[0], current[0]),
            wasserstein_h1=None if previous is None else wasserstein(previous[1], current[1]),
            h1_persistencia_maxima=max((death - birth for birth, death in current[1]), default=0),
            cambio_abs_media=None if previous is None else abs(mean_log - previous_mean),
        )
        previous, previous_mean = current, mean_log


def main():
    with (HERE.parent / "datos" / "transformados" / "series_diarias_pagina.csv").open(encoding="utf-8-sig", newline="") as f:
        source = list(csv.DictReader(f))
    dates = [date.fromisoformat(row["fecha"]) for row in source]
    values = [int(row[METRIC]) for row in source]
    if any(b - a != timedelta(days=1) for a, b in pairwise(dates)):
        raise ValueError("El archivo debe tener una fila por día, en orden y sin huecos.")
    configurations = [
        ("log1p", 7, 28, log1p),
        ("log1p", 7, 21, log1p),
        ("log1p", 7, 35, log1p),
        ("log1p", 5, 28, log1p),
        ("log1p", 9, 28, log1p),
        ("bruto", 7, 28, float),
        ("raiz", 7, 28, sqrt),
    ]
    all_rows = []
    for scale, dimension, points, transform in configurations:
        rows = list(scan(dates, values, dimension, points, transform))
        all_rows.extend(dict(escala=scale, dimension=dimension, puntos=points, **row)
                        for row in rows)
        for metric in ("wasserstein_h0", "wasserstein_h1", "cambio_abs_media"):
            ordered = sorted(rows[1:], key=lambda row: row[metric], reverse=True)
            peaks = [(str(row["fecha"]), round(row[metric], 4)) for row in ordered[:5]]
            print(scale, dimension, points, metric, peaks)
    with (HERE / "distancias.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)


if __name__ == "__main__":
    main()
