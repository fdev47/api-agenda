#!/usr/bin/env python3
"""
Script para ejecutar User Service
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Agregar el directorio padre al path para poder importar user_service
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv()

def main():
    """Función principal"""
    
    # Configuración del servicio
    host = "0.0.0.0"
    port = int(os.getenv("USER_SERVICE_PORT", "8002"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"🚀 Iniciando User Service...")
    print(f"📍 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"🌍 Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔗 Auth Service URL: {os.getenv('AUTH_SERVICE_URL', 'http://localhost:8001')}")
    print(f"🗄️ Database URL configurado: {bool(os.getenv('DATABASE_URL'))}")
    print()
    
    # Verificar configuración
    if not os.getenv("DATABASE_URL"):
        print("❌ Error: DATABASE_URL no configurado en .env")
        print("💡 Asegúrate de tener un archivo .env con DATABASE_URL=postgresql://...")
        sys.exit(1)
    
    if not os.getenv("AUTH_SERVICE_URL"):
        print("⚠️  Advertencia: AUTH_SERVICE_URL no configurado, usando default")
    
    try:
        # Ejecutar el servidor
        uvicorn.run(
            "user_service.api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 User Service detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar User Service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 