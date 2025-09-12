from agente___.algorithms.informed import a_estrella, greedy_codicioso
from agente___.algorithms.heuristics import (
    h_hamming_factory, h_manhattan_factory,
    h_manhattan_linear_conflict_factory, h_gaschnig_factory
)
from agente___.environments.sliding_graph import SlidingLazyGraph
import argparse

# Estado 3x3 (8-puzzle): 0 = vacío
inicio = (6,8,3,
          1,2,4,
          7,0,5)

goal =  (1,2,3,
         4,5,6,
         7,8,0)

def _select_heuristic(name: str, goal):
    name = (name or "").lower()
    if name in ("hamming", "h"):
        return h_hamming_factory(goal)
    if name in ("manhattan", "m"):
        return h_manhattan_factory(goal)
    if name in ("linear_conflict", "mlc", "manhattan_lc", "lc"):
        return h_manhattan_linear_conflict_factory(goal)
    if name in ("gaschnig", "g"):
        return h_gaschnig_factory(goal)
    raise ValueError(f"Heurística no reconocida: {name}")


grafo = SlidingLazyGraph()

# --- Elige la heurística:
# h = h_hamming_factory(goal)
# h = h_manhattan_factory(goal)
# h = h_manhattan_linear_conflict_factory(goal)
h = h_gaschnig_factory(goal)

def n_from_state(s):
    import math
    n = int(math.isqrt(len(s)))
    assert n*n == len(s)
    return n

def render_grid(s):
    n = n_from_state(s)
    for r in range(n):
        fila = s[r*n:(r+1)*n]
        print(" ".join(f"{x:2d}" if x != 0 else "  " for x in fila))
    print()

def paso(prev, curr):
    """Devuelve (dir, ficha_movida). Dir describe el movimiento del '0' (hueco)."""
    n = n_from_state(prev)
    i0_prev = prev.index(0)
    i0_curr = curr.index(0)
    dr = (i0_curr // n) - (i0_prev // n)
    dc = (i0_curr % n) - (i0_prev % n)
    if dr == -1 and dc == 0:  # hueco subió
        d = "↑"
    elif dr == 1 and dc == 0: # hueco bajó
        d = "↓"
    elif dr == 0 and dc == -1: # hueco fue a la izq
        d = "←"
    elif dr == 0 and dc == 1:  # hueco fue a la der
        d = "→"
    else:
        d = "?"
    # La ficha que se movió al hueco previo:
    ficha = curr[i0_prev]
    return d, ficha

def mostrar_trayectoria(camino, h_func=None, mostrar_costes=True):
    if not camino:
        print("No hay solución.")
        return
    n = n_from_state(camino[0])
    g = 0.0
    print(f"Puzzle {n}x{n}\n")
    print("Paso 0 (inicio):")
    render_grid(camino[0])
    if mostrar_costes and h_func:
        f = g + h_func(camino[0])
        print(f"g={g:.0f}  h={h_func(camino[0]):.0f}  f={f:.0f}\n")

    for i in range(1, len(camino)):
        prev, curr = camino[i-1], camino[i]
        d, ficha = paso(prev, curr)
        g += 1.0
        print(f"Paso {i}: mover ficha {ficha} ({d})")
        render_grid(curr)
        if mostrar_costes and h_func:
            f = g + h_func(curr)
            print(f"g={g:.0f}  h={h_func(curr):.0f}  f={f:.0f}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agente informando para Sliding Tiles (Greedy / A*)")
    parser.add_argument("--algo", choices=["a*", "greedy"], default="a*", help="Algoritmo de búsqueda")
    parser.add_argument("--h", choices=["hamming", "manhattan", "linear_conflict", "gaschnig"], default="manhattan", help="Heurística admisible")
    parser.add_argument("--show-costs", action="store_true", default=True, help="Mostrar g, h, f durante la trayectoria")
    args = parser.parse_args()

    # Seleccionar heurística y grafo
    h = _select_heuristic(args.h, goal)
    # grafo ya declarado arriba
    print(f"[CLI] algoritmo={args.algo}  heurística={args.h}")

    if args.algo == "greedy":
        camino, costo, expandidos = greedy_codicioso(grafo, inicio, goal, h)
    else:
        camino, costo, expandidos = a_estrella(grafo, inicio, goal, h)

    if camino:
        print(f"Pasos: {len(camino)-1} | Costo: {costo:.0f} | Expandidos: {expandidos}")
        mostrar_trayectoria(camino, h_func=h, mostrar_costes=args.show_costs)
    else:
        print("Sin solución.")
