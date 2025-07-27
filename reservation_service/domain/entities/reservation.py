"""
Entidad principal de reserva
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .reservation_status import ReservationStatus
from .order_number import OrderNumber
from .customer_data import CustomerData
from .branch_data import BranchData
from .sector_data import SectorData


@dataclass
class Reservation:
    """Entidad Reservation - representa una reserva completa con todos sus datos"""
    
    # Datos de la sucursal (completos, no solo ID)
    branch_data: BranchData
    
    # Datos del sector (completos, no solo ID)
    sector_data: SectorData
    
    # Datos del cliente (completos, no solo ID)
    customer_data: CustomerData
    
    # Información de la mercadería
    unloading_time_minutes: int  # Tiempo de descarga en minutos
    reason: str  # Motivo de la reserva
    
    # Números de pedidos (lista completa)
    order_numbers: List[OrderNumber]
    
    # Horario de la reserva
    reservation_date: datetime
    start_time: datetime
    end_time: datetime
    
    # Identificación básica
    id: Optional[int] = None
    user_id: Optional[int] = None
    customer_id: Optional[int] = None
    
    # Estado y metadatos
    status: ReservationStatus = ReservationStatus.PENDING
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not self.branch_data:
            raise ValueError("Los datos de la sucursal son obligatorios")
        
        if not self.sector_data:
            raise ValueError("Los datos del sector son obligatorios")
        
        if not self.customer_data:
            raise ValueError("Los datos del cliente son obligatorios")
        
        if not self.order_numbers or len(self.order_numbers) == 0:
            raise ValueError("Debe incluir al menos un número de pedido")
        
        if self.unloading_time_minutes <= 0:
            raise ValueError("El tiempo de descarga debe ser mayor a 0")
        
        if not self.reason or not self.reason.strip():
            raise ValueError("El motivo de la reserva es obligatorio")
        
        if not self.reservation_date:
            raise ValueError("La fecha de reserva es obligatoria")
        
        if not self.start_time or not self.end_time:
            raise ValueError("El horario de inicio y fin es obligatorio")
        
        if self.start_time >= self.end_time:
            raise ValueError("El horario de inicio debe ser anterior al de fin")
        
        # Asignar timestamps si no están definidos
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    def confirm(self):
        """Confirma la reserva"""
        self.status = ReservationStatus.CONFIRMED
        self.updated_at = datetime.utcnow()

    def cancel(self):
        """Cancela la reserva"""
        self.status = ReservationStatus.CANCELLED
        self.updated_at = datetime.utcnow()

    def complete(self):
        """Marca la reserva como completada"""
        self.status = ReservationStatus.COMPLETED
        self.updated_at = datetime.utcnow()

    def is_active(self) -> bool:
        """Verifica si la reserva está activa (confirmada o pendiente)"""
        return self.status in [ReservationStatus.PENDING, ReservationStatus.CONFIRMED]

    def is_cancelled(self) -> bool:
        """Verifica si la reserva está cancelada"""
        return self.status == ReservationStatus.CANCELLED

    def is_completed(self) -> bool:
        """Verifica si la reserva está completada"""
        return self.status == ReservationStatus.COMPLETED
    
    def get_total_unloading_time_hours(self) -> float:
        """Obtiene el tiempo total de descarga en horas"""
        return self.unloading_time_minutes / 60.0
    
    def get_order_codes(self) -> List[str]:
        """Obtiene la lista de códigos de pedidos"""
        return [order.code for order in self.order_numbers]
    
    # Métodos de conveniencia para acceder a IDs
    def get_branch_id(self) -> int:
        """Obtiene el ID de la sucursal"""
        return self.branch_data.branch_id
    
    def get_sector_id(self) -> int:
        """Obtiene el ID del sector"""
        return self.sector_data.sector_id
    
    def get_sector_type_id(self) -> int:
        """Obtiene el ID del tipo de sector"""
        return self.sector_data.sector_type_id
    
    def get_country_id(self) -> int:
        """Obtiene el ID del país"""
        return self.branch_data.country_id
    
    def get_state_id(self) -> int:
        """Obtiene el ID del estado"""
        return self.branch_data.state_id
    
    def get_city_id(self) -> int:
        """Obtiene el ID de la ciudad"""
        return self.branch_data.city_id

    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "customer_data": self.customer_data.__dict__,
            "branch_data": self.branch_data.__dict__,
            "sector_data": self.sector_data.__dict__,
            "schedule_date": self.reservation_date.isoformat() if self.reservation_date else None,
            "schedule_start_time": self.start_time.strftime("%H:%M") if self.start_time else None,
            "schedule_end_time": self.end_time.strftime("%H:%M") if self.end_time else None,
            "merchandise_description": self.reason,
            "merchandise_quantity": self.unloading_time_minutes,
            "merchandise_unit": self.sector_data.measurement_unit_name,
            "special_requirements": self.notes,
            "status": self.status.value,
            "order_numbers": [order.code for order in self.order_numbers],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reservation':
        """Crear desde diccionario"""
        # Convertir datos del cliente
        customer_data = CustomerData(**data.get("customer_data", {}))
        
        # Convertir datos de la sucursal
        branch_data = BranchData(**data.get("branch_data", {}))
        
        # Convertir datos del sector
        sector_data = SectorData(**data.get("sector_data", {}))
        
        # Convertir fecha
        reservation_date = None
        if data.get("schedule_date"):
            reservation_date = datetime.fromisoformat(data["schedule_date"])
        
        # Convertir horarios
        start_time = None
        end_time = None
        if data.get("schedule_start_time") and data.get("schedule_end_time"):
            start_time = datetime.strptime(data["schedule_start_time"], "%H:%M").time()
            end_time = datetime.strptime(data["schedule_end_time"], "%H:%M").time()
        
        # Convertir números de pedido
        order_numbers = []
        for order_code in data.get("order_numbers", []):
            order_numbers.append(OrderNumber(code=order_code))
        
        return cls(
            id=data.get("id"),
            customer_data=customer_data,
            branch_data=branch_data,
            sector_data=sector_data,
            reservation_date=reservation_date,
            start_time=start_time,
            end_time=end_time,
            reason=data.get("merchandise_description"),
            unloading_time_minutes=data.get("merchandise_quantity"),
            notes=data.get("special_requirements"),
            status=ReservationStatus(data.get("status", "PENDING")),
            order_numbers=order_numbers,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None
        )

    def is_affected_by_schedule_change(self, new_schedule_start: str = None, 
                                     new_schedule_end: str = None, 
                                     new_days: list = None) -> bool:
        """Verificar si la reserva se ve afectada por un cambio de horario"""
        from datetime import time
        
        # Verificar si el día de la reserva ya no está disponible
        if new_days:
            reservation_day = self.reservation_date.isoweekday()
            if reservation_day not in new_days:
                return True
        
        # Verificar si el horario de la reserva ya no está disponible
        if new_schedule_start and new_schedule_end:
            reservation_start = self.start_time.time()
            reservation_end = self.end_time.time()
            new_start = datetime.strptime(new_schedule_start, "%H:%M").time()
            new_end = datetime.strptime(new_schedule_end, "%H:%M").time()
            
            # Verificar si hay solapamiento
            if (reservation_start >= new_end or reservation_end <= new_start):
                return True
        
        return False
    
    def mark_for_rescheduling(self):
        """Marcar la reserva para reagendamiento"""
        self.status = ReservationStatus.RESCHEDULING_REQUIRED
        self.updated_at = datetime.utcnow() 