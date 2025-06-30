"""
Infrastructure del microservicio de usuarios
"""
# Importar componentes del módulo común
from commons.database import (
    Base, 
    db_manager, 
    create_tables, 
    get_db_session, 
    test_connection,
    DatabaseManager
)

# Re-exportar para compatibilidad con código existente
__all__ = [
    'Base',
    'db_manager', 
    'create_tables',
    'get_db_session',
    'test_connection',
    'DatabaseManager'
]
