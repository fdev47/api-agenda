"""
Modelo de infraestructura para estados
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class State(Base):
    """Modelo de base de datos para estados"""
    __tablename__ = "states"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(10), nullable=False, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    country = relationship("Country", back_populates="states")
    cities = relationship("City", back_populates="state")
    branches = relationship("Branch", back_populates="state")
    
    def __repr__(self):
        return f"<State(id={self.id}, name='{self.name}', code='{self.code}', country_id={self.country_id})>" 