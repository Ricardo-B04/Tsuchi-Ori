"""Mapper de curvas de métricas de los días 0 a 6. Python 3.8+."""

import csv
import json
from collections import defaultdict
from itertools import combinations
from math import dist
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DAYS = range(7)


def load_videos(path, column="Reproducciones de video de 3 segundos"):
    daily = defaultdict(dict)
    published = {}
    with path.open(encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            video_id = row["Identificador del activo de video"]
            age = int(row["Días desde la publicación"])
            if age in daily[video_id]:
                raise ValueError(f"Edad duplicada para el video {video_id}")
            daily[video_id][age] = float(row[column]) if row[column] else None
            published[video_id] = row["Hora de publicación"]

    videos, excluded = [], []
    for video_id, counts in sorted(daily.items()):
        missing = [day for day in DAYS if counts.get(day) is None]
        if missing:
            excluded.append({"id": video_id, "motivo": f"Faltan valores en los días {missing}"})
            continue
        curve = [counts[day] for day in DAYS]
        total = sum(curve)
        if total <= 0:
            excluded.append({"id": video_id, "motivo": "Total semanal cero"})
            continue
        videos.append({
            "id": video_id, "publicacion": published[video_id],
            "total": total, "curva": curve, "forma": [value / total for value in curve],
            "lente": sum(curve[:2]) / total,
        })
    return videos, excluded


def components(indices, distances, radius):
    """Componentes conexas del grafo de vecinos a distancia <= radio."""
    remaining = set(indices)
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        members = [seed]
        for current in members:
            neighbors = sorted(i for i in remaining if distances[current][i] <= radius)
            remaining.difference_update(neighbors)
            members.extend(neighbors)
        yield sorted(members)


def mapper(videos, intervals, overlap, radius):
    lens = [video["lente"] for video in videos]
    low, high = min(lens), max(lens)
    width = (high - low) / (1 + (intervals - 1) * (1 - overlap))
    step = width * (1 - overlap)
    distances = [[dist(a["forma"], b["forma"]) for b in videos] for a in videos]
    nodes = []
    for interval in range(intervals):
        start = low + interval * step
        end = start + width
        indices = [i for i, value in enumerate(lens) if start - 1e-12 <= value <= end + 1e-12]
        for members in components(indices, distances, radius):
            nodes.append({"intervalo": interval + 1, "limites": [start, end], "videos": members})
    edges = []
    for a, b in combinations(range(len(nodes)), 2):
        common = sorted(set(nodes[a]["videos"]) & set(nodes[b]["videos"]))
        if common:
            edges.append({"a": a, "b": b, "videos": common})
    return {"intervalos": intervals, "solapamiento": overlap, "radio": radius,
            "nodos": nodes, "aristas": edges}


def main():
    configurations = [(5, .35, .12), (4, .35, .12), (6, .45, .12),
                      (5, .35, .10), (5, .35, .15), (5, .35, .08)]
    metrics = ["Reproducciones de video de 3 segundos", "Segundos reproducidos",
               "Reacciones, comentarios y veces que se compartió"]
    results = []
    for metric in metrics:
        videos, excluded = load_videos(ROOT / "datos" / "transformados" / "series_diarias_por_video.csv", metric)
        graphs = [mapper(videos, *config) for config in configurations] if videos else []
        weighted = [
            dict(video, lente=sum(day * share for day, share in enumerate(video["forma"])))
            for video in videos
        ]
        age_graphs = [mapper(weighted, *config) for config in configurations] if weighted else []
        results.append({"metrica": metric, "videos": videos, "excluidos": excluded, "grafos": graphs,
                        "por_edad": {"videos": weighted, "excluidos": excluded, "grafos": age_graphs}})
    data = {"metricas": results}
    template = (HERE / "mapper_videos_plantilla.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    (HERE / "mapper_videos.html").write_text(template.replace("__DATOS__", payload), encoding="utf-8")
    for result in results:
        print(result["metrica"], len(result["videos"]), "videos")
        for graph in result["grafos"]:
            print(graph["intervalos"], graph["solapamiento"], graph["radio"],
                  len(graph["nodos"]), len(graph["aristas"]))


if __name__ == "__main__":
    main()
