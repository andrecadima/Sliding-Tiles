# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, time, csv, os
from typing import Tuple, List

from agente___.algorithms.informed import a_estrella, greedy_codicioso
from agente___.algorithms.heuristics import (
    h_hamming_factory, h_manhattan_factory, h_manhattan_linear_conflict_factory
)
from agente___.environments.sliding_graph import SlidingLazyGraph
from agente___.algorithms.npuzzle_utils import generar_estado, es_soluble

EstadoST = Tuple[int, ...]

class GraphAdapter:
    def __init__(self, base):
        self.base = base
    def get(self, s, default=None):
        return self.base.get(s, default)
    def __getitem__(self, s):
        # devuelve siempre el diccionario de sucesores
        return self.base.get(s, {})
    def __contains__(self, s):
        # asume que cualquier estado válido puede consultarse
        return True

def goal_canon(n: int) -> EstadoST:
    return tuple(list(range(1, n*n)) + [0])

def get_heuristic_factory(name: str):
    name = name.lower()
    if name in ("hamming", "h"):
        return h_hamming_factory
    if name in ("manhattan", "m"):
        return h_manhattan_factory
    if name in ("linear_conflict", "mlc", "manhattan_lc", "lc"):
        return h_manhattan_linear_conflict_factory
    raise ValueError(f"Heurística no soportada en benchmark: {name}")

def run_once(algo: str, hname: str, grafo, inicio: EstadoST, goal: EstadoST):
    h_factory = get_heuristic_factory(hname)
    h = h_factory(goal)
    t0 = time.perf_counter()
    if algo == "a*":
        camino, costo, expandidos = a_estrella(grafo, inicio, goal, h)
    else:
        camino, costo, expandidos = greedy_codicioso(grafo, inicio, goal, h)
    t1 = time.perf_counter()
    ok = camino is not None and len(camino) > 0
    pasos = (len(camino)-1) if ok else None
    return {
        "ok": ok,
        "pasos": pasos,
        "costo": costo if ok else None,
        "expandidos": expandidos,
        "ms": (t1 - t0) * 1000.0,
    }

def main():
    parser = argparse.ArgumentParser(description="Benchmark N-puzzle (1000 casos aleatorios)")
    parser.add_argument("--n", type=int, default=3, help="Tamaño del tablero (n x n)")
    parser.add_argument("--count", type=int, default=1000, help="Número de casos aleatorios")
    parser.add_argument("--shuffle", type=int, default=100, help="Pasos de barajado desde el goal para generar cada estado")
    parser.add_argument("--out", type=str, default="results.csv", help="Ruta al CSV con resultados detallados")
    args = parser.parse_args()

    n = args.n
    goal = goal_canon(n)
    grafo = GraphAdapter(SlidingLazyGraph())
    algos = ["a*", "greedy"]
    heuristics = ["hamming", "manhattan", "linear_conflict"]

    if os.path.dirname(args.out):
        os.makedirs(os.path.dirname(args.out), exist_ok=True)

    rows: List[dict] = []
    for i in range(args.count):
        inicio = generar_estado(n, pasos_barajado=args.shuffle, seed=None)
        assert es_soluble(inicio, goal), "Estado generado no soluble"

        for algo in algos:
            for hname in heuristics:
                r = run_once(algo, hname, grafo, inicio, goal)
                rows.append({
                    "case": i,
                    "algo": algo,
                    "heuristic": hname,
                    **r
                })
        if (i+1) % 50 == 0:
            print(f"[{i+1}/{args.count}] casos completados...")

    # Guardar CSV
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Resumen por (algo, heurística)
    print("\n=== Resumen ===")
    for algo in algos:
        for hname in heuristics:
            subset = [r for r in rows if r["algo"] == algo and r["heuristic"] == hname]
            ok_rate = sum(1 for r in subset if r["ok"]) / len(subset)
            pasos = [r["pasos"] for r in subset if r["ok"] and r["pasos"] is not None]
            tiempos = [r["ms"] for r in subset if r["ok"]]
            expanded = [r["expandidos"] for r in subset if r["ok"]]
            pasos_avg = (sum(pasos) / len(pasos)) if pasos else 0.0
            ms_avg = (sum(tiempos) / len(tiempos)) if tiempos else 0.0
            exp_avg = (sum(expanded) / len(expanded)) if expanded else 0.0
            print(f"{algo} / {hname}: ok={ok_rate*100:.1f}%  pasos_avg={pasos_avg:.2f}  ms_avg={ms_avg:.1f}  exp_avg={exp_avg:.1f}")

if __name__ == "__main__":
    main()
