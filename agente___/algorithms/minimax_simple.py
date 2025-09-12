from __future__ import annotations
from typing import Dict, List, Optional, Tuple, Literal, Protocol

Jugador = Literal["MAX", "MIN"]

class EntornoMinimax(Protocol):
    def sucesores(self, nodo: str) -> List[str]: ...
    def es_terminal(self, nodo: str) -> bool: ...
    def utilidad(self, nodo: str) -> float: ...

def MiniMax(env: EntornoMinimax, estado: str, jugador: Jugador,
            etiquetas: Optional[Dict[str, float]] = None) -> float:
    if env.es_terminal(estado):
        v = env.utilidad(estado)
        if etiquetas is not None:
            etiquetas[estado] = v
        return v

    if jugador == "MAX":
        v = valorMax(env, estado, etiquetas)
    else:
        v = valorMin(env, estado, etiquetas)

    if etiquetas is not None:
        etiquetas[estado] = v
    return v

def valorMax(env: EntornoMinimax, estado: str,
             etiquetas: Optional[Dict[str, float]] = None) -> float:
    v = float("-inf")
    for hijo in env.sucesores(estado):
        v = max(v, MiniMax(env, hijo, "MIN", etiquetas))
    return v

def valorMin(env: EntornoMinimax, estado: str,
             etiquetas: Optional[Dict[str, float]] = None) -> float:
    v = float("+inf")
    for hijo in env.sucesores(estado):
        v = min(v, MiniMax(env, hijo, "MAX", etiquetas))
    return v
