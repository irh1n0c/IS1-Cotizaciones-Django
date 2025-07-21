
from datetime import datetime
from typing import List, Optional, Any


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


    def get_quotation_type() -> str:

        quotation_type = input("Ingrese el tipo de cotización (C/H): ").upper().strip()
        
        if quotation_type not in ['C', 'H']:
            raise ValueError("El tipo de cotización debe ser 'C' para Comercial o 'H' para Habitacional")
        
        return quotation_type

    def get_current_year() -> int:

        return datetime.now().year

    def get_sequence_number() -> int:

        try:
            sequence_input = input("Ingrese el número secuencial (001-999): ")
            sequence_number = int(sequence_input)
            
            if not 1 <= sequence_number <= 999:
                raise ValueError("El número secuencial debe estar entre 1 y 999")
            
            return sequence_number
            
        except ValueError as error:
            if "invalid literal" in str(error):
                raise ValueError("Debe ingresar un número válido") from error
            raise

    def generate_quotation_number() -> str:

        quotation_type = get_quotation_type()
        year = get_current_year()
        sequence_number = get_sequence_number()
        
        return f"{quotation_type}{year}{sequence_number:03d}"

    def find_quotation_by_number(quotation_number: str, quotations_list: List[Any]) -> Optional[Any]:

        for quotation in quotations_list:
            if hasattr(quotation, 'num_quotation') and quotation.num_quotation == quotation_number:
                return quotation
        return None
    
    # Ejemplo de uso
    if __name__ == "__main__":
        try:
            # Generar nuevo número de cotización
            nuevo_numero = generate_quotation_number()
            print(f"Número de cotización generado: {nuevo_numero}")
            
        except ValueError as error:
            print(f"Error: {error}")
    
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



