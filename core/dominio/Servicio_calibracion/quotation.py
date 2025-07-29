"""
Módulo para manejo de detalles de equipos médicos.
Contiene la clase EquipmentDetails con validaciones y propiedades.
"""

import re
from typing import Optional


class EquipmentDetails:
    """Maneja los detalles del equipo médico con validaciones robustas."""
    
    def __init__(self):
        self._name = None
        self._brand = None
        self._model = None
        self._description = None
        self._price = None
        self._serial_number = None

    @property
    def name(self) -> Optional[str]:
        """Nombre del equipo médico."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Establece el nombre del equipo con validación."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre debe ser una cadena de texto no vacía")
        self._name = name.strip()

    @property
    def brand(self) -> Optional[str]:
        """Marca del equipo médico."""
        return self._brand

    @brand.setter
    def brand(self, brand: str) -> None:
        """Establece la marca del equipo con validación."""
        if not isinstance(brand, str) or not brand.strip():
            raise ValueError("La marca debe ser una cadena de texto no vacía")
        self._brand = brand.strip()

    @property
    def model(self) -> Optional[str]:
        """Modelo del equipo médico."""
        return self._model

    @model.setter
    def model(self, model: str) -> None:
        """Establece el modelo del equipo con validación."""
        if not isinstance(model, str) or not model.strip():
            raise ValueError("El modelo debe ser una cadena de texto no vacía")
        self._model = model.strip()

    @property
    def description(self) -> Optional[str]:
        """Descripción del equipo médico."""
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        """Establece la descripción del equipo (puede ser vacía)."""
        self._description = description.strip() if description else None

    @property
    def price(self) -> Optional[float]:
        """Precio del equipo médico."""
        return self._price

    @price.setter
    def price(self, price: float) -> None:
        """Establece el precio del equipo con validación."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("El precio debe ser un número positivo")
        self._price = float(price)

    @property
    def serial_number(self) -> Optional[str]:
        """Número de serie del equipo médico."""
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number: str) -> None:
        """Establece el número de serie con validación de formato."""
        if not self._is_valid_serial_number(serial_number):
            raise ValueError("El número de serie solo debe contener letras, números y guiones")
        self._serial_number = serial_number

    @staticmethod
    def _is_valid_serial_number(serial_number: str) -> bool:
        """Valida el formato del número de serie."""
        pattern = r'^[A-Za-z0-9-]+$'
        return bool(re.match(pattern, serial_number))

    def __str__(self) -> str:
        """Representación en cadena del equipo."""
        return (f"EquipmentDetails(name='{self.name}', brand='{self.brand}', "
                f"model='{self.model}', price={self.price})")

    def __repr__(self) -> str:
        """Representación oficial del equipo."""
        return self.__str__()


class Quotation:
    """Clase vacía para evitar errores de importación."""
    pass