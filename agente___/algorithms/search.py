# -*- coding: utf-8 -*-
from collections import deque

def dfs_iterativo(grafo, inicio, objetivo):
    frontera = [[inicio]]            # cada elemento es un camino
    expandidos = 0
    while frontera:
        camino = frontera.pop()      # LIFO
        nodo = camino[-1]
        expandidos += 1
        if nodo == objetivo:
            return camino, expandidos
        for hijo in grafo.get(nodo, []):
            if hijo not in camino:   # evita ciclos básicos
                frontera.append(camino + [hijo])
    return None, expandidos

def bfs_iterativo(grafo, inicio, objetivo):
    frontera = deque([[inicio]])     # cada elemento es un camino
    expandidos = 0
    visitado = set([inicio])
    while frontera:
        camino = frontera.popleft()  # FIFO
        nodo = camino[-1]
        expandidos += 1
        if nodo == objetivo:
            return camino, expandidos
        for hijo in grafo.get(nodo, []):
            if hijo not in visitado:
                visitado.add(hijo)
                frontera.append(camino + [hijo])
    return None, expandidos

def backtrack(asignaciones, variables, dominio, restricciones):
    if len(asignaciones) == len(variables):
        return asignaciones
    for var in variables:
        if var not in asignaciones:
            break
    else:
        return asignaciones
    for valor in dominio[var]:
        if restricciones(asignaciones, var, valor):
            asignaciones[var] = valor
            resultado = backtrack(asignaciones, variables, dominio, restricciones)
            if resultado is not None:
                return resultado
            del asignaciones[var]
    return None


