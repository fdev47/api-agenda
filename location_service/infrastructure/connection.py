"""
Conexión a base de datos para location_service
"""
from commons.database import db_manager, get_db_session
from commons.config import config

# Re-exportar para uso en location_service
__all__ = ["db_manager", "get_db_session", "config"] 