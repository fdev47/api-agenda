"""
Modelo de base de datos para reservas
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Float, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .base import Base
from ...domain.entities.reservation_status import ReservationStatus
from ...domain.entities.reservation import Reservation
from ...domain.entities.branch_data import BranchData
from ...domain.entities.sector_data import SectorData
from ...domain.entities.customer_data import CustomerData
from ...domain.entities.order_number import OrderNumber


class ReservationModel(Base):
    """Modelo de base de datos para reservas"""
    
    __tablename__ = "reservations"
    
    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Identificación básica
    user_id = Column(Integer, nullable=False, index=True)
    customer_id = Column(Integer, nullable=True, index=True)
    
    # IDs de referencia (para consultas eficientes) - Sin foreign keys para evitar dependencias
    branch_id = Column(Integer, nullable=False, index=True)
    sector_id = Column(Integer, nullable=False, index=True)
    
    # Información de la mercadería
    unloading_time_minutes = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    
    # Horario de la reserva
    reservation_date = Column(DateTime, nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    
    # Estado y metadatos
    status = Column(SQLEnum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    
    # Datos completos en JSON (para integridad histórica)
    branch_data = Column(JSON, nullable=False)  # Datos completos de la sucursal
    sector_data = Column(JSON, nullable=False)  # Datos completos del sector
    customer_data = Column(JSON, nullable=False)  # Datos completos del cliente
    
    # Campos de auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    order_numbers = relationship("ReservationOrderNumberModel", back_populates="reservation", cascade="all, delete-orphan")
    
    def to_domain(self) -> 'Reservation':
        """Convierte el modelo de BD a entidad de dominio"""
        
        # Convertir datos JSON a objetos de dominio
        branch_data = BranchData(**self.branch_data)
        sector_data = SectorData(**self.sector_data)
        customer_data = CustomerData(**self.customer_data)
        
        # Convertir números de pedido
        order_numbers = [
            OrderNumber(code=order.code, description=order.description)
            for order in self.order_numbers
        ]
        
        return Reservation(
            id=self.id,
            user_id=self.user_id,
            customer_id=self.customer_id,
            branch_data=branch_data,
            sector_data=sector_data,
            customer_data=customer_data,
            unloading_time_minutes=self.unloading_time_minutes,
            reason=self.reason,
            order_numbers=order_numbers,
            reservation_date=self.reservation_date,
            start_time=self.start_time,
            end_time=self.end_time,
            status=self.status,
            notes=self.notes,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_domain(cls, reservation: 'Reservation') -> 'ReservationModel':
        """Convierte la entidad de dominio a modelo de BD"""
        # Convertir objetos de dominio a JSON
        branch_data = {
            "branch_id": reservation.branch_data.branch_id,
            "name": reservation.branch_data.name,
            "code": reservation.branch_data.code,
            "address": reservation.branch_data.address,
            "country_id": reservation.branch_data.country_id,
            "country_name": reservation.branch_data.country_name,
            "state_id": reservation.branch_data.state_id,
            "state_name": reservation.branch_data.state_name,
            "city_id": reservation.branch_data.city_id,
            "city_name": reservation.branch_data.city_name
        }
        
        sector_data = {
            "sector_id": reservation.sector_data.sector_id,
            "name": reservation.sector_data.name,
            "description": reservation.sector_data.description,
            "sector_type_id": reservation.sector_data.sector_type_id,
            "sector_type_name": reservation.sector_data.sector_type_name,
            "capacity": reservation.sector_data.capacity,
            "measurement_unit_id": reservation.sector_data.measurement_unit_id,
            "measurement_unit_name": reservation.sector_data.measurement_unit_name
        }
        
        customer_data = {
            "customer_id": reservation.customer_data.customer_id,
            "name": reservation.customer_data.name,
            "email": reservation.customer_data.email,
            "phone": reservation.customer_data.phone
        }
        
        return cls(
            user_id=reservation.user_id,
            customer_id=reservation.customer_id,
            branch_id=reservation.branch_data.branch_id,
            sector_id=reservation.sector_data.sector_id,
            unloading_time_minutes=reservation.unloading_time_minutes,
            reason=reservation.reason,
            reservation_date=reservation.reservation_date,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status,
            notes=reservation.notes,
            branch_data=branch_data,
            sector_data=sector_data,
            customer_data=customer_data
        )


class ReservationOrderNumberModel(Base):
    """Modelo de base de datos para números de pedido de reservas"""
    
    __tablename__ = "reservation_order_numbers"
    
    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Relación con la reserva (foreign key interno del servicio)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False, index=True)
    
    # Datos del pedido
    code = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Campos de auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relaciones
    reservation = relationship("ReservationModel", back_populates="order_numbers")
    
    def __repr__(self):
        return f"<ReservationOrderNumberModel(id={self.id}, code='{self.code}')>" 