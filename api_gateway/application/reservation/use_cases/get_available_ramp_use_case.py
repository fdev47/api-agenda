"""
Caso de uso para obtener una rampa disponible
"""
import logging
from datetime import datetime
from typing import Optional, List
from commons.api_client import HTTPError, APIClient
from commons.config import config
from ....domain.reservation.dto.requests.available_ramp_request import AvailableRampRequest
from ....domain.reservation.dto.responses.available_ramp_response import AvailableRampResponse

logger = logging.getLogger(__name__)


class GetAvailableRampUseCase:
    """Caso de uso para obtener una rampa disponible"""
    
    def __init__(self):
        from commons.config import config
        self.location_client = APIClient(base_url=config.LOCATION_SERVICE_URL)
        self.reservation_client = APIClient(base_url=config.RESERVATION_SERVICE_URL)
    
    async def execute(self, request: AvailableRampRequest, access_token: str = "") -> List[AvailableRampResponse]:
        """Ejecutar el caso de uso"""
        
        try:
            # Convertir fechas
            start_datetime = datetime.strptime(request.start_date, "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(request.end_date, "%Y-%m-%d %H:%M:%S")
            
            if start_datetime >= end_datetime:
                raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")
            
            # Usar context managers para los clientes HTTP
            async with self.location_client as location_client, self.reservation_client as reservation_client:
                # 1. Obtener todas las rampas de la sucursal desde location_service
                logger.info(f"🔍 Obteniendo rampas de la sucursal {request.branch_id}")
                ramps_response = await location_client.get(
                    f"{config.API_PREFIX}/ramps?branch_id={request.branch_id}&is_available=true&limit=50",
                    headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
                )
                
                if not ramps_response.get("ramps"):
                    raise ValueError(f"No hay rampas disponibles en la sucursal {request.branch_id}")
                
                ramps = ramps_response["ramps"]
                logger.info(f"📋 Encontradas {len(ramps)} rampas en la sucursal")
                
                # 2. Obtener reservas existentes en el rango de fechas desde reservation_service
                logger.info(f"🔍 Verificando reservas existentes en el rango {request.start_date} - {request.end_date}")
                reservations_response = await reservation_client.get(
                    f"{config.API_PREFIX}/reservations?branch_id={request.branch_id}&start_date={request.start_date}&end_date={request.end_date}&status=CONFIRMED,PENDING",
                    headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
                )
                
                existing_reservations = reservations_response.get("reservations", [])
                logger.info(f"📋 Encontradas {len(existing_reservations)} reservas existentes")
                
                # 3. Filtrar rampas que no tienen conflictos de horario
                available_ramps = []
                for ramp in ramps:
                    ramp_id = ramp["id"]
                    has_conflict = False
                    
                    for reservation in existing_reservations:
                        # Verificar si la reserva usa esta rampa
                        if reservation.get("ramp_id") == ramp_id:
                            has_conflict = True
                            break
                    
                    if not has_conflict:
                        available_ramps.append(ramp)
                
                if not available_ramps:
                    raise ValueError(f"No hay rampas disponibles en la sucursal {request.branch_id} para el horario especificado")
                
                # 4. Retornar la primera rampa disponible en un array
                selected_ramp = available_ramps[0]
                logger.info(f"✅ Rampa disponible encontrada: {selected_ramp['name']} (ID: {selected_ramp['id']})")
                
                return [
                    AvailableRampResponse(
                        ramp_id=selected_ramp["id"],
                        ramp_name=selected_ramp["name"],
                        branch_id=selected_ramp["branch_id"],
                        is_available=True,
                        start_date=start_datetime,
                        end_date=end_datetime,
                        cargo_type=request.cargo_type
                    )
                ]
            
        except ValueError as e:
            logger.error(f"❌ Error de validación: {str(e)}")
            raise e
        except HTTPError as e:
            logger.error(f"❌ Error HTTP: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
            raise Exception(f"Error interno del servidor: {str(e)}") 