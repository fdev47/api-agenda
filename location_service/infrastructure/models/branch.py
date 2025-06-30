"""
Modelo de base de datos para sucursales
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Branch(Base):
    """Modelo de base de datos para sucursales"""
    __tablename__ = "branches"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    local_id = Column(Integer, ForeignKey("locals.id"), nullable=False, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False, index=True)
    address = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relaciones
    local = relationship("Local", back_populates="branches")
    country = relationship("Country", back_populates="branches")
    state = relationship("State", back_populates="branches")
    city = relationship("City", back_populates="branches")
    ramps = relationship("Ramp", back_populates="branch", cascade="all, delete-orphan")
    sectors = relationship("Sector", back_populates="branch", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Branch(id={self.id}, name='{self.name}', code='{self.code}', local_id={self.local_id})>" 