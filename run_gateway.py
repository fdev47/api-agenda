#!/usr/bin/env python3
"""
Script para ejecutar API Gateway
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def main():
    """Función principal"""
    
    # Configuración del servicio
    host = "0.0.0.0"
    port = int(os.getenv("GATEWAY_SERVICE_PORT", "8000"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    print(f"🚀 Iniciando API Gateway...")
    print(f"📍 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"🌍 Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🔗 Auth Service URL: {os.getenv('AUTH_SERVICE_URL', 'http://localhost:8001')}")
    print(f"👥 User Service URL: {os.getenv('USER_SERVICE_URL', 'http://localhost:8002')}")
    print()
    
    # Verificar configuración
    if not os.getenv("AUTH_SERVICE_URL"):
        print("❌ Error: AUTH_SERVICE_URL no configurado en .env")
        print("💡 Asegúrate de tener un archivo .env con AUTH_SERVICE_URL=http://localhost:8001")
        sys.exit(1)
    
    if not os.getenv("USER_SERVICE_URL"):
        print("❌ Error: USER_SERVICE_URL no configurado en .env")
        print("💡 Asegúrate de tener un archivo .env con USER_SERVICE_URL=http://localhost:8002")
        sys.exit(1)
    
    try:
        # Ejecutar el servidor
        uvicorn.run(
            "api_gateway.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 API Gateway detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar API Gateway: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 