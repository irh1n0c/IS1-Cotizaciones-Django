from datetime import datetime
from typing import Optional


class Quotation:
    def __init__(self, client_id: int, description: str, quotation_number: str):
        self.num_quotation = quotation_number  # Código único generado
        self.client_id = client_id
        self.description = description
        self.date_added = datetime.now()
        self.date_created = datetime.now()
        self.date_deleted = None
        self.marca = None
        self.numero_serie = None
        self.equipos_medicos = []

    def cantidad_equipos(self) -> int:
        return len(self.equipos_medicos)

    def asignar_marca_equipo(self, marca: str):
        if not isinstance(marca, str):
            raise ValueError("La marca debe ser una cadena de texto.")
        self.marca = marca

    def guardar_numero_serie(self, numero_serie: str):
        import re
        patron = r'^[A-Za-z0-9-]+$'
        if not re.match(patron, numero_serie):
            raise ValueError("El número de serie solo debe contener letras, números y guiones.")
        self.numero_serie = numero_serie

    def marcar_como_eliminada(self):
        self.date_deleted = datetime.now()

    @staticmethod
    def generar_numero_quotation(tipo: str, secuencia: int) -> str:
        if tipo not in ['C', 'H']:
            raise ValueError("El tipo debe ser 'C' (Comercial) o 'H' (Habitacional)")
        year = datetime.now().year
        return f"{tipo}{year}{secuencia:03d}"
