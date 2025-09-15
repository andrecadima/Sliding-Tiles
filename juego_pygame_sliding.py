# juego_pygame_sliding.py
# -*- coding: utf-8 -*-
import sys, os, time, random
import pygame

# === IMPORTS DE TU PROYECTO (ajusta si tu estructura difiere) ===
from agente___.environments.sliding_graph import SlidingLazyGraph
from agente___.algorithms.informed import a_estrella, greedy_codicioso
from agente___.algorithms.heuristics import (
    h_manhattan_linear_conflict_factory, h_manhattan_factory
)
from agente___.algorithms.npuzzle_utils import generar_estado, es_soluble

# ============ CONFIGURACIÓN ============
N = 5                                  # tamaño del tablero NxN
TILE_SIZE = 100                        # px por casilla
GAP = 4                                # separación entre casillas
MARGIN = 20                            # margen exterior
FONT_SIZE = 20
FPS = 60
ANIM_DELAY_MS = 120                   # ms entre pasos de animación

# Colores
BG = (245, 246, 248)
TILE = (235, 238, 242)
TILE_EMPTY = (210, 215, 224)
TEXT = (40, 44, 52)
ACCENT = (66, 133, 244)

# ============ UTILIDADES ESTADO ============
def goal_canon(n):
    return tuple(list(range(1, n*n)) + [0])

def to_grid(state, n):
    """convierte tupla plana -> matriz n x n (lista de listas)"""
    return [list(state[i*n:(i+1)*n]) for i in range(n)]

def to_tuple(grid):
    """convierte matriz -> tupla plana"""
    return tuple(x for row in grid for x in row)

def find_pos(state, val, n):
    idx = state.index(val)
    return divmod(idx, n)  # (r, c)

def are_adjacent(p0, p1):
    return abs(p0[0]-p1[0]) + abs(p0[1]-p1[1]) == 1

def swap_positions(state, p0, p1, n):
    """intercambia dos posiciones (r,c) en estado tupla"""
    lst = list(state)
    i0 = p0[0]*n + p0[1]
    i1 = p1[0]*n + p1[1]
    lst[i0], lst[i1] = lst[i1], lst[i0]
    return tuple(lst)

# ============ DIBUJO ============
def board_rect(n):
    size = n*TILE_SIZE + (n-1)*GAP
    x = MARGIN
    y = MARGIN
    return pygame.Rect(x, y, size, size)

def tile_rect(n, r, c):
    bx, by, _, _ = board_rect(n)
    x = bx + c*(TILE_SIZE + GAP)
    y = by + r*(TILE_SIZE + GAP)
    return pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

def draw_board(screen, font, state, n, info=None):
    screen.fill(BG)
    rect_b = board_rect(n)
    # baldosa
    for r in range(n):
        for c in range(n):
            v = state[r*n+c]
            rect = tile_rect(n, r, c)
            if v == 0:
                pygame.draw.rect(screen, TILE_EMPTY, rect, border_radius=12)
            else:
                pygame.draw.rect(screen, TILE, rect, border_radius=12)
                label = font.render(str(v), True, TEXT)
                screen.blit(label, label.get_rect(center=rect.center))
    # overlay info
    if info:
        overlay_lines = [
            f"R: resolver (A* + Linear Conflict)",
            f"N: sugerir 1 paso (Greedy + LC)",
            f"",
            f"Estado objetivo: {goal_canon(n)}",
            f"Algoritmo: {info.get('algo','-')}  Heurística: {info.get('heur','-')}",
            f"Pasos: {info.get('pasos','-')}  Tiempo(ms): {info.get('ms','-')}  Expandidos: {info.get('exp','-')}",
        ]
        x0 = rect_b.right + 20
        y0 = MARGIN
        for line in overlay_lines:
            txt = font.render(line, True, TEXT)
            screen.blit(txt, (x0, y0))
            y0 += FONT_SIZE + 6

