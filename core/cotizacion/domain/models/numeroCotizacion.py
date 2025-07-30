#!/usr/bin/python
# -*- coding: utf-8 -*-

class NumeroCotizacion:
    def __init__(self):
        self.prefijo = None
        self.numero = None
        self.year = None
        self.generador = GeneradorCotizacion()
        self.validador = ValidadorCotizacion()

    def generar(self):
        self.prefijo, self.numero, self.year = self.generador.generar()

    def valido(self):
        return self.validador.validar(self)

class GeneradorCotizacion:
    def generar(self):
        # 
        return None, None, None

class ValidadorCotizacion:
    def validar(self, cotizacion):
        return cotizacion.numero is not None and cotizacion.prefijo == "COT"
