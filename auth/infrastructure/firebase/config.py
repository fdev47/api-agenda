"""
Configuración específica para Firebase Auth
"""
import os
import logging
from typing import Optional
from commons.config import config

logger = logging.getLogger(__name__)

class FirebaseConfig:
    """Configuración específica para Firebase"""
    
    def __init__(self):
        # Obtener configuración de timeouts con valores por defecto
        self.connect_timeout = int(os.getenv("FIREBASE_CONNECT_TIMEOUT", "10"))
        self.read_timeout = int(os.getenv("FIREBASE_READ_TIMEOUT", "30"))
        self.total_timeout = self.connect_timeout + self.read_timeout
        self.retries = int(os.getenv("FIREBASE_RETRIES", "3"))
        
        # Configuración de credenciales
        self.credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        self.project_id = os.getenv("FIREBASE_PROJECT_ID")
        
        logger.info(f"🔧 Firebase Config: connect={self.connect_timeout}s, read={self.read_timeout}s, total={self.total_timeout}s, retries={self.retries}")
    
    def get_timeout_config(self) -> dict:
        """Obtener configuración de timeouts"""
        return {
            'connect_timeout': self.connect_timeout,
            'read_timeout': self.read_timeout,
            'total_timeout': self.total_timeout,
            'retries': self.retries
        }
    
    def get_app_config(self) -> dict:
        """Obtener configuración para inicializar Firebase App"""
        return {
            'projectId': self.project_id,
            'httpTimeout': self.total_timeout
        }
    
    def validate_config(self) -> bool:
        """Validar que la configuración es correcta"""
        if not self.project_id:
            logger.error("❌ FIREBASE_PROJECT_ID no configurado")
            return False
        
        if not self.credentials_path or not os.path.exists(self.credentials_path):
            logger.warning("⚠️ FIREBASE_CREDENTIALS_PATH no configurado o archivo no existe")
            # No es fatal, puede usar credenciales por defecto
        
        logger.info("✅ Configuración de Firebase válida")
        return True

# Instancia global de configuración
firebase_config = FirebaseConfig() 