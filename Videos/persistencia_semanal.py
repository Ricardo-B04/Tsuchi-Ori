"""Persistencia H0 por superniveles sobre una trayectoria diaria."""


def picos_secundarios(curva):
    """Devuelve (día del pico, día de fusión, persistencia) para barras finitas positivas."""
    padres = {}

    def raiz(dia):
        while padres[dia] != dia:
            dia = padres[dia]
        return dia

    barras = []
    for dia in sorted(range(len(curva)), key=lambda d: (-curva[d], d)):
        padres[dia] = dia
        for vecino in (dia - 1, dia + 1):
            if vecino not in padres:
                continue
            a, b = sorted((raiz(dia), raiz(vecino)), key=lambda d: (-curva[d], d))
            if a != b:
                persistencia = curva[b] - curva[dia]
                if persistencia > 0:
                    barras.append((b, dia, persistencia))
                padres[b] = a
    return sorted(barras, key=lambda barra: -barra[2])


def con_lente_h0(videos):
    """Usa la mayor persistencia finita en proporción del total semanal."""
    resultado = []
    for video in videos:
        barras = picos_secundarios(video["curva"])
        lente = barras[0][2] / video["total"] if barras else 0.0
        resultado.append(dict(video, lente=lente, barras_h0=barras))
    return resultado
