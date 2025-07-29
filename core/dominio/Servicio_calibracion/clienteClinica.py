# #!/usr/bin/python
# # -*- coding: utf-8 -*-

# class ClienteClinica:
#     def __init__(self):
#         self.customName = None
#         self.adress = None
#         self.email = None
#         self.priceCredit = None
#         self.priceCash = None

#     def register(self, ):
#         pass

#     def login(self, ):
#         pass

#     def updateProfile(self, ):
#         pass
# core/dominio/SERVICIO_CALIBRACION/clienteClinica.py

from django.db import models

class ClienteClinica(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    rfc = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    def updatePerfil(self):
        # lógica a implementar luego
        pass
