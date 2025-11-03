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

                logger.info(f"🔍 Rampas disponibles: {ramps}")
                
                # Filtrar rampas según el tipo de carga
                filtered_ramps = []
                if request.cargo_type == "SECO":
                    # SECO: solo Rampa 2 o Rampa 3
                    filtered_ramps = [r for r in ramps if r["name"] in ["Rampa 2", "Rampa 3"]]
                    logger.info(f"🔍 Filtrando rampas para tipo SECO: Rampa 2 o Rampa 3")
                elif request.cargo_type == "FRIO":
                    # FRIO: solo Rampa 1
                    filtered_ramps = [r for r in ramps if r["name"] == "Rampa 1"]
                    logger.info(f"🔍 Filtrando rampas para tipo FRIO: Rampa 1")
                elif request.cargo_type == "FLV":
                    # FLV: solo Rampa 1 o Rampa 2
                    filtered_ramps = [r for r in ramps if r["name"] in ["Rampa 1", "Rampa 2"]]
                    logger.info(f"🔍 Filtrando rampas para tipo FLV: Rampa 1 o Rampa 2")
                else:
                    # Si no es ninguno de los tipos especificados, usar todas las rampas
                    filtered_ramps = ramps
                    logger.warning(f"⚠️ Tipo de carga '{request.cargo_type}' no reconocido, usando todas las rampas")
                
                if not filtered_ramps:
                    raise ValueError(f"No hay rampas disponibles para el tipo de carga '{request.cargo_type}' en la sucursal {request.branch_id}")
                
                ramps = filtered_ramps
                logger.info(f"📋 Encontradas {len(ramps)} rampas filtradas en la sucursal")
                
                # 2. Obtener reservas existentes en el rango de fechas desde reservation_service
                # Convertir fechas al formato YYYY-MM-DD para el filtro del reservation_service
                start_date_filter = start_datetime.strftime("%Y-%m-%d")
                end_date_filter = end_datetime.strftime("%Y-%m-%d")
                
                logger.info(f"🔍 Verificando reservas existentes en el rango {start_date_filter} - {end_date_filter}")
                reservations_response = await reservation_client.get(
                    f"{config.API_PREFIX}/reservations?branch_id={request.branch_id}&reservation_date_from={start_date_filter}&reservation_date_to={end_date_filter}&reservation_status=PENDING",
                    headers={"Authorization": f"Bearer {access_token}"} if access_token else {}
                )
                
                existing_reservations = reservations_response.get("items", [])
                logger.info(f"📋 Encontradas {len(existing_reservations)} reservas existentes")
                
                # 3. Filtrar rampas que no tienen conflictos de horario
                available_ramps = []
                for ramp in ramps:
                    ramp_id = ramp["id"]
                    has_conflict = False
                    
                    for reservation in existing_reservations:
                        # main_reservations es una lista, iterar sobre ella
                        main_reservations = reservation.get("main_reservations", [])
                        for main_reservation in main_reservations:
                            # Verificar si alguna main_reservation usa esta rampa
                            sector_data = main_reservation.get("sector_data", {})
                            logger.info(f"🔍 Sector data: {sector_data}")
                            if sector_data.get("ramp_id") == ramp_id:
                                has_conflict = True
                                logger.info(f"⏭️ Rampa '{ramp['name']}' (ID: {ramp_id}) tiene conflicto de horario")
                                break
                        
                        if has_conflict:
                            break
                    
                    if not has_conflict:
                        available_ramps.append(ramp)
                        logger.info(f"✅ Rampa '{ramp['name']}' (ID: {ramp_id}) disponible")
                
                # 4. Validar que al menos una rampa esté disponible
                if not available_ramps:
                    raise ValueError(f"No hay rampas disponibles para el tipo de carga '{request.cargo_type}' en la sucursal {request.branch_id} para el horario especificado")
                
                logger.info(f"📋 Total de rampas disponibles: {len(available_ramps)}")
                
                # 5. Retornar TODAS las rampas disponibles en un array
                response_list = []
                for ramp in available_ramps:
                    response_list.append(
                        AvailableRampResponse(
                            ramp_id=ramp["id"],
                            ramp_name=ramp["name"],
                            branch_id=ramp["branch_id"],
                            is_available=True,
                            start_date=start_datetime,
                            end_date=end_datetime,
                            cargo_type=request.cargo_type
                        )
                    )
                
                return [response_list[0]]
            
        except ValueError as e:
            logger.error(f"❌ Error de validación: {str(e)}")
            raise e
        except HTTPError as e:
            logger.error(f"❌ Error HTTP: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
            raise Exception(f"Error interno del servidor: {str(e)}") 