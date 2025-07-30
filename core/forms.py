from django import forms
from django.contrib.auth.models import User
from .models import PerfilCliente

"""code josel"""
from .cotizacion.domain.models.equipment_details import MedicalEquipment, MedicalEquipmentValidator
from decimal import Decimal
""""""

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


"""equipment_details"""


class MedicalEquipmentForm(forms.ModelForm):
    class Meta:
        model = MedicalEquipment
        fields = ['name', 'brand', 'series', 'description', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del equipo médico'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca del equipo'
            }),
            'series': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de serie'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada (opcional)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Usar el validador personalizado
        validation_errors = MedicalEquipmentValidator.validate_equipment_data(cleaned_data)
        
        for field, errors in validation_errors.items():
            for error in errors:
                self.add_error(field, error)
        
        return cleaned_data

class MedicalEquipmentSearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre'
        })
    )
    brand = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por marca'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Precio mínimo'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Precio máximo'
        })
    )