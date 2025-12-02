"""
Use case para exportar reservas a CSV
"""
import logging
import csv
import io
from datetime import datetime
from typing import List
from ...domain.dto.requests.export_reservations_request import ExportReservationsRequest
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from .list_reservations_use_case import ListReservationsUseCase

logger = logging.getLogger(__name__)


class ExportReservationsCsvUseCase:
    """Caso de uso para exportar reservas a formato CSV"""
    
    def __init__(
        self,
        reservation_repository: ReservationRepository,
        main_reservation_repository: MainReservationRepository
    ):
        self.reservation_repository = reservation_repository
        self.main_reservation_repository = main_reservation_repository
        self.list_reservations_use_case = ListReservationsUseCase(
            reservation_repository=reservation_repository,
            main_reservation_repository=main_reservation_repository
        )
    
    def _parse_date(self, date_str: str) -> datetime:
        """Función helper para parsear fechas en diferentes formatos"""
        if not date_str or not date_str.strip():
            return None
            
        date_str = date_str.strip()
        
        try:
            # Formato YYYY-MM-DD
            if len(date_str) == 10 and date_str.count('-') == 2:
                return datetime.strptime(date_str, "%Y-%m-%d")
            
            # Formato YYYY-MM-DD HH:MM:SS
            elif len(date_str) == 19 and date_str.count('-') == 2 and date_str.count(':') == 2:
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            
            # Formato YYYY-MM-DDTHH:MM:SS (ISO sin zona horaria)
            elif 'T' in date_str and date_str.count(':') == 2:
                date_str_std = date_str.replace('T', ' ')
                return datetime.strptime(date_str_std, "%Y-%m-%d %H:%M:%S")
            
            # Formato YYYY-MM-DDTHH:MM:SS.SSS (ISO con milisegundos)
            elif 'T' in date_str and '.' in date_str:
                date_str_std = date_str.replace('T', ' ')
                return datetime.strptime(date_str_std, "%Y-%m-%d %H:%M:%S.%f")
            
            # Intentar formato ISO estándar
            else:
                return datetime.fromisoformat(date_str)
                
        except ValueError as e:
            raise ValueError(f"Formato de fecha inválido: {date_str}. Formatos soportados: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, YYYY-MM-DDTHH:MM:SS")
    
    def _format_status(self, status: str) -> str:
        """Formatear el estado de la reserva a español"""
        status_map = {
            "PENDING": "Pendiente",
            "CONFIRMED": "Confirmado",
            "CANCELLED": "Cancelado",
            "COMPLETED": "Finalizado",
            "RESCHEDULING_REQUIRED": "Reagendado"
        }
        return status_map.get(status, status)
    
    async def execute(self, request: ExportReservationsRequest) -> bytes:
        """Ejecutar el caso de uso y retornar el contenido CSV como bytes"""
        logger.info("🚀 ExportReservationsCsvUseCase.execute() iniciado")
        
        try:
            # Parsear fechas
            date_from = None
            date_to = None
            
            if request.reservation_date_from:
                date_from = self._parse_date(request.reservation_date_from)
            if request.reservation_date_to:
                date_to = self._parse_date(request.reservation_date_to)
            
            # Crear request para el filtro (mapear company_name a customer_name)
            export_request = ReservationFilterRequest(
                user_id=request.user_id,
                customer_id=request.customer_id,
                branch_id=request.branch_id,
                branch_name=request.branch_name,
                branch_code=request.branch_code,
                sector_id=request.sector_id,
                sector_name=request.sector_name,
                customer_name=request.company_name,  # Mapear company_name a customer_name (el repositorio usa customer_name para filtrar company_name)
                customer_email=None,
                reservation_date_from=date_from,
                reservation_date_to=date_to,
                status=request.reservation_status,
                order_code=request.order_code,
                cargo_type=request.cargo_type,
                page=1,
                limit=100  # Límite alto para obtener todas las reservas
            )
            
            # Obtener reservas usando el caso de uso de listado
            result = await self.list_reservations_use_case.execute(export_request)
            reservations = result.items
            
            logger.info(f"📊 Exportando {len(reservations)} reservas a CSV")
            
            # Crear buffer en memoria para el CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Escribir encabezados
            writer.writerow([
                "proveedor",
                "fecha",
                "hora",
                "carga",
                "estado",
                "sucursal"
            ])
            
            # Escribir datos
            for reservation in reservations:
                # Formatear fecha
                fecha = ""
                if reservation.reservation_date:
                    fecha = reservation.reservation_date.strftime("%Y-%m-%d")
                
                # Formatear hora
                hora = ""
                if reservation.start_time:
                    if isinstance(reservation.start_time, datetime):
                        hora = reservation.start_time.strftime("%H:%M")
                    else:
                        hora = str(reservation.start_time)
                
                # Formatear estado
                estado = self._format_status(reservation.status or "")
                
                writer.writerow([
                    reservation.customer_data.company_name or "",
                    fecha,
                    hora,
                    reservation.cargo_type or "",
                    estado,
                    reservation.branch_data.code or ""
                ])
            
            # Obtener el contenido del CSV y convertir a bytes
            csv_content = output.getvalue()
            output.close()
            
            # Convertir a bytes con encoding UTF-8
            csv_bytes = csv_content.encode('utf-8')
            
            logger.info("✅ Exportación a CSV completada exitosamente")
            return csv_bytes
            
        except Exception as e:
            logger.error(f"❌ Error al exportar reservas a CSV: {str(e)}", exc_info=True)
            raise

