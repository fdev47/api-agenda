"""
Modelo de base de datos para Address
"""
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class AddressDB(Base):
    """Modelo de base de datos para direcciones"""
    __tablename__ = "addresses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    street = Column(String(255), nullable=False)
    city_id = Column(UUID(as_uuid=True), nullable=False)
    state_id = Column(UUID(as_uuid=True), nullable=False)
    country_id = Column(UUID(as_uuid=True), nullable=False)
    postal_code = Column(String(20), nullable=True)
    additional_info = Column(Text, nullable=True)