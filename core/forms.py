from django import forms
from django.contrib.auth.models import User
from .models import PerfilCliente

class RegistroClienteForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

    class Meta:
        model = PerfilCliente
        fields = ['ruc', 'direccion', 'telefono']