"""
Modelo para unidades de medida
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .base import Base


class MeasurementUnit(Base):
    """Modelo para unidades de medida"""
    
    __tablename__ = "measurement_units"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    code = Column(String(20), nullable=False, unique=True, index=True)
    description = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<MeasurementUnit(id={self.id}, name='{self.name}', code='{self.code}')>" 