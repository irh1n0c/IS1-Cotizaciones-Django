from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from core.cotizacion.application.registrar_cotizacion import RegistrarCotizacion
from core.cotizacion.infrastructure.repositories.cotizacion_repository_impl import CotizacionRepositoryImpl


@csrf_exempt
def crear_cotizacion_view(request):
    if request.method == "POST":
        try:
            datos_json = json.loads(request.body)

            datos = {
                "tipo": datos_json["tipo"],
                "secuencia": int(datos_json["secuencia"]),
                "cliente_id": int(datos_json["cliente_id"]),
                "descripcion": datos_json["descripcion"],
            }

            use_case = RegistrarCotizacion(CotizacionRepositoryImpl())
            cotizacion = use_case.ejecutar(datos)

            return JsonResponse({
                "numero": cotizacion.num_quotation,
                "cliente_id": cotizacion.client_id,
                "descripcion": cotizacion.description
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


from django.shortcuts import render

def crear_cotizacion_form_view(request):
    if request.method == "POST":
        try:
            datos = {
                "tipo": request.POST["tipo"],
                "secuencia": int(request.POST["secuencia"]),
                "cliente_id": int(request.POST["cliente_id"]),
                "descripcion": request.POST["descripcion"]
            }

            use_case = RegistrarCotizacion(CotizacionRepositoryImpl())
            cotizacion = use_case.ejecutar(datos)

            return render(request, "cotizacion/crear_cotizacion.html", {
                "numero": cotizacion.num_quotation
            })

        except Exception as e:
            return render(request, "cotizacion/crear_cotizacion.html", {
                "error": str(e)
            })

    return render(request, "cotizacion/crear_cotizacion.html")
