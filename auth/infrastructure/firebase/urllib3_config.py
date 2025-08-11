"""
Configuración específica para urllib3 y timeouts de Firebase
"""
import os
import logging
import urllib3
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Urllib3Config:
    """Configuración específica para urllib3 y Firebase"""
    
    def __init__(self):
        # Obtener configuración de timeouts
        self.connect_timeout = int(os.getenv("FIREBASE_CONNECT_TIMEOUT", "30"))
        self.read_timeout = int(os.getenv("FIREBASE_READ_TIMEOUT", "120"))
        self.retries = int(os.getenv("FIREBASE_RETRIES", "5"))
        self.backoff_factor = float(os.getenv("FIREBASE_BACKOFF_FACTOR", "2.0"))
        
        # Configurar urllib3 globalmente
        self._configure_urllib3()
        
        logger.info(f"🔧 Urllib3 Config: connect={self.connect_timeout}s, read={self.read_timeout}s, retries={self.retries}")
    
    def _configure_urllib3(self):
        """Configurar urllib3 con timeouts optimizados"""
        try:
            # Configurar timeouts por defecto
            urllib3.util.Timeout.DEFAULT_TIMEOUT = urllib3.util.Timeout(
                connect=self.connect_timeout,
                read=self.read_timeout
            )
            
            # Configurar retry por defecto
            urllib3.util.Retry.DEFAULT_ALLOWED_METHODS = frozenset([
                'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE'
            ])
            
            # Configurar pool de conexiones
            urllib3.util.Retry.DEFAULT_BACKOFF_MAX = 120  # Máximo 2 minutos de backoff
            
            # Configurar timeouts más agresivos para evitar reintentos excesivos
            urllib3.util.Retry.DEFAULT_RETRY_AFTER_STATUS_CODES = [429, 500, 502, 503, 504]
            
            # Reducir el número máximo de reintentos para errores de red
            urllib3.util.Retry.DEFAULT_MAX_RETRIES = 3
            
            logger.info("✅ Urllib3 configurado exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error configurando urllib3: {e}")
    
    def get_retry_strategy(self) -> urllib3.util.Retry:
        """Obtener estrategia de retry configurada"""
        return urllib3.util.Retry(
            total=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'TRACE'])
        )
    
    def get_timeout_config(self) -> Dict[str, Any]:
        """Obtener configuración de timeouts"""
        return {
            'connect_timeout': self.connect_timeout,
            'read_timeout': self.read_timeout,
            'retries': self.retries,
            'backoff_factor': self.backoff_factor
        }

# Instancia global de configuración
urllib3_config = Urllib3Config()
