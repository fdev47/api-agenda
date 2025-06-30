from datetime import datetime, time
from sqlalchemy import Column, Integer, String, DateTime, Time, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseModel
from ...domain.entities.schedule import DayOfWeek


class BranchScheduleModel(BaseModel):
    """Modelo de base de datos para horarios de sucursales"""
    
    __tablename__ = "branch_schedules"
    
    # Relación con la sucursal
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    
    # Configuración del horario
    day_of_week = Column(SQLEnum(DayOfWeek), nullable=False, index=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    interval_minutes = Column(Integer, default=60, nullable=False)  # Intervalo por defecto 1 hora
    
    # Estado
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    def to_domain(self) -> 'BranchSchedule':
        """Convierte el modelo de BD a entidad de dominio"""
        from ...domain.entities.schedule import BranchSchedule
        
        return BranchSchedule(
            id=self.id,
            branch_id=self.branch_id,
            day_of_week=self.day_of_week,
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
            id=schedule.id,
            branch_id=schedule.branch_id,
            day_of_week=schedule.day_of_week,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            interval_minutes=schedule.interval_minutes,
            is_active=schedule.is_active,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at
        )
    
    def __repr__(self):
        return f"<BranchSchedule(id={self.id}, branch_id={self.branch_id}, day={self.day_of_week.name}, time={self.start_time}-{self.end_time})>" 