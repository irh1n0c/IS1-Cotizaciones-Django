class Quotation:
    def __init__(self):
        self.numQuotation = None
        self.ClientId = None
        self.dateAdded = None
        self.description = None
        self.datecreate = None
        self.datedelete = None

    def add_fecha(self, ):
        from datetime import datetime
        self.dateAdded = datetime.now()

    @staticmethod
    def numero_quotation(num_quotation, quotations_list):
        
        for quotation in quotations_list:
            if quotation.num_quotation == num_quotation:
                return quotation
        return None
    
    def cantidad(self):
        if hasattr(self, 'equipos_medicos') and self.equipos_medicos is not None:
            return len(self.equipos_medicos)
        return 0
    def marca_equipo(self, marca):
        if not isinstance(marca, str):
            raise ValueError("La marca debe ser una cadena de texto.")
        self.marca = marca

    def guardar_numero_serie(self, numero_serie):

        import re
        patron = r'^[A-Za-z0-9-]+$'
        if re.match(patron, numero_serie):
            self.numero_serie = numero_serie
        else:
            raise ValueError("El número de serie solo debe contener letras, números y guiones.")
    

    def addQuotation(self, ):
        pass

    def updateQuotation(self, ):
        pass

    def removeService(self, ):
        pass



    

    def quotationvencida(self, ):
        pass



