"""
Configuración de logging para Firebase
"""
import logging

def configure_firebase_logging():
    """Configurar logging para reducir warnings de Firebase"""
    
    # Obtener nivel de logging desde variables de entorno
    import os
    firebase_log_level = os.getenv("FIREBASE_LOG_LEVEL", "ERROR")
    urllib3_log_level = os.getenv("URLLIB3_LOG_LEVEL", "ERROR")
    google_auth_log_level = os.getenv("GOOGLE_AUTH_LOG_LEVEL", "ERROR")
    
    # Configurar urllib3 para reducir warnings de red
    urllib3_logger = logging.getLogger("urllib3.connectionpool")
    urllib3_logger.setLevel(getattr(logging, urllib3_log_level))
    
    # Configurar google.auth para reducir warnings
    google_logger = logging.getLogger("google.auth")
    google_logger.setLevel(getattr(logging, google_auth_log_level))
    
    # Configurar firebase_admin para reducir warnings
    firebase_logger = logging.getLogger("firebase_admin")
    firebase_logger.setLevel(getattr(logging, firebase_log_level))
    
    # Configurar requests para reducir warnings
    requests_logger = logging.getLogger("requests")
    requests_logger.setLevel(getattr(logging, urllib3_log_level))
    
    # Configurar logging de urllib3.connection para errores de DNS
    urllib3_connection_logger = logging.getLogger("urllib3.connection")
    urllib3_connection_logger.setLevel(getattr(logging, urllib3_log_level))
    
    # Configurar logging de urllib3.util para errores de retry
    urllib3_util_logger = logging.getLogger("urllib3.util")
    urllib3_util_logger.setLevel(getattr(logging, urllib3_log_level))
