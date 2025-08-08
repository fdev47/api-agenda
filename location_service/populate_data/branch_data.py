"""
Script para poblar la tabla Branch con datos de sucursales de Paraguay
"""
from datetime import datetime
from commons.database import db_manager
from infrastructure.models.branch import Branch
from infrastructure.models.country import Country
from infrastructure.models.state import State
from infrastructure.models.city import City
from infrastructure.models.local import Local
from infrastructure.models.ramp import Ramp
from sqlalchemy.ext.asyncio import AsyncSession
from commons.database import get_db_manager
from commons.config import config

BRANCHES_CSV = [
    {"code": "F", "name": "FORTIS Pedro Juan Caballero", "address": "Avda. R. Mal. Floriano c/ Cincuentenario de la Guerra del Chaco", "state": "Amambay", "city": "Pedro Juan Caballero"},
    {"code": "F1", "name": "FORTIS Abasto", "address": "Avda. Defensores del Chaco c/ 11 de Septiembre", "state": "Asunción", "city": "Asunción"},
    {"code": "F2", "name": "FORTIS Jockey", "address": "Avda. Eusebio Ayala c/ Cedro", "state": "Asunción", "city": "Asunción"},
    {"code": "F3", "name": "FORTIS Mariano Roque Alonso", "address": "Ruta Transchaco c/ Bernardino Caballero", "state": "Central", "city": "Mariano Roque Alonso"},
    {"code": "F4", "name": "FORTIS Ciudad del Este", "address": "Ruta PY02 Avda. Monseñor Rodríguez km 4.3", "state": "Alto Paraná", "city": "Ciudad del Este"},
    {"code": "F5", "name": "FORTIS Coronel Oviedo", "address": "Ruta PY02 Mcal. Estigarribia c/ Ayolas", "state": "Caaguazú", "city": "Coronel Oviedo"},
    {"code": "F6", "name": "FORTIS Concepción", "address": "Ruta PY05 km 1 Gral. Bernardino Caballero", "state": "Concepción", "city": "Concepción"},
    {"code": "F7", "name": "FORTIS Laurelty", "address": "(Zona Laurelty, dirección exacta pendiente)", "state": "Central", "city": "San Lorenzo"},
]

async def get_country_id(session, name="Paraguay"):
    result = await session.execute(
        Country.__table__.select().where(Country.name == name)
    )
    country = result.fetchone()
    return country.id if country else None

async def get_state_id(session, name):
    result = await session.execute(
        State.__table__.select().where(State.name == name)
    )
    state = result.fetchone()
    return state.id if state else None

async def get_city_id(session, name, state_id):
    result = await session.execute(
        City.__table__.select().where(City.name == name, City.state_id == state_id)
    )
    city = result.fetchone()
    return city.id if city else None

async def get_local_id(session):
    result = await session.execute(Local.__table__.select())
    local = result.fetchone()
    return local.id if local else None

async def populate_branch_data(dry_run: bool = False):
    print("🏢 Poblando sucursales (Branch)...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")

    location_db_url = config.LOCATION_DATABASE_URL
    if not location_db_url:
        raise ValueError("LOCATION_DATABASE_URL no está configurada")
    
    # Obtener el gestor de base de datos para location
    db_manager = get_db_manager(location_db_url)
    session: AsyncSession = await db_manager.get_session()
    try:
        country_id = await get_country_id(session)
        if not country_id:
            raise Exception("No se encontró el país Paraguay en la BD")
        local_id = await get_local_id(session)
        if not local_id:
            raise Exception("No se encontró ningún local en la BD")
        
        branches = []
        for row in BRANCHES_CSV:
            state_id = await get_state_id(session, row["state"])
            if not state_id:
                print(f"❌ Estado no encontrado: {row['state']}")
                continue
            city_id = await get_city_id(session, row["city"], state_id)
            if not city_id:
                print(f"❌ Ciudad no encontrada: {row['city']} (estado: {row['state']})")
                continue
            branch = Branch(
                code=row["code"],
                name=row["name"],
                address=row["address"],
                country_id=country_id,
                state_id=state_id,
                city_id=city_id,
                local_id=local_id,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            branches.append(branch)
            if not dry_run:
                session.add(branch)
        if not dry_run:
            await session.commit()
            for branch in branches:
                await session.refresh(branch)
                print(f"✅ Sucursal creada: {branch.name} (ID: {branch.id})")
        else:
            for branch in branches:
                print(f"🔍 Simulación: Sucursal a crear -> {branch}")
        return {"branches": len(branches)}
    except Exception as e:
        print(f"❌ Error poblando sucursales: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close() 