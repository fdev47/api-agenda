"""
Script para iniciar el servicio auth usando la configuración del .env
"""
import os
import uvicorn
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def start_auth_service():
    """Iniciar el servicio auth"""
    
    # Obtener configuración del .env
    service_port = int(os.getenv("AUTH_SERVICE_PORT"))
    service_name = os.getenv("AUTH_SERVICE_NAME")
    environment = os.getenv("ENVIRONMENT")
    
    print(f"🚀 Iniciando {service_name}...")
    print(f"📡 Puerto: {service_port}")
    print(f"🌍 Entorno: {environment}")
    print(f"📄 .env cargado: {os.path.exists('.env')}")
    
    # Configurar uvicorn
    uvicorn.run(
        "auth.api.main:app",
        host="0.0.0.0",
        port=service_port,
        reload=environment == "development",
        log_level="info"
    )

if __name__ == "__main__":
    start_auth_service() 