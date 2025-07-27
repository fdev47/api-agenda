"""
Script para eliminar todas las tablas de la base de datos de location_service
"""
import asyncio
import sys
import os

# Agregar el directorio raíz al path para poder importar commons
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from commons.database import db_manager
from infrastructure.models import Base

async def drop_tables():
    print("🗑️  Eliminando todas las tablas de location_service...")
    await db_manager.drop_tables(Base)
    print("✅ Tablas eliminadas exitosamente!")

async def main():
    print("🚀 Iniciando eliminación de tablas...")
    try:
        await drop_tables()
        print("\n🎉 ¡Eliminación completada!")
    except Exception as e:
        print(f"❌ Error durante la eliminación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 