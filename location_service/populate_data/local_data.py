"""
Script para poblar la tabla Local con datos de ejemplo
"""
from datetime import datetime
from commons.database import db_manager
from infrastructure.models.local import Local
from sqlalchemy.ext.asyncio import AsyncSession

async def populate_local_data(dry_run: bool = False):
    print("🏢 Poblando tabla Local...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")

    session: AsyncSession = await db_manager.get_session()
    try:
        local = Local(
            name="Fortis",
            code="fortis-may",
            phone="0981222333",
            email="test@gmail.com",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        if not dry_run:
            session.add(local)
            await session.commit()
            await session.refresh(local)
            print(f"✅ Local creado: {local.name} (ID: {local.id})")
        else:
            print(f"🔍 Simulación: Local a crear -> {local}")
        return {"locals": 1}
    except Exception as e:
        print(f"❌ Error poblando Local: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close() 