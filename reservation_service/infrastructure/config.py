import os
from typing import List
from commons.config import config


class Settings:
    """Configuración del servicio de reservas"""
    
    # Configuración del servicio
    SERVICE_NAME: str = os.getenv("RESERVATION_SERVICE_NAME", "reservation-service")
    SERVICE_VERSION: str = os.getenv("RESERVATION_SERVICE_VERSION", "1.0.0")
    SERVICE_PORT: int = int(os.getenv("RESERVATION_SERVICE_PORT", "8004"))
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("RESERVATION_CORS_ORIGINS", "http://localhost:3000,http://localhost:8080,*").split(",")
    
    # Base de datos - usar la configuración del módulo común
    DATABASE_URL: str = config.DATABASE_URL or os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/reservation_db")
    
    # Servicios externos
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://localhost:8002")
    LOCATION_SERVICE_URL: str = os.getenv("LOCATION_SERVICE_URL", "http://localhost:8003")
    
    # Configuración de horarios
    DEFAULT_INTERVAL_MINUTES: int = int(os.getenv("DEFAULT_INTERVAL_MINUTES", "60"))
    MAX_INTERVAL_MINUTES: int = int(os.getenv("MAX_INTERVAL_MINUTES", "1440"))
    
    # Configuración de reservas
    MAX_RESERVATION_DURATION_HOURS: int = int(os.getenv("MAX_RESERVATION_DURATION_HOURS", "24"))
    MIN_RESERVATION_DURATION_MINUTES: int = int(os.getenv("MIN_RESERVATION_DURATION_MINUTES", "30"))


# Instancia global de configuración
settings = Settings() 