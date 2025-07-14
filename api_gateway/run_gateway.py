#!/usr/bin/env python3
"""
Script para ejecutar el API Gateway
"""
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Agregar el directorio raíz del proyecto al path para importar módulos
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Cargar variables de entorno desde la raíz del proyecto
env_path = os.path.join(project_root, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()  # Buscar .env en el directorio actual

def main():
    """Función principal para ejecutar el API Gateway"""
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: No se encontró el archivo main.py")
        print("💡 Asegúrate de ejecutar este script desde el directorio api_gateway")
        sys.exit(1)
    
    # Verificar archivo .env en la raíz del proyecto
    if not os.path.exists(env_path):
        print("⚠️  Advertencia: No se encontró el archivo .env en la raíz del proyecto")
        print(f"💡 Buscando en: {env_path}")
        print("💡 Crea un archivo .env basado en env.example")
    
    # Configuración del servidor
    host = "0.0.0.0"
    port = int(os.getenv("GATEWAY_SERVICE_PORT", "8000"))
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    log_level = os.getenv("LOG_LEVEL", "INFO").lower()
    
    print("🚀 Iniciando API Gateway...")
    print(f"📡 Host: {host}")
    print(f"🔌 Puerto: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"📝 Log Level: {log_level}")
    print(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"📄 .env encontrado: {os.path.exists(env_path)}")
    print(f"📂 Directorio actual: {os.getcwd()}")
    print(f"🏠 Raíz del proyecto: {project_root}")
    
    # Verificar servicios configurados
    auth_url = os.getenv("AUTH_SERVICE_URL")
    user_url = os.getenv("USER_SERVICE_URL")
    location_url = os.getenv("LOCATION_SERVICE_URL")
    
    print(f"🔗 Auth Service URL: {auth_url}")
    print(f"👥 User Service URL: {user_url}")
    print(f"📍 Location Service URL: {location_url}")
    
    try:
        # Ejecutar el servidor
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 API Gateway detenido por el usuario")
    except Exception as e:
        print(f"❌ Error al iniciar API Gateway: {e}")
        print(f"💡 Asegúrate de que todas las dependencias estén instaladas")
        sys.exit(1)

if __name__ == "__main__":
    main() 