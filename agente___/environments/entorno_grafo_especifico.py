from __future__ import annotations
from typing import Dict, List

class EntornoGrafoEspecifico:
    """
    Árbol/grafo para juegos de suma cero:
      - adj[nodo] = lista de hijos
      - ut[nodo_hoja] = utilidad (perspectiva de MAX)
    Un nodo es terminal si no tiene hijos (o no aparece en adj).
    """
    def __init__(self, adj: Dict[str, List[str]], utilidad: Dict[str, float]):
        self.adj = adj
        self.ut = utilidad

    def sucesores(self, nodo: str) -> List[str]:
        return self.adj.get(nodo, [])

    def es_terminal(self, nodo: str) -> bool:
        return (nodo not in self.adj) or (len(self.adj.get(nodo, [])) == 0)

    def utilidad(self, nodo: str) -> float:
        return self.ut[nodo]
