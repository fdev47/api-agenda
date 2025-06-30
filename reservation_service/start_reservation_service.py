#!/usr/bin/env python3
"""
Script para ejecutar Reservation Service
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Agregar el directorio padre al path para poder importar reservation_service
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv()

def main():
    """Función principal"""
    
    # Configuración del servicio
    host = "0.0.0.0"
    port = int(os.getenv("RESERVATION_SERVICE_PORT", "8004"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"🚀 Iniciando Reservation Service...")
    print(f"📍 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"🌍 Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🗄️ Database URL configurado: {bool(os.getenv('DATABASE_URL'))}")
    print()
    
    # Verificar configuración
    if not os.getenv("DATABASE_URL"):
        print("❌ Error: DATABASE_URL no configurado en .env")
        print("💡 Asegúrate de tener un archivo .env con DATABASE_URL=postgresql://...")
        sys.exit(1)
    
    try:
        # Ejecutar el servidor
        uvicorn.run(
            "reservation_service.api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Reservation Service detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar Reservation Service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 