"""
Entidad User del dominio - Usuarios internos del sistema
"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from typing import List, Literal, Optional
from .profile import ProfileSimple

# Definir el tipo como variable para mejor mantenibilidad
UserType = Literal['root', 'admin', 'user', 'recepcionista', 'recepcionista_rampa', 'recepcionista_rampa_frio']

class User(BaseModel):
    """Entidad User del dominio - Usuarios internos del sistema"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID = Field(default_factory=uuid4, description="Identificador único del usuario")
    auth_uid: str = Field(..., description="UID del proveedor de autenticación")
    email: str = Field(..., description="Email del usuario")
    username: Optional[str] = Field(None, description="Nombre de usuario")
    branch_code: Optional[str] = Field(None, description="Código de sucursal")
    first_name: str | None = Field(None, description="Nombre del usuario")
    last_name: str | None = Field(None, description="Apellido del usuario")
    phone: str | None = Field(None, description="Número de teléfono fijo")
    cellphone_number: str | None = Field(None, description="Número de celular")
    cellphone_country_code: str | None = Field(None, description="Código de país del celular (+595)")
    is_active: bool = Field(True, description="Estado activo del usuario")
    user_type: UserType = Field(..., description="Tipo de usuario interno")
    profiles: List[ProfileSimple] = Field(default=[], description="Perfiles del usuario") 