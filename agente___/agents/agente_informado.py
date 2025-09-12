# -*- coding: utf-8 -*-
import time
from typing import Dict, Tuple, Optional, List, Callable
from agente___.algorithms.informed import greedy_codicioso, a_estrella
from agente___.algorithms.utils import camino_menor_costo_ucs  # UCS existente

Estado = str
GrafoPonderado = Dict[Estado, Dict[Estado, float]]
Path = List[Estado]

class AgenteInformado:
    """
    Algoritmos disponibles:
      - "greedy":  Búsqueda Codiciosa (prioriza por h(n) = costo_h)
      - "a*":      A estrella (prioriza por f(n) = g(n) + h(n))
      - "ucs":     Costo Uniforme (tu implementación en utils.py)
    """
    def __init__(self, grafo_ponderado: GrafoPonderado, inicio: Estado, objetivo: Estado,
                 algoritmo: str = "a*", heuristica: Optional[Callable[[Estado], float]] = None):
        self.grafo = grafo_ponderado
        self.inicio = inicio
        self.objetivo = objetivo
        self.algoritmo = algoritmo.lower()
        self.h = heuristica or (lambda _: 0.0)

    def resolver(self) -> Tuple[Optional[Path], float, int, float]:
        t0 = time.perf_counter()

        if self.algoritmo == "greedy":
            camino, costo, expandidos = greedy_codicioso(self.grafo, self.inicio, self.objetivo, self.h)
        elif self.algoritmo == "ucs":
            camino, costo, expandidos = camino_menor_costo_ucs(self.grafo, self.inicio, self.objetivo)
        else:
            camino, costo, expandidos = a_estrella(self.grafo, self.inicio, self.objetivo, self.h)

        dur_ms = (time.perf_counter() - t0) * 1000.0
        return camino, costo, expandidos, dur_ms
