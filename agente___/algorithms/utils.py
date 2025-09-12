"""
Utilidades para grafos ponderados.
"""

def get_costo_arista(u, v, grafo_ponderado):
    """Devuelve el costo (peso) de la arista u–v en un grafo ponderado no dirigido.
    Si no existe, devuelve None.
    grafo_ponderado: dict[str, dict[str, float]]
    """
    if u in grafo_ponderado and v in grafo_ponderado[u]:
        return grafo_ponderado[u][v]
    if v in grafo_ponderado and u in grafo_ponderado[v]:
        return grafo_ponderado[v][u]
    return None


def get_costo(camino, grafo_ponderado, *, raise_on_missing=True):
    """Suma el costo total de un camino dado un grafo ponderado.
    Devuelve (costo_total, desglose[(u,v,costo), ...]).
    """
    if not camino or len(camino) == 1:
        return 0.0, []

    total = 0.0
    desglose = []
    for u, v in zip(camino[:-1], camino[1:]):
        costo = get_costo_arista(u, v, grafo_ponderado)
        if costo is None:
            if raise_on_missing:
                raise ValueError(f"No existe peso para la arista {u} - {v}.")
            costo = 0.0
        total += float(costo)
        desglose.append((u, v, float(costo)))
    return total, desglose


#costo
def camino_menor_costo_ucs(grafo_ponderado, inicio, objetivo):
    """
    Uniform-Cost Search (cola de prioridad por costo acumulado).
    - Procesa primero el camino con MENOR costo.
    - Requiere costos positivos.
    Devuelve: (camino, costo_total, expandidos)
    """
    from heapq import heappush, heappop

    frontera = []                       
    heappush(frontera, (0.0, [inicio]))
    mejor_costo = {inicio: 0.0}         
    expandidos = 0

    while frontera:
        costo, camino = heappop(frontera)
        nodo = camino[-1]
        expandidos += 1

        if nodo == objetivo:
            return camino, costo, expandidos

        #vecinos con sus pesos
        for vecino, w in grafo_ponderado.get(nodo, {}).items():
            nuevo = costo + float(w)
            # relajación: solo empujar si encontramos una ruta más barata
            if vecino not in mejor_costo or nuevo < mejor_costo[vecino]:
                mejor_costo[vecino] = nuevo
                heappush(frontera, (nuevo, camino + [vecino]))

    return None, float("inf"), expandidos