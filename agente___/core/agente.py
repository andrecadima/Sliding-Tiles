# -*- coding: utf-8 -*-
class Agente:
    def __init__(self, agente_id, nombre, entorno=None):
        self.agente_id = agente_id
        self.nombre = nombre
        self.entorno = entorno
        self.sensores = []
        self.actuadores = []
        self.rendimiento = 0.0

    def percibir(self, percepcion):
        raise NotImplementedError

    def decidir(self):
        raise NotImplementedError

    def actuar(self, accion):
        pass

    def recompensar(self, valor):
        self.rendimiento += float(valor)
