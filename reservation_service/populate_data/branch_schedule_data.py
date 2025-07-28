"""
Script para poblar horarios de sucursales en reservation_service usando api_gateway
"""
import os
import sys
import asyncio
from datetime import time
from typing import List, Dict, Any

# Agregar el directorio raíz al path para poder importar commons
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from commons.api_client import APIClient
from commons.config import config
from commons.database import get_db_session

# Imports del reservation_service
from reservation_service.domain.entities.day_of_week import DayOfWeek
from reservation_service.domain.entities.branch_schedule import BranchSchedule
from reservation_service.infrastructure.repositories.schedule_repository_impl import ScheduleRepositoryImpl


async def get_branches(api_client: APIClient) -> List[Dict[str, Any]]:
    """
    Obtener sucursales disponibles desde api_gateway
    """
    try:
        print(f"🔍 Intentando obtener sucursales desde: {config.API_PREFIX}/location/branches/")
        response = await api_client.get(f"{config.API_PREFIX}/location/branches/")
        print(f"📡 Respuesta del API Gateway: {response}")
        
        if response:
            # La respuesta tiene 'branches' no 'items'
            branches = response.get('branches', [])
            print(f"📋 Se encontraron {len(branches)} sucursales")
            if branches:
                print("📍 Sucursales encontradas:")
                for branch in branches[:3]:  # Mostrar solo las primeras 3
                    print(f"   - ID: {branch.get('id')}, Nombre: {branch.get('name')}")
                if len(branches) > 3:
                    print(f"   ... y {len(branches) - 3} más")
            return branches
        else:
            print("⚠️  No se recibió respuesta del API Gateway")
        return []
    except Exception as e:
        print(f"⚠️  Error obteniendo sucursales: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        return []


async def create_branch_schedule(
    schedule_repository: ScheduleRepositoryImpl,
    branch_id: int,
    day_of_week: DayOfWeek,
    start_time: time,
    end_time: time,
    interval_minutes: int = 120  # 2 horas por defecto
) -> bool:
    """
    Crear un horario para una sucursal
    """
    try:
        print(f"      🔧 Creando horario para sucursal {branch_id}, día {day_of_week.name}")
        
        # Crear la entidad de dominio
        schedule = BranchSchedule(
            branch_id=branch_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            interval_minutes=interval_minutes,
            is_active=True
        )
        
        print(f"      📝 Entidad creada: {schedule}")
        
        # Guardar en la base de datos
        created_schedule = await schedule_repository.create(schedule)
        
        print(f"      ✅ Horario creado con ID: {created_schedule.id}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error creando horario para sucursal {branch_id}, día {day_of_week.name}: {e}")
        return False


async def populate_branch_schedule_data(dry_run: bool = False):
    """
    Poblar datos de horarios de sucursales usando el api_gateway
    """
    print("🏢 Poblando horarios de sucursales...")
    
    # Configuración del API Gateway
    api_gateway_url = config.API_GATEWAY_URL
    access_token = os.getenv("ACCESS_TOKEN")
    
    print(f"🔧 Configuración:")
    print(f"   - API Gateway URL: {api_gateway_url}")
    print(f"   - API Prefix: {config.API_PREFIX}")
    print(f"   - ACCESS_TOKEN configurado: {'Sí' if access_token else 'No'}")
    if access_token:
        print(f"   - Token (primeros 10 chars): {access_token[:10]}...")
    
    if not access_token:
        print("❌ ERROR: ACCESS_TOKEN no configurado en variables de entorno")
        print("   Configura ACCESS_TOKEN en tu archivo .env")
        return {"schedules": 0}
    
    # Obtener sucursales disponibles
    async with APIClient(api_gateway_url, access_token) as api_client:
        branches = await get_branches(api_client)
        
        if not branches:
            print("⚠️  No se encontraron sucursales para poblar horarios")
            return {"schedules": 0}
    
    # Configuración de horarios: Lunes a Viernes, 8:00 a 18:00, intervalo de 2 horas
    work_days = [
        DayOfWeek.MONDAY,
        DayOfWeek.TUESDAY, 
        DayOfWeek.WEDNESDAY,
        DayOfWeek.THURSDAY,
        DayOfWeek.FRIDAY
    ]
    
    start_time = time(8, 0)  # 8:00 AM
    end_time = time(18, 0)   # 6:00 PM
    interval_minutes = 120    # 2 horas
    
    if dry_run:
        print(f"🔍 Simulando creación de horarios...")
        print(f"   - Días laborables: {[day.name for day in work_days]}")
        print(f"   - Horario: {start_time} - {end_time}")
        print(f"   - Intervalo: {interval_minutes} minutos")
        print(f"   - Sucursales: {len(branches)}")
        
        total_schedules = len(branches) * len(work_days)
        print(f"   - Total de horarios a crear: {total_schedules}")
        
        for branch in branches:
            print(f"   📍 Sucursal: {branch.get('name', 'N/A')} (ID: {branch.get('id', 'N/A')})")
            for day in work_days:
                print(f"      - {day.name}: {start_time} - {end_time}")
        
        return {"schedules": total_schedules}
    
    inserted_count = 0
    
    try:
        # Crear repositorio
        schedule_repository = ScheduleRepositoryImpl()
        
        for branch in branches:
            branch_id = branch.get('id')
            branch_name = branch.get('name', 'N/A')
            
            if not branch_id:
                print(f"   ⚠️  Sucursal sin ID válido: {branch_name}")
                continue
            
            print(f"   📍 Procesando sucursal: {branch_name} (ID: {branch_id})")
            
            for day in work_days:
                try:
                    success = await create_branch_schedule(
                        schedule_repository=schedule_repository,
                        branch_id=branch_id,
                        day_of_week=day,
                        start_time=start_time,
                        end_time=end_time,
                        interval_minutes=interval_minutes
                    )
                    
                    if success:
                        print(f"      ✅ {day.name}: {start_time} - {end_time}")
                        inserted_count += 1
                    else:
                        print(f"      ❌ {day.name}: Error al crear horario")
                        
                except Exception as e:
                    print(f"      ❌ Error en {day.name}: {e}")
                    continue
                    
    except Exception as e:
        print(f"❌ Error general: {e}")
        return {"schedules": 0}
    
    print(f"\n✅ Se crearon {inserted_count} horarios de sucursales exitosamente")
    return {"schedules": inserted_count} 