from sqlalchemy import Column, String, Boolean, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .profile import ProfileDB
from .base import Base

user_profiles = Table(
    "user_profiles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("profile_id", UUID(as_uuid=True), ForeignKey("profiles.id"), primary_key=True),
)

class UserDB(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_uid = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)  # Teléfono fijo
    cellphone_number = Column(String(20), nullable=True)  # Número de celular
    cellphone_country_code = Column(String(5), nullable=True)  # Código de país del celular
    is_active = Column(Boolean, default=True)
    user_type = Column(String(20), nullable=False)
    profiles = relationship("ProfileDB", secondary=user_profiles, backref="users")
