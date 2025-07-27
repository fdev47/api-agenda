"""
Modelo base para el microservicio de reservas
"""
from commons.database import Base

# Re-exportar Base para compatibilidad con código existente
__all__ = ['Base'] 