"""
Caso de uso para obtener slots disponibles de rampas
"""
import logging
import random
from datetime import time, datetime, timedelta
from typing import List, Set, Tuple, Dict
from commons.api_client import HTTPError
from ....domain.ramp.dto.requests.ramp_slots_request import RampSlotsRequest
from ....domain.ramp.dto.responses.ramp_slots_response import RampSlotsResponse, SlotInfo
from ....domain.ramp.dto.requests.ramp_filter_request import RampFilterRequest
from ....domain.ramp_schedule.dto.requests.ramp_schedule_requests import RampScheduleFilterRequest
from .list_ramps_use_case import ListRampsUseCase
from ...ramp_schedule.use_cases.list_ramp_schedules_use_case import ListRampSchedulesUseCase

logger = logging.getLogger(__name__)


class GetRampSlotsUseCase:
    """Caso de uso para obtener slots disponibles de rampas"""
    
    def __init__(self):
        self.list_ramps_use_case = ListRampsUseCase()
        self.list_schedules_use_case = ListRampSchedulesUseCase()
    
    async def execute(self, request: RampSlotsRequest, access_token: str = "") -> RampSlotsResponse:
        """
        Ejecutar caso de uso para obtener slots disponibles
        
        Args:
            request: Request con tipo, branch_id, fecha e interval_time
            access_token: Token de acceso para autenticación
            
        Returns:
            RampSlotsResponse con los slots disponibles
        """
        try:
            logger.info(f"🔍 Obteniendo slots para tipo={request.type}, branch_id={request.branch_id}, fecha={request.schedule_date}, intervalo={request.interval_time}min")
            
            # 1. Obtener todas las rampas de la sucursal usando el use case
            logger.info(f"📞 Obteniendo rampas de la sucursal {request.branch_id}")
            ramp_filter = RampFilterRequest(
                branch_id=request.branch_id,
                is_available=True,
                skip=0,
                limit=50
            )
            ramps_response = await self.list_ramps_use_case.execute(ramp_filter, access_token)
            
            if not ramps_response.ramps:
                raise ValueError(f"No hay rampas disponibles en la sucursal {request.branch_id}")
            
            # Convertir ramps a diccionarios para compatibilidad
            ramps = [
                {
                    "id": ramp.id,
                    "name": ramp.name,
                    "branch_id": ramp.branch_id,
                    "is_available": ramp.is_available
                }
                for ramp in ramps_response.ramps
            ]
            
            # 2. Filtrar rampas según el tipo de carga
            filtered_ramps = self._filter_ramps_by_cargo_type(ramps, request.type)
            
            if not filtered_ramps:
                raise ValueError(f"No hay rampas disponibles para el tipo de carga '{request.type}' en la sucursal {request.branch_id}")
            
            logger.info(f"📋 Encontradas {len(filtered_ramps)} rampas para tipo '{request.type}': {[r['name'] for r in filtered_ramps]}")
            
            # 3. Obtener horarios de cada rampa filtrada y mapear rangos a rampas
            # Obtener el día de la semana (1=Lunes, 7=Domingo)
            day_of_week = request.schedule_date.isoweekday()
            logger.info(f"📅 Día de la semana: {day_of_week}")
            
            # Diccionario para mapear rangos de tiempo a las rampas que los tienen
            # Clave: (start_time, end_time), Valor: lista de rampas con ese rango
            time_ranges_to_ramps: Dict[Tuple[time, time], List[dict]] = {}
            
            for ramp in filtered_ramps:
                ramp_id = ramp["id"]
                ramp_name = ramp["name"]
                
                # Obtener horarios de esta rampa usando el use case
                schedule_filter = RampScheduleFilterRequest(
                    ramp_id=ramp_id,
                    day_of_week=day_of_week,
                    is_active=True,
                    limit=100,
                    offset=0
                )
                schedules_response = await self.list_schedules_use_case.execute(schedule_filter, access_token)
                
                schedules = schedules_response.schedules
                logger.info(f"📋 Rampa '{ramp_name}' (ID: {ramp_id}): {len(schedules)} horarios encontrados")
                
                for schedule in schedules:
                    start_time = self._parse_time(schedule.start_time)
                    end_time = self._parse_time(schedule.end_time)
                    time_range = (start_time, end_time)
                    
                    # Agregar esta rampa a la lista de rampas disponibles en este rango
                    if time_range not in time_ranges_to_ramps:
                        time_ranges_to_ramps[time_range] = []
                    time_ranges_to_ramps[time_range].append(ramp)
                    
                    logger.info(f"   ⏰ {schedule.name}: {start_time} - {end_time}")
            
            if not time_ranges_to_ramps:
                logger.warning(f"⚠️ No hay horarios configurados para las rampas en el día {day_of_week}")
                return RampSlotsResponse(
                    schedule_date=request.schedule_date,
                    slots=[],
                    total_slots=0,
                    available_slots=0
                )
            
            # 4. Generar slots basados en interval_time para cada rango
            # NO combinar rangos, generar slots por separado para cada rango
            all_slots = self._generate_slots_with_ramps(time_ranges_to_ramps, request.interval_time)
            logger.info(f"✅ {len(all_slots)} slots generados (antes de deduplicar)")
            
            # 5. Eliminar slots duplicados (mismo start_time y end_time)
            # Preservar el primero encontrado
            slots = self._deduplicate_slots(all_slots)
            logger.info(f"✅ {len(slots)} slots únicos después de deduplicar")
            
            # 6. Por ahora, todos los slots están disponibles (TODO: verificar reservas existentes)
            available_count = len(slots)
            
            response = RampSlotsResponse(
                schedule_date=request.schedule_date,
                slots=slots,
                total_slots=len(slots),
                available_slots=available_count
            )
            
            logger.info(f"✅ Slots obtenidos: {response.total_slots} total, {response.available_slots} disponibles")
            return response
            
        except ValueError as e:
            logger.error(f"❌ Error de validación: {str(e)}")
            raise e
        except HTTPError as e:
            logger.error(f"❌ Error HTTP: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"❌ Error obteniendo slots: {str(e)}", exc_info=True)
            raise
    
    def _filter_ramps_by_cargo_type(self, ramps: List[dict], cargo_type: str) -> List[dict]:
        """Filtrar rampas según el tipo de carga"""
        if cargo_type == "SECO":
            # SECO: solo Rampa 2 o Rampa 3
            return [r for r in ramps if r["name"] in ["Rampa 2", "Rampa 3"]]
        elif cargo_type == "FRIO":
            # FRIO: solo Rampa 1
            return [r for r in ramps if r["name"] == "Rampa 1"]
        elif cargo_type == "FLV":
            # FLV: solo Rampa 1 o Rampa 2
            return [r for r in ramps if r["name"] in ["Rampa 1", "Rampa 2"]]
        else:
            # Si no es ninguno de los tipos especificados, usar todas las rampas
            logger.warning(f"⚠️ Tipo de carga '{cargo_type}' no reconocido, usando todas las rampas")
            return ramps
    
    def _parse_time(self, time_obj) -> time:
        """Parsear string de tiempo o objeto time"""
        if isinstance(time_obj, str):
            # Formato puede ser "HH:MM:SS" o "HH:MM"
            parts = time_obj.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
            return time(hour, minute)
        elif isinstance(time_obj, time):
            return time_obj
        else:
            # Si es otro tipo (datetime), extraer el time
            return time_obj.time() if hasattr(time_obj, 'time') else time_obj
    
    def _merge_time_ranges(self, ranges: List[Tuple[time, time]]) -> List[Tuple[time, time]]:
        """
        Combinar rangos de tiempo que se solapan o son contiguos
        Ejemplo: [(7:00, 12:00), (9:00, 12:00)] -> [(7:00, 12:00)]
        Ejemplo: [(7:00, 12:00), (14:00, 19:00)] -> [(7:00, 12:00), (14:00, 19:00)]
        """
        if not ranges:
            return []
        
        # Ordenar rangos por hora de inicio
        sorted_ranges = sorted(ranges, key=lambda x: (x[0].hour, x[0].minute))
        
        merged = [sorted_ranges[0]]
        
        for current_start, current_end in sorted_ranges[1:]:
            last_start, last_end = merged[-1]
            
            # Si el rango actual se solapa o es contiguo con el último
            if current_start <= last_end:
                # Extender el último rango si es necesario
                if current_end > last_end:
                    merged[-1] = (last_start, current_end)
            else:
                # No hay solapamiento, agregar como nuevo rango
                merged.append((current_start, current_end))
        
        return merged
    
    def _generate_slots_with_ramps(
        self, 
        time_ranges_to_ramps: Dict[Tuple[time, time], List[dict]], 
        interval_minutes: int
    ) -> List[SlotInfo]:
        """
        Generar slots de tiempo basados en los rangos y asignar rampas
        Para cada slot, si hay múltiples rampas disponibles, seleccionar una al azar
        
        Args:
            time_ranges_to_ramps: Diccionario que mapea (start_time, end_time) a lista de rampas
            interval_minutes: Intervalo en minutos para cada slot
            
        Returns:
            Lista de SlotInfo con rampa asignada
        """
        slots = []
        
        # Ordenar los rangos por hora de inicio
        sorted_ranges = sorted(time_ranges_to_ramps.keys(), key=lambda x: (x[0].hour, x[0].minute))
        
        for start_time, end_time in sorted_ranges:
            available_ramps = time_ranges_to_ramps[(start_time, end_time)]
            
            # Convertir time a datetime para poder sumar minutos
            current = datetime.combine(datetime.today(), start_time)
            end = datetime.combine(datetime.today(), end_time)
            
            while current < end:
                slot_start = current.time()
                current += timedelta(minutes=interval_minutes)
                
                # Si el siguiente slot excede el final, no crear un slot incompleto
                if current > end:
                    break
                
                slot_end = current.time()
                
                # Seleccionar una rampa al azar de las disponibles
                selected_ramp = random.choice(available_ramps)
                
                # Agregar el slot con la rampa asignada
                slots.append(SlotInfo(
                    start_time=slot_start,
                    end_time=slot_end,
                    is_available=True,  # TODO: verificar contra reservas existentes
                    ramp_id=selected_ramp["id"],
                    ramp_name=selected_ramp["name"]
                ))
        
        return slots
    
    def _deduplicate_slots(self, slots: List[SlotInfo]) -> List[SlotInfo]:
        """
        Eliminar slots duplicados basados en start_time y end_time
        Preserva el primero encontrado
        
        Args:
            slots: Lista de slots que puede contener duplicados
            
        Returns:
            Lista de slots únicos (sin duplicados)
        """
        seen_times = set()
        unique_slots = []
        
        for slot in slots:
            time_key = (slot.start_time, slot.end_time)
            
            if time_key not in seen_times:
                seen_times.add(time_key)
                unique_slots.append(slot)
                logger.debug(f"   ✓ Slot único: {slot.start_time} - {slot.end_time} (Rampa: {slot.ramp_name})")
            else:
                logger.debug(f"   ⏭️ Slot duplicado ignorado: {slot.start_time} - {slot.end_time} (Rampa: {slot.ramp_name})")
        
        return unique_slots

