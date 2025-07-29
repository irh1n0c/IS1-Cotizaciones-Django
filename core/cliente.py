from django.db import models
from django.contrib.auth.models import User

class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ruc = models.CharField(max_length=11)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - Cliente"