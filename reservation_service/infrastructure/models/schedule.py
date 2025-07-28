"""
Modelo de base de datos para horarios
"""
from datetime import datetime, time
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from ...domain.entities.day_of_week import DayOfWeek
from ...domain.entities.branch_schedule import BranchSchedule


class BranchScheduleModel(Base):
    """Modelo de base de datos para horarios de sucursales"""
    
    __tablename__ = "branch_schedules"
    
    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Relación con la sucursal (sin foreign key para evitar dependencias entre servicios)
    branch_id = Column(Integer, nullable=False, index=True)
    
    # Configuración del horario
    day_of_week = Column(Enum(DayOfWeek), nullable=False, index=True)  # Usar Enum directamente
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    interval_minutes = Column(Integer, default=60, nullable=False)  # Intervalo por defecto 1 hora
    
    # Estado
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Campos de auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_domain(self) -> 'BranchSchedule':
        """Convierte el modelo de BD a entidad de dominio"""
        
        return BranchSchedule(
            id=self.id,
            branch_id=self.branch_id,
            day_of_week=self.day_of_week,  # Ya es un enum
            start_time=self.start_time,
            end_time=self.end_time,
            interval_minutes=self.interval_minutes,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_domain(cls, schedule: 'BranchSchedule') -> 'BranchScheduleModel':
        """Convierte la entidad de dominio a modelo de BD"""
        return cls(
            branch_id=schedule.branch_id,
            day_of_week=schedule.day_of_week,  # Ya es un enum
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            interval_minutes=schedule.interval_minutes,
            is_active=schedule.is_active
        )
    
    def __repr__(self):
        return f"<BranchSchedule(id={self.id}, branch_id={self.branch_id}, day={self.day_of_week.name}, time={self.start_time}-{self.end_time})>" 