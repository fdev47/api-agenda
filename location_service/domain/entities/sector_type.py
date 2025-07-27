"""
Entidad SectorType del dominio de ubicaciones
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .measurement_unit import MeasurementUnit


@dataclass
class SectorType:
    """Entidad SectorType - representa un tipo de sector"""
    
    id: int
    name: str
    code: str
    created_at: datetime
    measurement_unit: MeasurementUnit
    description: Optional[str] = None
    is_active: bool = True
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del tipo de sector no puede estar vacío")
        
        if not self.code or not self.code.strip():
            raise ValueError("El código del tipo de sector no puede estar vacío")
    
    def update_name(self, new_name: str) -> None:
        """Actualizar el nombre del tipo de sector"""
        if not new_name or not new_name.strip():
            raise ValueError("El nombre del tipo de sector no puede estar vacío")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
    
    def update_code(self, new_code: str) -> None:
        """Actualizar el código del tipo de sector"""
        if not new_code or not new_code.strip():
            raise ValueError("El código del tipo de sector no puede estar vacío")
        
        self.code = new_code.strip()
        self.updated_at = datetime.utcnow() 