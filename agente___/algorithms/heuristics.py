"""
Heurísticas para grafos en Rumania.
- get_ubicacion(ciudad): devuelve (lat, lon)
- distancia_sld(ciudad_a, ciudad_b): "straight-line distance" (euclidiana simple en lat-lon)
- heuristica_sld_a_objetivo(objetivo): devuelve h(n) = dist(n, objetivo)
"""
from typing import Tuple, Callable
from math import sqrt
from agente___.data.ubicacionCiudadesRomania import ubicacionCiudadesRomania 

#norm de nombres
_ALIASES = {
    "Rimnicu": "Rimnicu Vilcea",
    "Timisoara": "Timișoara",
    "Timisoara*": "Timișoara",
    "Bucharest": "Bucarest",
    "Râmnicu Vâlcea": "Rimnicu Vilcea",
}

def _normaliza(ciudad: str) -> str:
    if ciudad in ubicacionCiudadesRomania:
        return ciudad
    return _ALIASES.get(ciudad, ciudad)

def get_ubicacion(ciudad: str) -> Tuple[float, float]:
    c = _normaliza(ciudad)
    lat, lon = ubicacionCiudadesRomania[c]
    return float(lat), float(lon)

def distancia_sld(a: str, b: str) -> float:
    lat1, lon1 = get_ubicacion(a)
    lat2, lon2 = get_ubicacion(b)
    return sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def heuristica_sld_a_objetivo(objetivo: str) -> Callable[[str], float]:  #sld manhatannnnnn
    objetivo_norm = _normaliza(objetivo)
    def h(nodo: str) -> float:
        return distancia_sld(nodo, objetivo_norm)
    return h







# --- Heurísticas para Sliding Tile (n×n) ------------------------------------
from typing import Tuple, Callable, Dict, List

EstadoST = Tuple[int, ...]  # p.ej. (1,2,3,4,5,6,7,8,0) para 3x3

def _n_from_state(s: EstadoST) -> int:
    import math
    n = int(math.isqrt(len(s)))
    assert n * n == len(s), "El estado no es un cuadrado perfecto"
    return n

def _rc(idx: int, n: int) -> Tuple[int, int]:
    return divmod(idx, n)  # (fila, col)

def _goal_pos_map(goal: EstadoST) -> Dict[int, Tuple[int,int]]:
    n = _n_from_state(goal)
    return {v: _rc(i, n) for i, v in enumerate(goal)}

# --- Hamming: piezas mal colocadas (no cuenta el 0) ---
def h_hamming_factory(goal: EstadoST) -> Callable[[EstadoST], float]:
    def h(s: EstadoST) -> float:
        return sum(1 for i,(a,b) in enumerate(zip(s, goal)) if a != 0 and a != b)
    return h

# --- Manhattan total: suma |Δfila|+|Δcol| para cada pieza (≠0) ---
def h_manhattan_factory(goal: EstadoST) -> Callable[[EstadoST], float]:
    goal_pos = _goal_pos_map(goal)
    def h(s: EstadoST) -> float:
        n = _n_from_state(s)
        total = 0
        for i, v in enumerate(s):
            if v == 0: 
                continue
            r, c = _rc(i, n)
            rg, cg = goal_pos[v]
            total += abs(r - rg) + abs(c - cg)
        return float(total)
    return h

# --- Manhattan + Conflicto lineal (fila y columna), suma +2 por conflicto ---
def h_manhattan_linear_conflict_factory(goal: EstadoST) -> Callable[[EstadoST], float]:
    goal_pos = _goal_pos_map(goal)
    def _manhattan(s: EstadoST) -> int:
        n = _n_from_state(s)
        m = 0
        for i, v in enumerate(s):
            if v == 0: 
                continue
            r, c = _rc(i, n)
            rg, cg = goal_pos[v]
            m += abs(r - rg) + abs(c - cg)
        return m

    def _row_conflicts(s: EstadoST) -> int:
        n = _n_from_state(s)
        confl = 0
        for r in range(n):
            row_tiles = []
            for c in range(n):
                v = s[r*n + c]
                if v != 0 and goal_pos[v][0] == r:
                    row_tiles.append((c, goal_pos[v][1]))
            for i in range(len(row_tiles)):
                for j in range(i+1, len(row_tiles)):
                    cg_i = row_tiles[i][1]
                    cg_j = row_tiles[j][1]
                    if cg_i > cg_j:
                        confl += 1
        return confl

    def _col_conflicts(s: EstadoST) -> int:
        n = _n_from_state(s)
        confl = 0
        for c in range(n):
            col_tiles = []
            for r in range(n):
                v = s[r*n + c]
                if v != 0 and goal_pos[v][1] == c:
                    col_tiles.append((r, goal_pos[v][0]))
            for i in range(len(col_tiles)):
                for j in range(i+1, len(col_tiles)):
                    rg_i = col_tiles[i][1]
                    rg_j = col_tiles[j][1]
                    if rg_i > rg_j:
                        confl += 1
        return confl

    def h(s: EstadoST) -> float:
        m = _manhattan(s)
        lc = _row_conflicts(s) + _col_conflicts(s)
        return float(m + 2 * lc)
    return h

def h_gaschnig_factory(goal: EstadoST) -> Callable[[EstadoST], float]:
    goal_index = {v: i for i, v in enumerate(goal)}
    def h(s: EstadoST) -> float:
        if s == goal:
            return 0.0
        arr = list(s)
        swaps = 0
        blank_idx = arr.index(0)
        while tuple(arr) != goal:
            goal_blank_idx = goal_index[0]
            if blank_idx != goal_blank_idx:
                v_needed = goal[blank_idx]
                v_idx = arr.index(v_needed)
                arr[blank_idx], arr[v_idx] = arr[v_idx], arr[blank_idx]
                blank_idx = v_idx
            else:
                for i, v in enumerate(arr):
                    if v != 0 and goal_index[v] != i:
                        arr[blank_idx], arr[i] = arr[i], arr[blank_idx]
                        blank_idx = i
                        break
            swaps += 1
        return float(swaps)
    return h
