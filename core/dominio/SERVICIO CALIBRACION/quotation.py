#!/usr/bin/python
# -*- coding: utf-8 -*-

class Quotation:
    def __init__(self):
        self.numQuotation = None
        self.ClientId = None
        self.dateAdded = None
        self.description = None
        self.datecreate = None
        self.datedelete = None

    def addQuotation(self, ):
        pass

    def updateQuotation(self, ):
        pass

    def removeService(self, ):
        pass

    def changeState(self, ):
        pass

    def calculateprice(self, ):
        pass

    def calculateIGV(self, ):
        pass

    def quotationvencida(self, ):
        pass

    @staticmethod
    def get_by_numQuotation(numQuotation, quotations_list):
        """
        Busca una cotización por su número en una lista de cotizaciones.
        Retorna la cotización si la encuentra, de lo contrario None.
        """
        for quotation in quotations_list:
            if quotation.numQuotation == numQuotation:
                return quotation
        return None
