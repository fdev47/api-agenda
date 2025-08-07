"""
Conexión a base de datos para location_service
"""
from commons.database import get_db_manager, get_db_session
from commons.config import config

# Obtener el gestor de base de datos para este servicio
db_manager = get_db_manager()

# Re-exportar para uso en location_service
__all__ = ["db_manager", "get_db_session", "config"] 