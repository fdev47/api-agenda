"""
Modelo de base de datos para Address
"""
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base

class AddressDB(Base):
    """Modelo de base de datos para direcciones"""
    __tablename__ = "addresses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    street = Column(String(255), nullable=False)
    city_id = Column(Integer, nullable=False)
    state_id = Column(Integer, nullable=False)
    country_id = Column(Integer, nullable=False)
    postal_code = Column(String(20), nullable=True)
    additional_info = Column(Text, nullable=True)