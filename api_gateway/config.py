"""
Configuración específica del API Gateway
"""
import os
from commons.config import config


class GatewayConfig:
    """Configuración específica del API Gateway"""
    
    # Configuración del servicio
    SERVICE_NAME = os.getenv("GATEWAY_SERVICE_NAME", "api-gateway")
    SERVICE_VERSION = os.getenv("GATEWAY_SERVICE_VERSION", "1.0.0")
    SERVICE_PORT = int(os.getenv("GATEWAY_SERVICE_PORT", "8000"))
    
    # Configuración de la API
    API_VERSION = config.API_VERSION
    API_PREFIX = config.API_PREFIX
    
    # URLs de servicios
    AUTH_SERVICE_URL = config.AUTH_SERVICE_URL
    USER_SERVICE_URL = config.USER_SERVICE_URL
    LOCATION_SERVICE_URL = config.LOCATION_SERVICE_URL
    
    # Configuración global
    ENVIRONMENT = config.ENVIRONMENT
    LOG_LEVEL = config.LOG_LEVEL
    CORS_ORIGINS = config.GATEWAY_CORS_ORIGINS
    
    # Configuración de documentación
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    OPENAPI_URL = "/openapi.json"
    
    # Configuración de rutas
    HEALTH_CHECK_PATH = "/health"
    API_DOCS_REDIRECT_PATH = "/api/docs"
    API_REDOC_REDIRECT_PATH = "/api/redoc"
    API_OPENAPI_REDIRECT_PATH = "/api/openapi.json"
    
    @classmethod
    def get_service_info(cls) -> dict:
        """Obtener información del servicio"""
        return {
            "name": cls.SERVICE_NAME,
            "version": cls.SERVICE_VERSION,
            "port": cls.SERVICE_PORT,
            "api_version": cls.API_VERSION,
            "api_prefix": cls.API_PREFIX,
            "environment": cls.ENVIRONMENT
        }
    
    @classmethod
    def get_service_urls(cls) -> dict:
        """Obtener URLs de servicios"""
        return {
            "auth": cls.AUTH_SERVICE_URL,
            "user": cls.USER_SERVICE_URL,
            "location": cls.LOCATION_SERVICE_URL
        }
    
    @classmethod
    def validate_configuration(cls) -> bool:
        """Validar configuración mínima requerida"""
        required_urls = [
            cls.AUTH_SERVICE_URL,
            cls.USER_SERVICE_URL
        ]
        return all(url for url in required_urls) 