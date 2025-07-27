"""
Configuración común para todos los microservicios
"""
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List, Union
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env en la raíz del proyecto
load_dotenv()

class DatabaseSettings(BaseSettings):
    """Configuración específica para la base de datos"""
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignorar campos extra

class ServiceSettings(BaseSettings):
    """Configuración común para todos los servicios"""
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    SERVICE_PORT: int = 8000
    
    @field_validator('CORS_ORIGINS')
    @classmethod
    def parse_cors_origins(cls, v):
        """Convertir string de CORS a lista"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignorar campos extra

class Settings(BaseSettings):
    """Configuración completa que combina todas las configuraciones"""
    # Configuración de base de datos
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    
    # Configuración general del servicio
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    SERVICE_PORT: int = 8000
    
    # Configuración específica del servicio (debe ser sobrescrita por cada microservicio)
    SERVICE_NAME: str = "microservice"
    SERVICE_VERSION: str = "1.0.0"
    
    # Configuración de Firebase
    FIREBASE_CREDENTIALS_PATH: str = ""
    FIREBASE_PROJECT_ID: str = ""
    
    @field_validator('CORS_ORIGINS')
    @classmethod
    def parse_cors_origins(cls, v):
        """Convertir string de CORS a lista"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignorar campos extra

# Instancia global de configuración
settings = Settings()

# Configuraciones específicas
db_settings = DatabaseSettings()
service_settings = ServiceSettings()

"""
Configuración centralizada para el proyecto
"""
import os
from typing import List

class APIConfig:
    """Configuración centralizada de la API"""
    
    # Versión de la API (cambiar aquí para actualizar toda la aplicación)
    API_VERSION = os.getenv("API_VERSION", "v1")
    
    # Prefijo base de la API
    API_PREFIX = f"/api/{API_VERSION}"
    
    # Configuración de servicios
    API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8000")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8002")
    LOCATION_SERVICE_URL = os.getenv("LOCATION_SERVICE_URL", "http://localhost:8003")
    
    # Puertos de servicios
    API_GATEWAY_PORT = int(os.getenv("API_GATEWAY_PORT", "8000"))
    AUTH_SERVICE_PORT = int(os.getenv("AUTH_SERVICE_PORT", "8001"))
    USER_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT", "8002"))
    LOCATION_SERVICE_PORT = int(os.getenv("LOCATION_SERVICE_PORT", "8003"))
    
    # Configuración global
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    AUTH_TIMEOUT = int(os.getenv("AUTH_TIMEOUT", "30"))
    
    # CORS
    GATEWAY_CORS_ORIGINS = os.getenv("GATEWAY_CORS_ORIGINS", "*").split(",")
    AUTH_CORS_ORIGINS = os.getenv("AUTH_CORS_ORIGINS", "*").split(",")
    USER_CORS_ORIGINS = os.getenv("USER_CORS_ORIGINS", "*").split(",")
    LOCATION_CORS_ORIGINS = os.getenv("LOCATION_CORS_ORIGINS", "*").split(",")
    
    # Firebase
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    @classmethod
    def get_api_prefix(cls) -> str:
        """Obtener el prefijo de la API"""
        return cls.API_PREFIX
    
    @classmethod
    def get_api_version(cls) -> str:
        """Obtener la versión de la API"""
        return cls.API_VERSION
    
    @classmethod
    def get_service_urls(cls) -> dict:
        """Obtener URLs de servicios"""
        return {
            "gateway": cls.API_GATEWAY_URL,
            "auth": cls.AUTH_SERVICE_URL,
            "user": cls.USER_SERVICE_URL,
            "location": cls.LOCATION_SERVICE_URL
        }
    
    @classmethod
    def get_service_ports(cls) -> dict:
        """Obtener puertos de servicios"""
        return {
            "gateway": cls.API_GATEWAY_PORT,
            "auth": cls.AUTH_SERVICE_PORT,
            "user": cls.USER_SERVICE_PORT,
            "location": cls.LOCATION_SERVICE_PORT
        }

# Instancia global de configuración
config = APIConfig() 