from decimal import Decimal
from typing import List, Optional, Any, Dict
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator


class MedicalEquipment(models.Model):
    """Modelo para equipos médicos en detalles de cotización."""
    
    # Constantes
    MAX_NAME_LENGTH = 200
    MAX_BRAND_LENGTH = 100
    MAX_SERIES_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 500
    MIN_PRICE = Decimal('0.01')
    MAX_PRICE = Decimal('999999999.99')
    
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Nombre del Equipo Médico",
        help_text="Nombre descriptivo del equipo médico",
        validators=[MaxLengthValidator(MAX_NAME_LENGTH)]
    )
    
    brand = models.CharField(
        max_length=MAX_BRAND_LENGTH,
        verbose_name="Marca",
        help_text="Marca del equipo médico",
        validators=[MaxLengthValidator(MAX_BRAND_LENGTH)]
    )
    
    series = models.CharField(
        max_length=MAX_SERIES_LENGTH,
        verbose_name="Serie",
        help_text="Número de serie del equipo",
        validators=[MaxLengthValidator(MAX_SERIES_LENGTH)]
    )
    
    description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH,
        verbose_name="Descripción",
        help_text="Descripción detallada del equipo médico",
        blank=True,
        validators=[MaxLengthValidator(MAX_DESCRIPTION_LENGTH)]
    )
    
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Precio",
        help_text="Precio del equipo médico",
        validators=[MinValueValidator(MIN_PRICE)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Equipo Médico"
        verbose_name_plural = "Equipos Médicos"
        ordering = ['name', 'brand']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['brand']),
            models.Index(fields=['series']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} - {self.brand} ({self.series})"
    
    def clean(self) -> None:
        """Validaciones personalizadas del modelo."""
        super().clean()
        self._validate_name()
        self._validate_brand()
        self._validate_series()
        self._validate_price()
    
    def _validate_name(self) -> None:
        """Valida el nombre del equipo."""
        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'El nombre del equipo es obligatorio'})
        
        if self.name != self.name.strip():
            self.name = self.name.strip()
    
    def _validate_brand(self) -> None:
        """Valida la marca del equipo."""
        if not self.brand or not self.brand.strip():
            raise ValidationError({'brand': 'La marca del equipo es obligatoria'})
        
        if self.brand != self.brand.strip():
            self.brand = self.brand.strip()
    
    def _validate_series(self) -> None:
        """Valida la serie del equipo."""
        if not self.series or not self.series.strip():
            raise ValidationError({'series': 'La serie del equipo es obligatoria'})
        
        if self.series != self.series.strip():
            self.series = self.series.strip()
    
    def _validate_price(self) -> None:
        """Valida el precio del equipo."""
        if self.price is None:
            raise ValidationError({'price': 'El precio es obligatorio'})
        
        if self.price < self.MIN_PRICE:
            raise ValidationError({
                'price': f'El precio debe ser mayor a {self.MIN_PRICE}'
            })
        
        if self.price > self.MAX_PRICE:
            raise ValidationError({
                'price': f'El precio no puede exceder {self.MAX_PRICE}'
            })
    
    def save(self, *args, **kwargs) -> None:
        """Override del método save para ejecutar validaciones."""
        self.full_clean()
        super().save(*args, **kwargs)


