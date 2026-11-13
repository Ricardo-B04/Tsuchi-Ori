import csv, sys
from pathlib import Path
from math import log1p
from statistics import median, quantiles
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from enfoque_topologico.analisis import rips_diagrams, wasserstein
with open(ROOT / 'datos/transformados/series_diarias_pagina.csv',encoding='utf-8-sig') as f:
    rows=[r for r in csv.DictReader(f) if r['fecha']>='2026-04-08']
keys=list(rows[0])[1:6]
def calcular(sample):
    cols=[]
    for k in keys:
        vals=[log1p(int(r[k])) for r in sample]
        q1,_,q3=quantiles(vals,n=4)
        cols.append([(v-median(vals))/(q3-q1) for v in vals])
    resultados={}
    for nombre, columnas in [('Visualizaciones',cols[:1]),('Cinco métricas',cols),('Sin visualizaciones ni espectadores',cols[2:])]:
        vectors=[tuple(c[t-lag] for c in columnas for lag in range(7)) for t in range(6,len(sample))]
        previous=None
        cambios=[]
        for end in range(27,len(vectors)):
            dg=rips_diagrams(vectors[end-27:end+1])
            if previous is not None:
                cambios.append((sample[end+6]['fecha'],*(wasserstein(a,b) for a,b in zip(previous,dg))))
            previous=dg
        resultados[nombre]=cambios
    return resultados
if __name__ == "__main__":
    resultados = calcular(rows)
    with (ROOT / "Página/distancias_multivariadas.csv").open("w", encoding="utf-8", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["conjunto", "fecha", "wasserstein_h0", "wasserstein_h1"])
        for nombre, cambios in resultados.items():
            writer.writerows((nombre, *cambio) for cambio in cambios)
            ranking = sorted(cambios, key=lambda cambio: cambio[2], reverse=True)
            print(nombre, len(cambios), ranking[0])
            print("Puesto del 29 de agosto:", next(i for i, cambio in enumerate(ranking, 1)
                                                  if cambio[0] == "2026-08-29"))
