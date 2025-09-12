# AGENTEBUSCADOR

Proyecto mínimo para un **Agente Buscador** con **BFS/DFS** sobre un grafo (Rumania).

## Estructura
SISTEMASINTELIGENTES/EC1/
│
├─ agente__/              # Carpeta con el paquete y lógica base
│   ├─ core/              # Clases base (Agente, Entorno)
│   ├─ agents/            # Agentes específicos
│   ├─ environments/      # Entornos específicos
│   ├─ algorithms/        # Algoritmos (bfs, dfs, a*, etc.)
│   └─ data/              # Instancias y grafos
│
├─ main_agente_buscador.py # Script principal para el agente buscador
├─ main_agente_otro.py     # (Opcional) Otros experimentos
├─ README.md
└─ requirements.txt

## Uso
```bash
python main.py
```
Mostrará el rendimiento del agente y el resultado de la búsqueda desde Arad a Pitesti.





##Dentro de algunas carpetas:
SISTEMASINTELIGENTES/
└─ EC1/
   ├─ AGENTES/
   │  ├─ main_agente_buscador.py
   │  └─ main_agente_buscador_ponderado.py
   ├─ agente___/                 # paquete (recuerda __init__.py)
   │  ├─ __init__.py
   │  ├─ busquedas.py            # dfs, bfs, (luego) uniform-cost / dijkstra
   │  ├─ heuristicas.py          # si luego metes A*
   │  ├─ grafo.py                # clase Grafo (no ponderado / ponderado)
   │  └─ costo.py                # tu get_costo y utilidades de pesos
   ├─ datos/
   │  └─ grafos_ejemplo.json
   └─ README.md