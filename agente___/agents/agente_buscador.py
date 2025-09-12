# -*- coding: utf-8 -*-
from ..core.agente import Agente

class AgenteBuscador(Agente):
    """
    objetivo: 'camino_mas_corto' -> BFS
              'cualquier_camino'  -> DFS (ejemplo)
    """
    def __init__(self, agente_id, nombre, objetivo='camino_mas_corto', entorno=None):
        super().__init__(agente_id, nombre, entorno)
        self.objetivo = objetivo
        self.ultima_percepcion = None

    def percibir(self, percepcion):
        self.ultima_percepcion = percepcion

    def decidir(self):
        if self.objetivo == 'camino_mas_corto':
            return {'algoritmo': 'bfs'}
        else:
            return {'algoritmo': 'dfs'}
