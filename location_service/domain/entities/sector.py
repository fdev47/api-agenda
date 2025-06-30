"""
Entidad Sector del dominio de ubicaciones
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .measurement_unit import MeasurementUnit


@dataclass
class Sector:
    """Entidad Sector - representa un sector en una sucursal"""
    
    id: int
    name: str
    description: Optional[str]
    branch_id: int
    sector_type_id: int
    measurement_unit: MeasurementUnit
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del sector no puede estar vacío")
        
        if self.branch_id <= 0:
            raise ValueError("El ID de la sucursal debe ser mayor a 0")
        
        if self.sector_type_id <= 0:
            raise ValueError("El ID del tipo de sector debe ser mayor a 0")
        
        if not isinstance(self.measurement_unit, MeasurementUnit):
            raise ValueError("La unidad de medida debe ser una instancia válida de MeasurementUnit")
    
    def update_name(self, new_name: str) -> None:
        """Actualizar el nombre del sector"""
        if not new_name or not new_name.strip():
            raise ValueError("El nombre del sector no puede estar vacío")
        
        self.name = new_name.strip()
        self.updated_at = datetime.utcnow()
    
    def update_description(self, new_description: Optional[str]) -> None:
        """Actualizar la descripción del sector"""
        self.description = new_description.strip() if new_description else None
        self.updated_at = datetime.utcnow()
    
    def update_measurement_unit(self, new_unit: MeasurementUnit) -> None:
        """Actualizar la unidad de medida del sector"""
        if not isinstance(new_unit, MeasurementUnit):
            raise ValueError("La unidad de medida debe ser una instancia válida de MeasurementUnit")
        
        self.measurement_unit = new_unit
        self.updated_at = datetime.utcnow()
    
    def update_sector_type(self, new_sector_type_id: int) -> None:
        """Actualizar el tipo de sector"""
        if new_sector_type_id <= 0:
            raise ValueError("El ID del tipo de sector debe ser mayor a 0")
        
        self.sector_type_id = new_sector_type_id
        self.updated_at = datetime.utcnow() 