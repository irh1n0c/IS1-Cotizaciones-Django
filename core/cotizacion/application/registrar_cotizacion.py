from core.cotizacion.domain.models.equipment_details import MedicalEquipment

class RegistrarCotizacion:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, datos):
        numero = MedicalEquipment.generar_numero_quotation(datos["tipo"], datos["secuencia"])
        cotizacion = MedicalEquipment(
            client_id=datos["cliente_id"],
            description=datos["descripcion"],
            quotation_number=numero
        )
        self.repo.guardar(cotizacion)
        return cotizacion
