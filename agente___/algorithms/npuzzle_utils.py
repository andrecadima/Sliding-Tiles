# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Tuple, List
import random

EstadoST = Tuple[int, ...]

def _n_from_state(s: EstadoST) -> int:
    n2 = len(s)
    n = int(n2 ** 0.5)
    if n * n != n2:
        raise ValueError("Estado no es cuadrado")
    return n

def _rc(idx: int, n: int) -> tuple[int, int]:
    return divmod(idx, n)

def _index(r: int, c: int, n: int) -> int:
    return r * n + c

def _goal_canonical(n: int) -> EstadoST:
    return tuple(list(range(1, n*n)) + [0])

def contar_inversiones(arr: List[int]) -> int:
    inv = 0
    vals = [x for x in arr if x != 0]
    for i in range(len(vals)):
        ai = vals[i]
        for j in range(i+1, len(vals)):
            if ai > vals[j]:
                inv += 1
    return inv

def fila_desde_abajo(idx_blank: int, n: int) -> int:
    r, _ = _rc(idx_blank, n)
    return n - r

def es_soluble(estado: EstadoST, goal: EstadoST | None = None) -> bool:
    n = _n_from_state(estado)
    if goal is None:
        goal = _goal_canonical(n)
    inv_s = contar_inversiones(list(estado))
    if n % 2 == 1:
        return inv_s % 2 == 0
    inv_g = 0
    rb_s = fila_desde_abajo(estado.index(0), n)
    rb_g = fila_desde_abajo(goal.index(0), n)
    return (inv_s + rb_s) % 2 == (inv_g + rb_g) % 2

def generar_estado(n: int, pasos_barajado: int = 100, seed: int | None = None) -> EstadoST:
    if seed is not None:
        random.seed(seed)
    goal = _goal_canonical(n)
    s = list(goal)
    idx0 = s.index(0)
    prev = None
    for _ in range(max(1, pasos_barajado)):
        r, c = _rc(idx0, n)
        moves = []
        if r > 0:     moves.append(idx0 - n)
        if r < n-1:   moves.append(idx0 + n)
        if c > 0:     moves.append(idx0 - 1)
        if c < n-1:   moves.append(idx0 + 1)
        if prev in moves and len(moves) > 1:
            moves.remove(prev)
        nxt = random.choice(moves)
        s[idx0], s[nxt] = s[nxt], s[idx0]
        prev, idx0 = idx0, nxt
    estado = tuple(s)
    assert es_soluble(estado, goal), "Generador produjo estado no soluble"
    return estado
