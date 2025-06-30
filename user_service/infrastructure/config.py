"""
Configuración específica del microservicio de usuarios
"""
from pydantic import BaseSettings
from commons.config import Settings as BaseSettings

class UserServiceSettings(BaseSettings):
    """Configuración específica del servicio de usuarios"""
    SERVICE_NAME: str = "user-service"
    SERVICE_VERSION: str = "1.0.0"
    SERVICE_PORT: int = 8001
    
    # Configuraciones específicas del servicio de usuarios
    USER_DEFAULT_ROLE: str = "user"
    USER_ACTIVATION_REQUIRED: bool = False
    
    class Config:
        env_file = ".env"

# Instancia de configuración específica del servicio
user_settings = UserServiceSettings()

# Importar configuración común
from commons.config import settings, db_settings, service_settings 