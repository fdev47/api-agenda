"""
Modelo de base de datos para horarios de rampas
"""
from sqlalchemy import Column, Integer, String, Time, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class RampSchedule(Base):
    """Modelo de base de datos para horarios de rampas"""
    
    __tablename__ = "ramp_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    ramp_id = Column(Integer, ForeignKey("ramps.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False, index=True)  # 1=Lunes, 7=Domingo
    name = Column(String(100), nullable=False, index=True)  # "Turno 1", "Horario descarga", etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    ramp = relationship("Ramp", back_populates="schedules")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('day_of_week >= 1 AND day_of_week <= 7', name='check_day_of_week'),
        CheckConstraint('start_time < end_time', name='check_time_range')
    )
    
    def __repr__(self):
        return f"<RampSchedule(id={self.id}, ramp_id={self.ramp_id}, day={self.day_of_week}, name='{self.name}')>"

