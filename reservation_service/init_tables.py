"""
Script para inicializar las tablas de la base de datos del Reservation Service
"""
import sys
import os
import asyncio

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

from commons.database import create_tables, test_connection
from reservation_service.infrastructure.models.base import Base
from reservation_service.infrastructure.models.reservation import ReservationModel, ReservationOrderNumberModel
from reservation_service.infrastructure.models.schedule import BranchScheduleModel


async def init_tables():
    """Inicializar todas las tablas"""
    print("🚀 Iniciando creación de tablas para Reservation Service...")
    
    try:
        # Probar conexión
        print("🔍 Probando conexión a la base de datos...")
        if not await test_connection():
            print("❌ Error: No se pudo conectar a la base de datos")
            return
        
        print("✅ Conexión exitosa a la base de datos")
        
        # Crear todas las tablas
        print("📋 Creando tablas...")
        await create_tables(Base)
        print("✅ Tablas creadas exitosamente!")
        
        print("\n🎉 Todas las tablas del Reservation Service han sido creadas exitosamente!")
        print("\n📊 Tablas creadas:")
        print("  - reservations")
        print("  - reservation_order_numbers")
        print("  - branch_schedules")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(init_tables()) 