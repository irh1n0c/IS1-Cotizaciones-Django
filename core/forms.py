from django import forms
from django.contrib.auth.models import User
from .models import PerfilCliente


class RegistroClienteForm(forms.ModelForm):
    """
    Formulario de registro de cliente extendiendo el modelo PerfilCliente.
    Incluye campos adicionales para autenticación.
    """

    # Campos extra para crear el User (no están en PerfilCliente)
    username = forms.CharField(label="Nombre de usuario")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

    class Meta:
        model = PerfilCliente
        fields = ['ruc_dni', 'direccion', 'telefono']

    def clean_email(self):
        """
        Valida que el email no esté ya registrado en el sistema.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso.")
        return email
    




