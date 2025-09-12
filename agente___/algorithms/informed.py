# -*- coding: utf-8 -*-
"""
Algoritmos informados (Búsqueda Informada):
- Búsqueda Codiciosa (Greedy Best-First): ordena por h(n) = costo_h
- A* (A estrella): ordena por f(n) = g(n) + h(n) = costo_g + costo_h

Formato esperado del grafo ponderado: dict[str, dict[str, float]]
Ambos retornan: (camino, costo_total, expandidos)
"""

from heapq import heappush, heappop
from typing import Dict, List, Tuple, Callable, Optional, Set

Estado = str
GrafoPonderado = Dict[Estado, Dict[Estado, float]]
Path = List[Estado]


class GraphAdapter:
    def __init__(self, base):
        self.base = base
    def get(self, s, default=None):
        return self.base.get(s, default)
    def __getitem__(self, s):
        # devuelve siempre el diccionario de sucesores
        return self.base.get(s, {})
    def __contains__(self, s):
        # asume que cualquier estado válido puede consultarse
        return True

def _reconstruir_camino(padre: Dict[Estado, Estado], objetivo: Estado) -> Path:
    camino: Path = [objetivo]
    cur = objetivo
    while cur in padre:
        cur = padre[cur]
        camino.append(cur)
    camino.reverse()
    return camino


def greedy_codicioso(
    grafo: GrafoPonderado,
    inicio: Estado,
    objetivo: Estado,
    h: Callable[[Estado], float],  # costo_h estimado a meta
) -> Tuple[Optional[Path], float, int]:
    """
    Estrategia: Expandir primero el estado que se piensa más cerca de la meta (h(n) mínimo).
    No garantiza optimalidad en costo. (profundidad mal guiada si h es mala)
    """
    from agente___.algorithms.utils import get_costo  # para calcular costo real del camino

    grafo = GraphAdapter(grafo)  # adaptar para get_costo

    # frontera prioriza por h(n) = costo_h
    frontera: List[Tuple[float, Estado]] = []
    heappush(frontera, (h(inicio), inicio))

    visitado: Set[Estado] = set()
    padre: Dict[Estado, Estado] = {}
    expandidos = 0

    while frontera:
        costo_h, s = heappop(frontera)     # desencolar el más prometedor por h
        if s in visitado:
            continue
        visitado.add(s)
        expandidos += 1

        if s == objetivo:
            camino = _reconstruir_camino(padre, s)
            costo_total, _ = get_costo(camino, grafo, raise_on_missing=True)
            return camino, costo_total, expandidos

        # expandir sucesores
        for v, w in grafo.get(s, {}).items():
            if v in visitado:
                continue
            if v not in padre:             # no sobrescribir padre si ya tiene
                padre[v] = s
            heappush(frontera, (h(v), v))  # ordenar solo por h(n)

    return None, float("inf"), expandidos


def a_estrella(
    grafo: GrafoPonderado,
    inicio: Estado,
    objetivo: Estado,
    h: Callable[[Estado], float],  # costo_h estimado a meta (ideal: admisible/consistente)
) -> Tuple[Optional[Path], float, int]:
    """
    A*: combina Costo Uniforme (g) y Codicioso (h):
         f(n) = g(n) + h(n)
    - Óptimo si h es admisible (no sobreestima) y consistente.
    - ¡Finaliza al DESENCOLAR el objetivo de la frontera!
    """
    # frontera con tuplas (costo_f, estado), donde costo_f = costo_g + costo_h
    frontera: List[Tuple[float, Estado]] = []
    costo_g: Dict[Estado, float] = {inicio: 0.0}         # g(n): costo acumulado desde inicio
    padre: Dict[Estado, Estado] = {}
    cerrado: Set[Estado] = set()                         # ya optimizados/definitivos
    expandidos = 0

    heappush(frontera, (h(inicio), inicio))  # f(inicio)=0+h(inicio)

    while frontera:
        costo_f, s = heappop(frontera)       # SI: terminar al DESENCOLAR meta
        if s in cerrado:
            continue
        cerrado.add(s)
        expandidos += 1

        if s == objetivo:
            return _reconstruir_camino(padre, s), costo_g[s], expandidos

        # expandir sucesores
        for v, w in grafo.get(s, {}).items():
            if v in cerrado:
                continue
            nuevo_g = costo_g[s] + float(w)  # candidato g(nuevo)
            # relajación estándar
            if v not in costo_g or nuevo_g < costo_g[v]:
                costo_g[v] = nuevo_g
                padre[v] = s
                costo_h = h(v)
                costo_f = nuevo_g + costo_h  # f(n) = g(n) + h(n)
                heappush(frontera, (costo_f, v))

    return None, float("inf"), expandidos
