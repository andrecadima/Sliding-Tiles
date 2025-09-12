"""
AgenteAsignador: agente CSP (Satisfacción de Restricciones) para colorear
los departamentos de Bolivia con {rojo, amarillo, verde} evitando que dos
departamentos adyacentes tengan el mismo color.
"""

from typing import Dict, List, Optional
from agente___.core.agente import Agente        # tu clase base
from agente___.algorithms.search import backtrack


class AgenteAsignador(Agente):
    def __init__(
        self,
        agente_id: int,
        nombre: str,
        variables: List[str],
        dominio: Dict[str, List[str]],
        vecinos: Dict[str, List[str]],
        entorno=None
    ):
        super().__init__(agente_id, nombre, entorno)
        self.variables = variables
        self.dominio = dominio
        self.vecinos = vecinos

    def _restriccion_coloreo(self, asignaciones: Dict[str, str], var: str, valor: str) -> bool:
        """Restricción: un departamento no puede compartir color con sus vecinos."""
        for v in self.vecinos.get(var, []):
            if v in asignaciones and asignaciones[v] == valor:
                return False
        return True

    def resolver(self) -> Optional[Dict[str, str]]:
        """Ejecuta el backtracking para obtener una asignación completa válida."""
        asignaciones: Dict[str, str] = {}
        return backtrack(
            asignaciones=asignaciones,
            variables=self.variables,
            dominio=self.dominio,
            restricciones=self._restriccion_coloreo
        )
