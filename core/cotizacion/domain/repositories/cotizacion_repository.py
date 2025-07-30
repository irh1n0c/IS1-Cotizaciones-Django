from abc import ABC, abstractmethod
from core.cotizacion.domain.models.equipment_details import MedicalEquipment


class CotizacionRepository(ABC):
    @abstractmethod
    def guardar(self, cotizacion: MedicalEquipment):
        """Guarda una cotización en el sistema"""
        pass
