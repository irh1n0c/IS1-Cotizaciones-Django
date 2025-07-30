#!/usr/bin/env python
"""
Script de inicio rápido para el Sistema de Cotizaciones con DDD
Ejecuta: python run_server.py
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Imprime el banner de inicio."""
    print("=" * 60)
    print("🏥 SISTEMA DE COTIZACIONES - EQUIPOS MÉDICOS")
    print("🏗️  Arquitectura Domain-Driven Design (DDD)")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica la versión de Python."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Error: Se requiere Python 3.11 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_django():
    """Verifica que Django esté instalado."""
    try:
        import django
        print(f"✅ Django {django.get_version()} - OK")
        return True
    except ImportError:
        print("❌ Django no está instalado")
        print("   Ejecuta: pip install django==5.2.4")
        return False

def check_dependencies():
    """Verifica dependencias adicionales."""
    dependencies = [
        ('python-dateutil', 'dateutil'),
        ('typing-extensions', 'typing_extensions')
    ]
    
    missing = []
    for package_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            missing.append(package_name)
            print(f"⚠️  {package_name} - No instalado (opcional)")
    
    return missing

def setup_database():
    """Configura la base de datos."""
    print("\n🗄️  Configurando base de datos...")
    
    try:
        # Hacer migraciones
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migraciones creadas")
        else:
            print("⚠️  Sin nuevas migraciones")
        
        # Aplicar migraciones
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Base de datos configurada")
            return True
        else:
            print("❌ Error configurando base de datos:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_ddd_files():
    """Verifica que los archivos DDD existan."""
    print("\n🏗️  Verificando arquitectura DDD...")
    
    required_files = [
        'core/dominio/Servicio_calibracion/money.py',
        'core/dominio/Servicio_calibracion/domain_events.py',
        'core/dominio/Servicio_calibracion/estadoCotizacion.py',
        'core/dominio/Servicio_calibracion/cotizacionID.py',
        'core/servicios/repositories.py',
        'core/servicios/cotizacionServicioImpl.py',
        'core/dominio/Servicio_calibracion/ddd_config.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - No encontrado")
    
    if missing_files:
        print(f"\n❌ Faltan {len(missing_files)} archivos DDD")
        return False
    
    print("✅ Todos los archivos DDD presentes")
    return True

def start_server():
    """Inicia el servidor de desarrollo."""
    print("\n🚀 Iniciando servidor de desarrollo...")
    print("   URL: http://localhost:8000/")
    print("   Admin: http://localhost:8000/admin/")
    print("\n   Presiona Ctrl+C para detener el servidor")
    print("=" * 60)
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido. ¡Hasta luego!")

def main():
    """Función principal."""
    print_banner()
    
    # Verificaciones
    if not check_python_version():
        return
    
    if not check_django():
        return
    
    missing_deps = check_dependencies()
    
    if not check_ddd_files():
        print("\n💡 Tip: Asegúrate de que todos los archivos DDD estén presentes")
        return
    
    # Configurar base de datos
    if not setup_database():
        return
    
    # Mostrar información adicional
    print("\n📋 Información del sistema:")
    print("   • Bounded Contexts: Empresa (CRUD) + Cliente (Consulta)")
    print("   • Domain Events: Notificaciones automáticas")
    print("   • Value Objects: Money, CotizacionID")
    print("   • Aggregates: Quotation con reglas de negocio")
    print("   • Repositories: Especializados por contexto")
    
    if missing_deps:
        print(f"\n⚠️  Dependencias opcionales faltantes: {', '.join(missing_deps)}")
        print("   Instalar con: pip install " + " ".join(missing_deps))
    
    print("\n💡 Nota: Los warnings 'Apps aren't loaded yet' son normales durante el inicio")
    print("   La configuración DDD se cargará correctamente cuando Django esté listo")
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main()