"""
Configuración común para todos los microservicios
"""
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env en la raíz del proyecto
load_dotenv()

"""
Configuración centralizada para el proyecto
"""
import os
from typing import List

class APIConfig:
    """Configuración centralizada de la API"""
    
    # Versión de la API (cambiar aquí para actualizar toda la aplicación)
    API_VERSION = os.getenv("API_VERSION")
    
    # Prefijo base de la API
    API_PREFIX = f"/api/{API_VERSION}"

    # Configuración de servicios
    API_GATEWAY_NAME = os.getenv("API_GATEWAY_SERVICE_NAME")
    API_GATEWAY_VERSION = os.getenv("API_GATEWAY_SERVICE_VERSION")
    AUTH_SERVICE_NAME = os.getenv("AUTH_SERVICE_NAME")
    AUTH_SERVICE_VERSION = os.getenv("AUTH_SERVICE_VERSION")
    USER_SERVICE_NAME = os.getenv("USER_SERVICE_NAME")
    USER_SERVICE_VERSION = os.getenv("USER_SERVICE_VERSION")
    LOCATION_SERVICE_NAME = os.getenv("LOCATION_SERVICE_NAME")
    LOCATION_SERVICE_VERSION = os.getenv("LOCATION_SERVICE_VERSION")
    RESERVATION_SERVICE_NAME = os.getenv("RESERVATION_SERVICE_NAME")
    RESERVATION_SERVICE_VERSION = os.getenv("RESERVATION_SERVICE_VERSION")
    
    # Configuración de servicios
    API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
    LOCATION_SERVICE_URL = os.getenv("LOCATION_SERVICE_URL")
    RESERVATION_SERVICE_URL = os.getenv("RESERVATION_SERVICE_URL")
    
    # Puertos de servicios
    API_GATEWAY_PORT = int(os.getenv("API_GATEWAY_PORT"))
    AUTH_SERVICE_PORT = int(os.getenv("AUTH_SERVICE_PORT"))
    USER_SERVICE_PORT = int(os.getenv("USER_SERVICE_PORT"))
    LOCATION_SERVICE_PORT = int(os.getenv("LOCATION_SERVICE_PORT"))
    RESERVATION_SERVICE_PORT = int(os.getenv("RESERVATION_SERVICE_PORT"))
    
    # Configuración global
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    AUTH_TIMEOUT = int(os.getenv("AUTH_TIMEOUT"))
    
    # Firebase timeouts específicos
    FIREBASE_CONNECT_TIMEOUT = int(os.getenv("FIREBASE_CONNECT_TIMEOUT"))
    FIREBASE_READ_TIMEOUT = int(os.getenv("FIREBASE_READ_TIMEOUT"))
    FIREBASE_RETRIES = int(os.getenv("FIREBASE_RETRIES"))
    
    # Firebase timeout total (connect + read)
    FIREBASE_TOTAL_TIMEOUT = FIREBASE_CONNECT_TIMEOUT + FIREBASE_READ_TIMEOUT
    
    # CORS
    API_GATEWAY_CORS_ORIGINS = os.getenv("GATEWAY_CORS_ORIGINS").split(",")
    AUTH_CORS_ORIGINS = os.getenv("AUTH_CORS_ORIGINS").split(",")
    USER_CORS_ORIGINS = os.getenv("USER_CORS_ORIGINS").split(",")
    LOCATION_CORS_ORIGINS = os.getenv("LOCATION_CORS_ORIGINS").split(",")
    RESERVATION_CORS_ORIGINS = os.getenv("RESERVATION_CORS_ORIGINS").split(",")
    
    # Firebase
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
    
    # Database
    USER_DATABASE_URL = os.getenv("USER_DATABASE_URL")
    LOCATION_DATABASE_URL = os.getenv("LOCATION_DATABASE_URL")
    RESERVATION_DATABASE_URL = os.getenv("RESERVATION_DATABASE_URL")
    
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
            "location": cls.LOCATION_SERVICE_URL,
            "reservation": cls.RESERVATION_SERVICE_URL
        }
    
    @classmethod
    def get_service_ports(cls) -> dict:
        """Obtener puertos de servicios"""
        return {
            "gateway": cls.API_GATEWAY_PORT,
            "auth": cls.AUTH_SERVICE_PORT,
            "user": cls.USER_SERVICE_PORT,
            "location": cls.LOCATION_SERVICE_PORT,
            "reservation": cls.RESERVATION_SERVICE_PORT
        }

# Instancia global de configuración
config = APIConfig() 