"""
Modelo de base de datos para rampas
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Ramp(Base):
    """Modelo de base de datos para rampas"""
    
    __tablename__ = "ramps"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    is_available = Column(Boolean, default=True, nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    branch = relationship("Branch", back_populates="ramps")
    
    def __repr__(self):
        return f"<Ramp(id={self.id}, name='{self.name}', branch_id={self.branch_id})>" 