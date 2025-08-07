#!/usr/bin/env python3
"""
Script para ejecutar Location Service
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Agregar el directorio padre al path para poder importar location_service
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv()

def main():
    """Función principal"""
    
    # Configuración del servicio
    host = "0.0.0.0"
    port = int(os.getenv("LOCATION_SERVICE_PORT"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"🚀 Iniciando Location Service...")
    print(f"📍 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"🌍 Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🗄️ Database URL configurado: {bool(os.getenv('LOCATION_DATABASE_URL'))}")
    print()
    
    # Verificar configuración
    if not os.getenv("LOCATION_DATABASE_URL"):
        print("❌ Error: LOCATION_DATABASE_URL no configurado en .env")
        print("💡 Asegúrate de tener un archivo .env con LOCATION_DATABASE_URL=postgresql://...")
        sys.exit(1)
    
    try:
        # Ejecutar el servidor
        uvicorn.run(
            "location_service.api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Location Service detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar Location Service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 