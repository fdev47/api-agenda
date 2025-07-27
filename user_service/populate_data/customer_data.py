"""
Script para poblar clientes (customer) en user_service
"""
from commons.database import db_manager
from sqlalchemy.ext.asyncio import AsyncSession

async def populate_customer_data(dry_run: bool = False):
    print("🧑‍💼 Poblando clientes (customer)...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")
    # Aquí irá la lógica de inserción
    return {"customers": 0} 