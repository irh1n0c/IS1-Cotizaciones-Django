# test_medical_equipment.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from .cotizacion.domain.models.equipment_details import (
    MedicalEquipment,
    MedicalEquipmentManager,
    MedicalEquipmentValidator
)



class MedicalEquipmentModelTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'name': 'Electrocardiograma',
            'brand': 'Philips',
            'series': 'ECG-2024-001',
            'price': Decimal('15000.00'),
            'description': 'Electrocardiograma de 12 derivaciones'
        }
    
    def test_create_valid_equipment(self):
        """Test creación de equipo válido."""
        equipment = MedicalEquipment.objects.create(**self.valid_data)
        self.assertEqual(equipment.name, self.valid_data['name'])
        self.assertEqual(equipment.brand, self.valid_data['brand'])
        self.assertEqual(equipment.series, self.valid_data['series'])
        self.assertEqual(equipment.price, self.valid_data['price'])
    
    def test_equipment_str_representation(self):
        """Test representación string del equipo."""
        equipment = MedicalEquipment.objects.create(**self.valid_data)
        expected = f"{self.valid_data['name']} - {self.valid_data['brand']} ({self.valid_data['series']})"
        self.assertEqual(str(equipment), expected)
    
    def test_invalid_price(self):
        """Test validación de precio inválido."""
        self.valid_data['price'] = Decimal('0.00')
        equipment = MedicalEquipment(**self.valid_data)
        
        with self.assertRaises(ValidationError):
            equipment.full_clean()
    
    def test_empty_name(self):
        """Test validación de nombre vacío."""
        self.valid_data['name'] = ''
        equipment = MedicalEquipment(**self.valid_data)
        
        with self.assertRaises(ValidationError):
            equipment.full_clean()

class MedicalEquipmentManagerTest(TestCase):
    def setUp(self):
        self.equipment1 = MedicalEquipmentManager.create_equipment(
            name='Electrocardiograma',
            brand='Philips',
            series='ECG-001',
            price=Decimal('15000.00')
        )
        self.equipment2 = MedicalEquipmentManager.create_equipment(
            name='Desfibrilador',
            brand='Medtronic',
            series='DEF-001',
            price=Decimal('25000.00')
        )
    
    def test_find_by_name(self):
        """Test búsqueda por nombre."""
        results = MedicalEquipmentManager.find_by_name('Electro')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Electrocardiograma')
    
    def test_find_by_brand(self):
        """Test búsqueda por marca."""
        results = MedicalEquipmentManager.find_by_brand('Philips')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].brand, 'Philips')
    
    def test_find_by_series(self):
        """Test búsqueda por serie."""
        result = MedicalEquipmentManager.find_by_series('ECG-001')
        self.assertIsNotNone(result)
        self.assertEqual(result.series, 'ECG-001')
    
    def test_find_by_price_range(self):
        """Test búsqueda por rango de precios."""
        results = MedicalEquipmentManager.find_by_price_range(
            Decimal('10000.00'), 
            Decimal('20000.00')
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Electrocardiograma')

class MedicalEquipmentValidatorTest(TestCase):
    def test_valid_data(self):
        """Test validación de datos válidos."""
        data = {
            'name': 'Electrocardiograma',
            'brand': 'Philips',
            'series': 'ECG-001',
            'price': Decimal('15000.00'),
            'description': 'Descripción válida'
        }
        errors = MedicalEquipmentValidator.validate_equipment_data(data)
        self.assertEqual(len(errors), 0)
    
    def test_invalid_name(self):
        """Test validación de nombre inválido."""
        data = {
            'name': '',
            'brand': 'Philips',
            'series': 'ECG-001',
            'price': Decimal('15000.00')
        }
        errors = MedicalEquipmentValidator.validate_equipment_data(data)
        self.assertIn('name', errors)
    
    def test_invalid_price(self):
        """Test validación de precio inválido."""
        data = {
            'name': 'Electrocardiograma',
            'brand': 'Philips',
            'series': 'ECG-001',
            'price': 'invalid_price'
        }
        errors = MedicalEquipmentValidator.validate_equipment_data(data)
        self.assertIn('price', errors)