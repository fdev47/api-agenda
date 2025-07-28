"""
Entidad MeasurementUnit del dominio de ubicaciones
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class MeasurementUnit:
    """Entidad MeasurementUnit - representa una unidad de medida"""
    
    id: int
    name: str
    code: str
    created_at: datetime
    description: Optional[str] = None
    is_active: bool = True
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre de la unidad de medida no puede estar vacío")
        
        if not self.code or not self.code.strip():
            raise ValueError("El código de la unidad de medida no puede estar vacío")
    
    def update_name(self, new_name: str) -> None:
        """Actualizar el nombre de la unidad de medida"""
        if not new_name or not new_name.strip():
            raise ValueError("El nombre de la unidad de medida no puede estar vacío")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
    
    def update_code(self, new_code: str) -> None:
        """Actualizar el código de la unidad de medida"""
        if not new_code or not new_code.strip():
            raise ValueError("El código de la unidad de medida no puede estar vacío")
        
        self.code = new_code.strip()
        self.updated_at = datetime.utcnow() 