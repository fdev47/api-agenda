"""
Modelo Customer de la infraestructura - Clientes que reservan en el sistema
"""
from sqlalchemy import Column, String, Boolean, Table, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
import uuid
from .profile import ProfileDB
from .address import AddressDB
from .base import Base

customer_profiles = Table(
    "customer_profiles",
    Base.metadata,
    Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id"), primary_key=True),
    Column("profile_id", UUID(as_uuid=True), ForeignKey("profiles.id"), primary_key=True),
)

class CustomerDB(Base):
    """Modelo Customer de la base de datos - Clientes que reservan en el sistema"""
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_uid = Column(String(128), unique=True, nullable=False)
    ruc = Column(String(20), unique=True, nullable=False)
    company_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=True)  # Nuevo campo
    phone = Column(String(20), nullable=True)  # Teléfono fijo
    cellphone_number = Column(String(20), nullable=True)  # Número de celular
    cellphone_country_code = Column(String(5), nullable=True)  # Código de país del celular
    is_active = Column(Boolean, default=True, nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    profiles = relationship("ProfileDB", secondary=customer_profiles, backref="customers")
    address = relationship("AddressDB", backref="customers") 