# ============ LÓGICA DEL AGENTE ============
class PuzzleAgent:
    def __init__(self, n):
        self.n = n
        self.grafo = SlidingLazyGraph()
        self.goal = goal_canon(n)
        # Heurísticas precompiladas
        self.hA = h_manhattan_linear_conflict_factory(self.goal)   # para A*
        self.hG = h_manhattan_linear_conflict_factory(self.goal)   # para Greedy
        self.plan = []            # lista de estados (camino a reproducir)
        self.anim_on = False
        self._last_step_ts = 0    # timestamp para ritmo de animación

    def solve_astar(self, start):
        t0 = time.perf_counter()
        path, cost, expanded = a_estrella(self.grafo, start, self.goal, self.hA)
        t1 = time.perf_counter()
        if path and len(path) > 0 and path[0] == start:
            path = path[1:]  # remover estado actual
        self.plan = path or []
        self.anim_on = False
        return {
            "algo": "A*",
            "heur": "Linear Conflict",
            "pasos": (len(path) if path else 0),
            "ms": round((t1 - t0) * 1000.0, 1),
            "exp": expanded
        }

    def suggest_greedy(self, start):
        path, _, _ = greedy_codicioso(self.grafo, start, self.goal, self.hG)
        if path and len(path) >= 2:
            return path[1]  # siguiente estado
        return None

    def animate_step(self, current_state):
        """devuelve (nuevo_estado, finished:bool) según el reloj"""
        now = time.time() * 1000.0
        if self.anim_on and self.plan and (now - self._last_step_ts >= ANIM_DELAY_MS):
            self._last_step_ts = now
            nxt = self.plan.pop(0)
            finished = (len(self.plan) == 0)
            if finished: self.anim_on = False
            return nxt, finished
        return current_state, False

# ============ ENTRADA DEL USUARIO ============
def pos_from_mouse(n, mouse_pos):
    mx, my = mouse_pos
    rect_b = board_rect(n)
    if not rect_b.collidepoint(mx, my):
        return None
    rx = mx - rect_b.left
    ry = my - rect_b.top
    c = rx // (TILE_SIZE + GAP)
    r = ry // (TILE_SIZE + GAP)
    # validar dentro de casilla
    tr = tile_rect(n, int(r), int(c))
    if tr.collidepoint(mx, my):
        return (int(r), int(c))
    return None

def try_move(state, n, clicked_rc):
    """si click es adyacente al 0, intercambia y devuelve nuevo estado"""
    r0, c0 = find_pos(state, 0, n)
    if clicked_rc and are_adjacent((r0, c0), clicked_rc):
        return swap_positions(state, (r0, c0), clicked_rc, n)
    return state

# ============ LOOP PRINCIPAL ============
def main():
    pygame.init()
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    # ventana: tablero + panel info
    board_w = N*TILE_SIZE + (N-1)*GAP
    panel_w = 420
    width = MARGIN*2 + board_w + 20 + panel_w
    height = MARGIN*2 + board_w
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("N-Puzzle (pygame)")

    clock = pygame.time.Clock()

    # estado inicial
    state = generar_estado(N, pasos_barajado=60)
    goal = goal_canon(N)
    assert es_soluble(state, goal)

    agent = PuzzleAgent(N)
    info = {"algo": "-", "heur": "-", "pasos": "-", "ms": "-", "exp": "-"}

    running = True
    while running:
        dt = clock.tick(FPS)

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                rc = pos_from_mouse(N, event.pos)
                new_state = try_move(state, N, rc)
                if new_state != state:
                    state = new_state
                    agent.plan = []   # invalidar plan previo si el usuario mueve
                    agent.anim_on = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Resolver con A* + LC
                    info = agent.solve_astar(state)
                elif event.key == pygame.K_a:
                    # Animar plan (si existe)
                    if agent.plan:
                        agent.anim_on = True
                        agent._last_step_ts = 0
                elif event.key == pygame.K_n:
                    # Sugerir un paso con Greedy + LC
                    nxt = agent.suggest_greedy(state)
                    if nxt:
                        state = nxt
                        agent.plan = []
                        agent.anim_on = False
                elif event.key == pygame.K_s:
                    # Barajar un estado soluble
                    state = generar_estado(N, pasos_barajado=random.randint(40, 120))
                    agent.plan = []
                    agent.anim_on = False
                    info = {"algo": "-", "heur": "-", "pasos": "-", "ms": "-", "exp": "-"}

        # animación (si está activa)
        state, _finished = agent.animate_step(state)

        # dibujar
        draw_board(screen, font, state, N, info=info)
        pygame.display.flip()

        # objetivo alcanzado → detener animación
        if state == goal:
            agent.plan = []
            agent.anim_on = False

    pygame.quit()

if __name__ == "__main__":
    main()