# -*- coding: utf-8 -*-
from ..core.entorno import Entorno
from ..algorithms.search import bfs_iterativo, dfs_iterativo

class EntornoGrafo(Entorno):
    def __init__(self, nombre, grafo, inicio, objetivo):
        super().__init__(nombre)
        self.grafo = grafo
        self.inicio = inicio
        self.objetivo = objetivo
        self._terminado = False
        self.resultado = None  # {'camino': [...], 'expansiones': int, 'algoritmo': str}

    def estado_actual(self, agente):
        # Percepción minimalista: inicio, objetivo y nodos disponibles
        return {
            'inicio': self.inicio,
            'objetivo': self.objetivo,
            'nodos': tuple(self.grafo.keys())
        }

    def ejecutar_accion(self, agente, accion) -> float:
        # accion: {'algoritmo': 'bfs' | 'dfs'}
        algoritmo = accion.get('algoritmo', 'bfs').lower()
        if algoritmo == 'bfs':
            camino, exp = bfs_iterativo(self.grafo, self.inicio, self.objetivo)
        else:
            camino, exp = dfs_iterativo(self.grafo, self.inicio, self.objetivo)

        self.resultado = {'camino': camino, 'expansiones': exp, 'algoritmo': algoritmo}
        self._terminado = True
        # Recompensa: penaliza expansiones (menos es mejor), bonifica si encontró camino
        if camino is None:
            return -float(exp) - 10.0
        return 100.0 - float(exp)  # base 100 menos costo de búsqueda

    def acciones_admisibles(self, agente):
        return [{'algoritmo': 'bfs'}, {'algoritmo': 'dfs'}]

    def es_terminal(self) -> bool:
        return self._terminado
