import asyncio
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commons.database import get_db_session
from reservation_service.infrastructure.models import (
    BaseModel, 
    ReservationModel, 
    OrderNumberModel,
    BranchScheduleModel
)


async def init_tables():
    """Inicializar todas las tablas del servicio de reservas"""
    async with get_db_session() as session:
        try:
            # Crear todas las tablas
            async with session.begin():
                await session.run_sync(BaseModel.metadata.create_all)
                print("✅ Tablas del servicio de reservas creadas exitosamente")
                
                # Verificar que las tablas se crearon
                tables = await session.run_sync(lambda sync_session: BaseModel.metadata.tables.keys())
                print(f"📋 Tablas creadas: {list(tables)}")
                
        except Exception as e:
            print(f"❌ Error al crear las tablas: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(init_tables()) 