# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Entorno(ABC):
    def __init__(self, nombre):
        self.nombre = nombre
        self.agentes = []

    def registrar_agente(self, agente):
        self.agentes.append(agente)
        agente.entorno = self

    @abstractmethod
    def estado_actual(self, agente):
        pass

    @abstractmethod
    def ejecutar_accion(self, agente, accion) -> float:
        pass

    def acciones_admisibles(self, agente):
        return []

    @abstractmethod
    def es_terminal(self) -> bool:
        pass

    def paso(self):
        for ag in self.agentes:
            percepcion = self.estado_actual(ag)
            ag.percibir(percepcion)
            accion = ag.decidir()
            ag.actuar(accion)
            recompensa = self.ejecutar_accion(ag, accion)
            ag.recompensar(recompensa)
