"""
Script para poblar horarios de rampas
"""
from datetime import datetime, time
from commons.database import get_db_manager
from commons.config import config
from infrastructure.models.ramp import Ramp
from infrastructure.models.ramp_schedule import RampSchedule
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def populate_ramp_schedule_data(dry_run: bool = False):
    """
    Poblar horarios para cada rampa
    
    Horarios por rampa:
    - Rampa 1: Lunes a Sábado
        - Turno 1: 05:00-10:00
        - Turno 2: 12:00-19:00
    - Rampa 2: Lunes a Sábado
        - Turno 1: 06:00-11:00
        - Turno 2: 13:00-19:00
    - Rampa 3: Lunes a Sábado
        - Turno 1: 06:00-12:00
        - Turno 2: 14:00-19:00
    """
    print("📅 Poblando horarios de rampas...")
    if dry_run:
        print("🔍 MODO SIMULACIÓN: No se guardarán datos en la BD")
    
    location_db_url = config.LOCATION_DATABASE_URL
    if not location_db_url:
        raise ValueError("LOCATION_DATABASE_URL no está configurada")
    
    # Obtener el gestor de base de datos para location
    db_manager = get_db_manager(location_db_url)
    session: AsyncSession = await db_manager.get_session()
    
    try:
        # Obtener todas las rampas
        query = select(Ramp).order_by(Ramp.id)
        result = await session.execute(query)
        ramps = result.scalars().all()
        
        if not ramps:
            print("⚠️ No se encontraron rampas en la base de datos")
            return {"schedules": 0}
        
        print(f"📋 Encontradas {len(ramps)} rampas")
        
        # Definir horarios por nombre de rampa
        schedule_config = {
            "Rampa 1": [
                {"name": "Turno 1", "start": time(5, 0), "end": time(10, 0)},
                {"name": "Turno 2", "start": time(12, 0), "end": time(19, 0)}
            ],
            "Rampa 2": [
                {"name": "Turno 1", "start": time(6, 0), "end": time(11, 0)},
                {"name": "Turno 2", "start": time(13, 0), "end": time(19, 0)}
            ],
            "Rampa 3": [
                {"name": "Turno 1", "start": time(6, 0), "end": time(12, 0)},
                {"name": "Turno 2", "start": time(14, 0), "end": time(19, 0)}
            ]
        }
        
        # Días de la semana: 1=Lunes a 6=Sábado
        work_days = [1, 2, 3, 4, 5, 6]
        
        schedules = []
        total_created = 0
        
        for ramp in ramps:
            # Obtener configuración de horarios para esta rampa
            config_for_ramp = schedule_config.get(ramp.name)
            
            if not config_for_ramp:
                print(f"⚠️ No hay configuración de horarios para '{ramp.name}' (ID: {ramp.id})")
                continue
            
            print(f"\n🚚 Procesando '{ramp.name}' (ID: {ramp.id})...")
            
            # Crear horarios para cada día de la semana
            for day_of_week in work_days:
                for shift in config_for_ramp:
                    schedule = RampSchedule(
                        ramp_id=ramp.id,
                        day_of_week=day_of_week,
                        name=shift["name"],
                        start_time=shift["start"],
                        end_time=shift["end"],
                        is_active=True,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    
                    schedules.append(schedule)
                    
                    if not dry_run:
                        session.add(schedule)
                    
                    day_names = {1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes", 6: "Sábado", 7: "Domingo"}
                    print(f"   ✓ {day_names[day_of_week]} - {shift['name']}: {shift['start'].strftime('%H:%M')}-{shift['end'].strftime('%H:%M')}")
                    total_created += 1
        
        if not dry_run:
            await session.commit()
            print(f"\n✅ {total_created} horarios creados exitosamente")
        else:
            print(f"\n🔍 Simulación: {total_created} horarios a crear")
        
        return {"schedules": total_created}
        
    except Exception as e:
        print(f"❌ Error poblando horarios de rampas: {e}")
        if not dry_run:
            await session.rollback()
        raise
    finally:
        await session.close()

