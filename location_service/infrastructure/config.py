"""
Configuración específica del microservicio de ubicación
"""
from pydantic import BaseSettings
from commons.config import Settings as BaseSettings

class LocationServiceSettings(BaseSettings):
    """Configuración específica del servicio de ubicación"""
    SERVICE_NAME: str = "location-service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8003
    
    # Configuraciones específicas del servicio de ubicación
    LOCATION_DEFAULT_COUNTRY: str = "MEX"
    LOCATION_DEFAULT_STATE: str = "CDMX"
    
    class Config:
        env_file = ".env"

# Instancia de configuración específica del servicio
location_settings = LocationServiceSettings()

# Importar configuración común
from commons.config import settings, db_settings, service_settings 