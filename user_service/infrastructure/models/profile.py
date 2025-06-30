from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .role import RoleDB
from .base import Base

profile_roles = Table(
    "profile_roles",
    Base.metadata,
    Column("profile_id", UUID(as_uuid=True), ForeignKey("profiles.id"), primary_key=True),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True),
)

class ProfileDB(Base):
    __tablename__ = "profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    roles = relationship("RoleDB", secondary=profile_roles, backref="profiles")
