"""
Script para poblar rampas: 3 rampas por cada sucursal existente
"""
from datetime import datetime
from commons.database import db_manager
from infrastructure.models.branch import Branch
from infrastructure.models.ramp import Ramp
from sqlalchemy.ext.asyncio import AsyncSession

async def populate_ramp_data(dry_run: bool = False):
    print("🚚 Poblando rampas para cada sucursal...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")

    session: AsyncSession = await db_manager.get_session()
    try:
        branches_result = await session.execute(Branch.__table__.select())
        branches = branches_result.fetchall()
        ramps = []
        for branch in branches:
            for i in range(1, 4):
                ramp = Ramp(
                    name=f"Rampa {i}",
                    branch_id=branch.id,
                    is_available=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                ramps.append(ramp)
                if not dry_run:
                    session.add(ramp)
        if not dry_run:
            await session.commit()
            for ramp in ramps:
                await session.refresh(ramp)
                print(f"✅ Rampa creada: {ramp.name} (Sucursal ID: {ramp.branch_id}, Rampa ID: {ramp.id})")
        else:
            for ramp in ramps:
                print(f"🔍 Simulación: Rampa a crear -> {ramp.name} (Sucursal ID: {ramp.branch_id})")
        return {"ramps": len(ramps)}
    except Exception as e:
        print(f"❌ Error poblando rampas: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close() 