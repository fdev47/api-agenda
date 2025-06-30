"""
Script para inicializar las tablas de la base de datos
"""
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commons.database import get_db_session, engine
from location_service.infrastructure.models.base import Base
from location_service.infrastructure.models.country import Country
from location_service.infrastructure.models.state import State
from location_service.infrastructure.models.city import City
from location_service.infrastructure.models.local import Local
from location_service.infrastructure.models.branch import Branch
from location_service.infrastructure.models.ramp import Ramp
from location_service.infrastructure.models.sector import Sector
from location_service.infrastructure.models.sector_type import SectorType


def init_tables():
    """Inicializar todas las tablas"""
    print("Creando tablas...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    print("Tablas creadas exitosamente!")
    
    # Verificar que las tablas se crearon
    with get_db_session() as session:
        # Verificar tabla countries
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='countries'")
        if result.fetchone():
            print("✓ Tabla 'countries' creada")
        else:
            print("✗ Error: Tabla 'countries' no encontrada")
        
        # Verificar tabla states
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='states'")
        if result.fetchone():
            print("✓ Tabla 'states' creada")
        else:
            print("✗ Error: Tabla 'states' no encontrada")
        
        # Verificar tabla cities
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cities'")
        if result.fetchone():
            print("✓ Tabla 'cities' creada")
        else:
            print("✗ Error: Tabla 'cities' no encontrada")
        
        # Verificar tabla locals
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locals'")
        if result.fetchone():
            print("✓ Tabla 'locals' creada")
        else:
            print("✗ Error: Tabla 'locals' no encontrada")
        
        # Verificar tabla branches
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='branches'")
        if result.fetchone():
            print("✓ Tabla 'branches' creada")
        else:
            print("✗ Error: Tabla 'branches' no encontrada")
        
        # Verificar tabla ramps
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ramps'")
        if result.fetchone():
            print("✓ Tabla 'ramps' creada")
        else:
            print("✗ Error: Tabla 'ramps' no encontrada")
        
        # Verificar tabla sectors
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sectors'")
        if result.fetchone():
            print("✓ Tabla 'sectors' creada")
        else:
            print("✗ Error: Tabla 'sectors' no encontrada")
        
        # Verificar tabla sector_types
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sector_types'")
        if result.fetchone():
            print("✓ Tabla 'sector_types' creada")
        else:
            print("✗ Error: Tabla 'sector_types' no encontrada")


if __name__ == "__main__":
    init_tables() 