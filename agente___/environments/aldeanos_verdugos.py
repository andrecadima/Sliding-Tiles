from typing import List, Tuple, Dict

# Estado: (A_izq, V_izq, bote_izq)  donde bote_izq: True si el bote está a la izquierda, False si a la derecha.
Estado = Tuple[int, int, bool]

# Acciones posibles (personas que suben al bote, capacidad=2): (A, V)
ACCIONES: List[Tuple[int, int]] = [
    (1, 0), (2, 0),  
    (0, 1), (0, 2),  
    (1, 1),          
]

def es_valido(estado: Estado, A_total=3, V_total=3) -> bool:
    a_izq, v_izq, _ = estado
    a_der = A_total - a_izq
    v_der = V_total - v_izq

    if not (0 <= a_izq <= A_total and 0 <= v_izq <= V_total):
        return False

    # Si hay aldeanos en una orilla, no pueden ser menos que los verdugos
    if a_izq > 0 and v_izq > a_izq:
        return False
    if a_der > 0 and v_der > a_der:
        return False
    return True

def aplicar(estado: Estado, accion: Tuple[int, int], A_total=3, V_total=3) -> Tuple[bool, Estado]:
    a_izq, v_izq, bote_izq = estado
    a_mover, v_mover = accion
    if a_mover + v_mover == 0 or a_mover + v_mover > 2:
        return False, estado

    if bote_izq:
        # mover de izquierda -> derecha
        a_n = a_izq - a_mover
        v_n = v_izq - v_mover
        nuevo = (a_n, v_n, False)
    else:
        # mover de derecha -> izquierda
        a_n = a_izq + a_mover
        v_n = v_izq + v_mover
        nuevo = (a_n, v_n, True)

    if a_n < 0 or v_n < 0 or a_n > A_total or v_n > V_total:
        return False, estado

    if not es_valido(nuevo, A_total, V_total):
        return False, estado

    return True, nuevo

def generar_grafo_estados(A_total=3, V_total=3) -> Dict[Estado, List[Estado]]:
    """
    Genera el grafo (dict) de todos los estados válidos y las transiciones posibles
    mediante las ACCIONES. Los nodos son tuplas Estado hashables (sirven directo con tu BFS).
    """
    # Todos los estados posibles (cartesiano) y nos quedamos con los válidos
    estados = []
    for a in range(A_total + 1):
        for v in range(V_total + 1):
            for bote in (True, False):
                e = (a, v, bote)
                if es_valido(e, A_total, V_total):
                    estados.append(e)

    grafo: Dict[Estado, List[Estado]] = {e: [] for e in estados}

    for e in estados:
        for acc in ACCIONES:
            ok, nxt = aplicar(e, acc, A_total, V_total)
            if ok:
                grafo[e].append(nxt)

    return grafo

def estado_inicial(A_total=3, V_total=3) -> Estado:
    return (A_total, V_total, True)  # todo a la izquierda, bote a la izquierda

def estado_objetivo() -> Estado:
    return (0, 0, False)  # todo a la derecha (el lado del bote ya no importa para “éxito”)