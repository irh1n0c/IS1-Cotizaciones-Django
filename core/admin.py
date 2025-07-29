from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('userid', 'email', 'get_tipo_usuario_display', 'is_active', 'is_staff')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('userid', 'password')}),
        ('Información personal', {'fields': ('email', 'tipo_usuario')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'registerdate')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('userid', 'email', 'tipo_usuario', 'password1', 'password2'),
        }),
    )
    search_fields = ('userid', 'email')
    ordering = ('userid',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Usuario, UsuarioAdmin)