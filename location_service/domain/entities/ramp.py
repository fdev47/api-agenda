"""
Entidad Ramp del dominio de ubicaciones
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Ramp:
    """Entidad Ramp - representa una rampa en una sucursal"""
    
    id: int
    name: str
    is_available: bool
    branch_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre de la rampa no puede estar vacío")
        
        if self.branch_id <= 0:
            raise ValueError("El ID de la sucursal debe ser mayor a 0")
    
    def make_available(self) -> None:
        """Marcar la rampa como disponible"""
        self.is_available = True
        self.updated_at = datetime.utcnow()
    
    def make_unavailable(self) -> None:
        """Marcar la rampa como no disponible"""
        self.is_available = False
        self.updated_at = datetime.utcnow()
    
    def update_name(self, new_name: str) -> None:
        """Actualizar el nombre de la rampa"""
        if not new_name or not new_name.strip():
            raise ValueError("El nombre de la rampa no puede estar vacío")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow() 