"""
Modelo de infraestructura para países
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class Country(Base):
    """Modelo de base de datos para países"""
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(3), nullable=False, unique=True, index=True)  # ISO 3166-1 alpha-3
    phone_code = Column(String(5), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    states = relationship("State", back_populates="country")
    branches = relationship("Branch", back_populates="country")
    
    def __repr__(self):
        return f"<Country(id={self.id}, name='{self.name}', code='{self.code}')>" 