# admin.py
from django.contrib import admin
from core.cotizacion.domain.models.equipment_details import MedicalEquipment

@admin.register(MedicalEquipment)
class MedicalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'series', 'price', 'created_at')
    list_filter = ('brand', 'created_at', 'updated_at')
    search_fields = ('name', 'brand', 'series', 'description')
    ordering = ('name', 'brand')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'brand', 'series')
        }),
        ('Detalles', {
            'fields': ('description', 'price')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )