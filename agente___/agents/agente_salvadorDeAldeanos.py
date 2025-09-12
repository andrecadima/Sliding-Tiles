from typing import List, Tuple, Optional
from agente___.environments.aldeanos_verdugos import (
    generar_grafo_estados, estado_inicial, estado_objetivo, Estado
)
from agente___.algorithms.search import bfs_iterativo  # <-- reutilizamos BFS

class AgenteSalvadorDeAldeanos:
    def __init__(self, A_total=3, V_total=3):
        self.A_total = A_total
        self.V_total = V_total
        self.grafo = generar_grafo_estados(A_total, V_total)
        self.inicio = estado_inicial(A_total, V_total)
        self.meta = estado_objetivo()

    def resolver(self) -> Tuple[Optional[List[Estado]], int]:
        """
        Devuelve (camino_de_estados, nodos_expandidos)
        camino_de_estados es una lista de Estados desde inicio hasta meta (mínimo en cruces).
        """
        camino, expandidos = bfs_iterativo(self.grafo, self.inicio, self.meta)
        return camino, expandidos

    @staticmethod
    def render(e: Estado, A_total=3, V_total=3) -> str:
        a_izq, v_izq, bote_izq = e
        a_der = A_total - a_izq
        v_der = V_total - v_izq
        boteL = "Bote izq       " if bote_izq else ""
        boteR = "       Bote der" if not bote_izq else ""
        return f"[Izq] A:{a_izq} V:{v_izq} {boteL}  ||  {boteR} [Der] A:{a_der} V:{v_der}"