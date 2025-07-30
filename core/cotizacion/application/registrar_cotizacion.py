from core.cotizacion.domain.models.quotation import Quotation

class RegistrarCotizacion:
    def __init__(self, repo):
        self.repo = repo

    def ejecutar(self, datos):
        numero = Quotation.generar_numero_quotation(datos["tipo"], datos["secuencia"])
        cotizacion = Quotation(
            client_id=datos["cliente_id"],
            description=datos["descripcion"],
            quotation_number=numero
        )
        self.repo.guardar(cotizacion)
        return cotizacion
