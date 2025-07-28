"""
Conexión a base de datos para reservation_service
"""
from commons.database import get_db_session

# Re-exportar para uso en reservation_service
__all__ = ["get_db_session"] 