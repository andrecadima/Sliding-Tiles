from typing import Dict, Tuple, Iterable
from agente___.algorithms.heuristics import EstadoST, _n_from_state, _rc

class SlidingLazyGraph(dict):
    """
    "Grafo" perezoso para sliding tile nxn compatible con a_estrella(grafo,...).
    Implementa .get(estado, {}) devolviendo {sucesor: 1.0, ...} sin precomputar todo.
    """
    def __getitem__(self, key):
        # no usamos __getitem__ para evitar KeyError; usamos get() abajo.
        raise KeyError

    def get(self, s: EstadoST, default=None) -> Dict[EstadoST, float]:
        n = _n_from_state(s)
        idx0 = s.index(0)
        r0, c0 = _rc(idx0, n)
        sucesores: Dict[EstadoST, float] = {}

        def swap(idx_a, idx_b):
            lst = list(s)
            lst[idx_a], lst[idx_b] = lst[idx_b], lst[idx_a]
            return tuple(lst)

        # arriba
        if r0 > 0:
            sucesores[swap(idx0, idx0 - n)] = 1.0
        # abajo
        if r0 < n - 1:
            sucesores[swap(idx0, idx0 + n)] = 1.0
        # izquierda
        if c0 > 0:
            sucesores[swap(idx0, idx0 - 1)] = 1.0
        # derecha
        if c0 < n - 1:
            sucesores[swap(idx0, idx0 + 1)] = 1.0

        return sucesores if sucesores else (default or {})