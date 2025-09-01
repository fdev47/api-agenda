"""
Modelo de base de datos para sectores
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Sector(Base):
    """Modelo de base de datos para sectores"""
    
    __tablename__ = "sectors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False, index=True)
    sector_type_id = Column(Integer, ForeignKey("sector_types.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    branch = relationship("Branch", back_populates="sectors")
    sector_type = relationship("SectorType")
    
    def __repr__(self):
        return f"<Sector(id={self.id}, name='{self.name}', branch_id={self.branch_id})>" 