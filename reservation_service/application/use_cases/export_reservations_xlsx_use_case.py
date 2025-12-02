"""
Use case para exportar reservas a XLSX
"""
import logging
import io
from datetime import datetime
from typing import List
from ...domain.dto.requests.export_reservations_request import ExportReservationsRequest
from ...domain.dto.requests.reservation_filter_request import ReservationFilterRequest
from ...domain.interfaces.reservation_repository import ReservationRepository
from ...domain.interfaces.main_reservation_repository import MainReservationRepository
from .list_reservations_use_case import ListReservationsUseCase

logger = logging.getLogger(__name__)


class ExportReservationsXlsxUseCase:
    """Caso de uso para exportar reservas a formato XLSX"""
    
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
        """Ejecutar el caso de uso y retornar el contenido XLSX como bytes"""
        logger.info("🚀 ExportReservationsXlsxUseCase.execute() iniciado")
        
        try:
            # Verificar que xlsxwriter esté instalado
            try:
                import xlsxwriter
            except ImportError:
                logger.error("❌ xlsxwriter no está instalado")
                raise ImportError("xlsxwriter no está instalado. Ejecute: pip install xlsxwriter")
            
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
            
            logger.info(f"📊 Exportando {len(reservations)} reservas a XLSX")
            
            # Crear buffer en memoria para el XLSX
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('Reservas')
            
            # Definir formatos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#366092',
                'font_color': 'white',
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'border': 1
            })
            
            # Escribir encabezados
            headers = [
                "proveedor",
                "fecha",
                "hora",
                "carga",
                "estado",
                "sucursal"
            ]
            
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
            
            # Escribir datos
            for row, reservation in enumerate(reservations, start=1):
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
                
                worksheet.write(row, 0, reservation.customer_data.company_name or "", cell_format)
                worksheet.write(row, 1, fecha, cell_format)
                worksheet.write(row, 2, hora, cell_format)
                worksheet.write(row, 3, reservation.cargo_type or "", cell_format)
                worksheet.write(row, 4, estado, cell_format)
                worksheet.write(row, 5, reservation.branch_data.code or "", cell_format)
            
            # Ajustar ancho de columnas
            worksheet.set_column(0, 0, 30)  # proveedor
            worksheet.set_column(1, 1, 12)  # fecha
            worksheet.set_column(2, 2, 10)  # hora
            worksheet.set_column(3, 3, 20)  # carga
            worksheet.set_column(4, 4, 15)  # estado
            worksheet.set_column(5, 5, 15)  # sucursal
            
            # Cerrar el workbook
            workbook.close()
            
            # Obtener el contenido del XLSX
            output.seek(0)
            xlsx_content = output.getvalue()
            output.close()
            
            logger.info("✅ Exportación a XLSX completada exitosamente")
            return xlsx_content
            
        except ImportError:
            raise
        except Exception as e:
            logger.error(f"❌ Error al exportar reservas a XLSX: {str(e)}", exc_info=True)
            raise

