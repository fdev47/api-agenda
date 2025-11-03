"""
Modelo de base de datos para tipos de sector
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SqlEnum
from sqlalchemy.sql import func
from .base import Base
from domain.entities.measurement_unit import MeasurementUnit

class SectorType(Base):
    __tablename__ = "sector_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(20), nullable=False, unique=True)
    description = Column(String(200), nullable=True)
    measurement_unit = Column(SqlEnum(MeasurementUnit), nullable=False)
    merchandise_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<SectorType(id={self.id}, name='{self.name}', code='{self.code}', merchandise_type='{self.merchandise_type}')>" 