class MedicalEquipmentManager:
    """Manager para operaciones CRUD de equipos médicos."""
    
    @staticmethod
    def create_equipment(
        name: str,
        brand: str,
        series: str,
        price: Decimal,
        description: str = ""
    ) -> MedicalEquipment:
        """
        Crea un nuevo equipo médico.
        
        Args:
            name: Nombre del equipo médico
            brand: Marca del equipo
            series: Número de serie
            price: Precio del equipo
            description: Descripción opcional
            
        Returns:
            MedicalEquipment: Instancia del equipo creado
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        equipment = MedicalEquipment(
            name=name,
            brand=brand,
            series=series,
            price=price,
            description=description
        )
        equipment.save()
        return equipment
    
    @staticmethod
    def find_by_name(name: str) -> List[MedicalEquipment]:
        """
        Busca equipos por nombre (búsqueda parcial insensible a mayúsculas).
        
        Args:
            name: Nombre a buscar
            
        Returns:
            List[MedicalEquipment]: Lista de equipos encontrados
        """
        if not name or not isinstance(name, str):
            return []
        
        return list(MedicalEquipment.objects.filter(
            name__icontains=name.strip()
        ).order_by('name', 'brand'))
    
    @staticmethod
    def find_by_brand(brand: str) -> List[MedicalEquipment]:
        """
        Busca equipos por marca.
        
        Args:
            brand: Marca a buscar
            
        Returns:
            List[MedicalEquipment]: Lista de equipos de la marca
        """
        if not brand or not isinstance(brand, str):
            return []
        
        return list(MedicalEquipment.objects.filter(
            brand__iexact=brand.strip()
        ).order_by('name'))
    
    @staticmethod
    def find_by_series(series: str) -> Optional[MedicalEquipment]:
        """
        Busca un equipo por número de serie (único).
        
        Args:
            series: Número de serie a buscar
            
        Returns:
            Optional[MedicalEquipment]: Equipo encontrado o None
        """
        if not series or not isinstance(series, str):
            return None
        
        try:
            return MedicalEquipment.objects.get(series__iexact=series.strip())
        except MedicalEquipment.DoesNotExist:
            return None
    
    @staticmethod
    def find_by_price_range(
        min_price: Decimal,
        max_price: Decimal
    ) -> List[MedicalEquipment]:
        """
        Busca equipos en un rango de precios.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            List[MedicalEquipment]: Lista de equipos en el rango
        """
        if min_price is None or max_price is None:
            return []
        
        if min_price > max_price:
            min_price, max_price = max_price, min_price
        
        return list(MedicalEquipment.objects.filter(
            price__gte=min_price,
            price__lte=max_price
        ).order_by('price'))
    
    @staticmethod
    def get_all_equipment() -> List[MedicalEquipment]:
        """
        Obtiene todos los equipos médicos.
        
        Returns:
            List[MedicalEquipment]: Lista de todos los equipos
        """
        return list(MedicalEquipment.objects.all().order_by('name', 'brand'))
    
    @staticmethod
    def update_equipment(
        equipment_id: int,
        **kwargs
    ) -> Optional[MedicalEquipment]:
        """
        Actualiza un equipo médico.
        
        Args:
            equipment_id: ID del equipo a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Optional[MedicalEquipment]: Equipo actualizado o None si no existe
        """
        try:
            equipment = MedicalEquipment.objects.get(id=equipment_id)
            
            # Actualizar solo los campos proporcionados
            for field, value in kwargs.items():
                if hasattr(equipment, field):
                    setattr(equipment, field, value)
            
            equipment.save()
            return equipment
        except MedicalEquipment.DoesNotExist:
            return None
    
    @staticmethod
    def delete_equipment(equipment_id: int) -> bool:
        """
        Elimina un equipo médico.
        
        Args:
            equipment_id: ID del equipo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        try:
            equipment = MedicalEquipment.objects.get(id=equipment_id)
            equipment.delete()
            return True
        except MedicalEquipment.DoesNotExist:
            return False


class MedicalEquipmentValidator:
    """Validador para datos de equipos médicos."""
    
    @staticmethod
    def validate_equipment_data(data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Valida los datos de un equipo médico.
        
        Args:
            data: Diccionario con los datos del equipo
            
        Returns:
            Dict[str, List[str]]: Diccionario con errores por campo
        """
        errors = {}
        
        # Validar nombre
        name_errors = MedicalEquipmentValidator._validate_name(data.get('name'))
        if name_errors:
            errors['name'] = name_errors
        
        # Validar marca
        brand_errors = MedicalEquipmentValidator._validate_brand(data.get('brand'))
        if brand_errors:
            errors['brand'] = brand_errors
        
        # Validar serie
        series_errors = MedicalEquipmentValidator._validate_series(data.get('series'))
        if series_errors:
            errors['series'] = series_errors
        
        # Validar precio
        price_errors = MedicalEquipmentValidator._validate_price(data.get('price'))
        if price_errors:
            errors['price'] = price_errors
        
        # Validar descripción
        description_errors = MedicalEquipmentValidator._validate_description(
            data.get('description', '')
        )
        if description_errors:
            errors['description'] = description_errors
        
        return errors
    
    @staticmethod
    def _validate_name(name: Any) -> List[str]:
        """Valida el nombre del equipo."""
        errors = []
        
        if not name:
            errors.append("El nombre es obligatorio")
            return errors
        
        if not isinstance(name, str):
            errors.append("El nombre debe ser una cadena de texto")
            return errors
        
        if len(name.strip()) == 0:
            errors.append("El nombre no puede estar vacío")
        
        if len(name) > MedicalEquipment.MAX_NAME_LENGTH:
            errors.append(
                f"El nombre no puede exceder {MedicalEquipment.MAX_NAME_LENGTH} caracteres"
            )
        
        return errors
    
    @staticmethod
    def _validate_brand(brand: Any) -> List[str]:
        """Valida la marca del equipo."""
        errors = []
        
        if not brand:
            errors.append("La marca es obligatoria")
            return errors
        
        if not isinstance(brand, str):
            errors.append("La marca debe ser una cadena de texto")
            return errors
        
        if len(brand.strip()) == 0:
            errors.append("La marca no puede estar vacía")
        
        if len(brand) > MedicalEquipment.MAX_BRAND_LENGTH:
            errors.append(
                f"La marca no puede exceder {MedicalEquipment.MAX_BRAND_LENGTH} caracteres"
            )
        
        return errors
    
    @staticmethod
    def _validate_series(series: Any) -> List[str]:
        """Valida la serie del equipo."""
        errors = []
        
        if not series:
            errors.append("La serie es obligatoria")
            return errors
        
        if not isinstance(series, str):
            errors.append("La serie debe ser una cadena de texto")
            return errors
        
        if len(series.strip()) == 0:
            errors.append("La serie no puede estar vacía")
        
        if len(series) > MedicalEquipment.MAX_SERIES_LENGTH:
            errors.append(
                f"La serie no puede exceder {MedicalEquipment.MAX_SERIES_LENGTH} caracteres"
            )
        
        return errors
    
    @staticmethod
    def _validate_price(price: Any) -> List[str]:
        """Valida el precio del equipo."""
        errors = []
        
        if price is None:
            errors.append("El precio es obligatorio")
            return errors
        
        try:
            price_decimal = Decimal(str(price))
        except (ValueError, TypeError):
            errors.append("El precio debe ser un número válido")
            return errors
        
        if price_decimal < MedicalEquipment.MIN_PRICE:
            errors.append(f"El precio debe ser mayor a {MedicalEquipment.MIN_PRICE}")
        
        if price_decimal > MedicalEquipment.MAX_PRICE:
            errors.append(f"El precio no puede exceder {MedicalEquipment.MAX_PRICE}")
        
        return errors
    
    @staticmethod
    def _validate_description(description: Any) -> List[str]:
        """Valida la descripción del equipo."""
        errors = []
        
        if description is None:
            return errors
        
        if not isinstance(description, str):
            errors.append("La descripción debe ser una cadena de texto")
            return errors
        
        if len(description) > MedicalEquipment.MAX_DESCRIPTION_LENGTH:
            errors.append(
                f"La descripción no puede exceder {MedicalEquipment.MAX_DESCRIPTION_LENGTH} caracteres"
            )
        
        return errors